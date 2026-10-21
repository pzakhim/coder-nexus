"""Create and keep a work item's `design-uiux/` folder consistent.

`uiux.md` is the source of truth. `ux sync` turns its Workflows / Screens / Walkthrough tables into
`data/flows.js`, which `index.html` reads (file:// pages cannot fetch JSON).
"""

import json
import os
import re
from datetime import date
from pathlib import Path
from typing import Optional

from .kitgen import extract

TEMPLATES = Path(__file__).parent / "templates"
STATE_BLOCKS = {
    "default": '''  <section class="app-content" data-state="default">
    <div class="note">TODO: draw the default content with kit classes.</div>
  </section>''',
    "loading": '''  <section class="app-content" data-state="loading">
    <div class="app-shimmer" style="height:64px"></div>
    <div class="app-shimmer" style="height:44px"></div>
    <div class="app-shimmer" style="height:160px"></div>
  </section>''',
    "empty": '''  <section class="app-content" data-state="empty">
    <div class="app-nodata"><div class="icon">🗂</div><div class="title">TODO: empty title</div><div>TODO: empty message</div></div>
  </section>''',
    "error": '''  <section class="app-content" data-state="error">
    <div class="app-banner error">⛔ TODO: error message</div>
    <a class="app-button block outline">TODO: retry / fix action</a>
  </section>''',
}
GENERIC_STATE = '''  <section class="app-content" data-state="{state}">
    <div class="note">TODO: draw the "{state}" state.</div>
  </section>'''

WALKTHROUGH_ACTIONS = ("show", "tap", "type", "scan", "wait", "timer", "caption")
WALKTHROUGH_SECTION = 8

WORK_ITEM_RE = re.compile(r"\.superpowers/work-items/([^/]+)/(v\d+)/?$")


class ScaffoldError(ValueError):
    pass


# ---------------------------------------------------------------- paths

def resolve_work_item(path: str) -> tuple[Path, Path, str, str]:
    """-> (vN dir, .superpowers dir, slug, version). Accepts the vN folder or its design-uiux folder."""
    p = Path(path).resolve()
    if p.name == "design-uiux":
        p = p.parent
    m = WORK_ITEM_RE.search(p.as_posix())
    if not m:
        raise ScaffoldError(f"Not a work-item version folder: {path} (expected …/.superpowers/work-items/<slug>/vN)")
    superpowers = p.parents[2]
    return p, superpowers, m.group(1), m.group(2)


def _rel(target: Path, from_dir: Path) -> str:
    return os.path.relpath(target, from_dir).replace(os.sep, "/")


def _render(name: str, **values: str) -> str:
    text = (TEMPLATES / name).read_text(encoding="utf-8")
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", val)
    return text


def _ensure_kit(superpowers: Path) -> Path:
    kit = superpowers / "ux" / "kit"
    if not (kit / "kit.css").is_file():
        extract(superpowers.parent)
    return kit


def _write_new(path: Path, text: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


# ---------------------------------------------------------------- uiux.md tables

def _section(text: str, number: int) -> tuple[int, int]:
    m = re.search(rf"^##\s+{number}\.[^\n]*\n", text, re.MULTILINE)
    if not m:
        raise ScaffoldError(f"uiux.md has no '## {number}.' section")
    nxt = re.search(r"^##\s+", text[m.end():], re.MULTILINE)
    return m.end(), m.end() + (nxt.start() if nxt else len(text) - m.end())


def _rows(text: str, number: int, id_pattern: str) -> list[list[str]]:
    start, end = _section(text, number)
    rows = []
    for line in text[start:end].splitlines():
        if re.match(rf"^\|\s*`?{id_pattern}`?\s*\|", line.strip()):
            rows.append([c.strip().strip("`") for c in line.strip().strip("|").split("|")])
    return rows


def _append_row(text: str, number: int, row: list[str]) -> str:
    start, end = _section(text, number)
    body = text[start:end]
    lines = body.rstrip("\n").split("\n")
    last_table = max(i for i, l in enumerate(lines) if l.strip().startswith("|"))
    lines.insert(last_table + 1, "| " + " | ".join(row) + " |")
    return text[:start] + "\n".join(lines) + "\n\n" + text[end:].lstrip("\n")


def walkthrough_rows(text: str) -> list[dict]:
    """Rows of the optional `## 8. Walkthrough` table, in order, with their uiux.md line numbers.

    Columns: Workflow | # | Screen | State | Action | Target | Value | Wait (ms) | Caption.
    An empty Screen continues on the previous row's screen of the same workflow.
    """
    m = re.search(rf"^##\s+{WALKTHROUGH_SECTION}\.[^\n]*\n", text, re.MULTILINE)
    if not m:
        return []
    nxt = re.search(r"^##\s+", text[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    first_line = text[:m.end()].count("\n") + 1
    rows, last_screen = [], {}
    for offset, line in enumerate(text[m.end():end].splitlines()):
        if not re.match(r"^\|\s*`?W-\d+`?\s*\|", line.strip()):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        cells += [""] * (9 - len(cells))
        wid, step, screen, state, action, target, value, wait, caption = cells[:9]
        wid = wid.upper()
        screen = screen.upper() or last_screen.get(wid, "")
        last_screen[wid] = screen
        wait_ms = int(wait) if re.fullmatch(r"\d+", wait) else None
        rows.append({"workflow": wid, "step": step, "screen": screen, "state": state, "action": action.lower(),
                     "target": target, "value": value, "wait": wait_ms, "wait_raw": wait, "caption": caption,
                     "line": first_line + offset})
    return rows


STEP_RE = re.compile(r"^(?P<left>.*?)(?:→|->)\s*(?P<screen>S\d{2,})(?::(?P<state>[\w-]+))?\s*$")
STEP_N_RE = re.compile(r"^(?P<n>\d+(?:\.\d+)*[a-z]?)\.?(?:\s+(?P<label>.*))?$")


def parse_steps(cell: str) -> list[dict]:
    """Steps column of `## 4. Workflows` -> [{n, screen, title, state}].

    Accepts `1→S01, 2→S02` (old), `1 Chọn NG→S01`, `1. Chọn NG → S01`, `2 Quét LPN→S01:scan` (state) and bare `S01, S02`.
    `title` is the step label ("" when none); `state` is the screen state the step opens ("" = default).
    """
    steps: list[dict] = []
    for part in (p.strip() for p in cell.split(",") if p.strip()):
        m = STEP_RE.match(part)
        if not m:
            steps += [{"n": "", "screen": sid, "title": "", "state": ""} for sid in re.findall(r"\bS\d{2,}\b", part)]
            continue
        left = m.group("left").strip()
        nm = STEP_N_RE.match(left)
        n, label = (nm.group("n"), (nm.group("label") or "").strip()) if nm else ("", left)
        steps.append({"n": n, "screen": m.group("screen"), "title": label, "state": m.group("state") or ""})
    numbered = all(st["n"] for st in steps)
    for i, st in enumerate(steps):
        if not numbered:
            st["n"] = str(i + 1)
    return steps


def _field(text: str, name: str) -> str:
    m = re.search(rf"^>\s*\*\*{re.escape(name)}\*\*:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _lang(superpowers: Path) -> str:
    return "vi"


# ---------------------------------------------------------------- commands

def new_design(work_item: str, title: str, lang: Optional[str] = None) -> dict:
    vdir, superpowers, slug, version = resolve_work_item(work_item)
    kit = _ensure_kit(superpowers)
    d = vdir / "design-uiux"
    lang = lang or _lang(superpowers)
    created = []
    values = dict(title=title, slug=slug, version=version, date=date.today().isoformat(), lang=lang)
    for name, target in (("uiux.md", d / "uiux.md"), ("CHANGELOG.md", d / "CHANGELOG.md"), ("mock-data.js", d / "data" / "mock-data.js")):
        if _write_new(target, _render(name, **values)):
            created.append(target)
    # The viewer shell is generated: always (re)write it so a hand-edited index.html is restored.
    if shell_drift(d):
        (d / "index.html").parent.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(_render("index.html", kit=_rel(kit, d), **values), encoding="utf-8")
        created.append(d / "index.html")
    for sub in ("screens", "components", "assets"):
        (d / sub).mkdir(parents=True, exist_ok=True)
    _write_new(d / "shots" / ".gitignore", "# generated screenshots — not committed\n*\n")
    catalog = superpowers / "ux" / "screen-catalog.md"
    if _write_new(catalog, _render("screen-catalog.md", project=superpowers.parent.name)):
        created.append(catalog)
    sync(work_item)
    return {"design_dir": str(d), "created": [str(p) for p in created]}


def add_screen(work_item: str, screen_id: str, slug: str, title: str, steps: str = "", kind: str = "NEW",
               catalog: str = "", states: str = "default,loading,empty,error", lang: Optional[str] = None) -> dict:
    vdir, superpowers, _, _ = resolve_work_item(work_item)
    d = vdir / "design-uiux"
    if not (d / "uiux.md").is_file():
        raise ScaffoldError("Run `coder-nexus ux new` first.")
    if not re.fullmatch(r"S\d{2,}", screen_id):
        raise ScaffoldError("Screen id must look like S01.")
    kind = kind.upper()
    if kind not in {"NEW", "CHANGED", "EXISTING"}:
        raise ScaffoldError("Kind must be NEW, CHANGED or EXISTING.")
    kit = _ensure_kit(superpowers)
    state_list = [s.strip() for s in states.split(",") if s.strip()] or ["default"]
    blocks = "\n\n".join(STATE_BLOCKS.get(s, GENERIC_STATE.format(state=s)) for s in state_list)
    rel_file = f"screens/{screen_id}-{slug}.html"
    target = d / rel_file
    html = _render("screen.html", id=screen_id, title=title, steps=steps, catalog=catalog or "TODO",
                   kit=_rel(kit, target.parent), states=blocks, lang=lang or _lang(superpowers))
    created = _write_new(target, html)
    text = (d / "uiux.md").read_text(encoding="utf-8")
    if not any(r[0] == screen_id for r in _rows(text, 5, r"S\d+")):
        text = _append_row(text, 5, [screen_id, title, rel_file, catalog or "TODO", kind, steps or "TODO", ", ".join(state_list), "", ""])
        (d / "uiux.md").write_text(text, encoding="utf-8")
    sync(work_item)
    return {"file": str(target), "created": created}


def add_component(work_item: str, comp_id: str, slug: str, title: str, used_in: str = "", lang: Optional[str] = None) -> dict:
    vdir, superpowers, _, _ = resolve_work_item(work_item)
    d = vdir / "design-uiux"
    if not (d / "uiux.md").is_file():
        raise ScaffoldError("Run `coder-nexus ux new` first.")
    if not re.fullmatch(r"C\d{2,}", comp_id):
        raise ScaffoldError("Component id must look like C01.")
    kit = _ensure_kit(superpowers)
    rel_file = f"components/{comp_id}-{slug}.html"
    target = d / rel_file
    created = _write_new(target, _render("component.html", id=comp_id, title=title, used_in=used_in,
                                         kit=_rel(kit, target.parent), lang=lang or _lang(superpowers)))
    text = (d / "uiux.md").read_text(encoding="utf-8")
    if not any(r[0] == comp_id for r in _rows(text, 6, r"C\d+")):
        text = _append_row(text, 6, [comp_id, title, rel_file, used_in, "TODO"])
        (d / "uiux.md").write_text(text, encoding="utf-8")
    return {"file": str(target), "created": created}


def shell_drift(d: Path) -> bool:
    """True when design-uiux/index.html is not the rendered template (title, lang and kit path may differ)."""
    path = d / "index.html"
    if not path.is_file():
        return True
    pattern = re.escape((TEMPLATES / "index.html").read_text(encoding="utf-8").replace("\r\n", "\n").rstrip())
    pattern = re.sub(r"\\\{\\\{\w+\\\}\\\}", lambda _: "[^\n]*?", pattern)
    return re.fullmatch(pattern, path.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip()) is None


def flows_data(d: Path) -> tuple[dict, list[str]]:
    """Read-only: uiux.md of a design-uiux folder -> (flows.js data, consistency warnings)."""
    text = (d / "uiux.md").read_text(encoding="utf-8")
    title_m = re.search(r"^#\s+UI/UX:\s*(.+?)\s*(?:—\s*v\d+)?\s*$", text, re.MULTILINE)
    screens = [
        {"id": r[0], "title": r[1], "file": r[2], "catalog": r[3] if len(r) > 3 else "", "kind": (r[4] if len(r) > 4 else "").upper()}
        for r in _rows(text, 5, r"S\d+")
    ]
    flows = []
    walk = walkthrough_rows(text)
    titles = {s["id"]: s["title"] for s in screens}
    for r in _rows(text, 4, r"W-\d+"):
        steps = parse_steps(r[3] if len(r) > 3 else "")
        for st in steps:
            st["title"] = st["title"] or titles.get(st["screen"], "")
        flow = {"id": r[0], "title": r[1], "goals": r[2] if len(r) > 2 else "", "steps": steps}
        rows = [{k: w[k] for k in ("step", "screen", "state", "action", "target", "value", "wait", "caption")}
                for w in walk if w["workflow"] == r[0].upper()]
        if rows:
            flow["walkthrough"] = rows
        flows.append(flow)
    data = {
        "title": title_m.group(1) if title_m else d.parent.parent.name,
        "revision": _field(text, "Revision"),
        "approval": _field(text, "Status"),
        "flows": flows,
        "screens": screens,
    }
    ids = {s["id"] for s in screens}
    used = {st["screen"] for f in flows for st in f["steps"]}
    warnings = [f"{f['id']} step {st['screen']} has no row in ## 5. Screens" for f in flows for st in f["steps"] if st["screen"] not in ids]
    warnings += [f"{s['id']} is not in any workflow" for s in screens if s["id"] not in used]
    warnings += [f"{s['id']} file missing: {s['file']}" for s in screens if not (d / s["file"]).is_file()]
    return data, warnings


def render_flows(data: dict) -> str:
    return ("/* Generated by `coder-nexus ux sync` from uiux.md. Do not edit. */\n"
            f"window.UX_FLOWS = {json.dumps(data, ensure_ascii=False, indent=2)};\n")


def sync(work_item: str) -> dict:
    """uiux.md -> data/flows.js. Returns warnings about obvious inconsistencies."""
    vdir, _, _, _ = resolve_work_item(work_item)
    d = vdir / "design-uiux"
    data, warnings = flows_data(d)
    known = {f["id"].upper() for f in data["flows"]}
    text = (d / "uiux.md").read_text(encoding="utf-8")
    warnings = warnings + [f"Walkthrough row (uiux.md:{w['line']}) cites {w['workflow']}, which is not in ## 4. Workflows"
                           for w in walkthrough_rows(text) if w["workflow"] not in known]
    (d / "data").mkdir(parents=True, exist_ok=True)
    (d / "data" / "flows.js").write_text(render_flows(data), encoding="utf-8")
    return {"flows": len(data["flows"]), "screens": len(data["screens"]), "warnings": warnings, "file": str(d / "data" / "flows.js"),
            "walkthroughs": sum(1 for f in data["flows"] if f.get("walkthrough"))}
