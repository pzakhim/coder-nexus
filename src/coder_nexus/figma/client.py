"""Figma REST client (READ-ONLY): parse a frame/section link, render screens to PNG/JPG, save raw JSON, DTCG tokens.json, and Framelink-style <node>.spec.json.

Only two endpoints are called, both GET: `/v1/files/{key}/nodes` and `/v1/images/{key}`.
The token is sent to api.figma.com only, never to the rendered-image URL it returns.
"""

import asyncio
import json
import os
import urllib.parse
from pathlib import Path
from typing import Optional

import httpx
from pydantic import BaseModel, Field

from ..huly.auth import parse_env_file
from .summary import build_spec_and_tokens, extract_screen_nodes, render_summary
from .tokens import merge_and_save_tokens

API_BASE = "https://api.figma.com"
TOKEN_KEY = "FIGMA_TOKEN"
TOKEN_KEYS = (TOKEN_KEY, "FIGMA_ACCESS_TOKEN")
LINK_KINDS = ("design", "file", "proto")
DENIED = {401: "token rejected (401)", 403: "no access to this file with this token (403)", 404: "file or node not found (404)"}


class FigmaRef(BaseModel):
    """A Figma frame link: file key and node id in API form (`1150:10051`)."""

    url: str
    file_key: str
    node_id: Optional[str] = None


class FigmaFetchResult(BaseModel):
    """What `fetch` read. READ = files written; NOT_PROVIDED = no token; UNREACHABLE = API refused or failed."""

    status: str = Field(description="READ | NOT_PROVIDED | UNREACHABLE")
    url: str
    file_key: Optional[str] = None
    node_id: Optional[str] = None
    name: Optional[str] = Field(default=None, description="Frame name, when read")
    png_path: Optional[str] = None
    screen_images: list[str] = Field(default_factory=list, description="Per-screen rendered image paths (S01..SNN)")
    json_path: Optional[str] = None
    tokens_path: Optional[str] = Field(default=None, description="File-level W3C DTCG design tokens (tokens.json)")
    spec_path: Optional[str] = Field(default=None, description="Framelink-style normalized spec JSON (<node>.spec.json)")
    summary_path: Optional[str] = None
    note: Optional[str] = None


def parse_figma_url(url: str) -> FigmaRef:
    """`https://www.figma.com/design/<key>/<name>?node-id=1150-10051` -> key + `1150:10051`.

    Accepts /design/, /file/ and /proto/ links and branch links (`/design/<key>/branch/<branch>/…`).
    Raises ValueError for anything else.
    """
    parsed = urllib.parse.urlparse(url.strip())
    host = parsed.netloc.lower()
    if parsed.scheme not in ("http", "https") or not (host == "figma.com" or host.endswith(".figma.com")):
        raise ValueError(f"Not a Figma link: {url}")
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2 or parts[0] not in LINK_KINDS:
        raise ValueError(f"Not a Figma design/file link: {url}")
    key = parts[3] if len(parts) >= 4 and parts[2] == "branch" else parts[1]
    raw_node = (urllib.parse.parse_qs(parsed.query).get("node-id") or [None])[0]
    node_id = raw_node.replace("-", ":") if raw_node else None
    return FigmaRef(url=url, file_key=key, node_id=node_id)


def load_figma_token(workspace_path: Optional[str] = None) -> Optional[str]:
    """FIGMA_TOKEN (or FIGMA_ACCESS_TOKEN) from the Client workspace `.env`, falling back to the environment (like Huly)."""
    base = Path(workspace_path).resolve() if workspace_path else Path.cwd().resolve()
    env = parse_env_file(base / ".env")
    return next((v for key in TOKEN_KEYS if (v := env.get(key) or os.getenv(key))), None)


def node_file_stem(node_id: str) -> str:
    return node_id.replace(":", "-").replace(";", "_")


async def fetch_async(
    url: str,
    out_dir: str | Path,
    token: Optional[str],
    *,
    image_format: str = "png",
    timeout: float = 30.0,
    transport: Optional[httpx.AsyncBaseTransport] = None,
) -> FigmaFetchResult:
    """Save `<node>.<ext>`, per-screen `<node>-SNN.<ext>`, `<node>.json`, `tokens.json`, `<node>.spec.json` and `<node>.summary.md`.

    Never raises for API problems: the result says READ, NOT_PROVIDED or UNREACHABLE with a note.
    """
    try:
        ref = parse_figma_url(url)
    except ValueError as exc:
        return FigmaFetchResult(status="UNREACHABLE", url=url, note=str(exc))
    result = FigmaFetchResult(status="UNREACHABLE", url=url, file_key=ref.file_key, node_id=ref.node_id)
    if not token:
        result.status = "NOT_PROVIDED"
        result.note = f"No {TOKEN_KEY} in the Client .env: add a Figma personal access token (read-only scope) or export the frame manually."
        return result
    if not ref.node_id:
        result.note = "The link has no node-id (whole file). Ask for a link to the frame (Copy link to selection)."
        return result

    fmt = "jpg" if image_format.lower() in ("jpg", "jpeg") else "png"
    headers = {"X-Figma-Token": token}
    params = {"ids": ref.node_id}
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True, transport=transport) as http:
            nodes_res = await http.get(f"{API_BASE}/v1/files/{ref.file_key}/nodes", params=params, headers=headers)
            if nodes_res.status_code != 200:
                result.note = _http_note(nodes_res, "nodes")
                return result
            payload = nodes_res.json()
            entry = (payload.get("nodes") or {}).get(ref.node_id)
            if not entry or not entry.get("document"):
                result.note = f"Node {ref.node_id} not found in file {ref.file_key}."
                return result

            root_doc = entry["document"]
            out = Path(out_dir)
            out.mkdir(parents=True, exist_ok=True)
            stem = node_file_stem(ref.node_id)
            json_path = out / f"{stem}.json"
            json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            result.json_path, result.name = str(json_path), root_doc.get("name")

            screen_nodes = extract_screen_nodes(root_doc)
            extra_screen_ids = [
                str(s.get("id"))
                for s in screen_nodes
                if s.get("id") and str(s.get("id")) != ref.node_id
            ]
            image_ids = [ref.node_id, *extra_screen_ids]

            png_note = None
            screen_image_paths: dict[str, str] = {}
            screen_png_names: dict[str, str] = {}

            img_res = await http.get(
                f"{API_BASE}/v1/images/{ref.file_key}",
                params={"ids": ",".join(image_ids), "format": fmt, "scale": "2"},
                headers=headers,
            )
            images_map = (img_res.json().get("images") or {}) if img_res.status_code == 200 else {}
            image_url = images_map.get(ref.node_id)
            if image_url:
                png_res = await http.get(image_url)  # pre-signed render URL: no token
                if png_res.status_code == 200:
                    png_path = out / f"{stem}.{fmt}"
                    png_path.write_bytes(png_res.content)
                    result.png_path = str(png_path)
                else:
                    png_note = f"{fmt.upper()} download returned HTTP {png_res.status_code}"
            else:
                png_note = _http_note(img_res, "images") if img_res.status_code != 200 else "Figma did not render the frame"

            if extra_screen_ids:
                for idx, snode in enumerate(screen_nodes, start=1):
                    snid = str(snode.get("id") or "")
                    s_url = images_map.get(snid)
                    if not s_url:
                        continue
                    s_res = await http.get(s_url)  # pre-signed render URL: no token
                    if s_res.status_code == 200:
                        s_name = f"{stem}-S{idx:02d}.{fmt}"
                        s_path = out / s_name
                        s_path.write_bytes(s_res.content)
                        screen_image_paths[snid] = str(s_path)
                        screen_png_names[snid] = s_name
                        result.screen_images.append(str(s_path))
            elif result.png_path:
                result.screen_images = [result.png_path]

            spec_data, token_registry = build_spec_and_tokens(
                payload,
                ref.node_id,
                url,
                file_key=ref.file_key,
                root_image_path=result.png_path,
                screen_image_paths=screen_image_paths,
            )
            tokens_path = out / "tokens.json"
            merge_and_save_tokens(tokens_path, token_registry)
            result.tokens_path = str(tokens_path)

            spec_path = out / f"{stem}.spec.json"
            spec_path.write_text(json.dumps(spec_data, indent=2, ensure_ascii=False), encoding="utf-8")
            result.spec_path = str(spec_path)

            summary_path = out / f"{stem}.summary.md"
            summary_path.write_text(
                render_summary(
                    payload,
                    ref.node_id,
                    url,
                    png_name=f"{stem}.{fmt}" if result.png_path else None,
                    screen_png_names=screen_png_names,
                ),
                encoding="utf-8",
            )
            result.summary_path = str(summary_path)
            result.status = "READ"
            result.note = f"{png_note}; JSON and summary saved" if png_note else None
            return result
    except (httpx.HTTPError, ValueError) as exc:
        result.note = f"Figma request failed: {exc}"
        return result


def fetch(url: str, out_dir: str | Path, token: Optional[str], **kwargs) -> FigmaFetchResult:
    """Synchronous wrapper of `fetch_async`."""
    return asyncio.run(fetch_async(url, out_dir, token, **kwargs))


def _http_note(res: httpx.Response, what: str) -> str:
    reason = DENIED.get(res.status_code, f"HTTP {res.status_code}")
    try:
        detail = res.json().get("err") or res.json().get("message")
    except ValueError:
        detail = None
    return f"Figma {what}: {reason}" + (f" — {detail}" if detail else "")
