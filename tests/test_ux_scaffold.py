"""`coder-nexus ux new|screen|component|sync`: design-uiux scaffolding inside a work item."""

import json
import re
from pathlib import Path

import pytest

from coder_nexus.ux.scaffold import ScaffoldError, add_component, add_screen, new_design, resolve_work_item, sync


@pytest.fixture
def work_item(tmp_path):
    project = tmp_path / "wms-app"
    (project / "lib").mkdir(parents=True)
    (project / "pubspec.yaml").write_text("name: wms\n", encoding="utf-8")
    vdir = project / ".superpowers/work-items/is-no-po-count/v1"
    vdir.mkdir(parents=True)
    return vdir


def _flows(design: Path) -> dict:
    text = (design / "data/flows.js").read_text(encoding="utf-8")
    return json.loads(text[text.index("=") + 1:].rstrip().rstrip(";"))


def test_resolve_work_item_accepts_vn_or_design_folder(work_item):
    assert resolve_work_item(str(work_item))[2:] == ("is-no-po-count", "v1")
    assert resolve_work_item(str(work_item / "design-uiux"))[0] == work_item.resolve()
    with pytest.raises(ScaffoldError):
        resolve_work_item(str(work_item.parent))


def test_new_creates_structure_kit_and_catalog(work_item):
    res = new_design(str(work_item), "Kiểm đếm manual items")
    d = work_item / "design-uiux"
    for rel in ("uiux.md", "index.html", "CHANGELOG.md", "data/mock-data.js", "data/flows.js", "shots/.gitignore"):
        assert (d / rel).is_file(), rel
    for sub in ("screens", "components", "assets"):
        assert (d / sub).is_dir()
    sp = work_item.parents[2]
    assert (sp / "ux/kit/kit.css").is_file(), "kit generated on first use"
    assert (sp / "ux/screen-catalog.md").is_file()
    uiux = (d / "uiux.md").read_text(encoding="utf-8")
    assert "# UI/UX: Kiểm đếm manual items — v1" in uiux and "> **Work Item**: is-no-po-count" in uiux
    # index.html links resolve to the shared kit
    for href in re.findall(r'(?:href|src)="([^"]+)"', (d / "index.html").read_text(encoding="utf-8")):
        assert (d / href).resolve().is_file(), href
    # running again does not overwrite edits
    (d / "uiux.md").write_text(uiux + "\nEDITED\n", encoding="utf-8")
    assert new_design(str(work_item), "Other title")["created"] == []
    assert "EDITED" in (d / "uiux.md").read_text(encoding="utf-8")


def test_screen_and_component_add_files_rows_and_flows(work_item):
    new_design(str(work_item), "Kiểm đếm")
    d = work_item / "design-uiux"
    add_screen(str(work_item), "S01", "is-items-list", "Danh sách IS Items", "W-01#1", "changed", "wms.is-items.list")
    add_screen(str(work_item), "S02", "receive-qty", "Nhập số lượng", "W-01#2", "NEW", states="default,error,submitting")
    add_screen(str(work_item), "S02", "receive-qty", "Nhập số lượng", "W-01#2", "NEW")  # no duplicate row
    add_component(str(work_item), "C01", "no-po-warning", "Cảnh báo chưa có PO", "S02")

    s02 = (d / "screens/S02-receive-qty.html").read_text(encoding="utf-8")
    assert 'data-screen="S02"' in s02 and 'data-steps="W-01#2"' in s02 and 'data-catalog="TODO"' in s02
    assert [m for m in re.findall(r'data-state="(\w+)"', s02)] == ["default", "error", "submitting"]
    for href in re.findall(r'(?:href|src)="([^"]+\.(?:css|js))"', s02):
        assert (d / "screens" / href).resolve().is_file(), href
    s01 = (d / "screens/S01-is-items-list.html").read_text(encoding="utf-8")
    assert re.findall(r'data-state="(\w+)"', s01) == ["default", "loading", "empty", "error"]

    uiux = (d / "uiux.md").read_text(encoding="utf-8")
    assert len(re.findall(r"^\| S02 \|", uiux, re.MULTILINE)) == 1
    assert "| S01 | Danh sách IS Items | screens/S01-is-items-list.html | wms.is-items.list | CHANGED | W-01#1 |" in uiux
    assert "| C01 | Cảnh báo chưa có PO | components/C01-no-po-warning.html | S02 | TODO |" in uiux
    assert (d / "components/C01-no-po-warning.html").is_file()

    # workflow added by the designer in uiux.md -> flows.js + warnings
    uiux = uiux.replace("| Workflow | Title | Goals | Steps |\n|---|---|---|---|\n",
                        "| Workflow | Title | Goals | Steps |\n|---|---|---|---|\n| W-01 | Kiểm đếm | G-01 | 1→S01, 2→S02, 3→S03 |\n")
    (d / "uiux.md").write_text(uiux, encoding="utf-8")
    res = sync(str(work_item))
    assert res["flows"] == 1 and res["screens"] == 2
    assert res["warnings"] == ["W-01 step S03 has no row in ## 5. Screens"]
    flows = _flows(d)
    assert flows["revision"] == "r1" and flows["approval"] == "DRAFT"
    assert [s["screen"] for s in flows["flows"][0]["steps"]] == ["S01", "S02", "S03"]
    assert flows["screens"][0]["kind"] == "CHANGED"


def test_sync_reports_orphan_screens_and_missing_files(work_item):
    new_design(str(work_item), "X")
    add_screen(str(work_item), "S01", "a", "A", "W-01#1")
    (work_item / "design-uiux/screens/S01-a.html").unlink()
    warnings = sync(str(work_item))["warnings"]
    assert "S01 is not in any workflow" in warnings
    assert "S01 file missing: screens/S01-a.html" in warnings


def test_invalid_ids_and_missing_new(work_item):
    with pytest.raises(ScaffoldError, match="ux new"):
        add_screen(str(work_item), "S01", "a", "A")
    new_design(str(work_item), "X")
    with pytest.raises(ScaffoldError):
        add_screen(str(work_item), "screen1", "a", "A")
    with pytest.raises(ScaffoldError):
        add_screen(str(work_item), "S01", "a", "A", kind="MAYBE")
    with pytest.raises(ScaffoldError):
        add_component(str(work_item), "X1", "a", "A")


def test_sync_refreshes_a_stale_kit_but_keeps_decisions(work_item):
    import json
    from coder_nexus.ux.kitgen import ASSETS
    new_design(str(work_item), "X")
    sp = work_item.parents[2]
    ds_path = sp / "ux/design-system.json"
    ds = json.loads(ds_path.read_text(encoding="utf-8"))
    ds["source"]["decision"] = "D-07"
    ds_path.write_text(json.dumps(ds), encoding="utf-8")
    (sp / "ux/kit/kit.js").write_text("/* old kit without player */", encoding="utf-8")
    sync(str(work_item))
    assert (sp / "ux/kit/kit.js").read_text(encoding="utf-8") == (ASSETS / "kit.js").read_text(encoding="utf-8")
    assert json.loads(ds_path.read_text(encoding="utf-8"))["source"]["decision"] == "D-07"
