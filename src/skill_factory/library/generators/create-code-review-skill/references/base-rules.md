# Base Rules (Mandatory Across Every Workspace)

Generalised from Coder Nexus `plugins/core/agents/code_reviewer.md`, `review-workflow`, and the stack `code-review` rubrics. Every rule `R1`–`R14` is mandatory compliance and is adapted to the workspace's stack, validators, commands, and report location.

## 1. Mandatory Code Review Rules (`R1`–`R14`)

| # | Rule | Why | Goes into |
|---|---|---|---|
| **R1** | **Review a fixed revision.** Record `BASE_REVISION` and `REVIEW_REVISION` plus the full uncommitted scope of the item; review exactly that tree. | A verdict on a moving tree certifies code nobody reviewed. | `01` |
| **R2** | **Strictly read-only.** Never edit application code, tests, generated code, schemas, or dependencies; write only the review report. Any edit creates a new revision that invalidates evidence. | A reviewer who fixes code becomes the author and nobody reviews them. | `01` |
| **R3** | **Bug-hunt first, then compliance.** Run `bug-hunt` at `standard` (`deep` for high-risk or repeatedly returned items) cold from the code before reading design documents; then grade the rubric axes. | Reading intent first hides what the code actually does. | `SKILL.md`, `01` |
| **R4** | **Grade each applicable axis with the workspace's own rubric skill** (`clean-architecture`, `clean-code`, `code-simplification`, `unit-testing`, `secure-coding-standards`, plus domain/stack skills). | One standard for writer and reviewer ends subjective debates. | `02` |
| **R5** | **Trace acceptance criteria & prevent test tampering (`TEST-TAMPER-001`).** Every applicable AC maps to implementation and to an executable test or named check with evidence; deleting, skipping, or weakening assertions to pass is an automatic `BLOCKER`. | Untraced ACs and weakened assertions ship broken behavior. | `02` |
| **R6** | **Rerun the checks yourself.** Run validators, static analyzers, typecheckers, and the phase's test suite on `REVIEW_REVISION`; the writer's hand-off is a claim, not proof. `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` are never `PASS`. | Evidence produced on another tree or not run at all proves nothing. | `01`, `03` |
| **R7** | **No reviewer waivers.** The reviewer cannot excuse a rule or architecture violation, however convincing the technical argument; a genuine conflict with an approved plan/design is marked `PLAN_CONFLICT` and routed to planning/the user (`change-control`). | Waivers in reviews quietly rewrite the engineering standards. | `03` |
| **R8** | **Actionable findings.** Every finding states `ID` (`RV-NN`), `Pass`, `Severity` (`BLOCKER` / `MAJOR` / `MINOR`), `Confidence`, `File:line`, `Problem` (rule ID or defect first), `Evidence / scenario`, and `Fix direction` (what must change, not the replacement code). | Vague findings come back as questions and waste review rounds. | `03` |
| **R9** | **Scope discipline (diff + broken callers).** Review the changed files and any callers or module boundaries they break; pre-existing legacy debt outside the diff is recorded only as a non-blocking note. | Blocking on untouched legacy debt stalls delivery. | `01` |
| **R10** | **Verdict by explicit criteria.** `APPROVED` only when every re-run gate is `PASS`, every applicable AC is traced, `bug-hunt` left no `CONFIRMED` `BLOCKER`/`MAJOR`, no rubric `BLOCKER`/`MAJOR` remains, and UI/visual evidence passes when UI is affected. Otherwise `CHANGES_REQUESTED`, or `BLOCKED` when required evidence/environment is unavailable. | Explicit criteria make verdicts deterministic and reproducible. | `SKILL.md`, `03` |
| **R11** | **Three-round cap and escalation.** Cap review at 3 rounds per phase. If round 3 still does not reach `APPROVED`, stop and escalate with both positions stated (`change-control` for plan conflicts, user/coordinator otherwise). | Endless ping-pong wastes both roles. | `03` |
| **R12** | **No cosmetic blocking.** Require changes only for concrete rule violations or defects; pure refactoring/cleanup ideas without a rule breach or failure are listed as `NOTE` lines for `code-simplification`. | Cosmetic blocking erodes trust in real findings. | `03` |
| **R13** | **Revision-bound report.** Write the review report to the workspace's report location (`vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md`), recording revisions, re-run gate results, `bug-hunt` rows, axis assessments, findings, and verdict. | The report is the audit trail for the phase. | `03` |
| **R14** | **Delta re-review.** After a fix revision, inspect the delta (`previous REVIEW_REVISION..new REVIEW_REVISION`), verify each finding claimed closed, and re-run every affected gate and test on the new revision. | A fix can introduce regressions; old evidence never carries over. | `03` |

---

## 2. Unified Verification Gates & Severity Scale

- **Deterministic CLI & Validator Gates (`PASS` / `FAIL`):**
  - Every CLI check (analyzer, linter, typechecker, test runner, contract/migration check) is recorded as `PASS` or `FAIL` with its exact command and exit code.
  - `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`.
- **Unified Finding Severity Scale (`BLOCKER` / `MAJOR` / `MINOR`):**
  - Both defect findings (`bug-hunt`) and rubric compliance findings (`code-review`) use the single 3-tier scale:
    - `BLOCKER`: Architecture boundary violation (`ERROR`), broken AC, `TEST-TAMPER-001` (weakened/deleted tests or happy-path-only test suite missing mandatory error cases), security/auth/scope breach, schema/contract drift, or `CONFIRMED` `BLOCKER` defect.
    - `MAJOR`: Unresolved validator/analyzer warning that hides a real risk, missing negative/edge test case on changed behavior, resource/lifecycle leak, or `CONFIRMED` `MAJOR` defect.
    - `MINOR`: Localized non-critical rule deviation within the diff that does not threaten correctness, architecture boundaries, or security.
