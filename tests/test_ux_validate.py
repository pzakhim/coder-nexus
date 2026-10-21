"""`coder-nexus ux validate` / MCP `validate_ux_design`: rules UX-001 … UX-011 on scaffolded designs."""

import argparse
import json
import re
from pathlib import Path

import pytest

from coder_nexus.server import app
from coder_nexus.ux.commands import cmd_ux
from coder_nexus.ux.kitgen import DEFAULT_VIEWPORTS, save_viewports
from coder_nexus.ux.scaffold import add_component, add_screen, new_design, sync
from coder_nexus.ux.validate import content_hash, load_mock, mock_value, validate_design, write_content_hash

UIUX_BODY = """## 1. Summary

Thủ kho kiểm đếm hàng chưa có PO (G-01).

## 2. Sources

| Source | Kind | Used for |
|---|---|---|
| IMES-1190 | Huly ticket | workflow |

## 3. Platforms and design source

- **Viewports**: `.superpowers/ux/viewports.json` (decision: D-01)
- **Design source**: `.superpowers/ux/design-system.json` (decision: D-02)

## 4. Workflows

| Workflow | Title | Goals | Steps |
|---|---|---|---|
| W-01 | Kiểm đếm | G-01 | 1→S01, 2→S02 |

## 5. Screens

| Screen | Title | File | Catalog | Kind | Steps | States | Kit classes | New components |
|---|---|---|---|---|---|---|---|---|
| S01 | Danh sách | screens/S01-items.html | wms.items.list | CHANGED | W-01#1 | default, loading, empty, error | app-list | |
| S02 | Nhập số lượng | screens/S02-qty.html | wms.items.qty | NEW | W-01#2 | default, error | app-formfield | C01 |

## 6. New components

| Component | Title | File | Used in | Why not in the kit |
|---|---|---|---|---|
| C01 | Cảnh báo chưa có PO | components/C01-no-po.html | S02 | Kit banner has no inline action |

## 7. Approval

- **Approved revision**: NONE
- **Approved on**: NONE
- **User response**: NONE
"""

S01 = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><link rel="stylesheet" href="{kit}/kit.css"></head>
<body>
<main class="screen" data-screen="S01" data-steps="W-01#1" data-catalog="wms.items.list">
  <header class="app-appbar"><span class="title">Danh sách</span></header>
  <section class="app-content" data-state="default">
    <div class="app-list"><a class="app-list-item" href="S02-qty.html" data-next><span class="body"><div class="title" data-mock="items[0].name"></div></span></a></div>
    <div class="note" data-ref="AC-01">Danh sách chỉ hiện hàng chưa có PO.</div>
  </section>
  <section class="app-content" data-state="loading"><div class="app-shimmer" style="height:64px"></div></section>
  <section class="app-content" data-state="empty"><div class="app-nodata"><div class="title">Không có hàng</div></div></section>
  <section class="app-content" data-state="error"><div class="app-banner error">Không tải được dữ liệu</div></section>
</main>
</body></html>
"""

S02 = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><link rel="stylesheet" href="{kit}/kit.css"></head>
<body>
<main class="screen" data-screen="S02" data-steps="W-01#2" data-catalog="wms.items.qty">
  <header class="app-appbar"><span class="title">Nhập số lượng</span></header>
  <section class="app-content" data-state="default">
    <div class="new-component" data-name="Cảnh báo chưa có PO">Chưa có PO</div>
    <label class="app-formfield"><span>Số lượng</span><input data-mock="items[0].qty"></label>
    <a class="app-button">Lưu</a>
  </section>
  <section class="app-content" data-state="error"><div class="app-banner error">Số lượng phải lớn hơn 0</div></section>
</main>
</body></html>
"""

C01 = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><link rel="stylesheet" href="{kit}/kit.css"></head>
<body>
<main class="screen" data-component="C01" data-used-in="S02">
  <section class="app-content">
    <div class="note">Banner của kit không có nút hành động trong dòng.</div>
    <div class="new-component" data-name="Cảnh báo chưa có PO">Chưa có PO — báo thủ kho</div>
  </section>
</main>
</body></html>
"""

MOCK = """/* MOCK data */
window.MOCK = {
  // MOCK only
  items: [
    { name: 'Thùng carton (MOCK)', qty: 3, },
  ],
};
"""

REQUIREMENTS = """# Requirements

## 0. Goals

| Goal | Goal (outcome) | Success signal | Source | Status |
|---|---|---|---|---|
| G-01 | Thủ kho kiểm đếm hàng chưa có PO | đếm được | D-01 | CONFIRMED |
"""


@pytest.fixture
def work_item(tmp_path):
    project = tmp_path / "wms-app"
    (project / "lib").mkdir(parents=True)
    (project / "pubspec.yaml").write_text("name: wms\n", encoding="utf-8")
    vdir = project / ".superpowers/work-items/is-no-po/v1"
    vdir.mkdir(parents=True)
    return vdir


@pytest.fixture
def design(work_item):
    """A complete, consistent DRAFT design built with the scaffold commands, then filled in."""
    new_design(str(work_item), "Kiểm đếm")
    add_screen(str(work_item), "S01", "items", "Danh sách", "W-01#1", "CHANGED", "wms.items.list")
    add_screen(str(work_item), "S02", "qty", "Nhập số lượng", "W-01#2", "NEW", "wms.items.qty", "default,error")
    add_component(str(work_item), "C01", "no-po", "Cảnh báo chưa có PO", "S02")
    d = work_item / "design-uiux"
    header = (d / "uiux.md").read_text(encoding="utf-8").split("Open `index.html`")[0]
    (d / "uiux.md").write_text(header + UIUX_BODY, encoding="utf-8")
    kit = "../../../../../ux/kit"
    (d / "screens/S01-items.html").write_text(S01.format(kit=kit), encoding="utf-8")
    (d / "screens/S02-qty.html").write_text(S02.format(kit=kit), encoding="utf-8")
    (d / "components/C01-no-po.html").write_text(C01.format(kit=kit), encoding="utf-8")
    (d / "data/mock-data.js").write_text(MOCK, encoding="utf-8")
    (work_item / "requirements.md").write_text(REQUIREMENTS, encoding="utf-8")
    sync(str(work_item))
    return d


def _confirm_project(work_item: Path) -> None:
    project = work_item.parents[3]
    save_viewports(project, DEFAULT_VIEWPORTS, "D-01")
    ds_path = project / ".superpowers/ux/design-system.json"
    ds = json.loads(ds_path.read_text(encoding="utf-8"))
    ds["source"]["decision"] = "D-02"
    ds_path.write_text(json.dumps(ds), encoding="utf-8")


def _set(design: Path, old: str, new: str, rel: str = "uiux.md") -> None:
    path = design / rel
    text = path.read_text(encoding="utf-8")
    assert old in text, old
    path.write_text(text.replace(old, new), encoding="utf-8")


def _rules(res: dict, severity: str = "ERROR") -> list[str]:
    return [v["rule_id"] for v in res["violations"] if v["severity"] == severity]


def _approve(design: Path, work_item: Path) -> None:
    _confirm_project(work_item)
    _set(design, "> **Status**: DRAFT", "> **Status**: APPROVED")
    _set(design, "- **Approved revision**: NONE\n- **Approved on**: NONE\n- **User response**: NONE",
         "- **Approved revision**: r1\n- **Approved on**: 2026-10-21\n- **User response**: \"Duyệt r1\"")


def test_complete_design_passes(design, work_item):
    res = validate_design(str(work_item))
    assert res["status"] == "success" and res["document_type"] == "UIUX"
    assert res["violations"] == [], res["violations"]
    assert res["gate_status"] == "PASSED" and res["valid"] is True
    assert res["checked_rules"] == [f"UX-{i:03d}" for i in range(1, 12)]
    assert res["revision"] == "r1" and res["design_status"] == "DRAFT"
    assert validate_design(str(design))["valid"], "design-uiux folder is accepted too"


def test_validator_is_read_only(design, work_item):
    before = {p: p.read_bytes() for p in work_item.parents[2].rglob("*") if p.is_file()}
    _set(design, "1→S01, 2→S02", "1→S01, 2→S02, 3→S01")  # stale flows.js would be rewritten by sync
    before[design / "uiux.md"] = (design / "uiux.md").read_bytes()
    validate_design(str(work_item))
    after = {p: p.read_bytes() for p in work_item.parents[2].rglob("*") if p.is_file()}
    assert after == before


def test_missing_design_or_bad_path_fails_explicitly(work_item, tmp_path):
    res = validate_design(str(work_item))
    assert res["status"] == "error" and res["valid"] is False and "ux new" in res["message"]
    assert validate_design(str(tmp_path))["status"] == "error"


def test_ux001_fields_and_sections(design, work_item):
    _set(design, "> **Document type**: UIUX", "> **Document type**: SPEC")
    _set(design, "> **Revision**: r1", "> **Revision**: 1")
    _set(design, "## 2. Sources", "## Sources")
    msgs = [v["message"] for v in validate_design(str(work_item))["violations"] if v["rule_id"] == "UX-001"]
    assert any("Document type" in m for m in msgs)
    assert any("Revision" in m for m in msgs)
    assert any("'## 2.'" in m for m in msgs)


def test_ux002_todo_warns_in_draft_and_fails_in_review(work_item):
    new_design(str(work_item), "X")
    res = validate_design(str(work_item))
    assert "UX-002" in _rules(res, "WARNING") and "UX-002" not in _rules(res)
    _set(work_item / "design-uiux", "> **Status**: DRAFT", "> **Status**: IN_REVIEW")
    assert "UX-002" in _rules(validate_design(str(work_item)))


def test_ux003_workflow_goals(design, work_item):
    _set(design, "| W-01 | Kiểm đếm | G-01 |", "| W-01 | Kiểm đếm | G-02 |")
    res = validate_design(str(work_item))
    assert any(v["rule_id"] == "UX-003" and "G-02" in v["message"] for v in res["violations"])
    (work_item / "requirements.md").unlink()
    assert validate_design(str(work_item))["valid"], "no requirements.md: goals cannot be cross-checked"
    _set(design, "| W-01 | Kiểm đếm | G-02 |", "| W-01 | Kiểm đếm | — |")
    assert "UX-003" in _rules(validate_design(str(work_item)))


def test_ux004_workflow_screen_consistency(design, work_item):
    _set(design, "1→S01, 2→S02", "1→S01, 2→S02, 3→S03")
    _set(design, 'data-steps="W-01#2"', 'data-steps="W-01#3"', "screens/S02-qty.html")
    res = validate_design(str(work_item))
    msgs = [v["message"] for v in res["violations"] if v["rule_id"] == "UX-004"]
    assert any("S03 has no row" in m for m in msgs)
    assert any("data-steps='W-01#3'" in m for m in msgs)
    assert any(v["rule_id"] == "UX-004" and v["severity"] == "WARNING" and "flows.js" in v["message"] for v in res["violations"])

    _set(design, "1→S01, 2→S02, 3→S03", "1→S01")
    (design / "screens/S01-items.html").unlink()
    msgs = [v["message"] for v in validate_design(str(work_item))["violations"] if v["rule_id"] == "UX-004"]
    assert "S02 is not in any workflow." in msgs
    assert "S01 file missing: screens/S01-items.html." in msgs


def test_ux005_list_screen_states(design, work_item):
    s01 = design / "screens/S01-items.html"
    text = s01.read_text(encoding="utf-8")
    s01.write_text(re.sub(r'  <section class="app-content" data-state="empty">.*?</section>\n', "", text, flags=re.S), encoding="utf-8")
    res = validate_design(str(work_item))
    assert any(v["rule_id"] == "UX-005" and "'empty'" in v["message"] for v in res["violations"] if v["severity"] == "ERROR")
    _set(design, "Danh sách chỉ hiện hàng chưa có PO.", "Không có trạng thái empty: luôn có ít nhất một dòng.", "screens/S01-items.html")
    res = validate_design(str(work_item))
    assert "UX-005" not in _rules(res) and "UX-005" in _rules(res, "WARNING")
    _set(design, 'data-state="default"', 'data-state="main"', "screens/S02-qty.html")
    assert any("default" in v["message"] for v in validate_design(str(work_item))["violations"] if v["rule_id"] == "UX-005")


def test_ux006_kit_classes_and_inline_styles(design, work_item):
    _set(design, '<a class="app-button">Lưu</a>', '<a class="app-fancy-button" style="color:#ff0000">Lưu</a>', "screens/S02-qty.html")
    res = validate_design(str(work_item))
    assert any(v["rule_id"] == "UX-006" and "app-fancy-button" in v["message"] for v in res["violations"] if v["severity"] == "ERROR")
    assert "UX-006" in _rules(res, "WARNING")
    assert not any("height:64px" in v["message"] for v in res["violations"]), "sizes are not colors"


def test_ux007_new_components(design, work_item):
    _set(design, 'data-name="Cảnh báo chưa có PO">Chưa có PO<', 'data-name="Thanh tiến độ">x<', "screens/S02-qty.html")
    _set(design, "| Kit banner has no inline action |", "| TODO |")
    res = validate_design(str(work_item))
    msgs = [v["message"] for v in res["violations"] if v["rule_id"] == "UX-007"]
    assert any("Thanh tiến độ" in m for m in msgs)
    assert any("Why not in the kit" in m for m in msgs)
    (design / "components/C01-no-po.html").unlink()
    assert any("C01 file missing" in v["message"] for v in validate_design(str(work_item))["violations"])


def test_ux008_mock_paths(design, work_item):
    assert mock_value(load_mock(design / "data/mock-data.js"), "items[0].qty") == 3
    _set(design, 'data-mock="items[0].qty"', 'data-mock="items[1].qty"', "screens/S02-qty.html")
    assert any(v["rule_id"] == "UX-008" and "items[1].qty" in v["message"] for v in validate_design(str(work_item))["violations"])
    (design / "data/mock-data.js").write_text("window.MOCK = buildMock();\n", encoding="utf-8")
    res = validate_design(str(work_item))
    assert "UX-008" in _rules(res, "WARNING") and "UX-008" not in _rules(res)


def test_ux009_viewports_and_source_before_review(design, work_item):
    _set(design, "> **Status**: DRAFT", "> **Status**: IN_REVIEW")
    msgs = [v["message"] for v in validate_design(str(work_item))["violations"] if v["rule_id"] == "UX-009"]
    assert len(msgs) == 2
    _confirm_project(work_item)
    assert validate_design(str(work_item))["valid"]


def test_ux010_hash_and_approval(design, work_item):
    _approve(design, work_item)
    res = validate_design(str(work_item))
    assert any("no content hash" in v["message"] for v in res["violations"])

    stored = write_content_hash(str(work_item))
    assert f"> **Content hash**: {stored}" in (design / "uiux.md").read_text(encoding="utf-8")
    assert validate_design(str(work_item))["valid"]

    _set(design, "Lưu</a>", "Lưu lại</a>", "screens/S02-qty.html")
    res = validate_design(str(work_item))
    assert any(v["rule_id"] == "UX-010" and "changed after approval" in v["message"] for v in res["violations"])


def test_ux010_hash_ignores_approval_metadata_and_generated_flows(design, work_item):
    before = content_hash(design)
    _approve(design, work_item)
    (design / "data/flows.js").write_text("changed", encoding="utf-8")
    assert content_hash(design) == before
    _set(design, "> **Revision**: r1", "> **Revision**: r2")
    assert content_hash(design) != before


def test_ux010_rejects_self_approval(design, work_item):
    _approve(design, work_item)
    write_content_hash(str(work_item))
    _set(design, "> **Status**: APPROVED", "> **Status**: APPROVED_BY_DESIGNER")
    res = validate_design(str(work_item))
    assert any(v["rule_id"] == "UX-010" and "APPROVED_BY_DESIGNER" in v["message"] for v in res["violations"])
    assert not res["valid"]


def test_cli_exit_codes_and_write_hash(design, work_item, capsys):
    ns = argparse.Namespace(ux_command="validate", work_item=str(work_item), write_hash=False, json=False)
    assert cmd_ux(ns) == 0
    assert "PASSED" in capsys.readouterr().out
    ns.write_hash = True
    assert cmd_ux(ns) == 0
    capsys.readouterr()
    assert "sha256:" in (design / "uiux.md").read_text(encoding="utf-8")
    _set(design, "| W-01 | Kiểm đếm | G-01 |", "| W-01 | Kiểm đếm | G-09 |")
    ns.write_hash, ns.json = False, True
    assert cmd_ux(ns) == 1
    assert json.loads(capsys.readouterr().out)["gate_status"] == "FAILED"


@pytest.mark.anyio
async def test_mcp_tool_validate_ux_design(design, work_item):
    res = await app.call_tool("validate_ux_design", {"work_item_path": str(work_item)})
    assert res.is_error is False
    data = json.loads(res.content[0].text)
    assert data["gate_status"] == "PASSED" and data["document_type"] == "UIUX"
