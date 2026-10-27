"""Tests for SpecValidator (Proposal and Implementation Plan validation)."""

import pytest
from coder_nexus.architecture.spec_validator import spec_validator


SAMPLE_VALID_PROPOSAL = """# Proposal Kỹ Thuật: Banking Auth Flow

> **Tính năng / Task ID**: AUTH-01 — Banking Auth Flow
> **Module sở hữu**: `lib/modules/auth/`
> **Trạng thái phê duyệt thiết kế**: 🟡 `PENDING_REVIEW` (Chờ người dùng duyệt tại Design Approval Gate)

---

## 1. Bối Cảnh Nghiệp Vụ & Tiêu Chí Nghiệm Thu (ACs)
- **Mã Task**: `AUTH-01`
- **Tiêu đề**: Triển khai xác thực người dùng ngân hàng
- **Mô tả nghiệp vụ**: Luồng đăng nhập bằng mật khẩu hoặc sinh trắc học và khôi phục mật khẩu qua OTP.
- **Tiêu chí nghiệm thu**:
  - [x] Đăng nhập bằng password hoặc FaceID
  - [x] Quên mật khẩu qua OTP

---

## 2. Kết Quả Khảo Sát Không Gian Làm Việc (Context Scan)
- **Phân loại phạm vi**: `INIT`
- **Tên gói ứng dụng (Package Name)**: `banking_app`
- **Chuẩn Quản Lý Trạng Thái**: Pattern A (`BaseBlocState`)
- **Thư mục lưu trữ**: `lib/modules/auth/`

---

## 3. Bóc Tách Thiết Kế & Visual Intake Gate
- **Nguồn Thiết Kế**: Figma frame UIT-01 đến UIT-06
- **Trạng Thái Visual Intake**: `PASSED`
- **Bóc Tách Cấu Trúc Thị Giác**: 8pt grid, Brand primary #0052CC
- **Tiêu Chí Nghiệm Thu Thị Giác (Visual AC)**:
  - Sai lệch thiết kế Designer = FAILED

---

## 4. So Sánh Các Phương Án Kiến Trúc (Architectural Options & Trade-Offs)
### Phương Án A (Khuyến Nghị): Clean Architecture 3 lớp với Single Flow Cubit
- Ưu điểm: Tách bạch rõ Domain, Data, Presentation.
- Nhược điểm: Cần nhiều file hơn.

### Phương Án B: Stateful Widgets
- Ưu điểm: Viết nhanh.
- Nhược điểm: Phá vỡ Clean Architecture.

---

## 5. Bảng Phân Định Linh Kiện (Component Discovery Matrix)

| UI Element / AC | Phân loại | Component + variant/config | Import / workspace path | Source evidence + revision | Tokens / a11y | Gap hoặc lý do custom |
|---|---|---|---|---|---|---|
| Input Email | Input | AppTextField | package:app_ui_kit/... | VERIFIED | Standard text | Case 1: Match 1:1 |
| Nút Đăng nhập | Action | AppPrimaryButton | package:app_ui_kit/... | VERIFIED | Primary | Case 1: Match 1:1 |

---

## 6. Quy Chuẩn Xử Lý Lỗi & UX Patterns
- Xử lý lỗi xác thực theo auth_failure từ get_ux_error_patterns.
- Hiển thị inline errorText dưới field.

---

## 7. Thiết Kế Luồng Trạng Thái & Hợp Đồng Dữ Liệu

### Domain Entities & UseCases
- Entities: `AuthSessionEntity`, `OtpChallengeEntity`
- Repository Contract: `AuthRepository`
- UseCases: `LoginWithPasswordUseCase`, `VerifyOtpUseCase`

### BLoC State Design (Kế thừa BaseBlocState)
```dart
sealed class LoginState extends BaseBlocState {
  const LoginState();
}
class LoginInitial extends LoginState {}
class LoginLoading extends LoginState {}
class LoginSuccess extends LoginState {
  final AuthSessionEntity session;
  const LoginSuccess(this.session);
}
```

---

## 8. Đặc Tả Luồng Đa Màn Hình & Vòng Đời Điều Hướng (Multi-Screen Flow)
- **Kiến Trúc State Của Luồng (Flow State Architecture)**: Dùng Flow Cubit quản lý bước UIT-03 -> UIT-06.
- **Vòng Đời Điều Hướng & Nút Quay Lại (Navigation Lifecycle & Back Button)**: popUntil về màn Login khi reset pass thành công.
- **Kịch Bản Tiêu Cực & Xử Lý Lỗi (Unhappy Paths & Failure Scenarios)**: Lỗi 400 OTP sai hiển thị error dialog, đếm ngược tiếp tục.
- **Ràng Buộc Ô Nhập & Thời Điểm Validate (Inter-field Dependencies & Validation Timing)**: Validate realtime mật khẩu mới với checklist 4 tiêu chí.
- **Thử Thách Xác Thực Bảo Mật (Step-up Security / Biometrics / OTP)**: OTP 6 số qua SMS/Email đếm ngược 01:45.
- **Tác Động Sau Khi Hoàn Thành (Post-flow Cache Invalidation & Side Effects)**: Invalidate phiên cũ và chuyển hướng Dashboard.

---

## 9. Bảng Tự Rà Soát Trước Phê Duyệt (Pre-Review Self-Checklist)
- [x] Zero Mock Data
- [x] Clean Architecture 3 lớp
- [x] Đã tra cứu UI Kit

---

## 10. Cổng Phê Duyệt Thiết Kế (Design Approval Gate)
- **Trạng thái**: 🟡 `PENDING_REVIEW`
- **Người phê duyệt**: ______________________
- **Ngày phê duyệt**: ______________________
"""


SAMPLE_VALID_PLAN = """# Kế Hoạch Triển Khai: Banking Auth

## Lát Cắt 01: Core Theme & Tokens Foundation
- Tác động: `lib/core/theme/`

## Lát Cắt 02: Xác Thực Đăng Nhập (UIT-01)
- Domain: `lib/modules/auth/domain/entities/auth_session_entity.dart`, `lib/modules/auth/domain/usecases/login_usecase.dart`
- Data: `lib/modules/auth/data/data_sources/auth_data_source.dart`, `lib/modules/auth/data/repo_impl/auth_repo_impl.dart`
- Presentation: `lib/modules/auth/presentation/bloc/login_cubit.dart`, `lib/modules/auth/presentation/screens/login_screen.dart`
- DI: `lib/modules/auth/di.dart`
- Tests: `test/modules/auth/presentation/login_cubit_test.dart`
"""

SAMPLE_VALID_TASKS = """# Danh Sách Nhiệm Vụ

## Lát Cắt 02: Xác Thực Đăng Nhập

- [ ] **Task 01**: Xây dựng Domain & Data Layer cho Login
  - Trạng thái: `TODO`
  - Depends on: None
  - READY khi: Spec và token đã sẵn sàng
  - Files: `lib/modules/auth/domain/entities/auth_session_entity.dart`, `lib/modules/auth/domain/usecases/login_usecase.dart`, `lib/modules/auth/data/repo_impl/auth_repo_impl.dart`
  - Lệnh kiểm tra: `flutter test test/modules/auth/domain/login_usecase_test.dart`

- [ ] **Task 02**: Xây dựng Cubit, Screen & DI
  - Trạng thái: `TODO`
  - Depends on: Task 01
  - READY khi: Task 01 pass
  - Files: `lib/modules/auth/presentation/bloc/login_cubit.dart`, `lib/modules/auth/presentation/screens/login_screen.dart`, `lib/modules/auth/di.dart`
  - Lệnh kiểm tra: `flutter test test/modules/auth/presentation/login_cubit_test.dart`
"""


def test_validate_proposal_success():
    """Verify that a compliant proposal with all 10 sections passes."""
    res = spec_validator.validate_proposal(proposal_content=SAMPLE_VALID_PROPOSAL, feature_name="auth")
    assert res["status"] == "success"
    assert res["valid"] is True
    assert res["gate_status"] == "PASSED"
    assert res["errors_count"] == 0


def test_validate_proposal_missing_sections():
    """Verify that missing major sections are reported as errors."""
    truncated = """# Proposal Kỹ Thuật: Rút Gọn
## 1. Bối Cảnh Nghiệp Vụ & Tiêu Chí Nghiệm Thu (ACs)
Nội dung ngắn.
"""
    res = spec_validator.validate_proposal(proposal_content=truncated)
    assert res["status"] == "success"
    assert res["valid"] is False
    assert res["gate_status"] == "FAILED"
    assert res["errors_count"] >= 5
    rule_ids = [v["rule_id"] for v in res["violations"]]
    assert any("SPEC-001" in r for r in rule_ids)


def test_validate_proposal_self_approval_violation():
    """Verify that autonomous self-approval (APPROVED_BY_SPEC) is strictly rejected."""
    bad_proposal = SAMPLE_VALID_PROPOSAL.replace(
        "PENDING_REVIEW",
        "APPROVED_BY_SPEC",
    )
    res = spec_validator.validate_proposal(proposal_content=bad_proposal)
    assert res["valid"] is False
    assert any("SPEC-002" in v["rule_id"] for v in res["violations"])
    assert any("APPROVED_BY_SPEC" in v["message"] for v in res["violations"])


def test_validate_proposal_horizontal_views_only_violation():
    """Verify that proposals only defining unstructured views/ are rejected."""
    bad_proposal = SAMPLE_VALID_PROPOSAL.replace(
        "lib/modules/auth/", "lib/modules/auth/views/"
    )
    bad_proposal = bad_proposal.replace("AuthSessionEntity", "AuthViewData")
    bad_proposal = bad_proposal.replace("OtpChallengeEntity", "OtpViewData")
    bad_proposal = bad_proposal.replace("LoginWithPasswordUseCase", "LoginViewHelper")
    bad_proposal = bad_proposal.replace("VerifyOtpUseCase", "OtpViewHelper")
    bad_proposal = bad_proposal.replace("Entity", "Item")
    bad_proposal = bad_proposal.replace("UseCase", "Helper")

    res = spec_validator.validate_proposal(proposal_content=bad_proposal)
    assert res["valid"] is False
    rule_ids = [v["rule_id"] for v in res["violations"]]
    assert any("SPEC-003" in r for r in rule_ids)


def test_validate_proposal_missing_multi_screen_axis():
    """Verify that missing one of the 6 multi-screen axes is flagged."""
    incomplete = SAMPLE_VALID_PROPOSAL.replace(
        "- **Vòng Đời Điều Hướng & Nút Quay Lại (Navigation Lifecycle & Back Button)**: popUntil về màn Login khi reset pass thành công.",
        "- **Vòng Đời**: Đang cập nhật.",
    )
    res = spec_validator.validate_proposal(proposal_content=incomplete)
    assert res["valid"] is False
    assert any("SPEC-004-AXIS-2" in v["rule_id"] for v in res["violations"])


def test_validate_plan_success():
    """Verify that a compliant vertical slice plan and task list passes."""
    res = spec_validator.validate_plan(
        plan_content=SAMPLE_VALID_PLAN,
        task_content=SAMPLE_VALID_TASKS,
        feature_name="auth",
    )
    assert res["status"] == "success"
    assert res["valid"] is True
    assert res["gate_status"] == "PASSED"
    assert res["errors_count"] == 0


def test_validate_plan_horizontal_ui_slice_rejected():
    """Verify that horizontal UI slices are rejected."""
    bad_plan = """# Kế Hoạch Triển Khai
## Lát Cắt 02: Vẽ Màn Hình Đăng Nhập
- Tác động: `lib/modules/auth/views/login_screen.dart`, `lib/modules/auth/views/register_screen.dart`
"""
    res = spec_validator.validate_plan(
        plan_content=bad_plan,
        task_content="- [ ] **Task 01**: Vẽ màn hình\n  - Depends on: None\n  - READY khi: Ok\n  - Files: `lib/modules/auth/views/login_screen.dart`\n  - Lệnh kiểm tra: `flutter test`\n",
    )
    assert res["valid"] is False
    assert any("PLAN-001" in v["rule_id"] for v in res["violations"])


def test_validate_plan_bare_tasks_rejected():
    """Verify that 1-line bare checkbox tasks lacking metadata are rejected."""
    bad_tasks = """# Tasks
- [ ] Task 01: Xây dựng Màn hình Đăng nhập (UIT-01)
- [ ] Task 02: Xây dựng Màn hình Quên mật khẩu (UIT-03)
"""
    res = spec_validator.validate_plan(
        plan_content=SAMPLE_VALID_PLAN,
        task_content=bad_tasks,
    )
    assert res["valid"] is False
    assert any("PLAN-002" in v["rule_id"] for v in res["violations"])


def test_validate_plan_missing_testing_mandate():
    """Verify that plans with no automated tests are rejected."""
    no_test_tasks = SAMPLE_VALID_TASKS.replace("flutter test", "echo skip test").replace(".dart", ".dart")
    res = spec_validator.validate_plan(
        plan_content=SAMPLE_VALID_PLAN.replace("test/", "docs/"),
        task_content=no_test_tasks.replace("test/", "docs/").replace("_test.dart", ".dart"),
    )
    assert res["valid"] is False
    assert any("PLAN-003" in v["rule_id"] for v in res["violations"])


SPEC_WRITER_CODEBASE_NOTES = """# Codebase Notes: Versioned Spec Writer
- **Document Type:** `CODEBASE_NOTES`
- **Work Item:** `spec_writer`
- **Feature:** `planning/spec_writer`
- **Type:** `feature`
- **Version:** `v1`
- **Status:** `PENDING_REVIEW`
- **Created:** `2026-10-06`
- **Updated:** `2026-10-06`
- **Grill-Me Rounds:** `2`
- **Related Docs:** `requirements.md` | `design.md` | `implementation-plan.md`

## 0. Question Queue (Q-NN)
| ID | Status (`OPEN` \\| `CLOSED -> D-NN`) | Dimension | Question / Inference to Confirm | Recommended Option |
|---|---|---|---|---|
| **Q-01** | `CLOSED -> D-01` | Scope | How should requirements and context be split? | Unified `requirements.md` + `codebase-notes.md` |
| **Q-02** | `CLOSED -> D-02` | Architecture | Where should versioned artifacts live? | `docs/features/<module>/<feature>/vN/` |

## 1. Decision Log (D-NN)
| ID | Round | Dimension | Question Asked | Options Considered | User Confirmed Decision | Impacted `BR` / `AC` / Design | Owner |
|---|---|---|---|---|---|---|---|
| **D-01** | R1 | Scope | How should requirements and context be split? | 1. (Recommended) Unified `requirements.md` + `codebase-notes.md`<br>2. Separate `brief.md` | Unified `requirements.md` + `codebase-notes.md` | `BR-01`, `AC-01` | `spec_writer` |
| **D-02** | R2 | Architecture | Where should versioned artifacts live? | 1. (Recommended) `docs/features/<module>/<feature>/vN/`<br>2. Global `.agents/plan/` | `docs/features/<module>/<feature>/vN/` | `design.md` | `planning` |

## 2. Glossary
| Business / UX Term | Technical Equivalent | Notes |
|---|---|---|
| Gate 1 Spec | `requirements.md` + `codebase-notes.md` | Confirmed at Gate 1 |

## 3. Verified Baseline Facts & Cross-Agent Notes
- Existing plugin agents live under `plugins/coder-nexus-fe/agents/`.

## 4. Constraints & External Integrations
- Backend API Integration Status: `NONE` (workflow specification only).

## 5. Extended Rule Details
- `BR-01`: Every business rule must cite a confirmed `D-NN` entry in `codebase-notes.md`.

## 6. Change Log
| Date | Role | Summary |
|---|---|---|
| 2026-10-06 | `spec_writer` | Completed Gate 1 `grilling` rounds and locked in `D-01`..`D-02`. |
"""


SPEC_WRITER_REQUIREMENTS = """# Requirements: Versioned Spec Writer
> **Document type**: REQUIREMENTS
> **Feature**: planning/spec_writer
> **Version**: v1
> **Created**: 2026-10-06
> **Source references**: User decision in this conversation, 2026-10-06 (`D-01`)
> **Context file**: `codebase-notes.md`
> **Status**: PENDING_REVIEW
> **Approval reference**: NONE

## 0. Goals
| Goal ID | Goal (outcome) | Success signal | Source | Status |
|---|---|---|---|---|
| G-01 | Each feature keeps its own approved spec without collisions | Two features keep separate requirements files after both are approved | User decision 2026-10-06 (D-01) | CONFIRMED |

## 1. Scope & Alignment
- **Current baseline & problem**: Global spec files collide across features.
- **Scope in**: Discover requirements, design, and plan in three stages (`D-01`).
- **Scope out**: No Flutter production code during specification.

## 2. Actors & Permissions
Developer approves each stage; the Hub reads Huly only.

## 3. Business Rules
| Rule ID | Business Rule Description | Goal | Decision Ref |
|---|---|---|---|
| **BR-01** | Developer confirms requirements and `codebase-notes.md` before design begins. | G-01 | `D-01` |

## 4. Behavioral Scenarios
- **Given** a new feature request, **When** `spec_writer` runs `grilling`, **Then** each open `Q-NN` is asked one at a time and locked into `D-NN` (`AC-01`, `D-01`).

## 5. Acceptance criteria
| AC ID | Observable behavior | Source | Status | Goal |
|---|---|---|---|---|
| AC-01 | Developer confirms requirements before design begins | USER_CONFIRMED 2026-10-06 (D-01) | VERIFIED | G-01 |

## 6. Gate 1 approval
- **Decision summary**: Awaiting confirmation for this document revision.
- **Approved response**: NONE
- **Approved document revision**: NONE
"""


def test_requirements_accept_confirmed_user_source_without_huly():
    result = spec_validator.validate_proposal(proposal_content=SPEC_WRITER_REQUIREMENTS)
    assert result["valid"] is True
    assert result["document_type"] == "REQUIREMENTS"


def test_codebase_notes_validation_and_open_question_rejection():
    valid_res = spec_validator.validate_proposal(proposal_content=SPEC_WRITER_CODEBASE_NOTES)
    assert valid_res["valid"] is True
    assert valid_res["document_type"] == "CODEBASE_NOTES"

    open_q_content = SPEC_WRITER_CODEBASE_NOTES.replace("`CLOSED -> D-01`", "`OPEN`")
    bad_res = spec_validator.validate_proposal(proposal_content=open_q_content)
    assert bad_res["valid"] is False
    assert any(item["rule_id"] == "NOTES-003-OPEN-Q" for item in bad_res["violations"])


def test_requirements_reject_missing_ac_source():
    content = SPEC_WRITER_REQUIREMENTS.replace("USER_CONFIRMED 2026-10-06 (D-01)", "NONE")
    result = spec_validator.validate_proposal(proposal_content=content)
    assert result["valid"] is False
    assert any(item["rule_id"] == "REQ-004-AC-SOURCE" for item in result["violations"])


def test_requirements_reject_unresolved_options_or_open_questions_section():
    with_option = SPEC_WRITER_REQUIREMENTS + "\n### Option A\nDo X.\n### Option B\nDo Y.\n"
    result = spec_validator.validate_proposal(proposal_content=with_option)
    assert result["valid"] is False
    assert any("UNRESOLVED-OPTIONS" in item["rule_id"] for item in result["violations"])


def test_requirements_cross_checks_sibling_codebase_notes(tmp_path):
    version_dir = tmp_path / "v1"
    version_dir.mkdir()
    req_path = version_dir / "requirements.md"
    req_path.write_text(SPEC_WRITER_REQUIREMENTS, encoding="utf-8")
    missing_notes = spec_validator.validate_proposal(proposal_path=str(req_path))
    assert missing_notes["valid"] is False
    assert any(item["rule_id"] == "NOTES-000-MISSING" for item in missing_notes["violations"])

    notes_path = version_dir / "codebase-notes.md"
    notes_path.write_text(SPEC_WRITER_CODEBASE_NOTES, encoding="utf-8")
    valid_pair = spec_validator.validate_proposal(proposal_path=str(req_path))
    assert valid_pair["valid"] is True


def test_v2_requirements_require_prior_change_impact(tmp_path):
    version_dir = tmp_path / "v2"
    version_dir.mkdir()
    (version_dir / "codebase-notes.md").write_text(
        SPEC_WRITER_CODEBASE_NOTES.replace("`v1`", "`v2`"), encoding="utf-8"
    )
    requirements_path = version_dir / "requirements.md"
    requirements_path.write_text(SPEC_WRITER_REQUIREMENTS.replace("v1", "v2"), encoding="utf-8")
    result = spec_validator.validate_proposal(proposal_path=str(requirements_path))
    assert result["valid"] is False
    assert any(item["rule_id"] == "IMPACT-001-MISSING" for item in result["violations"])


SPEC_WRITER_DESIGN = """# Design: Versioned Spec Writer
> **Document type**: DESIGN
> **Feature**: planning/spec_writer
> **Version**: v1
> **Created**: 2026-10-06
> **Source references**: Approved design discussion on 2026-10-06 (`D-02`)
> **Status**: PENDING_REVIEW
> **Approval reference**: NONE
- **Requirements reference**: [requirements.md](requirements.md)
- **Context reference**: [codebase-notes.md](codebase-notes.md)
- **Gate 1 approval reference**: User confirmation on 2026-10-06
- **Scope classification**: EXTEND

## Architectural decision
- **Confirmed architecture (`D-02`)**: Use a stable feature folder and `v1`/`v2` subfolders while retaining `codebase-notes.md` permanently across the version lifecycle.

## Module and folder diff
- **Current structure and owners**: `.agents/brainstorm/` and `.agents/plan/` are global.
- **Proposed structure and owners**: `docs/features/<module>/<feature>/vN/` owns the version documents.
- **Cross-module and shared consumers**: Agent profiles and plugin skills use this path.
## Behavior, data, and state
Requirements, design, and plan each require the developer's confirmation.
## UI design system
N/A: this change modifies the agent workflow, not Flutter UI.
## Integration, errors, and risks
Existing Client artifacts remain legacy and do not imply approval.
## Verification strategy
Check every gate and the versioned handoff with real Client input.
## Gate 2 approval
Awaiting developer review of this design revision.
"""


def test_design_accepts_verified_workflow_change_without_speculative_classes():
    result = spec_validator.validate_proposal(proposal_content=SPEC_WRITER_DESIGN)
    assert result["valid"] is True
    assert result["document_type"] == "DESIGN"


def test_design_rejects_option_a_option_b_headings():
    bad_design = SPEC_WRITER_DESIGN + "\n### Option A\nKeep old global plan.\n### Option B\nUse versioned folders.\n"
    result = spec_validator.validate_proposal(proposal_content=bad_design)
    assert result["valid"] is False
    assert any("UNRESOLVED-OPTIONS" in item["rule_id"] for item in result["violations"])


def test_design_rejects_agent_approval_marker():
    result = spec_validator.validate_proposal(
        proposal_content=SPEC_WRITER_DESIGN.replace("PENDING_REVIEW", "APPROVED_BY_SPEC")
    )
    assert result["valid"] is False
    assert any(item["rule_id"] == "DESIGN-004-SELF-APPROVAL" for item in result["violations"])


VERSIONED_PHASE = """# PHASE-01: Requirements approval
> **Document type**: PHASE
> **Feature**: planning/spec_writer
> **Version**: v1
> **Created**: 2026-10-06
> **Source references**: requirements.md and design.md
> **Status**: PENDING_REVIEW
> **Approval reference**: NONE
- **Phase ID**: PHASE-01
- **Behavior**: Developer confirms requirements before design begins.
- **AC IDs**: AC-01
- **Depends on**: None
- **READY when**: Gate 1 has a source-backed requirements draft.
- **Files**: plugins/coder-nexus/agents/spec_writer.md
- **Owner**: Spec Writer coordinator
- **Verification**: dart analyze on the approved Flutter Client revision.
- **UI impact**: NO — agent workflow only.
- **Visual target/states**: N/A — no Flutter UI change.
## Code direction
Use the existing ask_question tool and preserve Huly read-only behavior.
## Design system source
N/A — no Flutter UI change.
## Done when
The actual user approves the requirements revision before design begins.
## Risks
The agent must not record its own approval as user consent.
"""


VERSIONED_PLAN = """# Implementation Plan: Versioned Spec Writer
> **Document type**: IMPLEMENTATION_PLAN
> **Feature**: planning/spec_writer
> **Version**: v1
> **Created**: 2026-10-06
> **Source references**: requirements.md and design.md
> **Status**: PENDING_REVIEW
> **Approval reference**: NONE
- **Gate 1 approval reference**: User confirmation on 2026-10-06
- **Gate 2 approval reference**: User design approval on 2026-10-06
## AC coverage
| AC ID | Phase ID | Verification evidence required |
|---|---|---|
| AC-01 | PHASE-01 | User response for this revision |
## Phase order
| Phase ID | Behavioral outcome | Phase file | Depends on | Owner |
|---|---|---|---|---|
| PHASE-01 | Requirements approval | [phase-01-requirements.md](phases/phase-01-requirements.md) | None | Spec Writer |
## Checkpoints and shared files
Spec Writer owns the approval handoff before implementation.
## Test and visual strategy
Run the approved analyzer and check user response provenance.
## Gate 3 approval
Awaiting user approval of this plan and its phase file.
"""


def test_versioned_plan_checks_linked_phase_and_ac_coverage(tmp_path):
    version_dir = tmp_path / "v1"
    phase_dir = version_dir / "phases"
    phase_dir.mkdir(parents=True)
    (version_dir / "codebase-notes.md").write_text(SPEC_WRITER_CODEBASE_NOTES, encoding="utf-8")
    (version_dir / "requirements.md").write_text(SPEC_WRITER_REQUIREMENTS, encoding="utf-8")
    (version_dir / "design.md").write_text(SPEC_WRITER_DESIGN, encoding="utf-8")
    (phase_dir / "phase-01-requirements.md").write_text(VERSIONED_PHASE, encoding="utf-8")
    plan_path = version_dir / "implementation-plan.md"
    plan_path.write_text(VERSIONED_PLAN, encoding="utf-8")

    result = spec_validator.validate_plan(plan_path=str(plan_path))
    assert result["valid"] is True
    assert result["document_type"] == "IMPLEMENTATION_PLAN"


def test_versioned_plan_rejects_phase_link_outside_version(tmp_path):
    version_dir = tmp_path / "v1"
    version_dir.mkdir()
    plan_path = version_dir / "implementation-plan.md"
    plan_path.write_text(
        VERSIONED_PLAN.replace("phases/phase-01-requirements.md", "../outside.md"),
        encoding="utf-8",
    )

    result = spec_validator.validate_plan(plan_path=str(plan_path))
    assert result["valid"] is False
    assert any(item["rule_id"] == "PLAN-V-007-TRAVERSAL" for item in result["violations"])


# ---------------------------------------------------------------- Goals (REQ-005 / DESIGN-007 / PLAN-V-010)

def _violation_ids(result):
    return {v["rule_id"] for v in result["violations"]}


def test_requirements_without_goals_are_rejected():
    no_goals = SPEC_WRITER_REQUIREMENTS.split("## 0. Goals")[0] + "## 1. Scope & Alignment" + SPEC_WRITER_REQUIREMENTS.split("## 1. Scope & Alignment", 1)[1]
    result = spec_validator.validate_proposal(proposal_content=no_goals)
    assert result["valid"] is False
    assert "REQ-005-NO-GOALS" in _violation_ids(result)


def test_goal_must_be_user_confirmed():
    unconfirmed = SPEC_WRITER_REQUIREMENTS.replace("(D-01) | CONFIRMED |", "(agent inference) | PROPOSED |")
    result = spec_validator.validate_proposal(proposal_content=unconfirmed)
    assert "REQ-005-GOAL-ROW" in _violation_ids(result)


def test_ac_and_br_must_serve_a_goal():
    orphan = SPEC_WRITER_REQUIREMENTS.replace("| VERIFIED | G-01 |", "| VERIFIED | — |").replace("| G-01 | `D-01` |", "| — | `D-01` |")
    ids = _violation_ids(spec_validator.validate_proposal(proposal_content=orphan))
    assert {"REQ-005-AC-GOAL", "REQ-005-BR-GOAL", "REQ-005-GOAL-UNCOVERED"} <= ids


def test_ac_citing_unknown_goal_is_rejected():
    bad = SPEC_WRITER_REQUIREMENTS.replace("| VERIFIED | G-01 |", "| VERIFIED | G-09 |")
    assert "REQ-005-AC-GOAL" in _violation_ids(spec_validator.validate_proposal(proposal_content=bad))


def test_design_must_align_with_every_goal(tmp_path):
    (tmp_path / "requirements.md").write_text(SPEC_WRITER_REQUIREMENTS, encoding="utf-8")
    design_path = tmp_path / "design.md"
    design_path.write_text("> **Document type**: DESIGN\n", encoding="utf-8")
    result = spec_validator.validate_proposal(
        proposal_content="> **Document type**: DESIGN\n> **Feature**: a/b\n> **Version**: v1\n> **Status**: PENDING_REVIEW\n",
        proposal_path=str(design_path),
    )
    assert "DESIGN-007-GOALS" in _violation_ids(result)
    aligned = spec_validator.validate_proposal(
        proposal_content="> **Document type**: DESIGN\n> **Feature**: a/b\n> **Version**: v1\n> **Status**: PENDING_REVIEW\n\n## Goal alignment\n| Goal | Delivered by |\n|---|---|\n| G-01 | Versioned docs folder per feature |\n",
        proposal_path=str(design_path),
    )
    assert "DESIGN-007-GOALS" not in _violation_ids(aligned)


def test_plan_must_deliver_every_goal(tmp_path):
    version_dir = tmp_path / "v1"
    phase_dir = version_dir / "phases"
    phase_dir.mkdir(parents=True)
    two_goals = SPEC_WRITER_REQUIREMENTS.replace(
        "| CONFIRMED |\n\n## 1.",
        "| CONFIRMED |\n| G-02 | Reviewers see one source of truth | Reviewer opens one versioned folder | User decision 2026-10-06 (D-01) | CONFIRMED |\n\n## 1.",
    ).replace(
        "| VERIFIED | G-01 |",
        "| VERIFIED | G-01 |\n| AC-02 | Reviewer opens one folder | USER_CONFIRMED 2026-10-06 (D-01) | PENDING | G-02 |",
    )
    (version_dir / "codebase-notes.md").write_text(SPEC_WRITER_CODEBASE_NOTES, encoding="utf-8")
    (version_dir / "requirements.md").write_text(two_goals, encoding="utf-8")
    (version_dir / "design.md").write_text(SPEC_WRITER_DESIGN, encoding="utf-8")
    (phase_dir / "phase-01-requirements.md").write_text(VERSIONED_PHASE, encoding="utf-8")
    plan_path = version_dir / "implementation-plan.md"
    plan_path.write_text(VERSIONED_PLAN, encoding="utf-8")
    ids = _violation_ids(spec_validator.validate_plan(plan_path=str(plan_path)))
    assert "PLAN-V-010-GOAL-COVERAGE" in ids


# ---------------------------------------------------------------- UI/UX design (REQ-006 / DESIGN-008)

UIUX_MD = """# UI/UX: Docs — v1

> **Document type**: UIUX
> **Revision**: r2
> **Status**: {status}

## 4. Workflows

| Workflow | Title | Goals | Steps |
|---|---|---|---|
| W-01 | Open docs | G-01 | 1→S01, 2→S02 |
| W-02 | Share docs | G-01 | 1→S01 |

## 5. Screens

| Screen | Title | File | Catalog | Kind | Steps | States | Kit classes | New components |
|---|---|---|---|---|---|---|---|---|
| S01 | Home | screens/S01-home.html | app.home | EXISTING | W-01#1, W-02#1 | default | | |
| S02 | Docs | screens/S02-docs.html | app.docs | NEW | W-01#2 | default | | C01 |

## 6. New components

| Component | Title | File | Used in | Why not in the kit |
|---|---|---|---|---|
| C01 | Folder tree | components/C01-tree.html | S02 | no tree in the kit |
"""


def _write_uiux(version_dir, status="APPROVED"):
    (version_dir / "design-uiux").mkdir(parents=True, exist_ok=True)
    (version_dir / "design-uiux" / "uiux.md").write_text(UIUX_MD.format(status=status), encoding="utf-8")


def test_requirements_must_map_approved_ui_workflows(tmp_path):
    req_path = tmp_path / "requirements.md"
    (tmp_path / "codebase-notes.md").write_text(SPEC_WRITER_CODEBASE_NOTES, encoding="utf-8")
    req_path.write_text(SPEC_WRITER_REQUIREMENTS, encoding="utf-8")
    baseline = _violation_ids(spec_validator.validate_proposal(proposal_path=str(req_path)))
    assert not any(rule.startswith("REQ-006") for rule in baseline), "no design-uiux/: rule does not apply"

    _write_uiux(tmp_path, status="IN_REVIEW")
    ids = _violation_ids(spec_validator.validate_proposal(proposal_path=str(req_path)))
    assert {"REQ-006-UIUX-NOT-APPROVED", "REQ-006-NO-WORKFLOWS"} <= ids

    _write_uiux(tmp_path)
    partial = SPEC_WRITER_REQUIREMENTS.replace(
        "## 1. Scope", "## Workflows\n\n| Workflow | Goal | Steps → screens | Scenarios / AC |\n|---|---|---|---|\n| W-01 | G-01 | 1→S01, 2→S02 | AC-01 |\n\n## 1. Scope", 1)
    req_path.write_text(partial, encoding="utf-8")
    result = spec_validator.validate_proposal(proposal_path=str(req_path))
    assert any(v["rule_id"] == "REQ-006-WORKFLOW-MISSING" and "W-02" in v["message"] for v in result["violations"])
    assert "REQ-006-UIUX-NOT-APPROVED" not in _violation_ids(result)
    assert "REQ-006" in result["checked_rules"]

    req_path.write_text(partial.replace("| AC-01 |\n\n## 1. Scope", "| AC-01 |\n| W-02 | G-01 | 1→S01 | AC-01 |\n\n## 1. Scope"), encoding="utf-8")
    assert not any(r.startswith("REQ-006") for r in _violation_ids(spec_validator.validate_proposal(proposal_path=str(req_path))))


def test_design_must_map_ui_screens_and_new_components(tmp_path):
    (tmp_path / "requirements.md").write_text(SPEC_WRITER_REQUIREMENTS, encoding="utf-8")
    design_path = tmp_path / "design.md"
    design_path.write_text("> **Document type**: DESIGN\n", encoding="utf-8")
    head = "> **Document type**: DESIGN\n> **Feature**: a/b\n> **Version**: v1\n> **Status**: PENDING_REVIEW\n"
    _write_uiux(tmp_path)
    result = spec_validator.validate_proposal(proposal_content=head, proposal_path=str(design_path))
    assert "DESIGN-008-NO-MAPPING" in _violation_ids(result) and "DESIGN-008" in result["checked_rules"]

    mapping = "\n## UI/UX mapping\n\n| Screen / component | Kind | Destination | Kit | Phase |\n|---|---|---|---|---|\n| S02 | NEW | DocsScreen /docs | app-list → List | PHASE-01 |\n"
    result = spec_validator.validate_proposal(proposal_content=head + mapping, proposal_path=str(design_path))
    unmapped = [v["message"] for v in result["violations"] if v["rule_id"] == "DESIGN-008-UNMAPPED"]
    assert unmapped and ("C01" in unmapped[0] or "C-01" in unmapped[0]) and "S01" not in unmapped[0] and "S-01" not in unmapped[0], "EXISTING screens need no mapping"

    full = mapping + "| C01 | NEW COMPONENT | widgets/folder_tree | app-list-item | PHASE-02 task 3 |\n"
    assert not any(r.startswith("DESIGN-008") for r in _violation_ids(
        spec_validator.validate_proposal(proposal_content=head + full, proposal_path=str(design_path))))

    _write_uiux(tmp_path, status="DRAFT")
    assert "DESIGN-008-UIUX-NOT-APPROVED" in _violation_ids(
        spec_validator.validate_proposal(proposal_content=head + full, proposal_path=str(design_path)))


def test_figma_intake_screens_and_workflows_validation_without_design_uiux(tmp_path):
    req_path = tmp_path / "requirements.md"
    (tmp_path / "codebase-notes.md").write_text(SPEC_WRITER_CODEBASE_NOTES, encoding="utf-8")

    # 1. Non-EXISTING S-NN in ## Screens & Visual Sources without ## Workflows triggers REQ-006-NO-WORKFLOWS
    req_with_screens_only = SPEC_WRITER_REQUIREMENTS.replace(
        "## 1. Scope",
        "## Screens & Visual Sources\n\n| Screen ID | Screen Name | Status | Visual Source | Notes |\n|---|---|---|---|---|\n| S-01 | Login | EXISTING | lib/modules/auth/login_screen.dart | — |\n| S-02 | Work Order List | NEW | Figma 1150:10051 (work-orders.spec.json, work-orders-S02.png) | 1440x900 |\n\n## 1. Scope",
        1,
    )
    req_path.write_text(req_with_screens_only, encoding="utf-8")
    res_no_wf = spec_validator.validate_proposal(proposal_path=str(req_path))
    assert "REQ-006-NO-WORKFLOWS" in _violation_ids(res_no_wf)

    # 2. ## Workflows referencing S-02 and G-01 and AC-01 passes REQ-006
    req_complete = req_with_screens_only.replace(
        "## 1. Scope",
        "## Workflows\n\n| Workflow | Goal | Steps → screens | Scenarios / AC |\n|---|---|---|---|\n| W-01 | G-01 | 1. Login (`S-01`) -> 2. View list (`S-02`) | `AC-01` |\n\n## 1. Scope",
        1,
    )
    req_path.write_text(req_complete, encoding="utf-8")
    res_ok = spec_validator.validate_proposal(proposal_path=str(req_path))
    assert not any(r.startswith("REQ-006") for r in _violation_ids(res_ok))

    # 3. design.md must map S-02 (NEW) in ## UI/UX mapping even without design-uiux/
    design_path = tmp_path / "design.md"
    head = "> **Document type**: DESIGN\n> **Feature**: a/b\n> **Version**: v1\n> **Status**: PENDING_REVIEW\n"
    design_path.write_text(head, encoding="utf-8")
    res_design_missing = spec_validator.validate_proposal(proposal_content=head, proposal_path=str(design_path))
    assert "DESIGN-008-NO-MAPPING" in _violation_ids(res_design_missing)

    mapping = "\n## UI/UX mapping\n\n| Screen / component | Kind | Destination | Kit | Phase |\n|---|---|---|---|---|\n| S-02 | NEW | WorkOrderListScreen /work-orders | AppScaffold, AppDataTable | PHASE-01 |\n"
    res_design_ok = spec_validator.validate_proposal(proposal_content=head + mapping, proposal_path=str(design_path))
    assert not any(r.startswith("DESIGN-008") for r in _violation_ids(res_design_ok))
