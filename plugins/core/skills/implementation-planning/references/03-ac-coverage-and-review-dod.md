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
   - When UI is in scope, every mapped screen (`S-NN`, except `EXISTING`) and component (`C-NN`) in `design.md` → `## UI/UX mapping` must belong to a phase, and every `NEW COMPONENT` (`C-NN`) must have an explicit task built from the extracted visual contract recorded in `design.md` (Figma `.spec.json` / `tokens.json` or HTML sitemap `sitemap/*.spec.json`).

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
   - `code_writer` verifies the 4 mandatory visual states (**Default**, **Loading**, **Empty**, **Error**), captures revision-bound screenshots under `evidence/<phase-id>/<REVIEW_REVISION>/visual/`, and lists them in `writer-handoff.md` (`Visual Artifacts:`) per `{{slot:visual-quality}}`.
   - `code_reviewer` visually inspects those screenshots via multimodal `read_file` on **every UI phase end and mid-phase `[REVIEW_CHECKPOINT]`** against `design.md`, extracted **Figma** (`figma/<stem>-SNN.png`) **or HTML sitemap** (`sitemap/screens/*.png`) renders, and the active profile's design-system guidance, recording `## Visual Comparison` before approving the phase.

### Master E2E Test Plan (`test-plan.md` at Gate 3), Hybrid E2E Choice & Fail-Fast Loop (`test_runner` ↔ `bug_fixer` ↔ `planning` → `code_writer`)
- **Developer Review DoD (`code_writer` & `code_reviewer`)**: Specifies the static analysis checks, developer unit/state tests (`{{slot:unit-testing}}`), and phase visual checks (`{{slot:visual-quality}}`) that `code_writer` must pass before `code_reviewer` approves each phase.
- **Hybrid E2E Planning Decision (Confirmed at Gate 3 Step 1, Frozen at Step 3)**: Explicitly decide and record in `implementation-plan.md` → `## Test and visual strategy` and `test-plan.md` whether the work item uses:
  1. **Live `E2E-01..E2E-N` only**: `test_runner` (strictly read-only) executes every `E2E-01..E2E-N` scenario live via Antigravity's builtin `browser` subagent / `chrome-devtools` MCP (web) or native simulator/emulator capture + multimodal `read_file` visual verification.
  2. **Live `E2E-01..E2E-N` + Optional Local `integration_test/`**: `planning` also schedules explicit `integration_test/` authoring tasks for `code_writer` inside the relevant phase(s); at `final_qa`, `test_runner` runs those existing `integration_test/` suites read-only AND executes live `E2E-01..E2E-N` flows.
- **Master E2E Test Plan (`vN/test-plan.md` at Gate 3)**: Alongside `implementation-plan.md` and `phases/`, `planning` authors `.superpowers/work-items/<slug>/vN/test-plan.md` from `work-item-contract` → `templates/e2e-test-plan.md.tpl`, defining sequential end-to-end scenarios (`- [ ] **E2E-01**` .. `- [ ] **E2E-N**`) covering 100% of `AC-NN` (Happy path, Negative/Validation, Permissions/Role, 4 Visual States / Data persistence, Out-of-Scope guards, and Workflow continuity `W-NN`) using the stack's verification ladder (`{{slot:verification}}` & `{{slot:visual-quality}}`).
- **Fail-Fast Scenario Loop & Anti-Test-Tampering Contract**:
  - Once approved at Gate 3, `E2E-01..E2E-N` in `test-plan.md` are frozen; neither `test_runner` nor `bug_fixer` may weaken, alter, or skip any scenario to force a pass.
  - In Phase 4 (`final_qa`), `test_runner` executes `E2E-01..E2E-N` sequentially one scenario at a time, ticking `- [x] **E2E-i**` on `PASS`.
  - On any `E2E-i` `FAIL`, `test_runner` stops immediately (`FAIL-FAST`, `CHANGES_REQUESTED` with `FAILED_AT: E2E-i`, writing `evidence/final_qa/<revision>/acceptance-report.md`) and invokes **`bug_fixer`** (Mode C): `L1` localized fixes return `READY_FOR_TEST` directly to `test_runner` (**max 3 rounds** before mandatory `L3` escalation); `L2` multi-file fixes go through `code_reviewer` (`APPROVED`) then `test_runner`; `L3` architectural/design/plan flaws raise `plan-changes/PCR-NN.md` (`ESCALATED`) to **`planning`** (`change-control`) to amend the plan, then **`code_writer`** implements the updated task(s), passes `code_reviewer`, and returns to `test_runner` for a full `E2E-01..E2E-N` re-run.

---

## 3. Pre-Gate 3 Self-Check, 3-Pass `gate-review` & Gate 3 Freeze Protocol

### Step 1 — 7-Item Author Self-Check
Before running `gate-review`, inspect `implementation-plan.md` and all `phases/phase-NN-*.md` files:
1. Every `AC-NN` in `requirements.md` is mapped in `## AC coverage`, listed in the target phase's `- **AC IDs**:` bullet, and backed by a building task + falsifiable check.
2. The high-level X-phase roadmap (`PHASE-00` + `PHASE-01..NN`, explicit `Scope in` / `Scope out`, and Hybrid E2E strategy) was locked in Gate 3 Step 1 before detailed phase authoring, any genuine cross-phase conflict, trade-off, or risk discovered during Step 2 detailing was resolved into `D-NN` in `codebase-notes.md`, and every feature phase (`PHASE-01`+) opens with `## Objective, approach & scope` containing `Why (Objective)`, `In-phase execution architecture & approach`, `Scope in`, `Scope out` (naming the owning `PHASE-NN`), `Cross-phase conflict & boundary check`, and `In-phase unit test plan`.
3. Zero scope overlap across phases: no behavior or deliverable in `PHASE-i`'s `Scope in` duplicates another phase's `Scope in`, and shared-file edits across phases are explicitly sequenced in `## Checkpoints and shared files` and `Cross-phase conflict & boundary check`.
4. Every logic-building task includes its developer unit test file in `Scope / Files` and runs named unit tests (`Happy/Pass`, `Negative/Fail`, `Edge/Empty`) in `Acceptance Criteria` + `Expected` (no standalone test-only tasks or deferred test phases); any scheduled local `integration_test/` files are explicitly listed in `Scope / Files`.
5. Every task's **Consumes** line matches an earlier **Produces** line (or existing codebase symbol) character for character.
6. Every `## Review focus` line names its owning task, and that task includes the verification check (or the section states `None found after checking every AC and BR`).
7. No task contains vague placeholders (`TBD`) or transcribed function bodies, and phase order starts with `PHASE-00`, schedules highest risk first in `PHASE-01`, places prefactor tasks before new behavior inside a phase, and orders **Expand** before **Contract**.

### Step 2 — Mandatory 3-Pass `gate-review` (`modes/plan.md`)
Execute `gate-review` (`modes/plan.md`) in strict sequential order:
1. **Pass 1 — Deterministic Validator (`PASS` / `FAIL`)**: Run `validate_plan_slices(plan_path="...")` and resolve every `PLAN-V-001` through `PLAN-V-010` error until the tool returns `PASS`. (If the validator cannot run, report `NOT_RUN`, never `PASS`.)
2. **Pass 2 — Plan Checklist (`P1`–`P5`, `BLOCKER` / `MAJOR` / `MINOR`)**: Audit Interface Pre-Flight (`Produces` ↔ `Consumes`), complete `AC-NN` / `BR-NN` / `C-NN` delivery, explicit `Scope in` / `Scope out` anti-overlap boundaries, mandatory in-phase unit tests, plan proportion, global constraint value alignment, and falsifiable task checks. Fix all `BLOCKER` and `MAJOR` findings inline; queue any issue requiring a user decision as an `OPEN` `Q-NN` in `codebase-notes.md`.
3. **Pass 3 — Fresh Cold-Reader Subagent Check (Reader Plays `code_writer`)**: Spawn one fresh read-only cold-reader via `invoke_subagent` (or a temporary `swarm{action:"add"}` helper if a swarm is active) using the exact prompt in `gate-review` → `modes/plan.md` (`P6`). Triage every returned question (`Answered already`, `Minor — Agent's call` fixed inline, or `User's call — OPEN Q-NN` asked via 2-Channel `grilling` and closed into `D-NN`).
- Present Gate 3 to the user **only when `0 OPEN Q-NN` remain**.

### Step 3 — Gate 3 Master Plan Report & Freeze (2-Channel `ask_question`)
When presenting Gate 3 (`implementation-plan.md`, linked `phases/`, and `test-plan.md`) to the user, output a structured **Gate 3 Master Plan Report** in **session chat (`content`)** before calling 1 short `ask_question`:
1. **Goal Recap & Overall Planning Strategy**: Confirmed `G-NN` goals, slicing & Hybrid E2E decisions (`D-NN`), and `gate-review` Pass 1–3 summary.
2. **Phase-by-Phase Breakdown Table**:
   ` | Phase ID | Why & Behavior (`AC-NN`) | Execution Architecture | Scope In | Scope Out (→ Owning Phase) | In-Phase Unit Tests | Cross-Phase Conflict Check | `
3. **Master E2E Test Plan Summary (`test-plan.md`)**: Overview of `E2E-01..E2E-N` scenarios and Hybrid E2E targets (live E2E + optional local `integration_test/`).

Then call 1 concise `ask_question` with three response paths (`(Recommended)` first):
1. **`(Recommended) Approve Plan & Proceed to Build`**: User approves Gate 3 $\implies$ specs, design, and plan are frozen (`APPROVED_FOR_BUILD`). `planning` updates `Status: APPROVED` with the user's approval reference and returns `READY_FOR_BUILD` naming `PHASE-00` (when `PHASE-00` is `[EXECUTE]`) or `PHASE-01` (when `PHASE-00` is `[INFO_NOTE]` and already carries an accepted `[x] PREPARED (INFO_READY)` or `[x] PREPARED (NO_EXTERNAL_API)` tick).
2. **`Refine Technical Decisions`**: User requests adjustments to task order, Mockoon rules, Hybrid E2E tasks, Review DoD, or `E2E-NN` scenarios $\implies$ `planning` updates `implementation-plan.md` / `phases/` / `test-plan.md`, re-runs `validate_plan_slices`, and re-presents Gate 3 without routing back to `spec_writer`.
3. **`Modify Business Scope / Requirements`**: User alters business rules, goals, or ACs $\implies$ `planning` halts and routes back to `spec_writer` (Gate 1) so specs and plan never drift apart.

After Gate 3 approval, the plan may only change through `change-control` (`work-item-contract` → `references/plan-and-task-contract.md` §4–5): `planning` amends `TASK_DETAIL` items in place and logs a row in `## Plan change log`; any change touching a frozen item (`G-NN`, `AC-NN` → phase mapping, phase list/outcomes, `## Global constraints`, `## Review focus`, `D-NN`, or `design.md`) is escalated as `DESIGN_CHANGE` (Gate 2) or `SCOPE_CHANGE` (Gate 1).
