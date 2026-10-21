"""Walkthrough (`## 8. Walkthrough` in uiux.md): sync -> flows.js, UX-011, kit.js player, `ux record`."""

import argparse
import json
import sys
from pathlib import Path

import pytest

from coder_nexus.ux.commands import cmd_ux
from coder_nexus.ux.record import record
from coder_nexus.ux.scaffold import TEMPLATES, ScaffoldError, sync, walkthrough_rows
from coder_nexus.ux.validate import validate_design

from .test_ux_validate import _confirm_project, _rules, _set, design, work_item  # noqa: F401 (fixtures)

ASSETS = Path(__file__).resolve().parents[1] / "src/coder_nexus/ux/assets"

WALKTHROUGH = """
## 8. Walkthrough

| Workflow | # | Screen | State | Action | Target | Value | Wait (ms) | Caption |
|---|---|---|---|---|---|---|---|---|
| W-01 | 1 | S01 | default | show | | | 600 | Thủ kho mở danh sách |
| W-01 | 1 | | | tap | item-row | | | Chọn hàng → mở màn nhập số lượng |
| W-01 | 2 | S02 | default | show | | | | |
| W-01 | 2 | | error | type | qty-field | 3 | 900 | Nhập số lượng → app kiểm tra (AC-02) |
| W-01 | 2 | | | timer | qty-field | 15s | 3000 | Tự xóa lỗi sau 15 giây |
"""


def _add_targets(design: Path) -> None:
    _set(design, '<a class="app-list-item" href="S02-qty.html" data-next>',
         '<a class="app-list-item" href="S02-qty.html" data-next data-ux-target="item-row">', "screens/S01-items.html")
    _set(design, '<input data-mock="items[0].qty">', '<input data-mock="items[0].qty" data-ux-target="qty-field">',
         "screens/S02-qty.html")
    _set(design, '<div class="app-banner error">Số lượng phải lớn hơn 0</div>',
         '<div class="app-banner error">Số lượng phải lớn hơn 0</div><input data-ux-target="qty-field">', "screens/S02-qty.html")


@pytest.fixture
def scripted(design, work_item):
    _add_targets(design)
    path = design / "uiux.md"
    path.write_text(path.read_text(encoding="utf-8") + WALKTHROUGH, encoding="utf-8")
    sync(str(work_item))
    return design


def _flows(design: Path) -> dict:
    text = (design / "data/flows.js").read_text(encoding="utf-8")
    return json.loads(text[text.index("=") + 1:].rstrip().rstrip(";"))


def _uxw(res: dict, severity: str = "ERROR") -> list[str]:
    return [v["message"] for v in res["violations"] if v["rule_id"] == "UX-011" and v["severity"] == severity]


def test_template_has_optional_walkthrough_section():
    text = (TEMPLATES / "uiux.md").read_text(encoding="utf-8")
    assert "## 8. Walkthrough" in text
    assert "| Workflow | # | Screen | State | Action | Target | Value | Wait (ms) | Caption |" in text


def test_sync_parses_walkthrough_into_flows(scripted, work_item):
    res = sync(str(work_item))
    assert res["walkthroughs"] == 1 and res["warnings"] == []
    flow = _flows(scripted)["flows"][0]
    assert [st["n"] for st in flow["steps"]] == ["1", "2"]
    wt = flow["walkthrough"]
    assert [r["action"] for r in wt] == ["show", "tap", "show", "type", "timer"]
    assert wt[1] == {"step": "1", "screen": "S01", "state": "", "action": "tap", "target": "item-row", "value": "",
                     "wait": None, "caption": "Chọn hàng → mở màn nhập số lượng"}, "empty Screen continues the previous screen"
    assert wt[3]["screen"] == "S02" and wt[3]["wait"] == 900 and wt[4]["value"] == "15s"


def test_sync_warns_about_rows_of_unknown_workflows(scripted, work_item):
    _set(scripted, "| W-01 | 2 | | | timer |", "| W-09 | 2 | | | timer |")
    warnings = sync(str(work_item))["warnings"]
    assert any("cites W-09" in w for w in warnings)
    assert len(_flows(scripted)["flows"][0]["walkthrough"]) == 4


def test_walkthrough_rows_without_section_is_empty():
    assert walkthrough_rows("# UI/UX\n\n## 7. Approval\n") == []


def test_consistent_walkthrough_passes(scripted, work_item):
    res = validate_design(str(work_item))
    assert "UX-011" in res["checked_rules"]
    assert [v for v in res["violations"] if v["rule_id"] == "UX-011"] == []


@pytest.mark.parametrize("old,new,expected", [
    ("| W-01 | 1 | S01 | default | show |", "| W-07 | 1 | S01 | default | show |", "W-07 is not in '## 4. Workflows'"),
    ("| W-01 | 2 | S02 | default | show |", "| W-01 | 2 | S09 | default | show |", "screen S09 is not in '## 5. Screens'"),
    ("| W-01 | 1 | S01 | default | show |", "| W-01 | 1 | S01 | busy | show |", 'S01 has no data-state="busy"'),
    ("| tap | item-row |", "| tap | row-item |", 'S01 has no data-ux-target="row-item"'),
    ("| W-01 | 2 | S02 | default | show |", "| W-01 | 3 | S02 | default | show |", "step '3' is not a step of W-01"),
    ("| W-01 | 2 | S02 | default | show |", "| W-01 | 1 | S02 | default | show |", "step 1 of W-01 is S01, not S02"),
    ("| tap | item-row |", "| swipe | item-row |", "unknown action 'swipe'"),
    ("| timer | qty-field | 15s |", "| timer | qty-field | soon |", "timer Value 'soon' is not a duration"),
    ("| type | qty-field | 3 |", "| type | | 3 |", "'type' needs a Target"),
])
def test_ux011_catches_unknown_references(scripted, work_item, old, new, expected):
    _set(scripted, old, new)
    errors = _uxw(validate_design(str(work_item)))
    assert any(expected in e for e in errors), errors


def test_ux011_target_must_be_drawn_in_the_active_state(scripted, work_item):
    # item-row is drawn only in S01's default state; a row's State applies after its action.
    _set(scripted, "| W-01 | 1 | | | tap | item-row |", "| W-01 | 1 | | error | show | | | | |\n| W-01 | 1 | | | tap | item-row |")
    errors = _uxw(validate_design(str(work_item)))
    assert any("not drawn in state 'error' of S01" in e for e in errors), errors


def test_ux011_warnings_for_selectors_and_values_not_in_mock(scripted, work_item):
    _set(scripted, "| tap | item-row |", "| tap | .app-list-item |")
    _set(scripted, "| type | qty-field | 3 |", "| type | qty-field | 42 |")
    res = validate_design(str(work_item))
    warnings = _uxw(res, "WARNING")
    assert any("CSS selector" in w for w in warnings)
    assert any("value '42' is not in data/mock-data.js" in w for w in warnings)
    _set(scripted, "| type | qty-field | 42 |", "| type | qty-field | @items[0].qty |")
    assert not any("mock-data" in w for w in _uxw(validate_design(str(work_item)), "WARNING"))
    _set(scripted, "| type | qty-field | @items[0].qty |", "| type | qty-field | @items[5].qty |")
    assert any("'@items[5].qty' is not in data/mock-data.js" in w for w in _uxw(validate_design(str(work_item)), "WARNING"))


def test_ux011_timer_note_without_walkthrough_warns_in_review(design, work_item):
    _set(design, "Danh sách chỉ hiện hàng chưa có PO.", "Danh sách tự động làm mới sau 15 giây.", "screens/S01-items.html")
    assert not _uxw(validate_design(str(work_item)), "WARNING"), "DRAFT does not ask for a walkthrough yet"
    _confirm_project(work_item)
    _set(design, "> **Status**: DRAFT", "> **Status**: IN_REVIEW")
    warnings = _uxw(validate_design(str(work_item)), "WARNING")
    assert any("W-01 has time-based or automatic behavior (S01 notes) but no walkthrough" in w for w in warnings), warnings


def test_kit_js_exposes_player_entry_points():
    js = (ASSETS / "kit.js").read_text(encoding="utf-8")
    for needle in ("UX.play = function", "UX.pause = function", "UX.stepOnce = function", "UX.setSpeed = function",
                   "UX.stop = function", '"ux:tap"', '"ux:type"', '"ux:highlight"', '"ux:done"', "data-ux-target",
                   "Mô phỏng — MOCK", 'params.get("play")', "data-ux-play", "ux-countdown", "ux-caption"):
        assert needle in js, needle
    assert "SPEEDS = [1, 1.5, 2]" in js
    css = (ASSETS / "base.css").read_text(encoding="utf-8")
    for cls in (".ux-play", ".ux-mocklabel", ".ux-countdown", ".ux-caption", ".ux-cursor", ".ux-ripple", ".ux-scan", ".ux-rec"):
        assert cls in css, cls


def test_record_fails_cleanly_without_playwright(scripted, work_item, monkeypatch, capsys):
    monkeypatch.setitem(sys.modules, "playwright", None)
    monkeypatch.setitem(sys.modules, "playwright.sync_api", None)
    with pytest.raises(ScaffoldError, match="Playwright is not installed"):
        record(str(work_item), "W-01")
    args = argparse.Namespace(ux_command="record", work_item=str(work_item), workflow="W-01", viewport=None)
    assert cmd_ux(args) == 1
    out = capsys.readouterr().out
    assert "Playwright is not installed" in out and "not a Coder Nexus dependency" in out
    assert not list((scripted / "shots").glob("*.webm"))


def test_record_needs_a_walkthrough(design, work_item):
    with pytest.raises(ScaffoldError, match="No walkthrough"):
        record(str(work_item))
