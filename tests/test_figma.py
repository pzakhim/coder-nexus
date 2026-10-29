"""Figma extraction: URL parsing, REST calls (httpx mocked, no network) and the task-detail hook."""

import asyncio
import json
from pathlib import Path

import httpx
import pytest

from coder_nexus.figma import (
    build_spec_dict,
    extract_icon_nodes,
    fetch_async,
    infer_canonical_pattern,
    load_figma_token,
    parse_figma_url,
)
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
                 "styles": {"fill": "s_brand", "text": "s_btn_text"},
                 "absoluteBoundingBox": {"x": 20, "y": 700, "width": 100, "height": 20},
                 "style": {"fontFamily": "Inter", "fontWeight": 600, "fontSize": 16, "lineHeightPx": 24},
                 "fills": [{"type": "SOLID", "color": {"r": 0, "g": 0.333, "b": 0.667, "a": 1}}]},
                {"id": "3", "name": "Title", "type": "TEXT", "characters": "Receive goods",
                 "absoluteBoundingBox": {"x": 20, "y": 40, "width": 200, "height": 28},
                 "style": {"fontFamily": "Inter", "fontWeight": 700, "fontSize": 22}, "fills": []},
                {"id": "4", "name": "Hidden", "type": "TEXT", "characters": "Secret draft", "visible": False,
                 "absoluteBoundingBox": {"x": 0, "y": 10, "width": 10, "height": 10}},
                {"id": "5", "name": "btn", "type": "INSTANCE", "componentId": "c1",
                 "componentProperties": {"Variant": {"type": "VARIANT", "value": "Primary"}},
                 "absoluteBoundingBox": {"x": 20, "y": 690, "width": 350, "height": 48}},
            ],
        },
        "components": {"c1": {"key": "k_c1", "name": "Button/Primary", "componentSetId": "cs1"}},
        "componentSets": {"cs1": {"key": "k_cs1", "name": "Button"}},
        "styles": {
            "s_brand": {"key": "k_brand", "name": "Primary/Brand 500", "styleType": "FILL"},
            "s_btn_text": {"key": "k_btntxt", "name": "Button/Label M", "styleType": "TEXT"},
        },
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
    assert res.screen_images == [res.png_path]
    assert json.loads(Path(res.json_path).read_text())["nodes"][NODE]["document"]["name"] == "Receive goods"
    spec = json.loads(Path(res.spec_path).read_text())
    assert spec["file_key"] == KEY and spec["root_node_id"] == NODE and spec["root_image_path"] == res.png_path
    assert spec["tokens_file"] == "tokens.json"
    assert len(spec["screens"]) == 1
    assert spec["screens"][0]["suggested_id"] == "S01"
    assert spec["screens"][0]["image_path"] == res.png_path
    assert spec["screens"][0]["bounds"] == {"x": 0, "y": 0, "width": 390, "height": 844}
    assert spec["screens"][0]["components"][0]["component_name"] == "Button/Primary"
    assert spec["screens"][0]["components"][0]["pattern_hint"] == "button"
    # Framelink-style tree referencing DTCG tokens by name
    tree = spec["screens"][0]["tree"]
    assert tree["id"] == NODE and tree["tokens"]["fill"] == "{color.unlinked.background-ffffff}"
    submit_node = next(c for c in tree["children"] if c["id"] == "2")
    assert submit_node["text"] == "Submit"
    assert submit_node["tokens"]["textColor"] == "{color.primary.brand-500}"
    assert submit_node["tokens"]["textStyle"] == "{typography.button.label-m}"
    btn_node = next(c for c in tree["children"] if c["id"] == "5")
    assert btn_node["component"] == {
        "id": "c1",
        "name": "Button/Primary",
        "componentSet": "Button",
        "properties": {"Variant": "Primary"},
        "patternHint": "button",
    }
    # DTCG tokens.json verification
    tokens = json.loads(Path(res.tokens_path).read_text())
    assert tokens["$schema"] == "https://tr.designtokens.org/format/"
    assert tokens["color"]["primary"]["brand-500"]["$type"] == "color"
    assert tokens["color"]["primary"]["brand-500"]["$value"] == "#0055AA"
    assert tokens["typography"]["button"]["label-m"]["$type"] == "typography"
    assert tokens["typography"]["button"]["label-m"]["$value"]["fontFamily"] == "Inter"
    assert tokens["$extensions"]["com.figma"]["componentSets"]["cs1"]["name"] == "Button"
    assert spec["design_tokens"]["component_catalog"] == [
        {
            "component_id": "c1",
            "component_name": "Button/Primary",
            "pattern_hint": "button",
            "instances_count": 1,
        }
    ]
    summary = Path(res.summary_path).read_text()
    assert summary.index("Receive goods  _(Inter 700 22px)_") < summary.index("Submit  _(Inter 600 16px, #0055AA)_")
    assert "Secret draft" not in summary
    assert "| #FFFFFF | 1 |" in summary and "| Button/Primary (layer: btn) | 1 |" in summary
    assert "FRAME 390×844" in summary and "![Receive goods](1150-10051.png)" in summary
    # the token goes to the Figma API only, never to the rendered-image host
    assert all(("x-figma-token" in r.headers) == (r.url.host == "api.figma.com") for r in seen)
    assert all(r.method == "GET" for r in seen)


def test_fetch_section_splits_screens_and_renders_each_screen_image(tmp_path: Path):
    sec_node = "2000:1"
    s1_node, s2_node = "2000:10", "2000:20"
    sec_url = f"https://www.figma.com/design/{KEY}/iMES-Mobile?node-id=2000-1"
    s1_img = "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/s1.png"
    s2_img = "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/s2.png"
    section_payload = {
        "name": "iMES Mobile",
        "lastModified": "2026-10-20T08:00:00Z",
        "nodes": {sec_node: {
            "document": {
                "id": sec_node,
                "name": "Receive Flow",
                "type": "SECTION",
                "absoluteBoundingBox": {"x": 0, "y": 0, "width": 900, "height": 844},
                "children": [
                    {
                        "id": s2_node,
                        "name": "02 - Scan Item",
                        "type": "FRAME",
                        "layoutMode": "VERTICAL",
                        "itemSpacing": 12,
                        "paddingTop": 16,
                        "paddingRight": 16,
                        "paddingBottom": 16,
                        "paddingLeft": 16,
                        "cornerRadius": 8,
                        "absoluteBoundingBox": {"x": 450, "y": 0, "width": 390, "height": 844},
                        "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1, "a": 1}}],
                        "children": [
                            {
                                "id": "2000:21",
                                "name": "Header",
                                "type": "FRAME",
                                "layoutMode": "HORIZONTAL",
                                "absoluteBoundingBox": {"x": 450, "y": 0, "width": 390, "height": 56},
                            }
                        ],
                    },
                    {
                        "id": s1_node,
                        "name": "01 - Receipt List",
                        "type": "FRAME",
                        "absoluteBoundingBox": {"x": 0, "y": 0, "width": 390, "height": 844},
                        "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1, "a": 1}}],
                        "children": [
                            {
                                "id": "2000:11",
                                "name": "NextBtn",
                                "type": "INSTANCE",
                                "componentId": "c1",
                                "transitionNodeID": s2_node,
                                "absoluteBoundingBox": {"x": 20, "y": 700, "width": 350, "height": 48},
                            }
                        ],
                    },
                ],
            },
            "components": {"c1": {"name": "Button/Primary"}},
        }},
    }

    def section_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == f"/v1/files/{KEY}/nodes":
            return httpx.Response(200, json=section_payload)
        if request.url.path == f"/v1/images/{KEY}":
            assert request.url.params["ids"] == f"{sec_node},{s1_node},{s2_node}"
            return httpx.Response(200, json={
                "err": None,
                "images": {sec_node: IMG_URL, s1_node: s1_img, s2_node: s2_img},
            })
        if str(request.url) in (IMG_URL, s1_img, s2_img):
            return httpx.Response(200, content=PNG)
        return httpx.Response(404)

    res = asyncio.run(
        fetch_async(sec_url, tmp_path, "figd_test", transport=httpx.MockTransport(section_handler))
    )
    assert res.status == "READ"
    assert len(res.screen_images) == 2
    assert Path(res.screen_images[0]).name == "2000-1-S01.png"
    assert Path(res.screen_images[1]).name == "2000-1-S02.png"
    spec = json.loads(Path(res.spec_path).read_text())
    assert [s["suggested_id"] for s in spec["screens"]] == ["S01", "S02"]
    assert [s["name"] for s in spec["screens"]] == ["01 - Receipt List", "02 - Scan Item"]
    assert spec["screens"][0]["image_path"] == res.screen_images[0]
    assert spec["screens"][0]["interactions"] == [
        {"trigger_node_id": "2000:11", "trigger_name": "NextBtn", "destination_node_id": s2_node}
    ]
    assert spec["screens"][1]["image_path"] == res.screen_images[1]
    assert spec["screens"][1]["layout"]["mode"] == "VERTICAL"
    assert spec["design_tokens"]["corner_radii"] == [8]
    summary = Path(res.summary_path).read_text()
    assert "## Screens (2)" in summary
    assert "![S01](2000-1-S01.png)" in summary and "![S02](2000-1-S02.png)" in summary


def test_fetch_jpg_format(tmp_path: Path):
    def jpg_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == f"/v1/files/{KEY}/nodes":
            return httpx.Response(200, json=NODES)
        if request.url.path == f"/v1/images/{KEY}":
            assert request.url.params["format"] == "jpg"
            return httpx.Response(200, json={"err": None, "images": {NODE: IMG_URL}})
        if str(request.url) == IMG_URL:
            return httpx.Response(200, content=b"\xff\xd8\xff\xe0fakejpg")
        return httpx.Response(404)

    res = asyncio.run(
        fetch_async(URL, tmp_path, "figd_test", image_format="jpg", transport=httpx.MockTransport(jpg_handler))
    )
    assert res.status == "READ"
    assert Path(res.png_path).name == "1150-10051.jpg"
    assert res.screen_images == [res.png_path]


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
    monkeypatch.delenv("FIGMA_ACCESS_TOKEN", raising=False)
    assert load_figma_token(str(tmp_path)) is None
    (tmp_path / ".env").write_text("HULY_EMAIL=a@b.c\nFIGMA_ACCESS_TOKEN=figd_alt\n")
    assert load_figma_token(str(tmp_path)) == "figd_alt"
    (tmp_path / ".env").write_text("HULY_EMAIL=a@b.c\nFIGMA_ACCESS_TOKEN=figd_alt\nFIGMA_TOKEN='figd_x'\n")
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


@pytest.mark.parametrize(
    "node_name,comp_name,set_name,expected",
    [
        ("Top Header", "AppBar/Default", "", "appbar"),
        ("Main Tabs", "BottomNav", "", "bottomnav"),
        ("Filter Sheet", "BottomSheet/Common", "", "bottomsheet"),
        ("Confirm Delete", "Modal/Dialog", "", "dialog"),
        ("Order Date", "DatePicker/Range", "", "datepicker"),
        ("Search SKU", "SearchBar", "", "search"),
        ("Warehouse Select", "Dropdown/Single", "", "dropdown"),
        ("Quantity Input", "TextField/Outlined", "", "formfield"),
        ("Save CTA", "Button/Primary", "Button", "button"),
        ("Status", "StatusPill", "Badge", "badge"),
        ("Filter Tag", "FilterChip", "", "chip"),
        ("Empty List", "NoData/Illustration", "", "nodata"),
        ("Skeleton Row", "ListViewShimmer", "", "loading"),
        ("Warning Notice", "Banner/Warning", "", "banner"),
        ("Order Summary", "Card/Elevated", "", "card"),
        ("Order Row", "ListItem", "", "list"),
        ("Custom Barcode Gauge", "Gauge/Radial", "", "custom"),
    ],
)
def test_infer_canonical_pattern(node_name, comp_name, set_name, expected):
    assert infer_canonical_pattern(node_name, comp_name, set_name) == expected


def test_repeating_children_deduplication_and_advanced_layout_semantics():
    root_id = "3000:1"
    payload = {
        "name": "iMES Warehouse",
        "lastModified": "2026-10-29T08:00:00Z",
        "nodes": {
            root_id: {
                "document": {
                    "id": root_id,
                    "name": "Stock List Screen",
                    "type": "FRAME",
                    "layoutMode": "VERTICAL",
                    "overflowDirection": "VERTICAL_SCROLLING",
                    "minWidth": 360,
                    "maxWidth": 768,
                    "absoluteBoundingBox": {"x": 0, "y": 0, "width": 390, "height": 844},
                    "children": [
                        {
                            "id": "3000:2",
                            "name": "Sticky Header",
                            "type": "FRAME",
                            "layoutMode": "HORIZONTAL",
                            "scrollBehavior": "STICKY_SCROLLING",
                            "absoluteBoundingBox": {"x": 0, "y": 0, "width": 390, "height": 56},
                            "children": [
                                {
                                    "id": "3000:3",
                                    "name": "Header Title",
                                    "type": "TEXT",
                                    "characters": "Warehouse Inventory Very Long Title",
                                    "maxLines": 1,
                                    "style": {
                                        "fontFamily": "Inter",
                                        "fontWeight": 700,
                                        "fontSize": 18,
                                        "textTruncation": "ENDING",
                                        "textAutoResize": "TRUNCATE",
                                        "textAlignHorizontal": "CENTER",
                                    },
                                    "absoluteBoundingBox": {"x": 16, "y": 16, "width": 300, "height": 24},
                                }
                            ],
                        },
                        {
                            "id": "3000:10",
                            "name": "Item Row 1",
                            "type": "INSTANCE",
                            "componentId": "comp_row",
                            "absoluteBoundingBox": {"x": 0, "y": 60, "width": 390, "height": 64},
                            "children": [
                                {"id": "3000:11", "name": "SKU", "type": "TEXT", "characters": "SKU-001", "style": {"fontFamily": "Inter", "fontSize": 14}, "absoluteBoundingBox": {"x": 16, "y": 70, "width": 100, "height": 20}},
                                {"id": "3000:12", "name": "Qty", "type": "TEXT", "characters": "120 pcs", "style": {"fontFamily": "Inter", "fontSize": 14}, "absoluteBoundingBox": {"x": 280, "y": 70, "width": 80, "height": 20}},
                            ],
                        },
                        {
                            "id": "3000:20",
                            "name": "Item Row 2",
                            "type": "INSTANCE",
                            "componentId": "comp_row",
                            "absoluteBoundingBox": {"x": 0, "y": 130, "width": 390, "height": 64},
                            "children": [
                                {"id": "3000:21", "name": "SKU", "type": "TEXT", "characters": "SKU-002", "style": {"fontFamily": "Inter", "fontSize": 14}, "absoluteBoundingBox": {"x": 16, "y": 140, "width": 100, "height": 20}},
                                {"id": "3000:22", "name": "Qty", "type": "TEXT", "characters": "85 pcs", "style": {"fontFamily": "Inter", "fontSize": 14}, "absoluteBoundingBox": {"x": 280, "y": 140, "width": 80, "height": 20}},
                            ],
                        },
                        {
                            "id": "3000:30",
                            "name": "Item Row 3",
                            "type": "INSTANCE",
                            "componentId": "comp_row",
                            "absoluteBoundingBox": {"x": 0, "y": 200, "width": 390, "height": 64},
                            "children": [
                                {"id": "3000:31", "name": "SKU", "type": "TEXT", "characters": "SKU-003", "style": {"fontFamily": "Inter", "fontSize": 14}, "absoluteBoundingBox": {"x": 16, "y": 210, "width": 100, "height": 20}},
                                {"id": "3000:32", "name": "Qty", "type": "TEXT", "characters": "40 pcs", "style": {"fontFamily": "Inter", "fontSize": 14}, "absoluteBoundingBox": {"x": 280, "y": 210, "width": 80, "height": 20}},
                            ],
                        },
                        {
                            "id": "3000:40",
                            "name": "Floating Scan Button",
                            "type": "INSTANCE",
                            "componentId": "comp_fab",
                            "layoutPositioning": "ABSOLUTE",
                            "scrollBehavior": "FIXED_WHEN_SCROLLING",
                            "constraints": {"horizontal": "MAX", "vertical": "MAX"},
                            "absoluteBoundingBox": {"x": 318, "y": 760, "width": 56, "height": 56},
                        },
                    ],
                },
                "components": {
                    "comp_row": {"name": "InventoryListItem"},
                    "comp_fab": {"name": "FAB/ScanButton"},
                },
            }
        },
    }

    spec = build_spec_dict(payload, root_id, "https://www.figma.com/design/KEY/File?node-id=3000-1", file_key="KEY")
    screen = spec["screens"][0]
    tree = screen["tree"]

    # 1. Screen root scrollDirection & minMax bounds
    assert tree["layout"]["scrollDirection"] == "vertical"
    assert tree["layout"]["minMax"] == {"minWidth": 360, "maxWidth": 768}

    # 2. Sticky header + textMeta (maxLines, truncation, autoResize, align)
    header_node = tree["children"][0]
    assert header_node["layout"]["scrollBehavior"] == "sticky"
    title_node = header_node["children"][0]
    assert title_node["textMeta"] == {
        "maxLines": 1,
        "truncation": "ellipsis",
        "autoResize": "truncate",
        "align": "center",
    }

    # 3. Repeating children deduplication: 3 consecutive comp_row items -> 1 representative with repeatCount=3
    assert len(tree["children"]) == 3  # Sticky Header, deduplicated Item Row 1 (x3), Floating Scan Button
    row_rep = tree["children"][1]
    assert row_rep["id"] == "3000:10"
    assert row_rep["repeatCount"] == 3
    assert row_rep["repeatedSamples"] == ["SKU-002 | 85 pcs", "SKU-003 | 40 pcs"]
    assert row_rep["component"]["patternHint"] == "list"

    # Full texts_reading_order and components list still preserve all 3 rows
    all_texts = [t["text"] for t in screen["texts_reading_order"]]
    assert "SKU-001" in all_texts and "SKU-002" in all_texts and "SKU-003" in all_texts
    assert len(screen["components"]) == 4

    # 4. Absolute positioning & fixed scroll behavior on FAB
    fab_node = tree["children"][2]
    assert fab_node["layout"]["positioning"] == "absolute"
    assert fab_node["layout"]["constraints"] == {"horizontal": "max", "vertical": "max"}
    assert fab_node["layout"]["scrollBehavior"] == "fixed"
    assert fab_node["component"]["patternHint"] == "button"


def test_export_icons_writes_svgs_without_leaking_token(tmp_path: Path):
    icon_id = "4000:99"
    svg_url = "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/barcode-icon.svg"
    svg_bytes = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z"/></svg>'

    icon_payload = {
        "name": "iMES Mobile",
        "lastModified": "2026-10-29T08:00:00Z",
        "nodes": {
            NODE: {
                "document": {
                    "id": NODE,
                    "name": "Scan Screen",
                    "type": "FRAME",
                    "absoluteBoundingBox": {"x": 0, "y": 0, "width": 390, "height": 844},
                    "children": [
                        {
                            "id": icon_id,
                            "name": "ic_barcode_scan",
                            "type": "FRAME",
                            "absoluteBoundingBox": {"x": 20, "y": 20, "width": 24, "height": 24},
                            "children": [
                                {"id": "4000:100", "name": "Vector", "type": "VECTOR"},
                            ],
                        }
                    ],
                },
            }
        },
    }

    assert extract_icon_nodes(icon_payload["nodes"][NODE]["document"]) == [
        {"id": icon_id, "name": "ic_barcode_scan"}
    ]

    seen: list[httpx.Request] = []

    def icon_handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path == f"/v1/files/{KEY}/nodes":
            return httpx.Response(200, json=icon_payload)
        if request.url.path == f"/v1/images/{KEY}":
            if request.url.params.get("format") == "svg":
                assert request.url.params["ids"] == icon_id
                return httpx.Response(200, json={"err": None, "images": {icon_id: svg_url}})
            return httpx.Response(200, json={"err": None, "images": {NODE: IMG_URL}})
        if str(request.url) == IMG_URL:
            return httpx.Response(200, content=PNG)
        if str(request.url) == svg_url:
            return httpx.Response(200, content=svg_bytes)
        return httpx.Response(404)

    res = asyncio.run(
        fetch_async(
            URL,
            tmp_path,
            "figd_test",
            export_icons=True,
            transport=httpx.MockTransport(icon_handler),
        )
    )
    assert res.status == "READ"
    assert len(res.icon_svg_paths) == 1
    svg_file = Path(res.icon_svg_paths[0])
    assert svg_file.exists() and svg_file.parent.name == "icons"
    assert svg_file.name == "4000-99-ic_barcode_scan.svg"
    assert svg_file.read_bytes() == svg_bytes

    spec = json.loads(Path(res.spec_path).read_text())
    assert spec["icon_svg_paths"] == res.icon_svg_paths

    # Verify token isolation: X-Figma-Token never sent to S3 render/SVG hosts
    assert all(("x-figma-token" in r.headers) == (r.url.host == "api.figma.com") for r in seen)
