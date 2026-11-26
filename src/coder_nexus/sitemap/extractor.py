"""Extract structured stages, screens, element logic tables, and PNGs from interactive HTML sitemaps.

Handles single-file interactive HTML sitemaps (such as `Huong_Dan_Sitemap_Tuong_Tac.html`)
where `const STAGES = [...]`, `const STAGE_BRIDGES = [...]`, and `const SCREENS = [...]`
embed full-resolution `data:image/...;base64,...` screenshots alongside screen navigation
graphs, pixel hotspots, overview bullets, and element/business-logic tables.

Strictly read-only on the source HTML file and zero external dependencies (Python stdlib + pydantic).
"""

from __future__ import annotations

import base64
import html as html_lib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import Any, Iterable, Optional

from pydantic import BaseModel, Field

from ..figma.summary import infer_canonical_pattern

AUTO_EXTRACT_ALL_MAX_SCREENS = 15

_JS_ARRAY_RE_TEMPLATE = r"\b(?:const|let|var)\s+{name}\s*=\s*"
_DATA_URI_RE = re.compile(r"^data:image/([a-zA-Z0-9.+-]+);base64,(.*)$", re.DOTALL)
_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
_SCREENS_MARKER_RE = re.compile(rb"\b(?:const|let|var)\s+SCREENS\s*=\s*\[")

# Vietnamese & UI-spec keyword fallback for canonical pattern hints
_VI_PATTERN_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("bottomsheet", ("bottom sheet", "bottomsheet", "sheet ", "menu trượt")),
    ("dialog", ("hộp thoại", "cảnh báo", "dialog", "modal", "popup", "xác nhận xóa")),
    ("appbar", ("appbar", "thanh tiêu đề", "header", "thanh điều hướng trên", "topbar")),
    ("bottomnav", ("floating dock", "bottom nav", "thanh điều hướng dưới", "tab bar")),
    ("datepicker", ("chọn ngày", "lịch", "date picker", "ngày bắt đầu", "ngày kết thúc")),
    ("search", ("tìm kiếm", "ô tìm", "search")),
    ("dropdown", ("dropdown", "chọn trạm", "chọn kho", "chọn thiết bị", "combo", "picker")),
    ("formfield", ("ô nhập", "trường ", "edittext", "textfield", "mật khẩu", "nhập liệu", "ô liên kết")),
    ("button", ("nút ", "cụm nút", "cta", "đăng nhập", "đăng xuất", "tiếp tục", "áp dụng", "đặt lại")),
    ("chip", ("chip", "bộ lọc nhanh", "nhóm chip")),
    ("badge", ("badge", "nhãn ", "pill", "tag ", "trạng thái")),
    ("loading", ("tiến trình", "bootstrap", "loading", "đang tải", "shimmer")),
    ("nodata", ("trống", "không có dữ liệu", "empty")),
    ("banner", ("banner", "toast", "thông báo nhanh", "scrim")),
    ("card", ("thẻ ", "khung ", "card", "panel")),
    ("list", ("danh sách", "bảng ", "table", "checklist")),
)


class SitemapExtractResult(BaseModel):
    """Structured result of inspecting or extracting an interactive HTML sitemap."""

    status: str = Field(description="READ | UNSUPPORTED | ERROR")
    source_path: str
    title: str = ""
    total_stages: int = 0
    total_screens: int = 0
    matched_screens: int = 0
    extracted_screens: int = 0
    index_only: bool = False
    out_dir: Optional[str] = None
    index_json_path: Optional[str] = None
    index_md_path: Optional[str] = None
    screen_specs: list[str] = Field(default_factory=list)
    screen_markdowns: list[str] = Field(default_factory=list)
    screen_images: list[str] = Field(default_factory=list)
    stages_summary: list[dict[str, Any]] = Field(default_factory=list)
    note: Optional[str] = None


def is_interactive_sitemap_html(path: Path) -> bool:
    """Fast streaming check: True when `path` looks like an interactive sitemap HTML with `SCREENS = [...]`."""
    if not path.is_file():
        return False
    if path.suffix.lower() not in {".html", ".htm"}:
        return False
    tail = b""
    try:
        with path.open("rb") as fh:
            while True:
                chunk = fh.read(1024 * 1024)
                if not chunk:
                    break
                window = tail + chunk
                if _SCREENS_MARKER_RE.search(window):
                    return True
                tail = window[-128:]
    except OSError:
        return False
    return False


def _extract_js_json_array(text: str, var_name: str) -> Optional[list[dict[str, Any]]]:
    """Decode `const/let/var <var_name> = [...]` cleanly from HTML script text using JSONDecoder.raw_decode."""
    pattern = re.compile(_JS_ARRAY_RE_TEMPLATE.format(name=re.escape(var_name)))
    for match in pattern.finditer(text):
        pos = match.end()
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos >= len(text) or text[pos] != "[":
            continue
        try:
            obj, _ = json.JSONDecoder().raw_decode(text, pos)
            if isinstance(obj, list):
                return [item for item in obj if isinstance(item, dict)]
        except json.JSONDecodeError:
            continue
    return None


def _clean_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", html_lib.unescape(value or "")).strip()


def _infer_element_pattern(name: str, behavior: str = "") -> str:
    """Infer a canonical UI pattern hint from element name + behavior (English & Vietnamese)."""
    hint = infer_canonical_pattern(name, name, "")
    if hint != "custom":
        return hint
    combined = f"{name} {behavior}".lower()
    for pattern_name, keywords in _VI_PATTERN_KEYWORDS:
        if any(k in combined for k in keywords):
            return pattern_name
    return "custom"


class _ScreenContentParser(HTMLParser):
    """Zero-dependency parser for per-screen `htmlContent` (overview bullets + element detail tables)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.overview: list[dict[str, str]] = []
        self.table_headers: list[str] = []
        self.table_rows: list[list[str]] = []
        self.extra_notes: list[str] = []

        self._in_li = False
        self._in_strong_first = False
        self._li_label_parts: list[str] = []
        self._li_body_parts: list[str] = []
        self._li_has_label = False

        self._in_table = False
        self._in_thead = False
        self._in_tr = False
        self._in_cell = False
        self._cell_is_header = False
        self._current_row: list[str] = []
        self._current_cell: list[str] = []
        self._in_code = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        t = tag.lower()
        if t == "code":
            self._in_code = True
            self._append_text("`")
        elif t == "li" and not self._in_table:
            self._in_li = True
            self._in_strong_first = False
            self._li_label_parts = []
            self._li_body_parts = []
            self._li_has_label = False
        elif t in ("strong", "b") and self._in_li and not self._li_has_label and not "".join(self._li_body_parts).strip():
            self._in_strong_first = True
        elif t == "table":
            self._in_table = True
        elif t == "thead" and self._in_table:
            self._in_thead = True
        elif t == "tr" and self._in_table:
            self._in_tr = True
            self._current_row = []
        elif t in ("th", "td") and self._in_tr:
            self._in_cell = True
            self._cell_is_header = (t == "th") or self._in_thead
            self._current_cell = []
        elif t == "br":
            self._append_text(" ")

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "code":
            if self._in_code:
                self._append_text("`")
                self._in_code = False
        elif t in ("strong", "b") and self._in_strong_first:
            self._in_strong_first = False
            self._li_has_label = True
        elif t == "li" and self._in_li:
            label = _clean_whitespace("".join(self._li_label_parts)).rstrip(":")
            body = _clean_whitespace("".join(self._li_body_parts)).lstrip(":").strip()
            if label or body:
                self.overview.append({"label": label, "text": body})
            self._in_li = False
        elif t in ("th", "td") and self._in_cell:
            cell_text = _clean_whitespace("".join(self._current_cell))
            self._current_row.append(cell_text)
            self._in_cell = False
        elif t == "tr" and self._in_tr:
            if any(self._current_row):
                if self._in_thead and not self.table_headers:
                    self.table_headers = self._current_row
                elif not self._in_thead:
                    self.table_rows.append(self._current_row)
            self._in_tr = False
        elif t == "thead":
            self._in_thead = False
        elif t == "table":
            self._in_table = False

    def handle_data(self, data: str) -> None:
        self._append_text(data)

    def _append_text(self, text: str) -> None:
        if self._in_cell:
            self._current_cell.append(text)
        elif self._in_li:
            if self._in_strong_first:
                self._li_label_parts.append(text)
            else:
                self._li_body_parts.append(text)


def parse_screen_html_content(
    html_content: str,
    hotspots: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    """Extract overview bullets and normalized element/business-logic rows from one screen's `htmlContent`."""
    parser = _ScreenContentParser()
    parser.feed(html_content or "")
    parser.close()

    hotspot_by_stt: dict[str, dict[str, Any]] = {}
    for hs in hotspots or []:
        stt = str(hs.get("stt", "")).strip()
        if stt:
            hotspot_by_stt[stt] = {
                "x1": hs.get("x1"),
                "y1": hs.get("y1"),
                "x2": hs.get("x2"),
                "y2": hs.get("y2"),
                "label": hs.get("label", ""),
            }

    elements: list[dict[str, Any]] = []
    headers = [h.lower() for h in parser.table_headers]
    has_preview_col = len(headers) >= 5 and any(k in headers[1] for k in ("preview", "khu vực", "hình"))

    for row_idx, row in enumerate(parser.table_rows, start=1):
        if len(row) >= 5 and (has_preview_col or len(headers) == 0):
            stt, region, name, behavior, logic = row[0], row[1], row[2], row[3], row[4]
        elif len(row) == 4:
            stt, region, name, behavior, logic = row[0], "", row[1], row[2], row[3]
        elif len(row) == 3:
            stt, region, name, behavior, logic = str(row_idx), "", row[0], row[1], row[2]
        elif len(row) >= 2:
            stt, region, name, behavior, logic = row[0], "", row[1], " | ".join(row[2:]), ""
        else:
            continue

        stt_clean = stt.strip() or str(row_idx)
        region_clean = region.replace("🎯", "").strip()
        name_clean = name.strip("* ").strip()
        elem: dict[str, Any] = {
            "stt": stt_clean,
            "region": region_clean,
            "name": name_clean,
            "pattern_hint": _infer_element_pattern(name_clean, behavior),
            "behavior": behavior.strip(),
            "business_logic": logic.strip(),
        }
        if stt_clean in hotspot_by_stt:
            elem["bbox"] = {
                k: hotspot_by_stt[stt_clean][k]
                for k in ("x1", "y1", "x2", "y2")
                if hotspot_by_stt[stt_clean].get(k) is not None
            }
        elements.append(elem)

    return {
        "overview": parser.overview,
        "elements": elements,
    }


def _safe_slug(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", (text or "").strip())
    return cleaned.strip("._-") or "screen"


def _screen_file_stem(screen: dict[str, Any]) -> str:
    sid = _safe_slug(str(screen.get("id") or f"H{screen.get('num', 0):02d}"))
    scode = _safe_slug(str(screen.get("screenCode") or ""))
    if scode and scode.lower() != sid.lower():
        return f"{sid}_{scode}"
    return sid


def _decode_data_uri(data_uri: str) -> Optional[tuple[str, bytes]]:
    m = _DATA_URI_RE.match((data_uri or "").strip())
    if not m:
        return None
    raw_ext = m.group(1).lower().split("+")[0]
    ext = {"jpeg": "jpg", "jpg": "jpg", "png": "png", "webp": "webp", "gif": "gif"}.get(raw_ext, "png")
    try:
        payload = base64.b64decode(m.group(2), validate=False)
    except (ValueError, TypeError):
        return None
    return ext, payload


def _expand_id_filters(raw_ids: Iterable[str]) -> set[str]:
    """Expand comma-separated IDs and simple numeric ranges like `H19-H25` or `19-25`."""
    expanded: set[str] = set()
    for token in raw_ids:
        for part in str(token).split(","):
            p = part.strip().upper()
            if not p:
                continue
            range_m = re.fullmatch(r"([A-Z]*)(\d+)\s*[-–..]+\s*([A-Z]*)(\d+)", p)
            if range_m and (range_m.group(1) == range_m.group(3) or not range_m.group(3)):
                prefix = range_m.group(1) or "H"
                start, end = int(range_m.group(2)), int(range_m.group(4))
                width = max(len(range_m.group(2)), len(range_m.group(4)), 2)
                if start <= end and (end - start) <= 500:
                    for n in range(start, end + 1):
                        expanded.add(f"{prefix}{n:0{width}d}")
                        expanded.add(f"{prefix}{n}")
                    continue
            expanded.add(p)
    return expanded


def _split_csv_tokens(values: Optional[Iterable[str]]) -> list[str]:
    tokens: list[str] = []
    for v in values or []:
        for part in str(v).split(","):
            s = part.strip()
            if s:
                tokens.append(s)
    return tokens


def _filter_screens(
    screens: list[dict[str, Any]],
    stages: list[dict[str, Any]],
    *,
    stage_filters: Optional[Iterable[str]] = None,
    screen_code_filters: Optional[Iterable[str]] = None,
    id_filters: Optional[Iterable[str]] = None,
    query: Optional[str] = None,
    include_neighbors: bool = False,
) -> list[dict[str, Any]]:
    """Filter screens by stage, screenCode/group, screen IDs, or free-text query."""
    st_tokens = [t.lower() for t in _split_csv_tokens(stage_filters)]
    code_tokens = [t.upper() for t in _split_csv_tokens(screen_code_filters)]
    id_set = _expand_id_filters(_split_csv_tokens(id_filters))
    q_norm = (query or "").strip().lower()

    has_filter = bool(st_tokens or code_tokens or id_set or q_norm)
    if not has_filter:
        return list(screens)

    # Resolve stage tokens against stage id, code, or trailing number ("2" -> STAGE_2)
    matched_stage_ids: set[str] = set()
    for st in stages:
        sid = str(st.get("id") or "")
        scode = str(st.get("code") or "")
        stitle = str(st.get("title") or "")
        smod = str(st.get("moduleCode") or "")
        for tok in st_tokens:
            if (
                tok == sid.lower()
                or tok == scode.lower()
                or (tok.isdigit() and sid.lower() == f"stage_{tok}")
                or tok in scode.lower()
                or tok in stitle.lower()
                or tok in smod.lower()
            ):
                matched_stage_ids.add(sid)

    matched_ids: set[str] = set()
    by_id = {str(s.get("id") or ""): s for s in screens}

    for s in screens:
        sid = str(s.get("id") or "")
        scode = str(s.get("screenCode") or "").upper()
        sgroup = str(s.get("group") or "").upper()
        sstage = str(s.get("stageId") or "")

        hit = False
        if st_tokens:
            if sstage in matched_stage_ids or any(t == sstage.lower() or (t.isdigit() and sstage.lower() == f"stage_{t}") for t in st_tokens):
                hit = True
        if code_tokens and not hit:
            if scode in code_tokens or sgroup in code_tokens or any(
                scode.startswith(tok) or tok in str(s.get("title") or "").upper() for tok in code_tokens
            ):
                hit = True
        if id_set and not hit:
            num_str = str(s.get("num") or "")
            if sid.upper() in id_set or (num_str and (f"H{int(num_str):02d}" in id_set or num_str in id_set)):
                hit = True
        if q_norm and not hit:
            haystack = " ".join(
                str(s.get(k) or "") for k in ("id", "code", "screenCode", "title", "shortTitle", "part", "role", "htmlContent")
            ).lower()
            if q_norm in haystack:
                hit = True

        if hit:
            matched_ids.add(sid)

    if include_neighbors and matched_ids:
        neighbors: set[str] = set()
        for sid in matched_ids:
            sc = by_id.get(sid)
            if not sc:
                continue
            for rel in (*(sc.get("parents") or []), *(sc.get("children") or [])):
                if str(rel) in by_id:
                    neighbors.add(str(rel))
        matched_ids |= neighbors

    return [s for s in screens if str(s.get("id") or "") in matched_ids]


def _cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def _render_index_md(
    title: str,
    source_path: Path,
    stages: list[dict[str, Any]],
    bridges: list[dict[str, Any]],
    screens: list[dict[str, Any]],
    extracted_map: dict[str, dict[str, str]],
) -> str:
    lines = [
        f"# Interactive HTML Sitemap Index — {title or source_path.name}",
        "",
        f"- **Source HTML**: `{source_path.name}`",
        f"- **Stages**: `{len(stages)}` | **Total Screens**: `{len(screens)}` | **Extracted Details**: `{len(extracted_map)}`",
        "",
        "> **Agent Usage**: Never open the raw multi-megabyte HTML directly. Read this index to identify the exact `Stage` or `Screen Code` (`M-XX`, `BS-XX`, `DLG-XX`) in ticket scope, then unpack only in-scope screens with:",
        f"> `coder-nexus sitemap extract \"{source_path}\" --stage <STAGE_ID>` or `--screens <CODE1,CODE2> --include-neighbors`",
        "",
    ]

    if stages:
        lines.append("## Stages Overview")
        lines.append("")
        lines.append("| Stage ID | Code | Modules | Screen Count | Title |")
        lines.append("|---|---|---|---|---|")
        count_by_stage: dict[str, int] = {}
        for s in screens:
            st_id = str(s.get("stageId") or "UNGROUPED")
            count_by_stage[st_id] = count_by_stage.get(st_id, 0) + 1
        for st in stages:
            sid = str(st.get("id") or "")
            lines.append(
                f"| `{_cell(sid)}` | {_cell(st.get('code'))} | `{_cell(st.get('moduleCode'))}` | "
                f"{count_by_stage.get(sid, 0)} | {_cell(st.get('title'))} |"
            )
        lines.append("")

    if bridges:
        lines.append("## Stage Bridges (Macro Flow)")
        lines.append("")
        for br in bridges:
            lines.append(f"- `{br.get('fromStage', '?')}` → `{br.get('toStage', '?')}`: {_cell(br.get('label'))}")
        lines.append("")

    # Group screens by stage
    screens_by_stage: dict[str, list[dict[str, Any]]] = {}
    for s in screens:
        screens_by_stage.setdefault(str(s.get("stageId") or "UNGROUPED"), []).append(s)

    stage_order = [str(st.get("id") or "") for st in stages]
    for st_id in screens_by_stage:
        if st_id not in stage_order:
            stage_order.append(st_id)
    stage_meta = {str(st.get("id") or ""): st for st in stages}

    lines.append("## Screen Catalog")
    lines.append("")
    for st_id in stage_order:
        st_screens = screens_by_stage.get(st_id) or []
        if not st_screens:
            continue
        meta = stage_meta.get(st_id)
        heading = f"### `{st_id}` — {meta.get('title', st_id)}" if meta else f"### `{st_id}`"
        lines.append(heading)
        lines.append("")
        lines.append("| ID | Screen Code | Role | Title | Viewport | Parents → Children | Hotspots | Extracted |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for s in st_screens:
            sid = str(s.get("id") or "")
            scode = str(s.get("screenCode") or "")
            vp = f"{s.get('imgWidth', '?')}×{s.get('imgHeight', '?')}"
            parents = ",".join(str(p) for p in (s.get("parents") or [])) or "—"
            children = ",".join(str(c) for c in (s.get("children") or [])) or "—"
            nav = f"{parents} → {children}"
            hs_count = len(s.get("hotspots") or [])
            ext_info = extracted_map.get(sid)
            ext_cell = f"`{Path(ext_info['md']).name}`" if ext_info and ext_info.get("md") else "*(index only)*"
            lines.append(
                f"| `{_cell(sid)}` | `{_cell(scode)}` | {_cell(s.get('role'))} | {_cell(s.get('title'))} | "
                f"{vp} | {nav} | {hs_count} | {ext_cell} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _render_screen_md(spec: dict[str, Any]) -> str:
    vp = spec.get("viewport") or {}
    parents = ", ".join(f"`{p}`" for p in (spec.get("parents") or [])) or "None (Entry)"
    children = ", ".join(f"`{c}`" for c in (spec.get("children") or [])) or "None (Leaf)"

    lines = [
        f"# {spec['id']} ({spec.get('screen_code') or 'N/A'}) — {spec.get('title', '')}",
        "",
        f"- **Stage**: `{spec.get('stage_id') or 'N/A'}` ({spec.get('part') or ''})",
        f"- **Role / Surface**: {spec.get('role') or 'N/A'} | **Main Flow**: `{spec.get('is_main_flow', False)}`",
        f"- **Viewport**: `{vp.get('width', '?')}×{vp.get('height', '?')}`",
        f"- **Image**: `{spec.get('image_path') or 'NOT_EXTRACTED'}`",
        f"- **Navigation**: Parents: {parents} → Children: {children}",
        "",
    ]

    overview = spec.get("overview") or []
    if overview:
        lines.append("## Overview & Action Flow")
        lines.append("")
        for item in overview:
            lbl = item.get("label") or ""
            txt = item.get("text") or ""
            lines.append(f"- **{lbl}**: {txt}" if lbl else f"- {txt}")
        lines.append("")

    elements = spec.get("elements") or []
    if elements:
        lines.append(f"## UI Elements & Business Logic ({len(elements)} items)")
        lines.append("")
        lines.append("| # | Region | Element / UI Label | Pattern Hint | Display & User Action | Business Logic / Rules |")
        lines.append("|---|---|---|---|---|---|")
        for el in elements:
            lines.append(
                f"| {_cell(el.get('stt'))} | {_cell(el.get('region'))} | {_cell(el.get('name'))} | "
                f"`{_cell(el.get('pattern_hint'))}` | {_cell(el.get('behavior'))} | {_cell(el.get('business_logic'))} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _parse_sitemap_file(source_path: Path) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    text = source_path.read_text(encoding="utf-8", errors="replace")
    title_m = _TITLE_RE.search(text[:20000])
    title = _clean_whitespace(title_m.group(1)) if title_m else source_path.stem
    stages = _extract_js_json_array(text, "STAGES") or []
    bridges = _extract_js_json_array(text, "STAGE_BRIDGES") or []
    screens = _extract_js_json_array(text, "SCREENS")
    if screens is None:
        raise ValueError(f"File '{source_path.name}' does not contain a parseable `SCREENS = [...]` JSON array.")
    return title, stages, bridges, screens


def inspect_sitemap(source_path: str | Path) -> SitemapExtractResult:
    """Read-only inspection of an interactive HTML sitemap: returns stages & screen counts without writing files."""
    path = Path(source_path).resolve()
    if not path.is_file():
        return SitemapExtractResult(status="ERROR", source_path=str(path), note=f"File not found: {path}")
    try:
        title, stages, _bridges, screens = _parse_sitemap_file(path)
    except Exception as exc:  # noqa: BLE001
        return SitemapExtractResult(status="UNSUPPORTED", source_path=str(path), note=str(exc))

    count_by_stage: dict[str, int] = {}
    codes_by_stage: dict[str, list[str]] = {}
    for s in screens:
        sid = str(s.get("stageId") or "UNGROUPED")
        count_by_stage[sid] = count_by_stage.get(sid, 0) + 1
        sc = str(s.get("screenCode") or "").strip()
        if sc and sc not in codes_by_stage.setdefault(sid, []):
            codes_by_stage[sid].append(sc)

    stages_summary = [
        {
            "id": st.get("id"),
            "code": st.get("code"),
            "title": st.get("title"),
            "module_code": st.get("moduleCode"),
            "screen_count": count_by_stage.get(str(st.get("id") or ""), 0),
            "screen_codes": codes_by_stage.get(str(st.get("id") or ""), []),
        }
        for st in stages
    ]
    return SitemapExtractResult(
        status="READ",
        source_path=str(path),
        title=title,
        total_stages=len(stages),
        total_screens=len(screens),
        matched_screens=len(screens),
        extracted_screens=0,
        index_only=True,
        stages_summary=stages_summary,
    )


def extract_sitemap(
    source_path: str | Path,
    out_dir: str | Path,
    *,
    stages_filter: Optional[Iterable[str]] = None,
    screen_codes_filter: Optional[Iterable[str]] = None,
    ids_filter: Optional[Iterable[str]] = None,
    query: Optional[str] = None,
    include_neighbors: bool = False,
    index_only: bool = False,
    extract_images: bool = True,
) -> SitemapExtractResult:
    """Extract `index.json`, `index.md`, and (unless `index_only`) per-screen `.png`, `.spec.json`, and `.md`."""
    path = Path(source_path).resolve()
    target = Path(out_dir).resolve()
    if not path.is_file():
        return SitemapExtractResult(status="ERROR", source_path=str(path), out_dir=str(target), note=f"File not found: {path}")

    try:
        title, stages, bridges, screens = _parse_sitemap_file(path)
    except Exception as exc:  # noqa: BLE001
        return SitemapExtractResult(status="UNSUPPORTED", source_path=str(path), out_dir=str(target), note=str(exc))

    matched = _filter_screens(
        screens,
        stages,
        stage_filters=stages_filter,
        screen_code_filters=screen_codes_filter,
        id_filters=ids_filter,
        query=query,
        include_neighbors=include_neighbors,
    )

    target.mkdir(parents=True, exist_ok=True)
    screens_dir = target / "screens"

    screen_specs: list[str] = []
    screen_markdowns: list[str] = []
    screen_images: list[str] = []
    extracted_map: dict[str, dict[str, str]] = {}

    if not index_only and matched:
        screens_dir.mkdir(parents=True, exist_ok=True)
        for s in matched:
            sid = str(s.get("id") or f"H{s.get('num', 0):02d}")
            stem = _screen_file_stem(s)
            img_path_str: Optional[str] = None

            if extract_images and isinstance(s.get("image"), str):
                decoded = _decode_data_uri(s["image"])
                if decoded is not None:
                    ext, raw_bytes = decoded
                    img_file = screens_dir / f"{stem}.{ext}"
                    img_file.write_bytes(raw_bytes)
                    img_path_str = str(img_file)
                    screen_images.append(img_path_str)

            parsed_content = parse_screen_html_content(s.get("htmlContent") or "", s.get("hotspots") or [])
            spec_obj: dict[str, Any] = {
                "source_kind": "html_sitemap",
                "source_html": path.name,
                "id": sid,
                "num": s.get("num"),
                "code": s.get("code"),
                "screen_code": s.get("screenCode"),
                "group": s.get("group"),
                "stage_id": s.get("stageId"),
                "part": s.get("part"),
                "title": s.get("title"),
                "short_title": s.get("shortTitle"),
                "role": s.get("role"),
                "is_main_flow": bool(s.get("isMainFlow", False)),
                "viewport": {
                    "width": s.get("imgWidth"),
                    "height": s.get("imgHeight"),
                },
                "image_path": img_path_str,
                "image_alt": s.get("imageAlt"),
                "parents": list(s.get("parents") or []),
                "children": list(s.get("children") or []),
                "overview": parsed_content["overview"],
                "elements": parsed_content["elements"],
                "hotspots": list(s.get("hotspots") or []),
            }

            spec_file = screens_dir / f"{stem}.spec.json"
            spec_file.write_text(json.dumps(spec_obj, indent=2, ensure_ascii=False), encoding="utf-8")
            screen_specs.append(str(spec_file))

            md_file = screens_dir / f"{stem}.md"
            md_file.write_text(_render_screen_md(spec_obj), encoding="utf-8")
            screen_markdowns.append(str(md_file))

            extracted_map[sid] = {
                "spec": str(spec_file),
                "md": str(md_file),
                **({"image": img_path_str} if img_path_str else {}),
            }

    # Preserve previously extracted screen files in the same output directory (incremental stage runs)
    if screens_dir.is_dir():
        for s in screens:
            sid = str(s.get("id") or f"H{s.get('num', 0):02d}")
            if sid in extracted_map:
                continue
            stem = _screen_file_stem(s)
            existing_spec = screens_dir / f"{stem}.spec.json"
            existing_md = screens_dir / f"{stem}.md"
            if existing_spec.is_file() and existing_md.is_file():
                entry: dict[str, str] = {"spec": str(existing_spec), "md": str(existing_md)}
                for ext in ("png", "jpg", "webp", "gif"):
                    existing_img = screens_dir / f"{stem}.{ext}"
                    if existing_img.is_file():
                        entry["image"] = str(existing_img)
                        break
                extracted_map[sid] = entry

    # Build lightweight catalog index (never includes raw base64 images or raw htmlContent)
    index_screens = [
        {
            "id": s.get("id"),
            "num": s.get("num"),
            "code": s.get("code"),
            "screen_code": s.get("screenCode"),
            "group": s.get("group"),
            "stage_id": s.get("stageId"),
            "title": s.get("title"),
            "short_title": s.get("shortTitle"),
            "role": s.get("role"),
            "is_main_flow": bool(s.get("isMainFlow", False)),
            "viewport": {"width": s.get("imgWidth"), "height": s.get("imgHeight")},
            "parents": list(s.get("parents") or []),
            "children": list(s.get("children") or []),
            "hotspot_count": len(s.get("hotspots") or []),
            "extracted": extracted_map.get(str(s.get("id") or "")),
        }
        for s in screens
    ]
    index_payload = {
        "source_kind": "html_sitemap",
        "source_html": path.name,
        "title": title,
        "total_stages": len(stages),
        "total_screens": len(screens),
        "extracted_screen_ids": sorted(extracted_map),
        "stages": [
            {
                "id": st.get("id"),
                "code": st.get("code"),
                "title": st.get("title"),
                "subtitle": st.get("subtitle"),
                "module_code": st.get("moduleCode"),
            }
            for st in stages
        ],
        "stage_bridges": bridges,
        "screens": index_screens,
    }
    index_json_path = target / "index.json"
    index_json_path.write_text(json.dumps(index_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    index_md_path = target / "index.md"
    index_md_path.write_text(
        _render_index_md(title, path, stages, bridges, screens, extracted_map),
        encoding="utf-8",
    )

    count_by_stage: dict[str, int] = {}
    for s in screens:
        sid = str(s.get("stageId") or "UNGROUPED")
        count_by_stage[sid] = count_by_stage.get(sid, 0) + 1
    stages_summary = [
        {
            "id": st.get("id"),
            "code": st.get("code"),
            "title": st.get("title"),
            "module_code": st.get("moduleCode"),
            "screen_count": count_by_stage.get(str(st.get("id") or ""), 0),
        }
        for st in stages
    ]

    note: Optional[str] = None
    if index_only:
        note = (
            f"Index-only extraction ({len(stages)} stages, {len(screens)} screens). "
            f"Unpack in-scope screens with: coder-nexus sitemap extract \"{path}\" --out \"{target}\" "
            "--stage <STAGE_ID> | --screens <CODE1,CODE2> [--include-neighbors]"
        )
    elif not matched:
        note = "No screens matched the supplied filter criteria; index.json and index.md were still written."

    return SitemapExtractResult(
        status="READ",
        source_path=str(path),
        title=title,
        total_stages=len(stages),
        total_screens=len(screens),
        matched_screens=len(matched),
        extracted_screens=len(screen_specs),
        index_only=index_only,
        out_dir=str(target),
        index_json_path=str(index_json_path),
        index_md_path=str(index_md_path),
        screen_specs=screen_specs,
        screen_markdowns=screen_markdowns,
        screen_images=screen_images,
        stages_summary=stages_summary,
        note=note,
    )
