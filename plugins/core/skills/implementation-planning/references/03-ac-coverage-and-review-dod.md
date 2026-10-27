# 03 — AC Coverage Matrix, Review DoD & Gate 3 Verification

> Topic: 100% `AC-NN` / `G-NN` / UI-UX traceability (`PLAN-V-006`, `PLAN-V-010`), Tech Lead Review Definition of Done (DoD) vs independent QA, Pre-Gate 3 3-pass `gate-review`, and Gate 3 freeze & change control.

## 1. 100% `AC-NN`, `G-NN` & UI/UX Traceability (`PLAN-V-006`, `PLAN-V-010`)

Every Acceptance Criterion (`AC-01`, `AC-02`...) in `requirements.md` MUST be mapped to an owning behavior phase with a decisive, falsifiable check.

### `## AC coverage` Table Format (`work-item-contract` → `templates/implementation-plan.md.tpl`)
Use the exact 4-column table heading validated in `implementation-plan.md`, naming both the decisive check and the stack test path inside `Verification evidence required`:

```markdown
## AC coverage

| AC ID | Phase ID | Verification evidence required | Goal |
|---|---|---|---|
| AC-01 | PHASE-01 | Unit test validates DTO parsing and mapper (`<stack test path>/<feature>/data/mapper_test`) | G-01 |
| AC-02 | PHASE-02 | Component/widget test validates empty state rendered on empty list (`<stack test path>/<feature>/presentation/empty_test`) | G-01 |
| AC-03 | PHASE-03 | State test validates error state emitted on 400 failure (`<stack test path>/<feature>/presentation/state_test`) | G-02 |

Every confirmed goal in `requirements.md` → `## 0. Goals` is delivered by at least one phase (validator `PLAN-V-010`).
```

Use the stack's test path convention from `{{slot:unit-testing}}` and `{{slot:verification}}`.

### Strict Validator & Traceability Rules
1. **No Orphaned ACs (`PLAN-V-006-AC-COVERAGE`)**: Every `AC-NN` in `requirements.md` must appear in `## AC coverage` mapped to an existing `PHASE-NN` (`PHASE-01`+).
2. **Bidirectional Phase AC Sync (`PLAN-V-006-AC-MISMATCH`)**: Every `AC-NN` mapped to `PHASE-NN` in `implementation-plan.md` → `## AC coverage` **MUST also be listed in that phase file's `- **AC IDs**:` metadata bullet** (`phases/phase-NN-*.md`). Conversely, `PHASE-00` (`phases/phase-00-prepare.md`) is a readiness phase and sets `- **AC IDs**: NONE (readiness phase)`.
3. **100% Goal Delivery (`PLAN-V-010`)**: Every confirmed goal (`G-NN`) in `requirements.md` → `## 0. Goals` must be delivered by at least one phase through its mapped `AC-NN` items and listed in that phase file's `- **Goals**:` metadata bullet.
4. **Complete `BR-NN` & UI/UX Delivery (`gate-review` `P2`)**:
   - Every behavioral business rule (`BR-NN`) and decision (`D-NN`) must be implemented by an explicit task.
   - When UI is in scope, every mapped screen (`S-NN`, except `EXISTING`) and component (`C-NN`) in `design.md` → `## UI/UX mapping` must belong to a phase, and every `NEW COMPONENT` (`C-NN`) must have an explicit task built from the extracted Figma `.spec.json` / `tokens.json` contract recorded in `design.md`.

---

## 2. Tech Lead's Definition of Done (DoD) for Code Review vs Independent QA

Populate `## Test and visual strategy` in `implementation-plan.md` and `Verification` / `Done when` in each `phases/phase-NN-*.md` using the concrete commands from `{{slot:verification}}`, `{{slot:unit-testing}}`, and `{{slot:visual-quality}}`.

### Developer Review DoD (Required from `code_writer` Before `READY_FOR_REVIEW`)
1. **Static Analysis Gate (`PASS` / `FAIL`)**: The stack's analyzer/linter runs on affected paths with `0` errors, `0` warnings, and `0` lint violations (`PASS`).
2. **Developer Unit & State Tests (`{{slot:unit-testing}}`)**:
   - **Entity & Mapper tests**: Verify DTO-to-Entity transformation, boundary values, and null/default handling.
   - **UseCase / Service tests**: Verify business rule delegation and repository contract invocation.
   - **State-holder tests**: Verify the exact sequence of state emissions covering the agreed **Pass/Default**, **Empty**, and **Fail** test data defined in `design.md`.
3. **Screen Visual Review Gate (`{{slot:visual-quality}}`, Mandatory When `UI impact: Yes`)**:
   - Use a screenshot-comparison harness only when approved and already configured in the workspace (or when its dependency addition was explicitly approved in `D-NN`); screenshot evidence supplements runtime checks and never proves live API integration.
   - `code_writer` verifies the 4 mandatory visual states (**Default**, **Loading**, **Empty**, **Error**) and captures baseline/runtime visual evidence per `{{slot:visual-quality}}`.
   - `code_reviewer` inspects the rendered visual evidence against `design.md`, extracted Figma screen renders (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png` when present), and the active profile's design-system guidance before approving the phase.

### Strict Boundary: Developer Review DoD vs Independent QA (`test_runner`)
- **`planning` owns Developer Review DoD**: Specifies the static analysis checks, developer unit/state tests, and phase visual checks that `code_writer` must pass before `code_reviewer` approves a phase.
- **`test_runner` owns Independent QA Acceptance Testing**: After all phases pass code review (`ALL_PHASES_REVIEWED`), `test_runner` independently designs and runs E2E/acceptance verification directly from `requirements.md` and BDD scenarios. `planning` never dictates or limits `test_runner`'s independent QA test cases.

---

## 3. Pre-Gate 3 Self-Check, 3-Pass `gate-review` & Gate 3 Freeze Protocol

### Step 1 — 5-Item Author Self-Check
Before running `gate-review`, inspect `implementation-plan.md` and all `phases/phase-NN-*.md` files:
1. Every `AC-NN` in `requirements.md` is mapped in `## AC coverage`, listed in the target phase's `- **AC IDs**:` bullet, and backed by a building task + falsifiable check.
2. Every task's **Consumes** line matches an earlier **Produces** line (or existing codebase symbol) character for character.
3. Every `## Review focus` line names its owning task, and that task includes the verification check (or the section states `None found after checking every AC and BR`).
4. No task contains vague placeholders (`TBD`) or transcribed function bodies.
5. Phase order starts with `PHASE-00`, schedules highest risk first in `PHASE-01`, places prefactor tasks before new behavior inside a phase, and orders **Expand** before **Contract**.

### Step 2 — Mandatory 3-Pass `gate-review` (`modes/plan.md`)
Execute `gate-review` (`modes/plan.md`) in strict sequential order:
1. **Pass 1 — Deterministic Validator (`PASS` / `FAIL`)**: Run `validate_plan_slices(plan_path="...")` and resolve every `PLAN-V-001` through `PLAN-V-010` error until the tool returns `PASS`. (If the validator cannot run, report `NOT_RUN`, never `PASS`.)
2. **Pass 2 — Plan Checklist (`P1`–`P5`, `BLOCKER` / `MAJOR` / `MINOR`)**: Audit Interface Pre-Flight (`Produces` ↔ `Consumes`), complete `AC-NN` / `BR-NN` / `C-NN` delivery, plan proportion, global constraint value alignment, and falsifiable task checks. Fix all `BLOCKER` and `MAJOR` findings inline; queue any issue requiring a user decision as an `OPEN` `Q-NN` in `codebase-notes.md`.
3. **Pass 3 — Fresh Cold-Reader Subagent Check (Reader Plays `code_writer`)**: Spawn one fresh read-only subagent using the exact prompt in `gate-review` → `modes/plan.md` (`P6`). Triage every returned question (`Answered already`, `Minor — Agent's call` fixed inline, or `User's call — OPEN Q-NN` asked via `grilling` one question at a time and closed into `D-NN`).
- Present Gate 3 to the user **only when `0 OPEN Q-NN` remain**.

### Step 3 — Gate 3 User Negotiation (`ask_question`) & Post-Gate 3 Change Control
Present `implementation-plan.md` and linked `phases/` to the user via `ask_question` (opening with the `G-NN` goal recap and `gate-review` summary) with three response paths:
1. **`[Approve Plan & Proceed to Build]`**: User approves Gate 3 $\implies$ specs, design, and plan are frozen (`APPROVED_FOR_BUILD`). `planning` updates `Status: APPROVED` with the user's approval reference and returns `READY_FOR_BUILD` naming `PHASE-00` (when `PHASE-00` is `[EXECUTE]`) or `PHASE-01` (when `PHASE-00` is `[INFO_NOTE]` and already carries an accepted `[x] PREPARED (INFO_READY)` or `[x] PREPARED (NO_EXTERNAL_API)` tick).
2. **`[Refine Technical Decisions]`**: User requests adjustments to task order, Mockoon rules, or Review DoD $\implies$ `planning` updates `implementation-plan.md` / `phases/`, re-runs `validate_plan_slices`, and re-presents Gate 3 without routing back to `spec_writer`.
3. **`[Modify Business Scope / Requirements]`**: User alters business rules, goals, or ACs $\implies$ `planning` halts and routes back to `spec_writer` (Gate 1) so specs and plan never drift apart.

After Gate 3 approval, the plan may only change through `change-control` (`work-item-contract` → `references/plan-and-task-contract.md` §4–5): `planning` amends `TASK_DETAIL` items in place and logs a row in `## Plan change log`; any change touching a frozen item (`G-NN`, `AC-NN` → phase mapping, phase list/outcomes, `## Global constraints`, `## Review focus`, `D-NN`, or `design.md`) is escalated as `DESIGN_CHANGE` (Gate 2) or `SCOPE_CHANGE` (Gate 1).
