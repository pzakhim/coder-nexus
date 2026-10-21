"""`coder-nexus ux validate` / MCP `validate_ux_design`: read-only checks of a work item's design-uiux/.

Rules UX-001 … UX-011 (see docs/handoff/2026-10-21-huly-goals-uiux.md §4.7). Only `write_content_hash`
writes, and only `uiux.md` (CLI `--write-hash`); the validator itself never writes.
"""

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional

from ..architecture.spec_validator import SpecViolation, goal_rows
from .scaffold import WALKTHROUGH_ACTIONS, ScaffoldError, _field, _rows, flows_data, render_flows, resolve_work_item, walkthrough_rows

STATUSES = {"DRAFT", "IN_REVIEW", "APPROVED"}
REVIEW_STATUSES = {"IN_REVIEW", "APPROVED"}
SELF_APPROVALS = ("APPROVED_BY_DESIGNER", "APPROVED_BY_AGENT")
LIST_STATES = ("loading", "empty", "error")
EMPTY_VALUES = {"", "NONE", "TODO", "N/A", "-"}
HASH_FIELD = "Content hash"
# Approval metadata changes when the user approves; it is not part of the design content.
APPROVAL_FIELDS = ("Status", "Approval reference", HASH_FIELD)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
CHECKED_RULES = [f"UX-{i:03d}" for i in range(1, 12)]
TARGET_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
# A note describing time-based or automatic behavior (auto-save, countdown, auto-reset, "15s").
TIMER_NOTE_RE = re.compile(
    r"\b\d+\s*(?:s|ms|sec|secs|seconds?|giây|phút|min|minutes?)\b|countdown|timeout|time-out|timer|"
    r"auto[- ]?(?:save|reset|submit|close|revert|refresh)|tự động|đếm ngược|hết giờ", re.IGNORECASE)


class _Page(HTMLParser):
    """What the markup contract needs from one screen or component file."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root: dict[str, str] = {}
        self.states: list[str] = []
        self.classes: set[str] = set()
        self.new_components: list[str] = []
        self.mocks: list[str] = []
        self.targets: dict[str, set[str]] = {}  # data-ux-target -> states it is drawn in ("" = outside any state)
        self.styles: list[str] = []
        self.has_table = False
        self.notes: list[str] = []
        self._open: list[str] = []
        self._note_depths: list[int] = []
        self._state_depths: list[tuple[int, str]] = []

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        classes = a.get("class", "").split()
        if not self.root and ("data-screen" in a or "data-component" in a):
            self.root = a
        if "data-state" in a:
            self.states.append(a["data-state"].strip())
        self.classes.update(classes)
        if "new-component" in classes:
            self.new_components.append(a.get("data-name", "").strip())
        if "data-mock" in a:
            self.mocks.append(a["data-mock"].strip())
        state = a["data-state"].strip() if "data-state" in a else (self._state_depths[-1][1] if self._state_depths else "")
        if a.get("data-ux-target"):
            self.targets.setdefault(a["data-ux-target"].strip(), set()).add(state)
        if a.get("style"):
            self.styles.append(a["style"])
        if tag == "table":
            self.has_table = True
        if tag in VOID_TAGS:
            return
        self._open.append(tag)
        if "data-state" in a:
            self._state_depths.append((len(self._open), state))
        if "note" in classes:
            self._note_depths.append(len(self._open))
            self.notes.append("")

    def handle_endtag(self, tag):
        if tag in VOID_TAGS or tag not in self._open:
            return
        while self._open:
            closed = len(self._open)
            if self._note_depths and self._note_depths[-1] == closed:
                self._note_depths.pop()
            if self._state_depths and self._state_depths[-1][0] == closed:
                self._state_depths.pop()
            if self._open.pop() == tag:
                break

    def handle_data(self, data):
        if self._note_depths:
            self.notes[-1] += data


def _parse(path: Path) -> _Page:
    page = _Page()
    page.feed(path.read_text(encoding="utf-8"))
    page.close()
    return page


def _ids(value: str, prefix: str) -> list[str]:
    return [m.upper() for m in re.findall(rf"\b{prefix}-?\d+\b", value, re.IGNORECASE)]


def _split(value: str) -> list[str]:
    return [v for v in re.split(r"[,\s]+", value.strip()) if v]


def _line_of(text: str, pattern: str) -> Optional[int]:
    m = re.search(pattern, text, re.MULTILINE)
    return text[:m.start()].count("\n") + 1 if m else None


def _section_text(text: str, number: int) -> str:
    m = re.search(rf"^##\s+{number}\.[^\n]*\n", text, re.MULTILINE)
    if not m:
        return ""
    nxt = re.search(r"^##\s+", text[m.end():], re.MULTILINE)
    return text[m.end():m.end() + nxt.start()] if nxt else text[m.end():]


def _bullet(text: str, name: str) -> str:
    m = re.search(rf"^\s*-\s*\*\*{re.escape(name)}\*\*:\s*(.*)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------- mock data

def _js_object_to_json(src: str) -> str:
    """Small JSON-ish conversion for a plain object literal: comments, single quotes, bare keys, trailing commas."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"'":
            j, buf = i + 1, []
            while j < n and src[j] != c:
                if src[j] == "\\" and j + 1 < n:
                    buf.append(src[j:j + 2])
                    j += 2
                    continue
                buf.append('\\"' if src[j] == '"' else src[j])
                j += 1
            out.append('"' + "".join(buf).replace("\\'", "'") + '"')
            i = j + 1
        elif src.startswith("//", i):
            i = src.find("\n", i) if src.find("\n", i) >= 0 else n
        elif src.startswith("/*", i):
            i = src.find("*/", i) + 2 if src.find("*/", i) >= 0 else n
        else:
            out.append(c)
            i += 1
    text = "".join(out)
    text = re.sub(r"([{,]\s*)([A-Za-z_$][\w$]*)\s*:", r'\1"\2":', text)
    return re.sub(r",(\s*[}\]])", r"\1", text)


def load_mock(path: Path) -> Optional[Any]:
    """window.MOCK from data/mock-data.js, or None when it is not a plain literal this parser understands."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"window\.MOCK\s*=\s*", text)
    if not m:
        return None
    body = text[m.end():].strip().rstrip(";").strip()
    try:
        return json.loads(_js_object_to_json(body))
    except ValueError:
        return None


def mock_value(data: Any, path: str) -> Any:
    """Same lookup as kit.js `get()`: dotted keys with optional `[index]`. Missing -> None."""
    cur = data
    for part in path.split("."):
        m = re.fullmatch(r"(\w+)\[(\d+)\]", part)
        if m:
            seq = cur.get(m.group(1)) if isinstance(cur, dict) else None
            idx = int(m.group(2))
            cur = seq[idx] if isinstance(seq, list) and idx < len(seq) else None
        else:
            cur = cur.get(part) if isinstance(cur, dict) else None
        if cur is None:
            return None
    return cur


# ---------------------------------------------------------------- content hash

def _hash_text(uiux: str) -> str:
    """uiux.md without approval metadata (status fields and `## 7. Approval`)."""
    lines = [line for line in uiux.splitlines()
             if not re.match(rf"^>\s*\*\*(?:{'|'.join(map(re.escape, APPROVAL_FIELDS))})\*\*:", line)]
    text = "\n".join(lines)
    m = re.search(r"^##\s+7\.[^\n]*$", text, re.MULTILINE)
    if m:
        nxt = re.search(r"^##\s+", text[m.end():], re.MULTILINE)
        text = text[:m.end()] + (text[m.end() + nxt.start():] if nxt else "")
    return text


def content_hash(design_dir: Path) -> str:
    """sha256 over uiux.md (minus approval metadata) + screens/ + components/ + data/ (minus generated flows.js)."""
    files = [design_dir / "uiux.md"]
    for sub in ("screens", "components", "data"):
        if (design_dir / sub).is_dir():
            files += [p for p in (design_dir / sub).rglob("*") if p.is_file()]
    h = hashlib.sha256()
    for path in sorted(set(files), key=lambda p: p.relative_to(design_dir).as_posix()):
        rel = path.relative_to(design_dir).as_posix()
        if rel == "data/flows.js" or path.name.startswith("."):
            continue
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
            if rel == "uiux.md":
                text = _hash_text(text)
            raw = text.encode("utf-8")
        except UnicodeDecodeError:
            pass
        h.update(rel.encode("utf-8") + b"\0" + raw + b"\0")
    return "sha256:" + h.hexdigest()


def write_content_hash(work_item: str) -> str:
    """Store the current content hash in uiux.md (`> **Content hash**:`). The only write in this module."""
    vdir, _, _, _ = resolve_work_item(work_item)
    d = vdir / "design-uiux"
    path = d / "uiux.md"
    if not path.is_file():
        raise ScaffoldError(f"No design-uiux/uiux.md in {vdir}")
    value = content_hash(d)
    text = path.read_text(encoding="utf-8")
    line = f"> **{HASH_FIELD}**: {value}"
    pattern = rf"^>\s*\*\*{re.escape(HASH_FIELD)}\*\*:.*$"
    if re.search(pattern, text, re.MULTILINE):
        text = re.sub(pattern, line, text, count=1, flags=re.MULTILINE)
    else:
        anchor = re.search(r"^>\s*\*\*(?:Approval reference|Status)\*\*:.*$", text, re.MULTILINE)
        if not anchor:
            raise ScaffoldError("uiux.md has no '> **Status**:' field to place the content hash after")
        text = text[:anchor.end()] + "\n" + line + text[anchor.end():]
    path.write_text(text, encoding="utf-8")
    return value


# ---------------------------------------------------------------- validator

def validate_design(work_item: str) -> dict[str, Any]:
    """Validate `<work item vN>/design-uiux/`. Read-only."""
    try:
        vdir, superpowers, slug, version = resolve_work_item(work_item)
    except ScaffoldError as exc:
        return _error(str(exc))
    d = vdir / "design-uiux"
    if not (d / "uiux.md").is_file():
        return _error(f"No design-uiux/uiux.md in {vdir}. Run `coder-nexus ux new` first.")

    violations: list[SpecViolation] = []

    def add(rule: str, message: str, suggestion: str, severity: str = "ERROR", line: Optional[int] = None) -> None:
        violations.append(SpecViolation(rule, severity, line, message, suggestion))

    text = (d / "uiux.md").read_text(encoding="utf-8")
    status = _field(text, "Status").upper()

    # UX-001 header fields and sections
    expected = {"Document type": "UIUX", "Work Item": slug, "Version": version}
    for name, value in expected.items():
        got = _field(text, name)
        if got != value:
            add("UX-001", f"uiux.md field '{name}' is '{got or 'missing'}', expected '{value}'.",
                f"Set '> **{name}**: {value}'.", line=_line_of(text, rf"^>\s*\*\*{re.escape(name)}\*\*"))
    revision = _field(text, "Revision")
    if not re.fullmatch(r"r\d+", revision):
        add("UX-001", f"uiux.md Revision '{revision or 'missing'}' is not rN.", "Set '> **Revision**: r1' and bump it on every round.")
    if status not in STATUSES and not any(s in status for s in SELF_APPROVALS):
        add("UX-001", f"uiux.md Status '{status or 'missing'}' is not one of {', '.join(sorted(STATUSES))}.", "Set '> **Status**: DRAFT'.")
    for number in range(1, 8):
        if not re.search(rf"^##\s+{number}\.", text, re.MULTILINE):
            add("UX-001", f"uiux.md has no '## {number}.' section.", "Restore the section from the uiux.md template.")

    # UX-002 TODO placeholders
    todo_severity = "ERROR" if status in REVIEW_STATUSES else "WARNING"
    todo_files = [d / "uiux.md"] + sorted((d / "screens").glob("*.html")) + sorted((d / "components").glob("*.html"))
    for path in todo_files:
        if not path.is_file():
            continue
        body = re.sub(r"<!--[\s\S]*?-->", "", path.read_text(encoding="utf-8"))
        count = len(re.findall(r"\bTODO\b", body))
        if count:
            add("UX-002", f"{path.relative_to(d).as_posix()} still has {count} TODO placeholder(s).",
                "Replace every TODO before review; Status DRAFT only warns.", todo_severity)

    # UX-003 workflows -> goals
    workflows = _rows(text, 4, r"W-\d+")
    req_path = vdir / "requirements.md"
    known_goals = set(goal_rows(req_path.read_text(encoding="utf-8"))) if req_path.is_file() else None
    if not workflows:
        add("UX-003", "uiux.md '## 4. Workflows' has no W-NN row.", "Confirm the workflows with the user and list them before drawing screens.")
    for row in workflows:
        goals = _ids(row[2] if len(row) > 2 else "", "G")
        if not goals:
            add("UX-003", f"{row[0]} cites no goal (G-NN).", "Every workflow serves a confirmed goal from requirements.md '## 0. Goals'.",
                line=_line_of(text, rf"^\|\s*`?{re.escape(row[0])}`?\s*\|"))
        elif known_goals is not None:
            for g in goals:
                if g not in known_goals:
                    add("UX-003", f"{row[0]} cites {g}, which is not in requirements.md '## 0. Goals'.",
                        "Cite an existing goal, or add the goal through spec_writer (Gate 1).",
                        line=_line_of(text, rf"^\|\s*`?{re.escape(row[0])}`?\s*\|"))

    # UX-004 workflows <-> screens <-> files (incl. `ux sync` warnings)
    flows, sync_warnings = flows_data(d)
    for w in sync_warnings:
        add("UX-004", w + ".", "Keep uiux.md tables, workflows and screen files consistent, then run `coder-nexus ux sync`.")
    for flow in flows["flows"]:
        if not flow["steps"]:
            add("UX-004", f"{flow['id']} lists no screen in its steps.", "Write steps as '1→S01, 2→S02'.")
    flow_ids = {f["id"] for f in flows["flows"]}
    screen_rows = _rows(text, 5, r"S\d+")
    pages: dict[str, _Page] = {}
    for row in screen_rows:
        sid, rel = row[0], row[2] if len(row) > 2 else ""
        row_steps = _split(row[5]) if len(row) > 5 else []
        for step in row_steps:
            wid = step.split("#")[0].upper()
            if re.fullmatch(r"W-\d+", wid) and wid not in flow_ids:
                add("UX-004", f"{sid} serves step {step}, but {wid} is not in '## 4. Workflows'.", "Fix the Steps column or add the workflow.")
        path = d / rel
        if not rel or not path.is_file():
            continue
        page = pages[sid] = _parse(path)
        if page.root.get("data-screen", "") != sid:
            add("UX-004", f"{rel}: data-screen='{page.root.get('data-screen', '')}' does not match row {sid}.",
                f"Set <main class=\"screen\" data-screen=\"{sid}\">.")
        if sorted(_split(page.root.get("data-steps", ""))) != sorted(row_steps):
            add("UX-004", f"{rel}: data-steps='{page.root.get('data-steps', '')}' does not match the row Steps '{', '.join(row_steps)}'.",
                "Keep data-steps and the uiux.md Steps column identical.")
    flows_js = d / "data" / "flows.js"
    if not flows_js.is_file() or flows_js.read_text(encoding="utf-8") != render_flows(flows):
        add("UX-004", "data/flows.js is missing or older than uiux.md.", "Run `coder-nexus ux sync`.", "WARNING")

    # UX-005 states
    for sid, page in pages.items():
        rel = next(r[2] for r in screen_rows if r[0] == sid)
        if "default" not in page.states:
            add("UX-005", f"{rel} has no data-state=\"default\" section.", "Every screen draws its default state.")
        if {"app-list", "app-list-item"} & page.classes or page.has_table:
            notes = " ".join(page.notes).lower()
            for state in LIST_STATES:
                if state in page.states:
                    continue
                if re.search(rf"\b{state}\b", notes):
                    add("UX-005", f"{rel} (list/data screen) has no '{state}' state; a note explains why.",
                        "Confirm the reason with the reviewer.", "WARNING")
                else:
                    add("UX-005", f"{rel} (list/data screen) has no '{state}' state.",
                        f"Draw data-state=\"{state}\", or add a .note saying why the {state} state does not apply.")

    # UX-006 kit classes only; inline colors/fonts
    kit_css = superpowers / "ux" / "kit" / "kit.css"
    kit_classes = set(re.findall(r"\.(app-[\w-]+)", kit_css.read_text(encoding="utf-8"))) if kit_css.is_file() else None
    if kit_classes is None:
        add("UX-006", f"Kit stylesheet not found: {kit_css}.", "Run `coder-nexus ux extract --project .`.")
    component_files = sorted((d / "components").glob("*.html"))
    all_pages = [(d / r[2], pages[r[0]]) for r in screen_rows if r[0] in pages]
    all_pages += [(p, _parse(p)) for p in component_files]
    for path, page in all_pages:
        rel = path.relative_to(d).as_posix()
        if kit_classes is not None:
            unknown = sorted(c for c in page.classes if c.startswith("app-") and c not in kit_classes)
            if unknown:
                add("UX-006", f"{rel} uses classes not in the kit: {', '.join(unknown)}.",
                    "Use classes from kit/components.html, or draw a new-component with a components/C-NN file.")
        for style in page.styles:
            if re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|font-family|font:", style):
                add("UX-006", f"{rel} has an inline color/font: style=\"{style}\".", "Use kit classes or var(--c-…).", "WARNING")

    # UX-007 new components
    comp_rows = _rows(text, 6, r"C\d+")
    for sid, page in pages.items():
        for name in page.new_components:
            match = [r for r in comp_rows
                     if r[0] in _ids(name, "C") or (len(r) > 1 and r[1] and name.lower().startswith(r[1].lower()))]
            if not name or not match:
                add("UX-007", f"{sid}: new-component '{name or '(no data-name)'}' has no row in '## 6. New components'.",
                    "Run `coder-nexus ux component` and use its title (or C-NN) as data-name.")
    for row in comp_rows:
        rel = row[2] if len(row) > 2 else ""
        if not rel or not (d / rel).is_file():
            add("UX-007", f"{row[0]} file missing: {rel or '(none)'}.", "Draw the component in components/C-NN-<slug>.html.")
        why = row[4] if len(row) > 4 else ""
        if why.upper() in EMPTY_VALUES:
            add("UX-007", f"{row[0]}: 'Why not in the kit' is empty.", "Explain why no kit class fits.")

    # UX-008 mock bindings
    mock_path = d / "data" / "mock-data.js"
    bindings = [(path.relative_to(d).as_posix(), m) for path, page in all_pages for m in page.mocks]
    mock = None
    if bindings:
        mock = load_mock(mock_path) if mock_path.is_file() else None
        if mock is None:
            add("UX-008", "data/mock-data.js could not be parsed; data-mock paths not checked.",
                "Keep window.MOCK a plain object literal.", "WARNING")
        else:
            for rel, binding in bindings:
                if mock_value(mock, binding) is None:
                    add("UX-008", f"{rel}: data-mock=\"{binding}\" is not in window.MOCK.", "Add the value to data/mock-data.js or fix the path.")

    # UX-011 walkthrough (optional `## 8. Walkthrough`)
    _check_walkthrough(text, status, flows["flows"], screen_rows, pages, mock, add)

    # UX-009 viewports and design source confirmed before review
    if status in REVIEW_STATUSES:
        vp = _read_json(superpowers / "ux" / "viewports.json")
        if not (vp or {}).get("confirmed"):
            add("UX-009", "Viewports are not confirmed (.superpowers/ux/viewports.json).",
                "Ask the user once, then `coder-nexus ux viewports … --decision D-NN`.")
        ds = _read_json(superpowers / "ux" / "design-system.json")
        if not ((ds or {}).get("source") or {}).get("decision"):
            add("UX-009", "Design source decision is not set (.superpowers/ux/design-system.json source.decision).",
                "Confirm the design source with the user and record its D-NN.")

    # UX-010 content hash and approval
    current = content_hash(d)
    stored = _field(text, HASH_FIELD)
    for marker in SELF_APPROVALS:
        if marker in text.upper():
            add("UX-010", f"uiux.md contains {marker}; only an actual user answer approves a design.",
                "Ask the user to approve the exact revision.", line=_line_of(text, re.escape(marker)))
    if status == "APPROVED":
        approval = _section_text(text, 7)
        approved_rev = _bullet(approval, "Approved revision")
        if approved_rev != revision:
            add("UX-010", f"'## 7. Approval' approved revision '{approved_rev or 'missing'}' does not match Revision '{revision}'.",
                "Record the exact revision the user approved.")
        for name in ("Approved on", "User response"):
            if _bullet(approval, name).upper() in EMPTY_VALUES:
                add("UX-010", f"'## 7. Approval' field '{name}' is empty.", "Record the user's actual answer and date.")
        if not stored.startswith("sha256:"):
            add("UX-010", "Status APPROVED but no content hash is stored.", "Run `coder-nexus ux validate --work-item … --write-hash` at approval.")
        elif stored != current:
            add("UX-010", "The design changed after approval (content hash mismatch).",
                "Start a new revision, set Status back to IN_REVIEW and ask for approval again.")
    elif stored.startswith("sha256:") and stored != current:
        add("UX-010", "The design changed since the content hash was written.", "Re-run with --write-hash when presenting the revision.", "WARNING")

    errors = sum(v.severity == "ERROR" for v in violations)
    return {
        "status": "success",
        "document_type": "UIUX",
        "work_item": slug,
        "version": version,
        "design_dir": str(d),
        "design_status": status,
        "revision": revision,
        "content_hash": current,
        "stored_hash": stored or None,
        "gate_status": "FAILED" if errors else "PASSED",
        "valid": not errors,
        "violations_count": len(violations),
        "errors_count": errors,
        "warnings_count": len(violations) - errors,
        "violations": [v.to_dict() for v in violations],
        "checked_rules": CHECKED_RULES,
    }


def _leaves(data: Any) -> set[str]:
    if isinstance(data, dict):
        return set().union(*(_leaves(v) for v in data.values())) if data else set()
    if isinstance(data, list):
        return set().union(*(_leaves(v) for v in data)) if data else set()
    return set() if data is None else {str(data)}


def _check_walkthrough(text: str, status: str, flows: list[dict], screen_rows: list[list[str]],
                       pages: dict[str, "_Page"], mock: Any, add) -> None:
    """UX-011: walkthrough rows cite existing workflows, steps, screens, states and data-ux-target names."""
    rows = walkthrough_rows(text)
    by_id = {f["id"].upper(): f for f in flows}
    screen_ids = {r[0] for r in screen_rows}
    fix = "Edit uiux.md '## 8. Walkthrough', then run `coder-nexus ux sync`."
    shown: dict[str, tuple[str, str]] = {}  # workflow -> (screen, state) on screen when the row starts
    for w in rows:
        prev_screen, prev_state = shown.get(w["workflow"], ("", "default"))
        active = (w["state"] or "default") if w["action"] == "show" else (prev_state if w["screen"] == prev_screen else "default")
        shown[w["workflow"]] = (w["screen"], w["state"] or active)
        where, line = f"Walkthrough {w['workflow']} #{w['step'] or '?'}", w["line"]
        flow = by_id.get(w["workflow"])
        if flow is None:
            add("UX-011", f"{where}: {w['workflow']} is not in '## 4. Workflows'.", "Script only confirmed workflows.", line=line)
            continue
        if w["action"] not in WALKTHROUGH_ACTIONS:
            add("UX-011", f"{where}: unknown action '{w['action'] or '(empty)'}'.",
                f"Use one of: {', '.join(WALKTHROUGH_ACTIONS)}.", line=line)
            continue
        steps = {st.get("n", str(i + 1)): st["screen"] for i, st in enumerate(flow["steps"])}
        if w["step"] and w["step"] not in steps:
            add("UX-011", f"{where}: step '{w['step']}' is not a step of {w['workflow']} ({', '.join(steps) or 'none'}).",
                "Mirror the confirmed workflow steps 1:1; a new step is a Q-NN for spec_writer, not a silent addition.", line=line)
        if not w["screen"]:
            add("UX-011", f"{where}: no screen (first row of a workflow must name one).", fix, line=line)
            continue
        if w["screen"] not in screen_ids:
            add("UX-011", f"{where}: screen {w['screen']} is not in '## 5. Screens'.", fix, line=line)
            continue
        if w["step"] in steps and steps[w["step"]] != w["screen"]:
            add("UX-011", f"{where}: step {w['step']} of {w['workflow']} is {steps[w['step']]}, not {w['screen']}.", fix, line=line)
        page = pages.get(w["screen"])
        if page is None:
            continue
        if w["state"] and w["state"] not in page.states:
            add("UX-011", f"{where}: {w['screen']} has no data-state=\"{w['state']}\".", "Draw the state or fix the State column.", line=line)
        if w["wait_raw"] and w["wait"] is None:
            add("UX-011", f"{where}: Wait (ms) '{w['wait_raw']}' is not a whole number.", "Write milliseconds, e.g. 1200.", line=line)
        target = w["target"]
        if w["action"] in ("tap", "type", "scan") and not target:
            add("UX-011", f"{where}: '{w['action']}' needs a Target.", "Name a data-ux-target on the screen.", line=line)
        if target:
            if TARGET_NAME_RE.fullmatch(target):
                if target not in page.targets:
                    add("UX-011", f"{where}: {w['screen']} has no data-ux-target=\"{target}\".",
                        f"Add data-ux-target=\"{target}\" to the element, or fix the Target.", line=line)
                elif not page.targets[target] & {"", active}:
                    add("UX-011", f"{where}: data-ux-target=\"{target}\" is not drawn in state '{active}' of {w['screen']} "
                        f"(only in {', '.join(sorted(page.targets[target]))}).",
                        "Show the right state first; a row's State applies after its action.", line=line)
            else:
                add("UX-011", f"{where}: Target '{target}' is a CSS selector.",
                    "Prefer a stable data-ux-target name (kebab-case); selectors break between revisions.", "WARNING", line=line)
        if w["action"] in ("type", "scan"):
            value = w["value"]
            if not value:
                add("UX-011", f"{where}: '{w['action']}' needs a Value.", "Use a MOCK value from data/mock-data.js.", line=line)
            elif mock is not None and page.mocks:
                missing = mock_value(mock, value[1:]) is None if value.startswith("@") else value not in _leaves(mock)
                if missing:
                    add("UX-011", f"{where}: value '{value}' is not in data/mock-data.js.",
                        "Use a MOCK value (or '@path') from data/mock-data.js so screens and playback agree.", "WARNING", line=line)
        if w["action"] == "timer" and not re.fullmatch(r"\d+(?:\.\d+)?\s*(?:s|ms)?", w["value"]):
            add("UX-011", f"{where}: timer Value '{w['value'] or '(empty)'}' is not a duration.",
                "Write the real duration, e.g. 15s; playback may be faster, the number on screen is not shortened.", line=line)
    if status == "IN_REVIEW":
        scripted = {w["workflow"] for w in rows}
        for flow in flows:
            timed = [st["screen"] for st in flow["steps"] if st["screen"] in pages
                     and any(TIMER_NOTE_RE.search(n) for n in pages[st["screen"]].notes)]
            if timed and flow["id"].upper() not in scripted:
                add("UX-011", f"{flow['id']} has time-based or automatic behavior ({', '.join(sorted(set(timed)))} notes) but no walkthrough.",
                    "Script it in '## 8. Walkthrough' so the reviewer can watch it play.", "WARNING")


def _read_json(path: Path) -> Optional[dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _error(message: str) -> dict[str, Any]:
    return {"status": "error", "document_type": "UIUX", "gate_status": "FAILED", "valid": False,
            "message": message, "violations": [], "checked_rules": CHECKED_RULES}
