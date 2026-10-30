# E2E Test Plan: {{Title}} ({{Version}})

> **Document Type**: `TEST_PLAN`
> **Work Item**: `{{Slug}}`
> **Version**: `{{Version}}`
> **Status**: `PENDING_APPROVAL` <!-- PENDING_APPROVAL -> APPROVED -> IN_PROGRESS -> PASSED -->
> **Context**: [codebase-notes.md](codebase-notes.md)
> **Requirements Reference**: [requirements.md](requirements.md)
> **Technical Design Reference**: [design.md](design.md)
> **Implementation Plan Reference**: [implementation-plan.md](implementation-plan.md)
> **Approval Reference**: `NONE`

---

## 1. Execution & Anti-Test-Tampering Contract (Fail-Fast Loop: `test_runner` <-> `bug_fixer` <-> `planning`)

1. **Independent Real-Target Verification**:
   - Every `E2E-01..E2E-N` scenario below MUST be executed sequentially by `test_runner` on the approved reviewed revision using the stack's real verification and visual targets (`{{slot:verification}}` and `{{slot:visual-quality}}`).
   - Developer unit tests written by `code_writer` are graded during phase review and never substitute for `E2E-01..E2E-N` acceptance verification.
2. **Strict Anti-Test-Tampering Rule**:
   - Once `test-plan.md` is approved by the user at Gate 3, both `test_runner` and `bug_fixer` are **100% FORBIDDEN** from editing, weakening, skipping, or adding unapproved stubs/mocks to any `E2E-01..E2E-N` scenario to make a failing check pass.
3. **Sequential Execution & Fail-Fast Scenario Loop (`test_runner` <-> `bug_fixer` <-> `planning`)**:
   - `test_runner` executes scenarios sequentially from `E2E-01` to `E2E-N`, one scenario at a time.
   - When `E2E-i` passes, `test_runner` ticks `- [x] **E2E-i**`, records fresh observable evidence in `Evidence:`, and proceeds to `E2E-(i+1)`.
   - **If any `E2E-i` fails (`FAIL`)**: **`test_runner` STOPS IMMEDIATELY (`FAIL-FAST`)**, records the exact failure context (`FAILED_AT: E2E-i`, steps, expected vs. actual, logs/trace/visual diff, `AC-NN`, and owning phase) in `evidence/final_qa/<revision>/acceptance-report.md`, and returns **`CHANGES_REQUESTED` (`FAILED_AT: E2E-i`)**.
   - The Coordinator immediately invokes **`bug_fixer`** (Mode C — In-Flight E2E QA Bug Resolution) to trace the root cause (`{{slot:root-cause-debugging}}`, `{{slot:bug-hunt}}`) and either fix the `L1`/`L2` defect with a Red-to-Green regression test (`L1` -> `READY_FOR_TEST` -> `test_runner`; `L2` -> `READY_FOR_REVIEW` -> `code_reviewer` -> `test_runner`) or raise `plan-changes/PCR-NN.md` (`ESCALATED`) to **`planning`** (`change-control`) when `E2E-i` exposes an `L3` architectural, design, or plan flaw.
   - After the fix is committed (and approved by `code_reviewer` when `L2` or `L3`), `test_runner` **re-runs all scenarios from start to finish (`E2E-01` -> `E2E-N`)** until **100% of `E2E-01..E2E-N` pass end-to-end**.

---

## 2. `AC-NN` to `E2E-NN` Traceability Matrix

| AC ID | Owning Phase | Requirement Summary (`requirements.md`) | Scenario IDs (`E2E-NN`) | Verification Level & Target | Status |
|---|---|---|---|---|---|
| **AC-01** | `PHASE-01` | {{ac_01_summary}} | `E2E-01` | {{e2e_01_target_and_level}} | `PENDING` |
| **AC-02** | `PHASE-02` | {{ac_02_summary}} | `E2E-02` | {{e2e_02_target_and_level}} | `PENDING` |

---

## 3. Sequential E2E Scenarios (`E2E-01` .. `E2E-N` — Fail-Fast Checklist)

- [ ] **E2E-01 (`test_runner`)**: {{e2e_01_title}} (`AC-01` — Happy Path)
  - **Target AC & Owning Phase**: `AC-01` (`PHASE-01`)
  - **Severity & Level**: `BLOCKER` · `{{ui_or_api_or_visual}}`
  - **Preconditions & Data / Role**: `{{e2e_01_preconditions_seed_or_account}}`
  - **Sequential Steps / Actions**:
    1. `{{e2e_01_step_1}}`
    2. `{{e2e_01_step_2}}`
  - **Expected Observable Outcome & States**:
    - `{{e2e_01_expected_result_and_states}}`
  - **Check Command / Runtime Action (`cwd`)**: `{{e2e_01_command_or_runtime_check}}`
  - **Evidence**: `PENDING`

- [ ] **E2E-02 (`test_runner`)**: {{e2e_02_title}} (`AC-02` — Negative / Edge / Guard Flow)
  - **Target AC & Owning Phase**: `AC-02` (`PHASE-02`)
  - **Severity & Level**: `MAJOR` · `{{ui_or_api_or_visual}}`
  - **Preconditions & Data / Role**: `{{e2e_02_preconditions_seed_or_account}}`
  - **Sequential Steps / Actions**:
    1. `{{e2e_02_step_1}}`
    2. `{{e2e_02_step_2}}`
  - **Expected Observable Outcome & States**:
    - `{{e2e_02_expected_result_and_states}}`
  - **Check Command / Runtime Action (`cwd`)**: `{{e2e_02_command_or_runtime_check}}`
  - **Evidence**: `PENDING`

---

## 4. Stack Verification & Regression Gates (`{{slot:verification}}` & `{{slot:visual-quality}}`)

- [ ] **Gate 1 — Stack Analyzer & Automated Test Suite (`{{slot:verification}}`)**:
  - **Command**: `{{stack_verification_command}}`
  - **Evidence**: `PENDING`
- [ ] **Gate 2 — Runtime / Visual / Persistence Verification (`{{slot:verification}}` / `{{slot:visual-quality}}`)**:
  - **Command / Action**: `{{stack_runtime_or_visual_check}}`
  - **Evidence**: `PENDING`
