"""Viewer improvements: orientation per platform, labelled steps with states, scenario sidebar, fixed generated shell."""

import argparse
import json
from pathlib import Path

import pytest

from coder_nexus.ux.commands import cmd_ux
from coder_nexus.ux.kitgen import load_viewports, oriented_size, save_viewports
from coder_nexus.ux.record import record_jobs
from coder_nexus.ux.scaffold import ScaffoldError, new_design, parse_steps, shell_drift, sync
from coder_nexus.ux.validate import validate_design

from .test_ux_validate import _confirm_project, _rules, _set, design, work_item  # noqa: F401 (fixtures)

ASSETS = Path(__file__).resolve().parents[1] / "src/coder_nexus/ux/assets"


def _vp_args(project: Path, **kw) -> argparse.Namespace:
    base = dict(ux_command="viewports", project=str(project), platforms=None, mobile=None, tablet=None, web=None,
                orientations=None, tablet_orientation=None, decision=None, json=False)
    base.update(kw)
    return argparse.Namespace(**base)


def _flows(design: Path) -> dict:
    text = (design / "data/flows.js").read_text(encoding="utf-8")
    return json.loads(text[text.index("=") + 1:].rstrip().rstrip(";"))


# ---------------------------------------------------------------- 1. orientation per platform

def test_schema1_viewports_migrate_to_orientations(tmp_path):
    path = tmp_path / ".superpowers/ux/viewports.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"schema": 1, "confirmed": True, "decision": "D-01", "platforms": {
        "mobile": {"width": 390, "height": 844, "orientation": "portrait"},
        "tablet": {"width": 1180, "height": 820, "orientation": "landscape"},
        "web": {"width": 1440, "height": 900, "orientation": "landscape"}}}), encoding="utf-8")
    data = load_viewports(tmp_path)
    assert data["platforms"] == {
        "mobile": {"width": 390, "height": 844, "orientations": ["portrait"]},
        "tablet": {"width": 820, "height": 1180, "orientations": ["landscape"]},
        "web": {"width": 1440, "height": 900, "orientations": ["landscape"]},
    }
    assert data["confirmed"] is True and data["orientations_confirmed"] is False, "schema 1 never asked for orientations"
    assert oriented_size(data["platforms"]["tablet"], "landscape") == (1180, 820)
    assert oriented_size(data["platforms"]["tablet"], "portrait") == (820, 1180)
    assert oriented_size(data["platforms"]["web"], "landscape") == (1440, 900)


def test_cli_orientations_per_platform(tmp_path, capsys):
    assert cmd_ux(_vp_args(tmp_path, platforms="mobile,tablet,web", tablet="800x1280",
                           orientations="mobile=portrait,tablet=portrait+landscape,web=landscape", decision="D-07")) == 0
    out = capsys.readouterr().out
    assert "tablet  portrait 800×1280 · landscape 1280×800" in out and "confirmed (D-07)" in out
    data = load_viewports(tmp_path)
    assert data["platforms"]["tablet"] == {"width": 800, "height": 1280, "orientations": ["portrait", "landscape"]}
    assert data["orientations_confirmed"] is True and data["schema"] == 2
    js = (tmp_path / ".superpowers/ux/kit/viewports.js").read_text(encoding="utf-8")
    assert '"orientations": ["portrait", "landscape"]' in js
    # a later size change keeps the confirmed orientations
    assert cmd_ux(_vp_args(tmp_path, mobile="412x915")) == 0
    data = load_viewports(tmp_path)
    assert data["orientations_confirmed"] is True and data["decision"] == "D-07"
    assert data["platforms"]["mobile"] == {"width": 412, "height": 915, "orientations": ["portrait"]}


def test_cli_orientations_rejects_bad_values(tmp_path, capsys):
    assert cmd_ux(_vp_args(tmp_path, orientations="tablet=sideways")) == 1
    assert cmd_ux(_vp_args(tmp_path, platforms="mobile", orientations="tablet=landscape")) == 1
    assert "not kept" in capsys.readouterr().out
    assert not (tmp_path / ".superpowers/ux/viewports.json").exists()


def test_cli_unconfirmed_orientations_are_flagged(tmp_path, capsys):
    save_viewports(tmp_path, {"mobile": {"width": 390, "height": 844}}, "D-01", orientations_confirmed=False)
    assert cmd_ux(_vp_args(tmp_path)) == 0
    out = capsys.readouterr().out
    assert "Orientations not confirmed" in out and "--orientations" in out


def test_record_jobs_follow_orientations():
    platforms = {"mobile": {"width": 390, "height": 844, "orientations": ["portrait"]},
                 "tablet": {"width": 820, "height": 1180, "orientations": ["landscape", "portrait"]}}
    jobs = record_jobs(platforms)
    assert [(j["platform"], j["orientation"], j["width"], j["height"]) for j in jobs] == [
        ("mobile", "portrait", 390, 844), ("tablet", "landscape", 1180, 820), ("tablet", "portrait", 820, 1180)]
    assert jobs[1]["query"] == "platform=tablet&orientation=landscape&speed=1&chrome=off"
    only = record_jobs(platforms, "tablet", "landscape")
    assert len(only) == 1 and only[0]["width"] == 1180
    with pytest.raises(ScaffoldError, match="allows landscape"):
        record_jobs(platforms, "mobile", "landscape")
    with pytest.raises(ScaffoldError, match="not in"):
        record_jobs(platforms, "web")


def test_cli_record_passes_orientation(monkeypatch, tmp_path):
    seen = {}

    def fake(work_item, workflow=None, viewport=None, orientation=None):
        seen.update(workflow=workflow, viewport=viewport, orientation=orientation)
        return {"videos": []}
    monkeypatch.setattr("coder_nexus.ux.record.record", fake)
    args = argparse.Namespace(ux_command="record", work_item=str(tmp_path), workflow="W-01", viewport="tablet", orientation="landscape")
    assert cmd_ux(args) == 0
    assert seen == {"workflow": "W-01", "viewport": "tablet", "orientation": "landscape"}


def test_ux009_needs_confirmed_orientations_before_review(design, work_item):
    _confirm_project(work_item)
    _set(design, "> **Status**: DRAFT", "> **Status**: IN_REVIEW")
    assert "UX-009" not in _rules(validate_design(str(work_item)))
    project = work_item.parents[3]
    save_viewports(project, {"mobile": {"width": 390, "height": 844}}, "D-01", orientations_confirmed=False)
    res = validate_design(str(work_item))
    assert any(v["rule_id"] == "UX-009" and "orientations" in v["message"] for v in res["violations"])


def test_kit_js_viewer_has_rotate_url_and_collapsible_sidebar():
    js = (ASSETS / "kit.js").read_text(encoding="utf-8")
    for needle in ("UX.setOrientation", "⟲", 'q.set("orientation"', "history.replaceState", "orientations(cur.platform).length > 1",
                   "length > 6", "ux-filter", "class=\"wt\"", "Trạng thái", "expanded[fi]", "f.steps[si].state", 'class="sid"'):
        assert needle in js, needle
    css = (ASSETS / "base.css").read_text(encoding="utf-8")
    assert ".ux-filter" in css and ".ux-step .sid" in css


# ---------------------------------------------------------------- 2. step labels and states

@pytest.mark.parametrize("cell, expected", [
    ("1→S01, 2→S02", [("1", "S01", "", ""), ("2", "S02", "", "")]),
    ("1 Chọn NG→S01, 2 Quét LPN→S01", [("1", "S01", "Chọn NG", ""), ("2", "S01", "Quét LPN", "")]),
    ("1. Chọn NG → S01, 2. Quét LPN -> S01:scan", [("1", "S01", "Chọn NG", ""), ("2", "S01", "Quét LPN", "scan")]),
    ("2a→S03:error", [("2a", "S03", "", "error")]),
    ("S01, S02", [("1", "S01", "", ""), ("2", "S02", "", "")]),
])
def test_parse_steps_old_and_new_formats(cell, expected):
    assert [(s["n"], s["screen"], s["title"], s["state"]) for s in parse_steps(cell)] == expected


def test_sync_puts_step_title_and_state(design, work_item):
    _set(design, "| W-01 | Kiểm đếm | G-01 | 1→S01, 2→S02 |", "| W-01 | Kiểm đếm | G-01 | 1 Chọn hàng→S01, 2 Nhập sai→S02:error |")
    sync(str(work_item))
    steps = _flows(design)["flows"][0]["steps"]
    assert steps == [{"n": "1", "screen": "S01", "title": "Chọn hàng", "state": ""},
                     {"n": "2", "screen": "S02", "title": "Nhập sai", "state": "error"}]
    assert validate_design(str(work_item))["valid"]


def test_old_steps_fall_back_to_screen_title(design):
    steps = _flows(design)["flows"][0]["steps"]
    assert [(s["n"], s["title"], s["state"]) for s in steps] == [("1", "Danh sách", ""), ("2", "Nhập số lượng", "")]


def test_ux004_step_state_must_exist_on_the_screen(design, work_item):
    _set(design, "| W-01 | Kiểm đếm | G-01 | 1→S01, 2→S02 |", "| W-01 | Kiểm đếm | G-01 | 1→S01, 2 Hết hàng→S02:empty |")
    sync(str(work_item))
    res = validate_design(str(work_item))
    msgs = [v["message"] for v in res["violations"] if v["rule_id"] == "UX-004" and v["severity"] == "ERROR"]
    assert any("state 'empty'" in m and "S02" in m for m in msgs), msgs


# ---------------------------------------------------------------- 3. scenario workflows

def test_scenario_workflows_share_screens(design, work_item):
    _set(design, "| W-01 | Kiểm đếm | G-01 | 1→S01, 2→S02 |",
         "| W-01 | Kiểm đếm | G-01 | 1 Chọn hàng→S01, 2 Nhập số lượng→S02 |\n"
         "| W-02 | Nhập sai số lượng | G-01 | 1 Chọn hàng→S01, 2 Báo lỗi→S02:error |")
    sync(str(work_item))
    flows = _flows(design)["flows"]
    assert [f["id"] for f in flows] == ["W-01", "W-02"] and flows[1]["steps"][1]["state"] == "error"
    assert "UX-004" not in _rules(validate_design(str(work_item)))


# ---------------------------------------------------------------- 4. fixed generated shell

def test_shell_drift_warns_and_ux_new_restores(design, work_item):
    assert not shell_drift(design)
    assert "UX-012" not in _rules(validate_design(str(work_item)), "WARNING")
    index = design / "index.html"
    index.write_text(index.read_text(encoding="utf-8").replace('<div id="ux"></div>', '<div id="ux"></div><div>custom</div>'),
                     encoding="utf-8")
    res = validate_design(str(work_item))
    hit = [v for v in res["violations"] if v["rule_id"] == "UX-012"]
    assert hit and hit[0]["severity"] == "WARNING" and "coder-nexus ux new" in hit[0]["suggestion"]
    uiux = (design / "uiux.md").read_text(encoding="utf-8")
    res = new_design(str(work_item), "Kiểm đếm")
    assert str(index) in res["created"] and "custom" not in index.read_text(encoding="utf-8")
    assert (design / "uiux.md").read_text(encoding="utf-8") == uiux, "ux new keeps the designer's files"
    assert not shell_drift(design)


def test_shell_drift_ignores_kit_path_title_and_lang(design):
    index = design / "index.html"
    text = index.read_text(encoding="utf-8")
    assert "../../../../ux/kit" in text and "Kiểm đếm" in text and 'lang="vi"' in text
    index.write_text(text.replace("../../../../ux/kit", "../../ux/kit").replace("Kiểm đếm", "Khác").replace('lang="vi"', 'lang="en"'),
                     encoding="utf-8")
    assert not shell_drift(design)
    index.unlink()
    assert shell_drift(design)
