"""Figma extraction: URL parsing, REST calls (httpx mocked, no network) and the task-detail hook."""

import asyncio
import json
from pathlib import Path

import httpx
import pytest

from coder_nexus.figma import fetch_async, load_figma_token, parse_figma_url
from coder_nexus.huly.client import _fetch_figma_source
from coder_nexus.huly.models import HulySource

KEY, NODE = "bWz9MHxiPgminB8QqZ7DMe", "1150:10051"
URL = f"https://www.figma.com/design/{KEY}/iMES-Mobile?node-id=1150-10051&t=abc"
IMG_URL = "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/render.png"
PNG = b"\x89PNG\r\n\x1a\nfake"

NODES = {
    "name": "iMES Mobile",
    "lastModified": "2026-10-20T08:00:00Z",
    "nodes": {NODE: {
        "document": {
            "id": NODE, "name": "Receive goods", "type": "FRAME",
            "absoluteBoundingBox": {"x": 0, "y": 0, "width": 390, "height": 844},
            "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1, "a": 1}}],
            "children": [
                {"id": "2", "name": "Submit", "type": "TEXT", "characters": "Submit",
                 "absoluteBoundingBox": {"x": 20, "y": 700, "width": 100, "height": 20},
                 "style": {"fontFamily": "Inter", "fontWeight": 600, "fontSize": 16},
                 "fills": [{"type": "SOLID", "color": {"r": 0, "g": 0.333, "b": 0.667, "a": 1}}]},
                {"id": "3", "name": "Title", "type": "TEXT", "characters": "Receive goods",
                 "absoluteBoundingBox": {"x": 20, "y": 40, "width": 200, "height": 28},
                 "style": {"fontFamily": "Inter", "fontWeight": 700, "fontSize": 22}, "fills": []},
                {"id": "4", "name": "Hidden", "type": "TEXT", "characters": "Secret draft", "visible": False,
                 "absoluteBoundingBox": {"x": 0, "y": 10, "width": 10, "height": 10}},
                {"id": "5", "name": "btn", "type": "INSTANCE", "componentId": "c1",
                 "absoluteBoundingBox": {"x": 20, "y": 690, "width": 350, "height": 48}},
            ],
        },
        "components": {"c1": {"name": "Button/Primary"}},
    }},
}


def make_transport(status: int = 200, seen: list | None = None) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        if request.url.host == "api.figma.com" and status != 200:
            return httpx.Response(status, json={"status": status, "err": "Forbidden"})
        if request.url.path == f"/v1/files/{KEY}/nodes":
            assert request.url.params["ids"] == NODE
            return httpx.Response(200, json=NODES)
        if request.url.path == f"/v1/images/{KEY}":
            assert request.url.params["format"] == "png" and request.url.params["scale"] == "2"
            return httpx.Response(200, json={"err": None, "images": {NODE: IMG_URL}})
        if str(request.url) == IMG_URL:
            return httpx.Response(200, content=PNG)
        return httpx.Response(404)
    return httpx.MockTransport(handler)


@pytest.mark.parametrize("url,key,node", [
    (URL, KEY, "1150:10051"),
    (f"https://figma.com/file/{KEY}/Name?type=design&node-id=1150%3A10051", KEY, "1150:10051"),
    (f"https://www.figma.com/design/{KEY}/branch/BRANCHKEY/Name?node-id=1-2", "BRANCHKEY", "1:2"),
    (f"https://www.figma.com/proto/{KEY}/Name?node-id=3-4&scaling=min-zoom", KEY, "3:4"),
    (f"https://www.figma.com/design/{KEY}/Name", KEY, None),
])
def test_parse_figma_url(url, key, node):
    ref = parse_figma_url(url)
    assert (ref.file_key, ref.node_id) == (key, node)


@pytest.mark.parametrize("url", ["https://example.com/design/x/y?node-id=1-2", "https://www.figma.com/community/file/1", "not a url"])
def test_parse_figma_url_rejects(url):
    with pytest.raises(ValueError):
        parse_figma_url(url)


def test_fetch_success_writes_png_json_summary(tmp_path: Path):
    seen: list[httpx.Request] = []
    res = asyncio.run(fetch_async(URL, tmp_path, "figd_test", transport=make_transport(seen=seen)))
    assert res.status == "READ" and res.name == "Receive goods" and res.note is None
    assert Path(res.png_path).name == "1150-10051.png" and Path(res.png_path).read_bytes() == PNG
    assert json.loads(Path(res.json_path).read_text())["nodes"][NODE]["document"]["name"] == "Receive goods"
    summary = Path(res.summary_path).read_text()
    assert summary.index("Receive goods  _(Inter 700 22px)_") < summary.index("Submit  _(Inter 600 16px, #0055AA)_")
    assert "Secret draft" not in summary
    assert "| #FFFFFF | 1 |" in summary and "| Button/Primary (layer: btn) | 1 |" in summary
    assert "FRAME 390×844" in summary and "![Receive goods](1150-10051.png)" in summary
    # the token goes to the Figma API only, never to the rendered-image host
    assert all(("x-figma-token" in r.headers) == (r.url.host == "api.figma.com") for r in seen)
    assert all(r.method == "GET" for r in seen)


def test_fetch_without_token_is_not_provided(tmp_path: Path):
    def boom(request):  # pragma: no cover - must not be called
        raise AssertionError("no request without a token")
    res = asyncio.run(fetch_async(URL, tmp_path / "out", None, transport=httpx.MockTransport(boom)))
    assert res.status == "NOT_PROVIDED" and "FIGMA_TOKEN" in res.note
    assert not (tmp_path / "out").exists()


def test_fetch_403_is_unreachable(tmp_path: Path):
    res = asyncio.run(fetch_async(URL, tmp_path, "bad", transport=make_transport(status=403)))
    assert res.status == "UNREACHABLE" and "403" in res.note
    assert list(tmp_path.iterdir()) == []


def test_fetch_link_without_node_is_unreachable(tmp_path: Path):
    res = asyncio.run(fetch_async(f"https://www.figma.com/design/{KEY}/Name", tmp_path, "t", transport=make_transport()))
    assert res.status == "UNREACHABLE" and "node-id" in res.note


def test_token_from_client_env(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("FIGMA_TOKEN", raising=False)
    assert load_figma_token(str(tmp_path)) is None
    (tmp_path / ".env").write_text("HULY_EMAIL=a@b.c\nFIGMA_TOKEN='figd_x'\n")
    assert load_figma_token(str(tmp_path)) == "figd_x"


REAL_ASYNC_CLIENT = httpx.AsyncClient


def _patch_httpx(monkeypatch, transport):
    class _Patched(REAL_ASYNC_CLIENT):
        def __init__(self, *a, **kw):
            kw["transport"] = transport
            super().__init__(*a, **kw)
    monkeypatch.setattr(httpx, "AsyncClient", _Patched)


def test_task_detail_hook_marks_figma_source(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("FIGMA_TOKEN", raising=False)
    _patch_httpx(monkeypatch, make_transport())
    link = HulySource(kind="link", title="Figma", origin="description", url=URL, status="EXTERNAL")

    sources = [link]
    asyncio.run(_fetch_figma_source(sources, URL, tmp_path / "figma", str(tmp_path)))
    assert link.kind == "figma" and link.status == "NOT_PROVIDED" and link.local_path is None

    (tmp_path / ".env").write_text("FIGMA_TOKEN=figd_test\n")
    asyncio.run(_fetch_figma_source(sources, URL, tmp_path / "figma", str(tmp_path)))
    assert len(sources) == 1 and link.status == "READ" and link.title == "Figma: Receive goods"
    assert link.local_path == str(tmp_path / "figma" / "1150-10051.png") and "Receive goods" in link.text

    _patch_httpx(monkeypatch, make_transport(status=404))
    fresh: list[HulySource] = []
    asyncio.run(_fetch_figma_source(fresh, URL, tmp_path / "f2", str(tmp_path)))
    assert fresh[0].kind == "figma" and fresh[0].status == "UNREACHABLE" and "404" in fresh[0].note
