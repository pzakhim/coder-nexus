"""DTCG (W3C Design Tokens Community Group) `tokens.json` extractor and file-level merger for Figma."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator, Optional

DTCG_SCHEMA = "https://tr.designtokens.org/format/"


def _walk_visible(node: dict, depth: int = 0) -> Iterator[tuple[dict, int]]:
    if node.get("visible") is False:
        return
    yield node, depth
    for child in node.get("children") or []:
        yield from _walk_visible(child, depth + 1)


def paint_to_hex(paint: dict) -> Optional[str]:
    """Convert a visible SOLID Figma paint to `#RRGGBB` or `#RRGGBBAA` (DTCG color format)."""
    if paint.get("type") != "SOLID" or paint.get("visible") is False or not paint.get("color"):
        return None
    c = paint["color"]
    rgb = "#" + "".join(f"{round(c.get(k, 0) * 255):02X}" for k in ("r", "g", "b"))
    alpha = c.get("a", 1.0) * paint.get("opacity", 1.0)
    if alpha >= 0.999:
        return rgb
    return f"{rgb}{round(alpha * 255):02X}"


def slugify_segment(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", text.strip()).strip("-").lower()
    return s or "token"


def style_name_to_path(style_name: str, prefix: str) -> list[str]:
    """Convert a Figma slash-separated style name (`Primary / Brand 500`) into DTCG path segments."""
    parts = [slugify_segment(p) for p in re.split(r"[/.]+", style_name) if p.strip()]
    if not parts:
        return [prefix, "default"]
    if parts[0] == prefix:
        return parts
    return [prefix, *parts]


def _set_nested_token(root: dict[str, Any], path: list[str], token_obj: dict[str, Any]) -> str:
    cur = root
    for seg in path[:-1]:
        if seg not in cur or not isinstance(cur[seg], dict) or "$value" in cur[seg]:
            cur[seg] = {}
        cur = cur[seg]
    leaf = path[-1]
    cur[leaf] = token_obj
    return ".".join(path)


def _bound_var_ids(node: dict, prop: str) -> list[str]:
    bv = node.get("boundVariables") or {}
    raw = bv.get(prop)
    if isinstance(raw, dict) and raw.get("id"):
        return [str(raw["id"])]
    if isinstance(raw, list):
        return [str(item["id"]) for item in raw if isinstance(item, dict) and item.get("id")]
    return []


class TokenRegistry:
    """Collects file-level DTCG tokens while mapping raw values and style IDs to dot-separated token paths."""

    def __init__(
        self,
        *,
        file_key: Optional[str] = None,
        file_name: str = "?",
        last_modified: Optional[str] = None,
        styles_meta: Optional[dict[str, Any]] = None,
        components_meta: Optional[dict[str, Any]] = None,
        component_sets_meta: Optional[dict[str, Any]] = None,
    ) -> None:
        self.file_key = file_key
        self.file_name = file_name
        self.last_modified = last_modified
        self.styles_meta = styles_meta or {}
        self.components_meta = components_meta or {}
        self.component_sets_meta = component_sets_meta or {}

        self.tree: dict[str, Any] = {
            "$schema": DTCG_SCHEMA,
            "$extensions": {
                "com.figma": {
                    "fileKey": file_key,
                    "fileName": file_name,
                    "lastModified": last_modified,
                    "componentSets": {},
                    "components": {},
                }
            },
            "color": {},
            "typography": {},
            "dimension": {
                "radius": {},
                "spacing": {},
            },
            "shadow": {},
        }
        self._register_catalog()

    def _register_catalog(self) -> None:
        figma_ext = self.tree["$extensions"]["com.figma"]
        for set_id, meta in self.component_sets_meta.items():
            if isinstance(meta, dict):
                figma_ext["componentSets"][set_id] = {
                    "key": meta.get("key"),
                    "name": meta.get("name", set_id),
                    "description": meta.get("description") or "",
                }
        for comp_id, meta in self.components_meta.items():
            if isinstance(meta, dict):
                figma_ext["components"][comp_id] = {
                    "key": meta.get("key"),
                    "name": meta.get("name", comp_id),
                    "description": meta.get("description") or "",
                    "componentSetId": meta.get("componentSetId"),
                }

    def register_color(
        self,
        hex_value: str,
        *,
        style_id: Optional[str] = None,
        var_ids: Optional[list[str]] = None,
        role_hint: str = "fill",
    ) -> str:
        meta = self.styles_meta.get(style_id or "", {}) if style_id else {}
        style_name = meta.get("name")
        if style_name:
            path = style_name_to_path(style_name, "color")
        else:
            clean_hex = hex_value.lstrip("#").lower()
            path = ["color", "unlinked", f"{role_hint}-{clean_hex}"]

        ext: dict[str, Any] = {"roleHint": role_hint}
        if style_id:
            ext["styleId"] = style_id
        if style_name:
            ext["styleName"] = style_name
        if meta.get("key"):
            ext["styleKey"] = meta["key"]
        if var_ids:
            ext["variableIds"] = var_ids

        token_obj: dict[str, Any] = {
            "$type": "color",
            "$value": hex_value,
            "$extensions": {"com.figma": ext},
        }
        if meta.get("description"):
            token_obj["$description"] = meta["description"]
        return _set_nested_token(self.tree, path, token_obj)

    def register_typography(
        self,
        style_dict: dict[str, Any],
        *,
        style_id: Optional[str] = None,
        var_ids: Optional[list[str]] = None,
    ) -> Optional[str]:
        family = style_dict.get("fontFamily")
        if not family:
            return None
        weight = style_dict.get("fontWeight", 400)
        size = style_dict.get("fontSize", 14)
        lh = style_dict.get("lineHeightPx")
        ls = style_dict.get("letterSpacing", 0)

        meta = self.styles_meta.get(style_id or "", {}) if style_id else {}
        style_name = meta.get("name")
        if style_name:
            path = style_name_to_path(style_name, "typography")
        else:
            fam_slug = slugify_segment(str(family))
            path = ["typography", "unlinked", f"{fam_slug}-{weight}-{round(size)}"]

        val: dict[str, Any] = {
            "fontFamily": family,
            "fontSize": f"{round(size) if isinstance(size, (int, float)) else size}px",
            "fontWeight": weight,
            "lineHeight": f"{round(lh)}px" if isinstance(lh, (int, float)) else "normal",
            "letterSpacing": f"{round(ls, 2)}px" if isinstance(ls, (int, float)) and ls != 0 else "0px",
        }
        ext: dict[str, Any] = {}
        if style_id:
            ext["styleId"] = style_id
        if style_name:
            ext["styleName"] = style_name
        if var_ids:
            ext["variableIds"] = var_ids

        token_obj: dict[str, Any] = {
            "$type": "typography",
            "$value": val,
        }
        if ext:
            token_obj["$extensions"] = {"com.figma": ext}
        if meta.get("description"):
            token_obj["$description"] = meta["description"]
        return _set_nested_token(self.tree, path, token_obj)

    def register_radius(self, radius_px: int | float, *, var_ids: Optional[list[str]] = None) -> str:
        r = round(radius_px)
        path = ["dimension", "radius", f"{r}px"]
        token_obj: dict[str, Any] = {
            "$type": "dimension",
            "$value": f"{r}px",
        }
        if var_ids:
            token_obj["$extensions"] = {"com.figma": {"variableIds": var_ids}}
        return _set_nested_token(self.tree, path, token_obj)

    def register_spacing(self, spacing_px: int | float, *, var_ids: Optional[list[str]] = None) -> str:
        s = round(spacing_px)
        path = ["dimension", "spacing", f"{s}px"]
        token_obj: dict[str, Any] = {
            "$type": "dimension",
            "$value": f"{s}px",
        }
        if var_ids:
            token_obj["$extensions"] = {"com.figma": {"variableIds": var_ids}}
        return _set_nested_token(self.tree, path, token_obj)

    def register_shadow(self, effect: dict[str, Any], *, style_id: Optional[str] = None) -> Optional[str]:
        if effect.get("visible") is False or effect.get("type") not in ("DROP_SHADOW", "INNER_SHADOW"):
            return None
        color = paint_to_hex({"type": "SOLID", "color": effect.get("color")}) or "#00000040"
        offset = effect.get("offset") or {}
        ox = round(offset.get("x", 0) or 0)
        oy = round(offset.get("y", 0) or 0)
        blur = round(effect.get("radius", 0) or 0)
        spread = round(effect.get("spread", 0) or 0)

        meta = self.styles_meta.get(style_id or "", {}) if style_id else {}
        style_name = meta.get("name")
        if style_name:
            path = style_name_to_path(style_name, "shadow")
        else:
            path = ["shadow", "unlinked", f"{ox}-{oy}-{blur}-{spread}"]

        token_obj: dict[str, Any] = {
            "$type": "shadow",
            "$value": {
                "color": color,
                "offsetX": f"{ox}px",
                "offsetY": f"{oy}px",
                "blur": f"{blur}px",
                "spread": f"{spread}px",
            },
        }
        if style_id or style_name:
            token_obj["$extensions"] = {"com.figma": {"styleId": style_id, "styleName": style_name}}
        return _set_nested_token(self.tree, path, token_obj)


def _deep_merge_dicts(base: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    for k, v in incoming.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict) and "$value" not in v:
            _deep_merge_dicts(base[k], v)
        else:
            base[k] = v
    return base


def merge_and_save_tokens(tokens_path: Path, registry: TokenRegistry) -> dict[str, Any]:
    """Write or merge `tokens.json` (DTCG format) at the file/folder level."""
    existing: dict[str, Any] = {}
    if tokens_path.is_file():
        try:
            loaded = json.loads(tokens_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                existing = loaded
        except (ValueError, OSError):
            existing = {}

    merged = _deep_merge_dicts(existing, registry.tree) if existing else registry.tree
    tokens_path.parent.mkdir(parents=True, exist_ok=True)
    tokens_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    return merged
