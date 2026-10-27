"""Specification and plan validator for Flutter Clean Architecture enforcement.

Deterministically validates Proposal specifications and Implementation Plans
against Clean Architecture standards, template completeness, anti-self-approval rules,
and vertical slicing requirements.
"""

from dataclasses import dataclass, asdict
import os
from pathlib import Path
import re
from typing import Any, Optional


@dataclass(frozen=True)
class SpecViolation:
    rule_id: str
    severity: str  # "ERROR" | "WARNING"
    line_number: Optional[int]
    message: str
    suggestion: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "line_number": self.line_number,
            "message": self.message,
            "suggestion": self.suggestion,
        }


REQUIRED_PROPOSAL_SECTIONS = [
    (
        "SEC-01",
        "Mục 1: Bối Cảnh Nghiệp Vụ & Tiêu Chí Nghiệm Thu (ACs)",
        re.compile(r"##\s*1\.\s*(Bối Cảnh Nghiệp Vụ|Business Context)", re.IGNORECASE),
        "Thêm mục '## 1. Bối Cảnh Nghiệp Vụ & Tiêu Chí Nghiệm Thu (ACs)' với thông tin Task Huly và ACs.",
    ),
    (
        "SEC-02",
        "Mục 2: Kết Quả Khảo Sát Không Gian Làm Việc (Context Scan)",
        re.compile(r"##\s*2\.\s*(Kết Quả Khảo Sát|Context Scan)", re.IGNORECASE),
        "Thêm mục '## 2. Kết Quả Khảo Sát Không Gian Làm Việc (Context Scan)' với Scope, Package Name, State Pattern.",
    ),
    (
        "SEC-03",
        "Mục 3: Bóc Tách Thiết Kế & Visual Intake Gate",
        re.compile(r"##\s*3\.\s*(Bóc Tách Thiết Kế|Visual Intake|Visual Deconstruction)", re.IGNORECASE),
        "Thêm mục '## 3. Bóc Tách Thiết Kế & Visual Intake Gate' với Visual AC và quy chuẩn Visual Fidelity.",
    ),
    (
        "SEC-04",
        "Mục 4: So Sánh Các Phương Án Kiến Trúc (Architectural Options & Trade-Offs)",
        re.compile(r"##\s*4\.\s*(So Sánh Các Phương Án|Architectural Options|Trade-Offs)", re.IGNORECASE),
        "Thêm mục '## 4. So Sánh Các Phương Án Kiến Trúc' với Phương Án A (khuyến nghị) và Phương Án B.",
    ),
    (
        "SEC-05",
        "Mục 5: Bảng Phân Định Linh Kiện (Component Discovery Matrix)",
        re.compile(r"##\s*5\.\s*(Bảng Phân Định Linh Kiện|Component Discovery Matrix)", re.IGNORECASE),
        "Thêm mục '## 5. Bảng Phân Định Linh Kiện' áp dụng Ma trận 4 trường hợp (4-Case Matrix).",
    ),
    (
        "SEC-06",
        "Mục 6: Quy Chuẩn Xử Lý Lỗi & UX Patterns",
        re.compile(r"##\s*6\.\s*(Quy Chuẩn Xử Lý Lỗi|Error Handling|UX Patterns)", re.IGNORECASE),
        "Thêm mục '## 6. Quy Chuẩn Xử Lý Lỗi & UX Patterns' áp dụng từ MCP get_ux_error_patterns.",
    ),
    (
        "SEC-07",
        "Mục 7: Thiết Kế Luồng Trạng Thái & Hợp Đồng Dữ Liệu",
        re.compile(r"##\s*7\.\s*(Thiết Kế Luồng Trạng Thái|State Design|BLoC State|Data Flow Contract)", re.IGNORECASE),
        "Thêm mục '## 7. Thiết Kế Luồng Trạng Thái & Hợp Đồng Dữ Liệu' với BLoC State (BaseBlocState) và Data Flow.",
    ),
    (
        "SEC-08",
        "Mục 8: Đặc Tả Luồng Đa Màn Hình & Vòng Đời Điều Hướng",
        re.compile(r"##\s*8\.\s*(Đặc Tả Luồng Đa Màn Hình|Multi-Screen Flow|Navigation Lifecycle)", re.IGNORECASE),
        "Thêm mục '## 8. Đặc Tả Luồng Đa Màn Hình & Vòng Đời Điều Hướng' với 6 trục logic khi có từ 2 màn hình.",
    ),
    (
        "SEC-09",
        "Mục 9: Bảng Tự Rà Soát Trước Phê Duyệt (Pre-Review Self-Checklist)",
        re.compile(r"##\s*9\.\s*(Bảng Tự Rà Soát|Pre-Review Self-Checklist|Self-Checklist)", re.IGNORECASE),
        "Thêm mục '## 9. Bảng Tự Rà Soát Trước Phê Duyệt' với các checkbox tự kiểm tra.",
    ),
    (
        "SEC-10",
        "Mục 10: Cổng Phê Duyệt Thiết Kế (Design Approval Gate)",
        re.compile(r"##\s*10\.\s*(Cổng Phê Duyệt Thiết Kế|Design Approval Gate)", re.IGNORECASE),
        "Thêm mục '## 10. Cổng Phê Duyệt Thiết Kế' với trạng thái ban đầu PENDING_REVIEW.",
    ),
]

MULTI_SCREEN_6_AXES = [
    (
        "AXIS-1",
        "Flow State Architecture",
        re.compile(r"(Flow State|Kiến Trúc State|Single Flow Cubit|Route Arguments)", re.IGNORECASE),
        "Bổ sung phân tích kiến trúc State của luồng (Single Flow Cubit vs Per-screen BLoC).",
    ),
    (
        "AXIS-2",
        "Navigation Lifecycle & Back Button",
        re.compile(r"(Navigation Lifecycle|Back Button|Vòng Đời Điều Hướng|Nút Quay Lại|popUntil)", re.IGNORECASE),
        "Bổ sung đặc tả vòng đời điều hướng và xử lý khi người dùng ấn nút Back.",
    ),
    (
        "AXIS-3",
        "Unhappy Paths & Failure Scenarios",
        re.compile(r"(Unhappy Path|Kịch Bản Tiêu Cực|Failure Scenarios|Xử Lý Lỗi|Lỗi 400|Timeout)", re.IGNORECASE),
        "Bổ sung kịch bản xử lý khi gặp lỗi mạng, OTP sai, hết phiên hoặc timeout.",
    ),
    (
        "AXIS-4",
        "Inter-field Dependencies & Validation Timing",
        re.compile(r"(Inter-field|Validation Timing|Ràng Buộc Ô Nhập|Thời Điểm Validate|Debounce)", re.IGNORECASE),
        "Bổ sung quy định thời điểm kiểm tra hợp lệ của các ô nhập và ràng buộc liên trường.",
    ),
    (
        "AXIS-5",
        "Step-up Security / Biometrics / OTP",
        re.compile(r"(Step-up|Biometrics|OTP|Xác Thực Bảo Mật|FaceID|Vân Tay)", re.IGNORECASE),
        "Bổ sung thử thách xác thực bảo mật trước khi submit giao dịch / lưu mật khẩu mới.",
    ),
    (
        "AXIS-6",
        "Post-flow Cache Invalidation & Side Effects",
        re.compile(r"(Cache Invalidation|Post-flow|Tác Động Sau Khi Hoàn Thành|Side Effects|Reload)", re.IGNORECASE),
        "Bổ sung hành vi làm mới cache, reload balance/danh sách sau khi luồng kết thúc.",
    ),
]


FORBIDDEN_UNRESOLVED_PATTERNS = [
    (
        "UNRESOLVED-OPTIONS",
        re.compile(r"^#{2,4}\s*(?:Option|Phương\s*án|Lựa\s*chọn)\s+[A-Z1-9]\b", re.MULTILINE | re.IGNORECASE),
        "Contains 'Option A/B' headings. Grill via ask_question (1 question at a time) first and record considered choices in codebase-notes.md Decision Log (D-NN); write only the single locked-in choice.",
    ),
    (
        "OPEN-QUESTIONS",
        re.compile(r"^#{2,4}\s*.*(?:\bOpen\s+Questions?\b|Câu\s+hỏi\s+mở|\bAssumptions?\b|\bGiả\s+định\b)", re.MULTILINE | re.IGNORECASE),
        "Contains 'Open Questions' or 'Assumptions' section. Record open questions as Q-NN in codebase-notes.md Question Queue and grill the user one by one until 0 remain.",
    ),
    (
        "TBD",
        re.compile(r"\b(?:TBD|TO_BE_DETERMINED|CHƯA_CHỐT)\b", re.IGNORECASE),
        "Contains unresolved 'TBD / TO_BE_DETERMINED / CHƯA_CHỐT' markers.",
    ),
]

CODEBASE_NOTES_SECTIONS = [
    ("0. Question Queue", re.compile(r"^##\s*0\.\s*(?:Hàng Đợi Câu Hỏi|Question Queue)", re.MULTILINE | re.IGNORECASE)),
    ("1. Decision Log", re.compile(r"^##\s*1\.\s*(?:Nhật Ký Quyết Định|Decision Log)", re.MULTILINE | re.IGNORECASE)),
    ("2. Glossary", re.compile(r"^##\s*2\.\s*(?:Bảng Thuật Ngữ|Glossary)", re.MULTILINE | re.IGNORECASE)),
    ("3. Verified Baseline Facts", re.compile(r"^##\s*3\.\s*(?:Hiện Trạng Codebase|Verified Baseline)", re.MULTILINE | re.IGNORECASE)),
    ("4. Constraints", re.compile(r"^##\s*4\.\s*(?:Ràng Buộc|Constraints)", re.MULTILINE | re.IGNORECASE)),
    ("6. Change Log", re.compile(r"^##\s*6\.\s*(?:Nhật Ký Thay Đổi|Change Log)", re.MULTILINE | re.IGNORECASE)),
]

D_ID_RE = re.compile(r"\bD-\d+\b", re.IGNORECASE)
Q_ID_RE = re.compile(r"\bQ-\d+\b", re.IGNORECASE)
G_ID_RE = re.compile(r"\bG-\d+\b", re.IGNORECASE)
MAX_GOALS = 3


def _table_rows(body: str, id_pattern: str) -> dict[str, list[str]]:
    """Rows of a Markdown table whose first cell is an ID like G-01 / AC-01 / BR-01."""
    rows: dict[str, list[str]] = {}
    for line in body.splitlines():
        m = re.match(rf"^\|\s*(?:\*\*|`)?({id_pattern})(?:\*\*|`)?\s*\|", line.strip(), re.IGNORECASE)
        if m:
            rows[m.group(1).upper()] = [c.strip().strip("*`").strip() for c in line.strip().strip("|").split("|")]
    return rows


def goal_rows(requirements: str) -> dict[str, list[str]]:
    """`## 0. Goals` rows: | G-NN | Goal (outcome) | Success signal | Source | Status |."""
    body = _section_body(_strip_html_comments(requirements), "Goals") or _section_body(_strip_html_comments(requirements), "Mục Tiêu")
    return _table_rows(body, r"G-\d+")


def ac_goal_map(requirements: str) -> dict[str, set[str]]:
    """AC-NN -> goals cited in its row (Goal column)."""
    cleaned = _strip_html_comments(requirements)
    body = _section_body(cleaned, "Acceptance criteria") or _section_body(cleaned, "Tiêu Chí Nghiệm Thu")
    return {ac: {g.upper() for g in G_ID_RE.findall(" | ".join(cells[1:]))} for ac, cells in _table_rows(body, r"AC-\d+").items()}


def _normalize_sc_id(token: str) -> str:
    """Normalize S01 / S-01 -> S-01 and C01 / C-01 -> C-01."""
    m = re.match(r"^([SC])-?(\d+)$", token.strip(), re.IGNORECASE)
    if not m:
        return token.strip().upper()
    return f"{m.group(1).upper()}-{int(m.group(2)):02d}"


def requirements_ui_summary(requirements_text: str) -> dict[str, Any]:
    """Extract UI screens (`S-NN`), workflows (`W-NN`), and components (`C-NN`) from `requirements.md`."""
    cleaned = _strip_html_comments(requirements_text)
    screens_body = _section_body(cleaned, "Screens & Visual Sources") or _section_body(cleaned, "Screens")
    workflows_body = _section_body(cleaned, "Workflows")
    screen_rows = _table_rows(screens_body, r"S-?\d+")
    screens: dict[str, str] = {}
    for sid, cells in screen_rows.items():
        norm_sid = _normalize_sc_id(sid)
        # | Screen ID | Screen Name | Status (NEW | CHANGED | EXISTING) | ...
        status_val = cells[2].upper() if len(cells) > 2 else ""
        if status_val not in {"NEW", "CHANGED", "EXISTING"} and len(cells) > 4:
            status_val = cells[4].upper()
        screens[norm_sid] = status_val or "NEW"
    workflow_rows = _table_rows(workflows_body, r"W-\d+")
    components = {_normalize_sc_id(c) for c in re.findall(r"\bC-?\d+\b", screens_body + "\n" + workflows_body, re.IGNORECASE)}
    return {
        "has_screens_section": bool(screens_body),
        "has_workflows_section": bool(workflows_body),
        "screens": screens,
        "workflows": workflow_rows,
        "components": components,
    }


def uiux_summary(version_dir: Path) -> Optional[dict[str, Any]]:
    """Legacy `design-uiux/uiux.md` or `requirements.md` UI summary for a work-item version."""
    path = version_dir / "design-uiux" / "uiux.md"
    if path.is_file():
        text = _strip_html_comments(path.read_text(encoding="utf-8"))
        screens = _table_rows(_section_body(text, "Screens"), r"S-?\d+")
        return {
            "status": _document_field(text, "Status").upper(),
            "revision": _document_field(text, "Revision"),
            "workflows": set(_table_rows(_section_body(text, "Workflows"), r"W-\d+")),
            "screens": {_normalize_sc_id(sid): (cells[4].upper() if len(cells) > 4 else "") for sid, cells in screens.items()},
            "components": {_normalize_sc_id(cid) for cid in _table_rows(_section_body(text, "New components"), r"C-?\d+")},
        }
    req_path = version_dir / "requirements.md"
    if req_path.is_file():
        summary = requirements_ui_summary(req_path.read_text(encoding="utf-8"))
        if summary["screens"] or summary["workflows"]:
            return {
                "status": "APPROVED",
                "revision": _document_field(req_path.read_text(encoding="utf-8"), "Version"),
                "workflows": set(summary["workflows"]),
                "screens": summary["screens"],
                "components": summary["components"],
            }
    return None


def _strip_html_comments(text: str) -> str:
    return re.sub(r"<!--[\s\S]*?-->", "", text)


def _document_field(content: str, name: str) -> str:
    cleaned = _strip_html_comments(content)
    match = re.search(
        rf"^>\s*\*\*{re.escape(name)}:?\*\*:?\s*([^\n>]+?)\s*$",
        cleaned,
        re.MULTILINE | re.IGNORECASE,
    )
    if match:
        return match.group(1).strip().strip("`").strip()
    fallback = re.search(
        rf"^\s*-\s*\*\*{re.escape(name)}:?\*\*:?\s*([^\n]+?)\s*$",
        cleaned,
        re.MULTILINE | re.IGNORECASE,
    )
    return fallback.group(1).strip().strip("`").strip() if fallback else ""


def _section_body(content: str, title: str) -> str:
    heading = re.search(rf"^##\s+(?:\d+\.\s*)?.*{re.escape(title)}.*$", content, re.MULTILINE | re.IGNORECASE)
    if not heading:
        return ""
    following = content[heading.end():]
    next_heading = re.search(r"^##\s+", following, re.MULTILINE)
    return following[:next_heading.start()].strip() if next_heading else following.strip()


def _has_content(value: str) -> bool:
    return bool(value.strip()) and "{{" not in value and "}}" not in value


def _bullet_field(content: str, name: str) -> str:
    cleaned = _strip_html_comments(content)
    match = re.search(rf"^\s*-\s*\*\*{re.escape(name)}:?\*\*:?\s*`?(.*?)`?\s*$", cleaned, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


class SpecValidator:
    """Validator engine for Proposal Markdown and Implementation Plan verification."""

    def validate_proposal(
        self,
        proposal_content: str = "",
        proposal_path: str = "",
        feature_name: str = "",
    ) -> dict[str, Any]:
        """Validate a feature proposal markdown document.

        Args:
            proposal_content: Raw markdown text of the proposal.
            proposal_path: Optional file path to read proposal from.
            feature_name: Optional feature module name.

        Returns:
            Dictionary containing validation status, violations, and section coverage.
        """
        content = proposal_content
        if not content and proposal_path:
            p = Path(proposal_path)
            if p.exists() and p.is_file():
                content = p.read_text(encoding="utf-8")
            else:
                return {
                    "status": "error",
                    "error": f"Proposal file not found at: {proposal_path}",
                }

        if not content or not content.strip():
            return {
                "status": "error",
                "error": "proposal_content cannot be empty.",
            }

        document_type = _document_field(content, "Document type").upper()
        if document_type in {"CODEBASE_NOTES", "CONTEXT"}:
            return self._validate_codebase_notes(content, set(), feature_name, document_type)
        if document_type in {"REQUIREMENTS", "CHANGE_IMPACT"}:
            return self._validate_feature_requirements(content, proposal_path, feature_name, document_type)
        if document_type == "DESIGN":
            return self._validate_feature_design(content, proposal_path, feature_name)

        lines = content.splitlines()
        violations: list[SpecViolation] = []
        checked_rules: list[str] = []

        # 1. SPEC-001: 10 Required Sections Check
        checked_rules.append("SPEC-001")
        for code, title, pattern, suggestion in REQUIRED_PROPOSAL_SECTIONS:
            if not pattern.search(content):
                violations.append(
                    SpecViolation(
                        rule_id=f"SPEC-001-{code}",
                        severity="ERROR",
                        line_number=None,
                        message=f"Missing required proposal section: '{title}'.",
                        suggestion=suggestion,
                    )
                )

        # 2. SPEC-002: Anti-Self-Approval Check
        checked_rules.append("SPEC-002")
        self._check_anti_self_approval(lines, content, violations)

        # 3. SPEC-003: Clean Architecture Integrity in Proposal
        checked_rules.append("SPEC-003")
        self._check_clean_arch_integrity(content, violations)

        # 4. SPEC-004: Multi-Screen Flow 6-Axis Completeness Check
        checked_rules.append("SPEC-004")
        self._check_multi_screen_flow(content, violations)

        # 5. SPEC-005: Component Matrix Check (Section 5)
        checked_rules.append("SPEC-005")
        self._check_component_matrix(content, violations)

        has_errors = any(v.severity == "ERROR" for v in violations)

        return {
            "status": "success",
            "feature_name": feature_name,
            "gate_status": "FAILED" if has_errors else "PASSED",
            "valid": not has_errors,
            "violations_count": len(violations),
            "errors_count": sum(1 for v in violations if v.severity == "ERROR"),
            "warnings_count": sum(1 for v in violations if v.severity == "WARNING"),
            "violations": [v.to_dict() for v in violations],
            "checked_rules": checked_rules,
        }

    def _check_unresolved_patterns(
        self,
        content: str,
        rule_prefix: str,
        violations: list[SpecViolation],
    ) -> None:
        cleaned = _strip_html_comments(content)
        for suffix, pattern, message in FORBIDDEN_UNRESOLVED_PATTERNS:
            if pattern.search(cleaned):
                violations.append(
                    SpecViolation(
                        rule_id=f"{rule_prefix}-{suffix}",
                        severity="ERROR",
                        line_number=None,
                        message=message,
                        suggestion="Resolve via 1-by-1 ask_question and record in codebase-notes.md Decision Log (D-NN).",
                    )
                )

    def _validate_codebase_notes(
        self,
        content: str,
        cited_ids: set[str],
        feature_name: str,
        document_type: str = "CODEBASE_NOTES",
    ) -> dict[str, Any]:
        violations: list[SpecViolation] = []
        cleaned = _strip_html_comments(content)

        if "{{" in cleaned or "}}" in cleaned:
            violations.append(
                SpecViolation(
                    "NOTES-001-PLACEHOLDER",
                    "ERROR",
                    None,
                    "Unfilled template placeholder in codebase-notes.md.",
                    "Resolve all placeholders from real evidence and confirmed decisions.",
                )
            )
        if "APPROVED_BY_SPEC" in cleaned or "APPROVED_BY_AGENT" in cleaned:
            violations.append(
                SpecViolation(
                    "NOTES-001-SELF-APPROVAL",
                    "ERROR",
                    None,
                    "Self-approval marker detected in codebase-notes.md.",
                    "Wait for human approval at Gate 1 / Gate 2.",
                )
            )

        for section_name, pattern in CODEBASE_NOTES_SECTIONS:
            if not pattern.search(cleaned):
                violations.append(
                    SpecViolation(
                        "NOTES-002-SECTION",
                        "ERROR",
                        None,
                        f"Missing mandatory section in codebase-notes.md: '{section_name}'.",
                        "Include all mandatory sections from codebase-notes.md.tpl.",
                    )
                )

        open_questions = sorted(
            {
                m.group(1).upper()
                for m in re.finditer(
                    r"^\|\s*(?:\*\*|`)?(Q-\d+)(?:\*\*|`)?\s*\|.*\bOPEN\b",
                    cleaned,
                    re.MULTILINE | re.IGNORECASE,
                )
            }
        )
        if open_questions:
            violations.append(
                SpecViolation(
                    "NOTES-003-OPEN-Q",
                    "ERROR",
                    None,
                    f"Question Queue still has OPEN questions: {open_questions}.",
                    "Ask the user one question at a time via ask_question and close each Q-NN into ANSWERED -> D-NN.",
                )
            )

        defined_decisions = {
            m.group(1).upper()
            for m in re.finditer(
                r"^\|\s*(?:\*\*|`)?(D-\d+)(?:\*\*|`)?\s*\|",
                cleaned,
                re.MULTILINE | re.IGNORECASE,
            )
        }
        if not defined_decisions:
            violations.append(
                SpecViolation(
                    "NOTES-004-NO-DECISIONS",
                    "ERROR",
                    None,
                    "Decision Log in codebase-notes.md has no confirmed D-NN rows.",
                    "Record every confirmed ask_question answer as a '| D-01 | ... |' row.",
                )
            )

        missing_decisions = sorted(cited_ids - defined_decisions)
        if missing_decisions:
            violations.append(
                SpecViolation(
                    "NOTES-004-MISSING-DECISION",
                    "ERROR",
                    None,
                    f"Decisions cited in spec/design but not defined in codebase-notes.md Decision Log: {missing_decisions}.",
                    "Add each cited D-NN row to Section 1 (Decision Log) of codebase-notes.md.",
                )
            )

        self._check_unresolved_patterns(cleaned, "NOTES-005", violations)

        has_errors = any(item.severity == "ERROR" for item in violations)
        return {
            "status": "success",
            "feature_name": feature_name,
            "document_type": document_type,
            "gate_status": "FAILED" if has_errors else "PASSED",
            "valid": not has_errors,
            "violations_count": len(violations),
            "errors_count": sum(item.severity == "ERROR" for item in violations),
            "warnings_count": sum(item.severity == "WARNING" for item in violations),
            "violations": [item.to_dict() for item in violations],
            "checked_rules": ["NOTES-001", "NOTES-002", "NOTES-003", "NOTES-004", "NOTES-005"],
        }

    def _validate_feature_requirements(
        self,
        content: str,
        proposal_path: str,
        feature_name: str,
        document_type: str,
    ) -> dict[str, Any]:
        violations: list[SpecViolation] = []
        cleaned = _strip_html_comments(content)

        def require(value: str, rule: str, message: str) -> None:
            if not _has_content(value):
                violations.append(SpecViolation(rule, "ERROR", None, message, "Supply a real source or mark the item BLOCKED."))

        feature_or_item = _document_field(cleaned, "Work Item") or _document_field(cleaned, "Feature")
        require(feature_or_item, "REQ-001", "Missing or unresolved Work Item / Feature.")
        for field in ("Version", "Source references", "Status"):
            value = _document_field(cleaned, field)
            require(value, "REQ-001", f"Missing or unresolved {field}.")
            if field == "Source references" and value.upper() in {"NONE", "UNKNOWN", "N/A"}:
                violations.append(SpecViolation("REQ-001-SOURCE", "ERROR", None, "Source references are missing.", "Cite actual Huly, user response, or workspace evidence."))
            if field == "Status" and value.upper().startswith("DRAFT"):
                violations.append(
                    SpecViolation(
                        "REQ-001-DRAFT",
                        "ERROR",
                        None,
                        "Status is still DRAFT; close every Q-NN with the user, then set PENDING_REVIEW.",
                        "Ask remaining OPEN Q-NN questions one by one via ask_question before Gate 1.",
                    )
                )

        grill_rounds = _document_field(cleaned, "Grill-Me Rounds")
        if grill_rounds and grill_rounds.upper() in {"0", "NONE", "N/A", "SKIPPED", "FALSE"}:
            violations.append(
                SpecViolation(
                    "REQ-001-GRILL-ROUNDS",
                    "ERROR",
                    None,
                    "'Grill-Me Rounds' cannot be 0/NONE; interview the user one question at a time first.",
                    "Conduct Stage 1C interactive grilling via ask_question and record the round count.",
                )
            )

        if "{{" in cleaned or "}}" in cleaned:
            violations.append(SpecViolation("REQ-001-PLACEHOLDER", "ERROR", None, "Unfilled template placeholder.", "Resolve it from evidence or mark the item BLOCKED."))
        if "APPROVED_BY_SPEC" in cleaned or "APPROVED_BY_AGENT" in cleaned:
            violations.append(SpecViolation("REQ-002-SELF-APPROVAL", "ERROR", None, "Agent approval marker is not human approval.", "Ask the user at Gate 1."))

        if document_type == "REQUIREMENTS":
            open_q_markers = sorted({m.upper() for m in Q_ID_RE.findall(cleaned)})
            if open_q_markers:
                violations.append(
                    SpecViolation(
                        "REQ-002-OPEN-Q",
                        "ERROR",
                        None,
                        f"Unconfirmed (Q-NN) markers remain in requirements.md: {open_q_markers}.",
                        "Ask the user via ask_question, record D-NN in codebase-notes.md, and replace (Q-NN) with locked wording + (D-NN).",
                    )
                )
            self._check_unresolved_patterns(cleaned, "REQ-003", violations)

            req_section_specs = (
                ("1. Goal / Scope", re.compile(r"^##\s*(?:\d+\.\s*)?(?:Mục Tiêu|Goal|Scope|Phạm Vi|Actors and permissions)", re.MULTILINE | re.IGNORECASE)),
                ("2. Scope / Actors", re.compile(r"^##\s*(?:\d+\.\s*)?(?:Phạm Vi|Scope|Actors|Tác Nhân)", re.MULTILINE | re.IGNORECASE)),
                ("3. Business Rules / Scenarios", re.compile(r"^##\s*(?:\d+\.\s*)?(?:Kịch Bản|Scenarios|Behavioral Scenarios|Luật Nghiệp Vụ|Business Rules|Behavior and exceptions)", re.MULTILINE | re.IGNORECASE)),
                ("4. Scenarios / Business Rules", re.compile(r"^##\s*(?:\d+\.\s*)?(?:Luật Nghiệp Vụ|Business Rules|Kịch Bản|Scenarios|Behavioral Scenarios|Behavior and exceptions)", re.MULTILINE | re.IGNORECASE)),
                ("5. Acceptance Criteria", re.compile(r"^##\s*(?:\d+\.\s*)?(?:Tiêu Chí Nghiệm Thu|Acceptance Criteria)", re.MULTILINE | re.IGNORECASE)),
                ("6. Gate 1 Approval", re.compile(r"^##\s*(?:\d+\.\s*)?(?:Cổng Phê Duyệt Gate 1|Gate 1 Approval)", re.MULTILINE | re.IGNORECASE)),
            )
            for label, pattern in req_section_specs:
                if not pattern.search(cleaned):
                    violations.append(
                        SpecViolation(
                            "REQ-003",
                            "ERROR",
                            None,
                            f"Missing required section in requirements.md: '{label}'.",
                            "Follow the 6-section human-readable requirements.md template.",
                        )
                    )

            ac_section = _section_body(cleaned, "Acceptance criteria") or _section_body(cleaned, "Tiêu Chí Nghiệm Thu")
            ac_rows = [
                line
                for line in ac_section.splitlines()
                if re.match(r"^\|\s*(?:\*\*|`)?AC-\d+(?:\*\*|`)?\s*\|", line.strip(), re.IGNORECASE)
            ]
            if not ac_rows:
                violations.append(SpecViolation("REQ-004-NO-AC", "ERROR", None, "No source-backed AC rows found.", "Add stable AC IDs, BR/source, and status."))
            seen_ac_ids: set[str] = set()
            for line in ac_rows:
                cells = [cell.strip().strip("*`") for cell in line.strip().strip("|").split("|")]
                ac_id = cells[0].upper()
                if ac_id in seen_ac_ids:
                    violations.append(SpecViolation("REQ-004-DUPLICATE-AC", "ERROR", None, f"Duplicate AC ID: {ac_id}.", "Give each criterion a stable unique ID."))
                seen_ac_ids.add(ac_id)
                if (
                    len(cells) < 4
                    or not all(_has_content(cell) for cell in cells[:4])
                    or cells[2].upper() in {"NONE", "UNKNOWN", "N/A"}
                    or cells[3].upper() not in {"VERIFIED", "BLOCKED", "PENDING"}
                ):
                    violations.append(
                        SpecViolation(
                            "REQ-004-AC-SOURCE",
                            "ERROR",
                            None,
                            "AC row lacks behavior, BR/source, or PENDING/VERIFIED/BLOCKED status.",
                            "Complete the AC row using real evidence or BR-NN reference.",
                        )
                    )

            self._check_goals(cleaned, violations)
            self._check_workflows(cleaned, Path(proposal_path).resolve().parent if proposal_path else None, violations)

            cited_decisions = {m.upper() for m in D_ID_RE.findall(cleaned)}
            notes_ref = _document_field(cleaned, "Codebase Notes") or _document_field(cleaned, "Context")
            if proposal_path:
                req_dir = Path(proposal_path).resolve().parent
                notes_path = req_dir / "codebase-notes.md"
                if not notes_path.is_file() and (req_dir / "context.md").is_file():
                    notes_path = req_dir / "context.md"
                if notes_path.is_file():
                    notes_res = self._validate_codebase_notes(
                        notes_path.read_text(encoding="utf-8"),
                        cited_decisions,
                        feature_name,
                    )
                    violations.extend(SpecViolation(**item) for item in notes_res["violations"])
                elif cited_decisions or notes_ref:
                    violations.append(
                        SpecViolation(
                            "NOTES-000-MISSING",
                            "ERROR",
                            None,
                            f"Sibling codebase-notes.md not found in {req_dir}.",
                            "Create codebase-notes.md (Question Queue Q-NN + Decision Log D-NN) alongside requirements.md.",
                        )
                    )

            version = _document_field(cleaned, "Version").lower()
            if re.fullmatch(r"v([2-9]|[1-9]\d+)", version):
                impact_path = Path(proposal_path).with_name("change-impact.md") if proposal_path else None
                if not impact_path or not impact_path.is_file():
                    violations.append(SpecViolation("IMPACT-001-MISSING", "ERROR", None, "v2+ requires a sibling change-impact.md.", "Write the actual-code baseline and AC delta before Gate 1."))
                else:
                    impact_content = impact_path.read_text(encoding="utf-8")
                    if _document_field(impact_content, "Document type").upper() != "CHANGE_IMPACT" or _document_field(impact_content, "Version").lower() != version:
                        violations.append(SpecViolation("IMPACT-001-MISMATCH", "ERROR", None, "Sibling change-impact type/version does not match requirements.", "Use CHANGE_IMPACT for this vN."))
                    impact = self._validate_feature_requirements(impact_content, "", feature_name, "CHANGE_IMPACT")
                    violations.extend(SpecViolation(**item) for item in impact["violations"])
        else:
            for title, rule in (
                ("Baseline", "IMPACT-001"),
                ("AC delta", "IMPACT-002"),
                ("Code impact", "IMPACT-003"),
                ("Regression and migration", "IMPACT-003"),
                ("Decision", "IMPACT-003"),
            ):
                require(_section_body(cleaned, title), rule, f"Missing or empty section: {title}.")
            for field in ("Previous version", "Previous requirements/design/as-built", "Baseline code revision", "Design versus actual code differences"):
                require(_bullet_field(cleaned, field), "IMPACT-001", f"Missing or unresolved {field}.")
            if not re.fullmatch(r"[0-9a-f]{7,40}", _bullet_field(cleaned, "Baseline code revision"), re.IGNORECASE):
                violations.append(SpecViolation("IMPACT-001-REVISION", "ERROR", None, "Baseline code revision must be an actual Git commit SHA.", "Commit or otherwise identify the implemented baseline before approving v2."))
            version_match = re.fullmatch(r"v(\d+)", _document_field(cleaned, "Version").lower())
            if version_match and int(version_match.group(1)) > 1:
                expected_previous = f"v{int(version_match.group(1)) - 1}"
                if _bullet_field(cleaned, "Previous version").lower() != expected_previous:
                    violations.append(SpecViolation("IMPACT-001-PREVIOUS", "ERROR", None, f"Previous version must be {expected_previous}.", "Compare against the immediately preceding version."))
            if not re.search(r"^\|\s*AC-\d+\s*\|\s*(?:Keep|Add|Change|Remove)\s*\|", _section_body(cleaned, "AC delta"), re.MULTILINE | re.IGNORECASE):
                violations.append(SpecViolation("IMPACT-002-NO-DELTA", "ERROR", None, "AC delta has no classified AC rows.", "Classify every affected AC from the prior baseline."))
            code_impact = _section_body(cleaned, "Code impact")
            if not any(line.startswith("|") and "{{" not in line and "---" not in line and "Module / file" not in line for line in code_impact.splitlines()):
                violations.append(SpecViolation("IMPACT-003-NO-CODE-IMPACT", "ERROR", None, "Code impact has no assessed consumers or files.", "Record the affected code or a reasoned no-impact result."))

        has_errors = any(item.severity == "ERROR" for item in violations)
        return {
            "status": "success",
            "feature_name": feature_name,
            "document_type": document_type,
            "gate_status": "FAILED" if has_errors else "PASSED",
            "valid": not has_errors,
            "violations_count": len(violations),
            "errors_count": sum(item.severity == "ERROR" for item in violations),
            "warnings_count": sum(item.severity == "WARNING" for item in violations),
            "violations": [item.to_dict() for item in violations],
            "checked_rules": ["REQ-001", "REQ-002", "REQ-003", "REQ-004", "REQ-005", "REQ-006", "NOTES-001", "IMPACT-001", "IMPACT-002", "IMPACT-003"],
        }

    @staticmethod
    def _check_workflows(cleaned: str, version_dir: Optional[Path], violations: list[SpecViolation]) -> None:
        """REQ-006: when UI screens/workflows are in scope, validate `## Screens & Visual Sources` and `## Workflows`."""
        req_ui = requirements_ui_summary(cleaned)
        goals = set(goal_rows(cleaned))
        active_screens = {sid for sid, status in req_ui["screens"].items() if status != "EXISTING"}

        if active_screens and not req_ui["workflows"]:
            violations.append(SpecViolation(
                "REQ-006-NO-WORKFLOWS", "ERROR", None,
                f"requirements.md defines non-EXISTING screens {sorted(active_screens)} in '## Screens & Visual Sources' but has no '## Workflows' rows.",
                "Add one W-NN row per UI workflow in '## Workflows' mapping Goal, Steps -> screens (S-NN), and Scenarios / AC.",
            ))

        referenced_screens: set[str] = set()
        for wid, cells in req_ui["workflows"].items():
            row_text = " | ".join(cells[1:])
            row_goals = {g.upper() for g in G_ID_RE.findall(row_text)}
            row_screens = {_normalize_sc_id(s) for s in re.findall(r"\bS-?\d+\b", row_text, re.IGNORECASE)}
            row_acs = {a.upper() for a in re.findall(r"\bAC-\d+\b", row_text, re.IGNORECASE)}
            referenced_screens |= row_screens

            if not row_goals or (goals and not (row_goals <= goals)):
                violations.append(SpecViolation(
                    "REQ-006-WORKFLOW-GOAL", "ERROR", None,
                    f"{wid} in '## Workflows' must cite a confirmed goal in '## 0. Goals'.",
                    "Reference the confirmed G-NN served by this workflow.",
                ))
            if not row_screens:
                violations.append(SpecViolation(
                    "REQ-006-WORKFLOW-SCREEN", "ERROR", None,
                    f"{wid} in '## Workflows' does not reference any S-NN screen ID in 'Steps -> screens'.",
                    "Include at least one S-NN screen ID in the Steps -> screens column.",
                ))
            if not row_acs:
                violations.append(SpecViolation(
                    "REQ-006-WORKFLOW-AC", "ERROR", None,
                    f"{wid} in '## Workflows' does not reference any AC-NN in 'Scenarios / AC'.",
                    "Link each W-NN workflow to at least one AC-NN acceptance criterion.",
                ))

        if active_screens and req_ui["workflows"]:
            unreferenced = sorted(active_screens - referenced_screens)
            if unreferenced:
                violations.append(SpecViolation(
                    "REQ-006-SCREEN-UNREFERENCED", "ERROR", None,
                    f"Non-EXISTING screens in '## Screens & Visual Sources' not referenced by any W-NN workflow: {unreferenced}.",
                    "Include each new or changed S-NN screen in at least one W-NN workflow step.",
                ))

        if version_dir is not None and (version_dir / "design-uiux" / "uiux.md").is_file():
            uiux = uiux_summary(version_dir)
            if uiux is not None:
                if uiux["status"] != "APPROVED":
                    violations.append(SpecViolation(
                        "REQ-006-UIUX-NOT-APPROVED", "ERROR", None,
                        f"design-uiux/uiux.md is {uiux['status'] or 'missing a Status'}; the UI/UX revision must be APPROVED by the user before Gate 1.",
                        "Record the user's approval in requirements.md.",
                    ))
                body = _section_body(cleaned, "Workflows")
                if not body:
                    violations.append(SpecViolation(
                        "REQ-006-NO-WORKFLOWS", "ERROR", None, "requirements.md has no '## Workflows' section.",
                        "Add one row per approved W-NN with its goal, steps -> screens and scenarios / AC.",
                    ))
                    return
                listed = {w.upper() for w in re.findall(r"\bW-\d+\b", body, re.IGNORECASE)}
                missing = sorted(uiux["workflows"] - listed)
                if missing:
                    violations.append(SpecViolation(
                        "REQ-006-WORKFLOW-MISSING", "ERROR", None, f"Workflows missing from requirements.md: {missing}.",
                        "Map each W-NN to scenarios and AC in '## Workflows'.",
                    ))

    @staticmethod
    def _check_goals(cleaned: str, violations: list[SpecViolation]) -> None:
        """Goals are confirmed outcomes; every BR and AC must serve one, every goal needs an AC."""
        goals = goal_rows(cleaned)
        if not goals:
            violations.append(SpecViolation(
                "REQ-005-NO-GOALS", "ERROR", None,
                "requirements.md has no confirmed goals in '## 0. Goals' (| G-NN | Goal | Success signal | Source | Status |).",
                "Draft 1-3 outcome goals from the sources, confirm them with the user via ask_question, record D-NN.",
            ))
            return
        if len(goals) > MAX_GOALS:
            violations.append(SpecViolation(
                "REQ-005-TOO-MANY-GOALS", "WARNING", None,
                f"{len(goals)} goals; more than {MAX_GOALS} usually means the batch is several features.",
                "Ask the user to pick the goals for this vN and move the rest to Non-goals or a later version.",
            ))
        confirmed: set[str] = set()
        for gid, cells in goals.items():
            if (
                len(cells) < 5
                or not all(_has_content(c) for c in cells[:5])
                or cells[4].upper() != "CONFIRMED"
                or not D_ID_RE.search(cells[3])
            ):
                violations.append(SpecViolation(
                    "REQ-005-GOAL-ROW", "ERROR", None,
                    f"{gid} needs a goal, an observable success signal, a source citing the user-confirmed D-NN, and Status CONFIRMED.",
                    "Confirm the goal with the user (ask_question) and cite the resulting D-NN.",
                ))
            else:
                confirmed.add(gid)

        acs = ac_goal_map(cleaned)
        for ac_id, cited in acs.items():
            if not cited:
                violations.append(SpecViolation(
                    "REQ-005-AC-GOAL", "ERROR", None, f"{ac_id} serves no goal.",
                    "Add the G-NN it serves in the Goal column, or move the behavior to Scope out / Non-goals.",
                ))
            elif cited - goals.keys():
                violations.append(SpecViolation(
                    "REQ-005-AC-GOAL", "ERROR", None, f"{ac_id} cites unknown goal(s) {sorted(cited - goals.keys())}.",
                    "Cite only goals listed in '## 0. Goals'.",
                ))
        served = set().union(*acs.values()) if acs else set()
        for gid in sorted(confirmed - served):
            violations.append(SpecViolation(
                "REQ-005-GOAL-UNCOVERED", "ERROR", None, f"{gid} has no acceptance criterion.",
                "Add at least one observable AC for the goal, or ask the user to drop it.",
            ))

        br_body = _section_body(cleaned, "Business Rules") or _section_body(cleaned, "Luật Nghiệp Vụ")
        for br_id, cells in _table_rows(br_body, r"BR-\d+").items():
            if not G_ID_RE.search(" | ".join(cells[1:])):
                violations.append(SpecViolation(
                    "REQ-005-BR-GOAL", "ERROR", None, f"{br_id} serves no goal.",
                    "Add the G-NN it serves, or remove the rule as out of scope.",
                ))

    def _validate_feature_design(self, content: str, proposal_path: str, feature_name: str) -> dict[str, Any]:
        violations: list[SpecViolation] = []
        cleaned = _strip_html_comments(content)

        def require(value: str, rule: str, message: str) -> None:
            if not _has_content(value) or value.upper() == "NONE":
                violations.append(SpecViolation(rule, "ERROR", None, message, "Use verified workspace evidence or mark the decision BLOCKED."))

        feature_or_item = _document_field(cleaned, "Work Item") or _document_field(cleaned, "Feature")
        require(feature_or_item, "DESIGN-001", "Missing or unresolved Work Item / Feature.")
        for field in ("Version", "Status"):
            require(_document_field(cleaned, field), "DESIGN-001", f"Missing or unresolved {field}.")
        if _document_field(cleaned, "Status").upper().startswith("DRAFT"):
            violations.append(
                SpecViolation(
                    "DESIGN-001-DRAFT",
                    "ERROR",
                    None,
                    "Design Status is still DRAFT; close all G2 Q-NN questions in codebase-notes.md first.",
                    "Set Status to PENDING_REVIEW after locking in all architectural decisions with the user.",
                )
            )

        design_section_specs = (
            ("Architectural decision", ("Architectural decision", "Target Architecture", "Quyết Định Kiến Trúc", "Kiến Trúc Mục Tiêu")),
            ("Module and folder diff", ("Module and folder diff", "Target Directory Tree", "Sơ Đồ Kiến Trúc", "Cấu Trúc Thư Mục")),
            ("Behavior, data, and state", ("Behavior, data, and state", "State Management", "Hợp Đồng Dữ Liệu")),
            ("UI design system", ("UI design system", "Core Usage", "Tái Sử Dụng")),
            ("Integration, errors, and risks", ("Integration, errors, and risks", "Backend API", "UX Error Handling", "Khảo Sát Xung Đột")),
            ("Verification strategy", ("Verification strategy", "Ma Trận Kiểm Thử", "Target Test Matrix")),
            ("Gate 2 approval", ("Gate 2 approval", "Cổng Phê Duyệt Gate 2")),
        )
        for label, aliases in design_section_specs:
            body = ""
            for alias in aliases:
                body = _section_body(cleaned, alias)
                if _has_content(body):
                    break
            require(body, "DESIGN-002", f"Missing or empty section: {label}.")

        for field in ("Requirements reference", "Gate 1 approval reference", "Scope classification"):
            val = _bullet_field(cleaned, field) or _document_field(cleaned, field)
            require(val, "DESIGN-003", f"Missing or unresolved {field}.")

        if "{{" in cleaned or "}}" in cleaned:
            violations.append(SpecViolation("DESIGN-001-PLACEHOLDER", "ERROR", None, "Unfilled design placeholder.", "Resolve it from real sources."))
        if "APPROVED_BY_SPEC" in cleaned or "APPROVED_BY_AGENT" in cleaned or "APPROVED_BY_PLANNING" in cleaned:
            violations.append(SpecViolation("DESIGN-004-SELF-APPROVAL", "ERROR", None, "Agent approval marker is not human approval.", "Ask the user at Gate 2."))

        open_q_markers = sorted({m.upper() for m in Q_ID_RE.findall(cleaned)})
        if open_q_markers:
            violations.append(
                SpecViolation(
                    "DESIGN-005-OPEN-Q",
                    "ERROR",
                    None,
                    f"Unconfirmed (Q-NN) markers remain in design.md: {open_q_markers}.",
                    "Close all G2 Q-NN questions in codebase-notes.md before writing design.md.",
                )
            )
        self._check_unresolved_patterns(cleaned, "DESIGN-005", violations)

        folder_diff = (
            _section_body(cleaned, "Module and folder diff")
            or _section_body(cleaned, "Target Directory Tree")
            or _section_body(cleaned, "Cấu Trúc Thư Mục")
        )
        proposed = _bullet_field(cleaned, "Proposed structure and owners")
        require(_bullet_field(cleaned, "Current structure and owners"), "DESIGN-006", "Current folder owners are missing.")
        require(proposed, "DESIGN-006", "Proposed folder owners are missing.")
        if re.search(r"lib/modules/\w+/views/", folder_diff):
            violations.append(SpecViolation("DESIGN-006-VIEWS", "ERROR", None, "Proposed top-level views/ bypasses presentation/.", "Place UI under presentation/ using the verified module pattern."))
        scope_class = (_bullet_field(cleaned, "Scope classification") or _document_field(cleaned, "Scope classification")).upper()
        if scope_class == "INIT" and not all(
            layer in folder_diff for layer in ("domain/", "data/", "presentation/")
        ):
            violations.append(SpecViolation("DESIGN-006-INIT-LAYERS", "ERROR", None, "A new module needs Domain, Data, and Presentation ownership.", "Map the real responsibilities without speculative classes."))

        cited_decisions = {m.upper() for m in D_ID_RE.findall(cleaned)}
        if proposal_path:
            design_dir = Path(proposal_path).resolve().parent
            if not (design_dir / "requirements.md").is_file():
                violations.append(SpecViolation("DESIGN-003-REQUIREMENTS", "ERROR", None, "Sibling requirements.md is missing.", "Complete Gate 1 in the same version directory."))
            else:
                goals = set(goal_rows((design_dir / "requirements.md").read_text(encoding="utf-8")))
                alignment = _section_body(cleaned, "Goal alignment") or _section_body(cleaned, "Bám Mục Tiêu")
                if goals and not _has_content(alignment):
                    violations.append(SpecViolation(
                        "DESIGN-007-GOALS", "ERROR", None, "design.md has no '## Goal alignment' section.",
                        "Show how the design delivers each confirmed G-NN; drop or justify elements that serve none.",
                    ))
                elif goals:
                    missing = sorted(goals - {g.upper() for g in G_ID_RE.findall(alignment)})
                    if missing:
                        violations.append(SpecViolation(
                            "DESIGN-007-GOALS", "ERROR", None, f"Goal alignment does not cover {missing}.",
                            "Name the design elements that deliver each goal.",
                        ))
            self._check_uiux_mapping(cleaned, design_dir, violations)
            notes_path = design_dir / "codebase-notes.md"
            if not notes_path.is_file() and (design_dir / "context.md").is_file():
                notes_path = design_dir / "context.md"
            if notes_path.is_file():
                notes_res = self._validate_codebase_notes(
                    notes_path.read_text(encoding="utf-8"),
                    cited_decisions,
                    feature_name,
                )
                violations.extend(SpecViolation(**item) for item in notes_res["violations"])

        has_errors = any(item.severity == "ERROR" for item in violations)
        return {
            "status": "success",
            "feature_name": feature_name,
            "document_type": "DESIGN",
            "gate_status": "FAILED" if has_errors else "PASSED",
            "valid": not has_errors,
            "violations_count": len(violations),
            "errors_count": sum(item.severity == "ERROR" for item in violations),
            "warnings_count": sum(item.severity == "WARNING" for item in violations),
            "violations": [item.to_dict() for item in violations],
            "checked_rules": ["DESIGN-001", "DESIGN-002", "DESIGN-003", "DESIGN-004", "DESIGN-005", "DESIGN-006", "DESIGN-007", "DESIGN-008"],
        }

    @staticmethod
    def _check_uiux_mapping(cleaned: str, version_dir: Path, violations: list[SpecViolation]) -> None:
        """DESIGN-008: when UI screens/components are in scope, design.md maps every non-EXISTING S-NN and every C-NN."""
        uiux = uiux_summary(version_dir)
        if uiux is None:
            return
        if uiux["status"] != "APPROVED":
            violations.append(SpecViolation(
                "DESIGN-008-UIUX-NOT-APPROVED", "ERROR", None,
                f"design-uiux/uiux.md is {uiux['status'] or 'missing a Status'}; design.md maps only an approved UI/UX revision.",
                "Get the Gate 1 specification approved first.",
            ))
        needed = {sid for sid, kind in uiux["screens"].items() if kind != "EXISTING"} | uiux["components"]
        if not needed and not (version_dir / "design-uiux" / "uiux.md").is_file():
            return
        body = _section_body(cleaned, "UI/UX mapping")
        if not body:
            violations.append(SpecViolation(
                "DESIGN-008-NO-MAPPING", "ERROR", None, "design.md has no '## UI/UX mapping' section although UI screens/components are in scope.",
                "Map each S-NN to its screen/route and each C-NN to a component in '## UI/UX mapping'.",
            ))
            return
        mapped = {_normalize_sc_id(m) for m in re.findall(r"\b[SC]-?\d+\b", body, re.IGNORECASE)}
        missing = sorted(needed - mapped)
        if missing:
            violations.append(SpecViolation(
                "DESIGN-008-UNMAPPED", "ERROR", None, f"UI/UX items without a mapping in design.md: {missing}.",
                "Add a row per screen and NEW COMPONENT; each NEW COMPONENT also becomes a task at Gate 3.",
            ))

    def _check_anti_self_approval(
        self,
        lines: list[str],
        content: str,
        violations: list[SpecViolation],
    ) -> None:
        """Verify that agent did not autonomously approve its own proposal."""
        # Detect APPROVED_BY_SPEC or similar unauthorized approval signatures
        self_approved_pattern = re.compile(
            r"(APPROVED_BY_SPEC|APPROVED_BY_AGENT|Tự duyệt|Tự phê duyệt)",
            re.IGNORECASE,
        )
        for idx, line in enumerate(lines, start=1):
            if self_approved_pattern.search(line):
                violations.append(
                    SpecViolation(
                        rule_id="SPEC-002-SELF-APPROVAL",
                        severity="ERROR",
                        line_number=idx,
                        message=(
                            "Autonomous self-approval detected ('APPROVED_BY_SPEC'). "
                            "Agent is strictly forbidden from approving proposals autonomously."
                        ),
                        suggestion=(
                            "Set status to '🟡 PENDING_REVIEW' and invoke 'ask_question' to request "
                            "explicit human developer approval at the Design Approval Gate."
                        ),
                    )
                )

        # In Header or Section 10: Status must be PENDING_REVIEW before human approval
        status_line_pattern = re.compile(
            r"Trạng thái\s*(phê duyệt)?\s*(thiết kế)?\s*:\s*.*?(APPROVED|ĐÃ DUYỆT)",
            re.IGNORECASE,
        )
        has_human_signature = bool(
            re.search(r"Người phê duyệt\s*:\s*(?!_|\s*$)[A-Za-z0-9\.\_\s\-]+", content)
        )

        for idx, line in enumerate(lines, start=1):
            if status_line_pattern.search(line) and not has_human_signature:
                violations.append(
                    SpecViolation(
                        rule_id="SPEC-002-UNVERIFIED-APPROVAL",
                        severity="ERROR",
                        line_number=idx,
                        message=(
                            "Proposal is marked as 'APPROVED' without a verified human approver signature. "
                            "Initial proposal state must be '🟡 PENDING_REVIEW'."
                        ),
                        suggestion="Change status to '🟡 PENDING_REVIEW' until the developer explicitly approves via ask_question.",
                    )
                )

    def _check_clean_arch_integrity(
        self,
        content: str,
        violations: list[SpecViolation],
    ) -> None:
        """Verify proposal specifies Clean Architecture 3 layers and contracts."""
        # Must mention Domain entities or UseCases
        has_domain_entity = bool(
            re.search(r"\b[A-Za-z0-9_]*Entity\b", content)
            or re.search(r"domain/entities", content, re.IGNORECASE)
        )
        has_domain_usecase = bool(
            re.search(r"\b[A-Za-z0-9_]*UseCase\b", content)
            or re.search(r"domain/usecases", content, re.IGNORECASE)
        )
        has_bloc_state = bool(
            re.search(r"\b[A-Za-z0-9_]*Cubit\b", content)
            or re.search(r"\bBaseBlocState\b", content)
            or re.search(r"BLoC State", content, re.IGNORECASE)
        )

        # Check for bad smell: proposal only lists views/ screens without 3 layers
        raw_views_only = bool(
            re.search(r"lib/modules/\w+/views/", content)
            and not re.search(r"lib/modules/\w+/domain/", content)
            and not re.search(r"lib/modules/\w+/data/", content)
        )

        if raw_views_only:
            violations.append(
                SpecViolation(
                    rule_id="SPEC-003-HORIZONTAL-VIEWS-ONLY",
                    severity="ERROR",
                    line_number=None,
                    message=(
                        "Proposal specifies a non-standard 'views/' directory without Clean Architecture "
                        "Domain, Data, and Presentation layers."
                    ),
                    suggestion=(
                        "Invoke 'get_project_structure(scope=\"module\", feature_name=\"...\")' and "
                        "adopt the 3-layer Clean Architecture structure: domain/, data/, presentation/, and di.dart."
                    ),
                )
            )

        if not has_domain_entity:
            violations.append(
                SpecViolation(
                    rule_id="SPEC-003-MISSING-DOMAIN-ENTITY",
                    severity="ERROR",
                    line_number=None,
                    message="Proposal does not define any Domain Entities (e.g., *Entity).",
                    suggestion="Specify domain business entities (pure Dart, immutable) in Section 7 or Section 1.",
                )
            )

        if not has_domain_usecase:
            violations.append(
                SpecViolation(
                    rule_id="SPEC-003-MISSING-DOMAIN-USECASE",
                    severity="ERROR",
                    line_number=None,
                    message="Proposal does not define business UseCases (e.g., *UseCase).",
                    suggestion="Define discrete business use cases in Section 7 or Section 4.",
                )
            )

        if not has_bloc_state:
            violations.append(
                SpecViolation(
                    rule_id="SPEC-003-MISSING-BLOC-STATE",
                    severity="ERROR",
                    line_number=None,
                    message="Proposal does not define BLoC/Cubit State contract (BaseBlocState).",
                    suggestion="Provide BLoC State snippet inheriting BaseBlocState in Section 7.",
                )
            )

    def _check_multi_screen_flow(
        self,
        content: str,
        violations: list[SpecViolation],
    ) -> None:
        """Verify Section 8 includes all 6 critical flow axes when multi-screen is involved."""
        # Detect if feature involves multiple screens (>= 2 screens)
        screen_matches = set(re.findall(r"\bUIT-\d+\b", content, re.IGNORECASE))
        multi_screen_indicated = len(screen_matches) >= 2 or bool(
            re.search(r"(đa màn hình|multi-screen|nhiều màn hình|liên hoàn)", content, re.IGNORECASE)
        )

        if not multi_screen_indicated:
            return

        # Extract Section 8 content
        sec8_match = re.search(
            r"##\s*8\..*?(?=##\s*9\.|\Z)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if not sec8_match:
            # Section 8 missing is already handled by SPEC-001
            return

        sec8_text = sec8_match.group(0)
        sec8_lines = sec8_text.splitlines()
        sec8_body = "\n".join(sec8_lines[1:]) if len(sec8_lines) > 1 else ""

        for axis_code, axis_name, pattern, suggestion in MULTI_SCREEN_6_AXES:
            if not pattern.search(sec8_body):
                violations.append(
                    SpecViolation(
                        rule_id=f"SPEC-004-{axis_code}",
                        severity="ERROR",
                        line_number=None,
                        message=f"Multi-screen flow is missing required axis: '{axis_name}'.",
                        suggestion=suggestion,
                    )
                )

    def _check_component_matrix(
        self,
        content: str,
        violations: list[SpecViolation],
    ) -> None:
        """Verify Section 5 has a component discovery matrix table."""
        sec5_match = re.search(
            r"##\s*5\..*?(?=##\s*6\.|\Z)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if not sec5_match:
            return

        sec5_text = sec5_match.group(0)
        # Check if table headers exist
        has_table = bool(re.search(r"\|\s*UI Element.*?\n\s*\|[\s\-:|]+\n", sec5_text, re.IGNORECASE))
        if not has_table:
            violations.append(
                SpecViolation(
                    rule_id="SPEC-005-MISSING-COMPONENT-TABLE",
                    severity="WARNING",
                    line_number=None,
                    message="Section 5 does not contain a structured Component Discovery Table.",
                    suggestion="Add a table mapping UI elements to app_ui_kit components or recorded Core gaps.",
                )
            )

    # -------------------------------------------------------------------------
    # PLAN VALIDATION
    # -------------------------------------------------------------------------

    def validate_plan(
        self,
        plan_content: str = "",
        plan_path: str = "",
        task_content: str = "",
        task_path: str = "",
        feature_name: str = "",
    ) -> dict[str, Any]:
        """Validate implementation plan and task breakdown documents.

        Args:
            plan_content: Raw text of implementation_plan.md.
            plan_path: Optional path to implementation_plan.md.
            task_content: Raw text of task.md.
            task_path: Optional path to task.md.
            feature_name: Optional feature module name.

        Returns:
            Dictionary containing validation status, violations, and slice analysis.
        """
        p_content = plan_content
        if not p_content and plan_path:
            p = Path(plan_path)
            if p.exists() and p.is_file():
                p_content = p.read_text(encoding="utf-8")

        t_content = task_content
        if not t_content and task_path:
            p = Path(task_path)
            if p.exists() and p.is_file():
                t_content = p.read_text(encoding="utf-8")

        if _document_field(p_content, "Document type").upper() == "IMPLEMENTATION_PLAN":
            return self._validate_versioned_plan(p_content, plan_path, feature_name)

        combined = f"{p_content}\n\n{t_content}".strip()
        if not combined:
            return {
                "status": "error",
                "error": "Both plan_content and task_content are empty.",
            }

        violations: list[SpecViolation] = []
        checked_rules: list[str] = []

        # 1. PLAN-001: Anti-Horizontal UI Slicing Check
        checked_rules.append("PLAN-001")
        self._check_vertical_slicing(p_content, t_content, violations)

        # 2. PLAN-002: Task Metadata Enforcement
        checked_rules.append("PLAN-002")
        self._check_task_metadata(t_content or p_content, violations)

        # 3. PLAN-003: Testing Strategy Mandate
        checked_rules.append("PLAN-003")
        self._check_testing_mandate(combined, violations)

        # 4. PLAN-004: Anti-Self-Approval for Plan
        checked_rules.append("PLAN-004")
        self._check_plan_approval_state(combined, violations)

        has_errors = any(v.severity == "ERROR" for v in violations)

        return {
            "status": "success",
            "feature_name": feature_name,
            "gate_status": "FAILED" if has_errors else "PASSED",
            "valid": not has_errors,
            "violations_count": len(violations),
            "errors_count": sum(1 for v in violations if v.severity == "ERROR"),
            "warnings_count": sum(1 for v in violations if v.severity == "WARNING"),
            "violations": [v.to_dict() for v in violations],
            "checked_rules": checked_rules,
        }

    def _validate_versioned_plan(self, content: str, plan_path: str, feature_name: str) -> dict[str, Any]:
        violations: list[SpecViolation] = []

        def issue(rule: str, message: str, suggestion: str) -> None:
            violations.append(SpecViolation(rule, "ERROR", None, message, suggestion))

        version = _document_field(content, "Version")
        if not _has_content(_document_field(content, "Feature")) and not _has_content(_document_field(content, "Work Item")):
            issue("PLAN-V-001", "Missing or unresolved Feature or Work Item.", "Complete the plan from real sources.")
        for field in ("Version", "Created", "Source references", "Status"):
            if not _has_content(_document_field(content, field)):
                issue("PLAN-V-001", f"Missing or unresolved {field}.", "Complete the plan from real sources.")
        for title in ("AC coverage", "Phase order", "Checkpoints and shared files", "Test and visual strategy", "Gate 3 approval"):
            if not _has_content(_section_body(content, title)):
                issue("PLAN-V-002", f"Missing or empty section: {title}.", "Fill the section with concrete scope and evidence.")
        for field in ("Gate 1 approval reference", "Gate 2 approval reference"):
            value = _bullet_field(content, field)
            if not _has_content(value) or value.upper() == "NONE":
                issue("PLAN-V-003", f"Missing {field}.", "Obtain actual user confirmation before planning.")
        if "{{" in content or "}}" in content:
            issue("PLAN-V-001-PLACEHOLDER", "Unfilled plan placeholder.", "Resolve it before Gate 3.")
        if "APPROVED_BY_SPEC" in content or "APPROVED_BY_AGENT" in content:
            issue("PLAN-V-004-SELF-APPROVAL", "Agent marker is not human approval.", "Ask the user at Gate 3.")

        if not plan_path:
            issue("PLAN-V-005-PATH", "Versioned plan requires plan_path to inspect linked phase files.", "Pass the saved implementation-plan.md path.")
            return self._versioned_plan_result(violations, feature_name)

        version_dir = Path(plan_path).resolve().parent
        requirements_path = version_dir / "requirements.md"
        design_path = version_dir / "design.md"
        if not requirements_path.is_file() or not design_path.is_file():
            issue("PLAN-V-005-PREREQUISITES", "Sibling requirements.md or design.md is missing.", "Complete Gates 1 and 2 in this version folder.")
        req_text = requirements_path.read_text(encoding="utf-8") if requirements_path.is_file() else ""
        ac_section = _section_body(req_text, "Acceptance criteria") or _section_body(req_text, "Tiêu Chí Nghiệm Thu")
        required_ac_ids = set(re.findall(r"^\|\s*(?:\*\*|`)?(AC-\d+)(?:\*\*|`)?\s*\|", ac_section, re.MULTILINE))
        coverage_rows = re.findall(r"^\|\s*(?:\*\*|`)?(AC-\d+)(?:\*\*|`)?\s*\|\s*(?:\*\*|`)?(PHASE-\d+)(?:\*\*|`)?\s*\|", _section_body(content, "AC coverage"), re.MULTILINE)
        coverage = dict(coverage_rows)
        if not required_ac_ids or not coverage or required_ac_ids - coverage.keys():
            issue("PLAN-V-006-AC-COVERAGE", "At least one requirements AC has no phase owner.", "Map every AC ID to a phase.")
        if len(coverage_rows) != len(coverage) or coverage.keys() - required_ac_ids:
            issue("PLAN-V-006-AC-COVERAGE", "Duplicate or unknown AC mapping.", "Map each requirements AC exactly once.")

        phase_order = _section_body(content, "Phase order")
        phase_links = re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", phase_order)
        if not phase_links:
            issue("PLAN-V-007-NO-PHASES", "Plan has no linked phase Markdown files.", "Link each phases/phase-XX-<behavior>.md file.")
        phase_root = (version_dir / "phases").resolve()
        phase_ac_ids: dict[str, set[str]] = {}
        phase_dependencies: dict[str, set[str]] = {}

        for link in phase_links:
            path = (version_dir / link).resolve()
            if not path.is_relative_to(phase_root):
                issue("PLAN-V-007-TRAVERSAL", f"Phase link escapes phases/: {link}", "Use a relative path inside this version's phases/ directory.")
                continue
            if not path.is_file():
                issue("PLAN-V-007-MISSING", f"Linked phase file does not exist: {link}", "Write the phase file before Gate 3.")
                continue
            phase = path.read_text(encoding="utf-8")
            phase_id = _bullet_field(phase, "Phase ID")
            if not re.fullmatch(r"PHASE-\d+", phase_id) or phase_id in phase_ac_ids:
                issue("PLAN-V-008-ID", f"Invalid or repeated phase ID in {link}.", "Give every phase a unique PHASE-NN ID.")
                continue
            if _document_field(phase, "Document type").upper() != "PHASE" or _document_field(phase, "Version") != version:
                issue("PLAN-V-008-VERSION", f"Phase type/version mismatch in {link}.", "Match the parent implementation plan version.")
            if "{{" in phase or "}}" in phase:
                issue("PLAN-V-008-PLACEHOLDER", f"Unfilled placeholder in {link}.", "Resolve from source evidence or mark the dependent work BLOCKED.")
            for field in ("Behavior", "AC IDs", "Depends on", "READY when", "Files", "Owner", "Verification", "UI impact", "Visual target/states"):
                if not _has_content(_bullet_field(phase, field)):
                    issue("PLAN-V-008-METADATA", f"{link} lacks {field}.", "Complete phase ownership and verification metadata.")
            for title in ("Code direction", "Design system source", "Done when", "Risks"):
                if not _has_content(_section_body(phase, title)):
                    issue("PLAN-V-008-SECTION", f"{link} lacks {title}.", "State the concrete code direction or a reasoned N/A.")
            if re.search(r"lib/modules/\w+/views/", _bullet_field(phase, "Files")):
                issue("PLAN-V-008-VIEWS", f"{link} places UI in top-level views/.", "Use the verified presentation/ structure.")
            if not re.search(r"\b(flutter|dart)\b", _bullet_field(phase, "Verification"), re.IGNORECASE):
                issue("PLAN-V-008-VERIFY", f"{link} has no executable Flutter/Dart check.", "Record the actual workspace command.")
            if _bullet_field(phase, "UI impact").upper().startswith("YES") and _bullet_field(phase, "Visual target/states").upper().startswith("N/A"):
                issue("PLAN-V-008-VISUAL", f"{link} has UI impact but no visual target/states.", "Specify platform, target, and required states.")
            phase_ac_ids[phase_id] = set(re.findall(r"AC-\d+", _bullet_field(phase, "AC IDs")))
            phase_dependencies[phase_id] = set(re.findall(r"PHASE-\d+", _bullet_field(phase, "Depends on")))

        goals = set(goal_rows(req_text))
        if goals:
            ac_goals = ac_goal_map(req_text)
            reached = {g for ac, phase_id in coverage.items() if phase_id in phase_ac_ids for g in ac_goals.get(ac, set())}
            for gid in sorted(goals - reached):
                issue("PLAN-V-010-GOAL-COVERAGE", f"{gid} is not delivered by any phase.", "Map the goal's ACs to phases, or ask the user to drop the goal at Gate 1.")
        for ac_id, phase_id in coverage.items():
            if ac_id not in phase_ac_ids.get(phase_id, set()):
                issue("PLAN-V-006-AC-MISMATCH", f"{ac_id} is not owned by {phase_id}'s file.", "Keep plan coverage and phase AC IDs consistent.")
        for phase_id, dependencies in phase_dependencies.items():
            if any(dep not in phase_ac_ids or int(dep.split("-")[1]) >= int(phase_id.split("-")[1]) for dep in dependencies):
                issue("PLAN-V-009-DEPENDENCY", f"{phase_id} has an unknown or forward dependency.", "Depend only on earlier listed phases.")
        return self._versioned_plan_result(violations, feature_name)

    @staticmethod
    def _versioned_plan_result(violations: list[SpecViolation], feature_name: str) -> dict[str, Any]:
        has_errors = any(item.severity == "ERROR" for item in violations)
        return {
            "status": "success",
            "feature_name": feature_name,
            "document_type": "IMPLEMENTATION_PLAN",
            "gate_status": "FAILED" if has_errors else "PASSED",
            "valid": not has_errors,
            "violations_count": len(violations),
            "errors_count": sum(item.severity == "ERROR" for item in violations),
            "warnings_count": sum(item.severity == "WARNING" for item in violations),
            "violations": [item.to_dict() for item in violations],
            "checked_rules": [f"PLAN-V-{index:03d}" for index in range(1, 10)],
        }

    def _check_vertical_slicing(
        self,
        plan_content: str,
        task_content: str,
        violations: list[SpecViolation],
    ) -> None:
        """Enforce that behavioral slices span all 3 layers + tests, rejecting pure UI slices."""
        text = f"{plan_content}\n\n{task_content}".strip()

        # Split by Slice headers (## Lát Cắt or ## Slice)
        slice_blocks = re.split(r"(?=##\s*(?:Lát Cắt|Slice))", text, flags=re.IGNORECASE)

        for block in slice_blocks:
            match = re.match(r"##\s*(?:Lát Cắt|Slice)\s*(\d+|[A-Za-z0-9_-]+)[:\s]*(.*?)(?:\n|$)", block, re.IGNORECASE)
            if not match:
                continue

            slice_id = match.group(1).strip()
            slice_title = match.group(2).strip()

            # Skip foundational design tokens or theme slices
            if re.search(r"(token|theme|foundation|cấu hình|setup)", slice_title, re.IGNORECASE):
                continue

            # Check files mentioned in this slice block
            has_domain = bool(re.search(r"domain/|Entity|UseCase", block, re.IGNORECASE))
            has_data = bool(re.search(r"data/|DataSource|RepoImpl|Model", block, re.IGNORECASE))
            has_presentation = bool(re.search(r"presentation/|Cubit|State|Screen|Page", block, re.IGNORECASE))
            has_only_views = bool(
                re.search(r"(views/|screens/)", block, re.IGNORECASE)
                and not has_domain
                and not has_data
            )

            if has_only_views:
                violations.append(
                    SpecViolation(
                        rule_id="PLAN-001-HORIZONTAL-UI-SLICE",
                        severity="ERROR",
                        line_number=None,
                        message=(
                            f"Slice {slice_id} ('{slice_title}') is a horizontal UI slice. "
                            "It only specifies views/screens without Domain or Data layers."
                        ),
                        suggestion=(
                            "Redesign this slice as a Vertical Slice spanning: "
                            "Domain (Entity + UseCase) -> Data (Source + Model + RepoImpl) -> "
                            "Presentation (Cubit + UI) -> DI -> Unit Test."
                        ),
                    )
                )

    def _check_task_metadata(
        self,
        task_content: str,
        violations: list[SpecViolation],
    ) -> None:
        """Enforce that each task checkbox has required metadata fields."""
        if not task_content.strip():
            return

        # Find task checkbox patterns: - [ ] Task XX or - [ ] **Task XX**
        task_pattern = re.compile(
            r"^[ \t]*-\s*\[[ xX]\]\s*(?:\*\*)?Task\s*([A-Za-z0-9_-]+)(?:\*\*)?[:\s]*(.*?)$",
            re.MULTILINE,
        )

        matches = list(task_pattern.finditer(task_content))
        if not matches:
            violations.append(
                SpecViolation(
                    rule_id="PLAN-002-NO-TASKS-FOUND",
                    severity="ERROR",
                    line_number=None,
                    message="No formatted tasks found (expected '- [ ] **Task XX**: ...').",
                    suggestion="Use template 'task.md.tpl' to structure tasks.",
                )
            )
            return

        for idx, match in enumerate(matches):
            task_id = match.group(1)
            task_title = match.group(2).strip()
            start_pos = match.end()
            end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(task_content)
            task_body = task_content[start_pos:end_pos]

            # Required metadata elements
            has_depends_on = bool(re.search(r"Depends\s*on", task_body, re.IGNORECASE))
            has_ready_when = bool(re.search(r"READY\s*khi", task_body, re.IGNORECASE))
            has_files = bool(re.search(r"Files\s*:", task_body, re.IGNORECASE))
            has_cmd = bool(re.search(r"Lệnh\s*kiểm\s*tra", task_body, re.IGNORECASE))

            missing_fields = []
            if not has_depends_on:
                missing_fields.append("Depends on")
            if not has_ready_when:
                missing_fields.append("READY khi")
            if not has_files:
                missing_fields.append("Files")
            if not has_cmd:
                missing_fields.append("Lệnh kiểm tra")

            if missing_fields:
                line_no = task_content[: match.start()].count("\n") + 1
                violations.append(
                    SpecViolation(
                        rule_id="PLAN-002-INSUFFICIENT-TASK-METADATA",
                        severity="ERROR",
                        line_number=line_no,
                        message=(
                            f"Task {task_id} ('{task_title}') is missing required metadata: "
                            f"{', '.join(missing_fields)}."
                        ),
                        suggestion=(
                            f"Add metadata block under Task {task_id}: "
                            "- Depends on: ...\n"
                            "- READY khi: ...\n"
                            "- Files: ...\n"
                            "- Lệnh kiểm tra: ..."
                        ),
                    )
                )

    def _check_testing_mandate(
        self,
        combined_content: str,
        violations: list[SpecViolation],
    ) -> None:
        """Enforce that the plan contains automated test tasks/commands in test/."""
        has_unit_tests = bool(
            re.search(r"test/modules/|flutter\s+test|\b_test\.dart\b", combined_content, re.IGNORECASE)
        )
        if not has_unit_tests:
            violations.append(
                SpecViolation(
                    rule_id="PLAN-003-MISSING-TEST-STRATEGY",
                    severity="ERROR",
                    line_number=None,
                    message=(
                        "Implementation plan does not specify any automated tests in 'test/'. "
                        "Every vertical slice must include unit/bloc tests."
                    ),
                    suggestion=(
                        "Add test tasks for Domain UseCases and Presentation Cubits "
                        "(e.g., 'flutter test test/modules/<feature>/...')."
                    ),
                )
            )

    def _check_plan_approval_state(
        self,
        combined_content: str,
        violations: list[SpecViolation],
    ) -> None:
        """Ensure plan has not been autonomously started before Plan Approval Gate."""
        # Detect unauthorized In Progress at the plan level when newly created
        unauthorized_start = bool(
            re.search(r"Plan\s*revision\s*đã\s*duyệt\s*:\s*(APPROVED_BY_SPEC|Tự duyệt)", combined_content, re.IGNORECASE)
        )
        if unauthorized_start:
            violations.append(
                SpecViolation(
                    rule_id="PLAN-004-SELF-APPROVAL",
                    severity="ERROR",
                    line_number=None,
                    message="Plan contains self-approved revision marker ('APPROVED_BY_SPEC').",
                    suggestion="Plan must be approved by the developer via ask_question before changing code.",
                )
            )


# Global singleton instance
spec_validator = SpecValidator()
