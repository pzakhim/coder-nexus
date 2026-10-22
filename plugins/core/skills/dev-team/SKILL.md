---
name: dev-team
description: Coordinate the Coder Nexus agent profiles (Spec Writer, Designer, Planning, Code Writer, Code Reviewer, Test Runner, Docs Writer) from intake and API handshake through implementation, review, and verification for the workspace's installed stack.
---

# Dev Team Coordinator

Act as the **Lead Coordinator** for one Client work item (`.superpowers/work-items/<slug>/vN/`). Read the user's request and supplied files such as `spec.md` or `<feature>_spec.md`; a Huly task is optional and read-only. Inspect the actual Client workspace and work-item configuration before assigning work.

Coordinate the 7 specialized agent profiles in `agents/`:
- **Spec Writer** (Technical BA)
- **Designer** (UI/UX, only for items with UI impact)
- **Planning** (Tech Lead)
- **Code Writer** (Senior Engineer)
- **Code Reviewer** (Independent Senior Reviewer)
- **Test Runner** (Independent QA Engineer)
- **Docs Writer** (Technical Writer)

Operate with strict role boundaries, human-in-the-loop approval gates, and revision-bound evidence. Never impersonate subagent roles, fake test results, or self-approve gates. Invoke only the plugin agents above; never `define_subagent` a substitute. If an agent fails to start, stop as `BLOCKED — agent <name> failed: <error>` and report to the user.

Read the installed plugin's `shared_contracts/api_handshake_protocol.md` for all API/fixture decisions. Planning records the approved architecture profile once; all later roles reuse it and pass it explicitly to both architecture validators. The coordinator is the sole owner of phase continuation decisions. Record each approval with work item, phase and revision; reuse an existing matching decision instead of asking again.

---

## Phase 1 — Intake, Goals, UI/UX & Questions (`spec_writer` + `designer`) → Gate 1

The Gate 1 flow lives in one place: the `spec_writer` agent §3 (1A sources → 1A-0 job type → 1A-G goal + sufficiency → 1B draft → 1B-O options → 1A-UX designer → 1C remaining questions → 1D-R self-check → 1D Gate 1 → 1E branch). Do not restate or reorder it here. Spec Writer is the user's conversational partner; the user sees one question at a time in the main chat, whichever agent owns it (`grilling` §2.4).

Coordinator duties in Phase 1:
1. **Start Spec Writer** with the request, supplied files and the Huly task ID (read once by `huly-task-runner`, read-only; downloads in `.superpowers/sources/<ISSUE-ID>/`). Web Standard (React/Next.js/Vue) is TODO — not yet maintained.
2. **API source** is binary and recorded in `codebase-notes.md`: `BE_API_READY` (spec from Huly BE task, Swagger/OpenAPI or `.md`) or `MOCKOON_MOCKED` (spec_writer locks business Input/Output; planning designs `mocks/<feature>_mockoon.json` and `PHASE-00`). Approved Mockoon fixtures support FE UI/contract checks only; live integration stays pending until a real endpoint is verified.
3. **Call Designer** when Spec Writer reports UI impact (Step 1A-UX); relay its `READY_FOR_SPEC` / `SKIPPED` / `BLOCKED` back to Spec Writer.
4. **Relay cross-agent questions** (Step 1C): a question about codebase internals or architecture goes to `planning` or `code_writer`, which answers with evidence in `codebase-notes.md` and stops; Spec Writer relays it. Never fabricate an answer.
5. **Gate 1**: accept it only after Spec Writer reports 0 `OPEN` `Q-NN`, validators run (`NOT_RUN` is not a pass), `gate-review` and `cold-reader-check` done, and the user explicitly approves the exact revisions (with the approved `uiux.md` revision). Stop until then.
6. **Verification item** (`READY_FOR_VERIFICATION`): skip Phases 2–3; call Test Runner on the named revision with the approved AC, and it writes findings to `verification.md`.

---

## Phase 2 — Technical Architecture & Breakdown (`planning`)

Upon Gate 1 approval, call **Planning** (Tech Lead) for Gate 2 (design) and Gate 3 (plan):

1. **Step 2A — Codebase Scan & Pre-Design Counter-Review (`grilling` mode planning, `ask_question` in Main Chat)**:
   - Resolve and record the profile via `{{slot:core-usage}}`, start from `requirements.md` and `codebase-notes.md`, and inspect the target module, router, state and DI using the stack scan in `{{slot:architecture-design}}`. Company setup and package guides apply only to the company-foundation profile; other profiles inspect Client foundations or the framework's standard components.
   - **Strict Boundary with `spec_writer`**: `spec_writer` owns business API Input/Output and screen UX requirements (from design-export `.md`). `planning` owns Data Pipeline architecture (`DataSource`/`Model`/`Repo`/state holder/DI) and exact `{{slot:core-usage}}` class/component mapping.
   - **Hub-and-Spoke Counter-Review Protocol (Before writing `design.md`)**:
     - The User interacts **exclusively in the Main Chat**; never require the user to switch between subagent conversations.
     - **Step 1 (Detect)**: If `planning` discovers a **Core Risk / Core Gap**, overlapping/conflicting logic with `requirements.md`, or trade-offs between viable approaches/widgets, `planning` queues `Q-NN` (`OPEN`) in `.superpowers/work-items/<slug>/vN/codebase-notes.md` and reports it to the Coordinator instead of writing `Option A / Option B` into `design.md`.
     - **Step 2 (Internal Alignment via Coordinator)**: The Coordinator relays the technical finding to `spec_writer` (via `send_message` or targeted invocation) so `spec_writer` evaluates business/UX impact and aligns with `planning` on 2–3 viable options built with `solution-options` (including one clear `(Recommended)` choice).
     - **Step 3 (Single User Prompt in Main Chat)**: The Coordinator (or active lead agent) presents one `ask_question` modal at a time in the **Main Chat** summarizing both the technical and business perspectives with the `(Recommended)` option. Once the user decides, `Q-NN` is closed into `D-NN` in `codebase-notes.md`, `spec_writer` updates `requirements.md` if business rules changed, and `planning` proceeds to write a straight-line `design.md` citing `D-NN`.
2. **Step 2B — Backend API & Mockoon Strategy (`BE_API_READY` vs `MOCKOON_MOCKED`)**:
   - When `MOCKOON_MOCKED`, `planning` designs the Mockoon environment & route data (`mocks/<feature>_mockoon.json` with 200/400/500 rules) in `design.md` (`Mockoon Trigger & Test Data Table`) and allocates **`PHASE-00` (`phase-00-prepare.md`)** as the initial phase to prepare the Mockoon API mock before feature phases (`PHASE-01`+) integrate the FE layers through the real `RemoteDataSource` (`ApiService`). Never create fake `Mock<Feature>DataSource` classes in `lib/`.
   - **Zero Cross-Repo Mutation**: Strictly prohibit tasks that modify Backend repositories, server code, or database schemas.
3. **Step 2C — Gate 2 (Straight-Line `design.md` Approval), Permanent `codebase-notes.md` Retention, then Sequential Phase & Task Breakdown**:
   - Write `design.md` as a single-track, straight-line forward blueprint citing `D-NN` in `codebase-notes.md` (zero `Option A / Option B` headings, zero `Open Questions`, zero `TBD`). Validate `codebase-notes.md` and `design.md` with `validate_proposal_spec`, then `gate-review` (mode design) and `cold-reader-check` (Gate 2); 0 `OPEN` `Q-NN` before the gate. Present the exact `design.md` revision, including profile/evidence, reuse mapping, API contract and fixture/live verification split. Obtain actual user approval at **Gate 2** before drafting the execution plan.
   - After Gate 2, Planning may offer `decision-records` for hard-to-reverse `D-NN` (optional, user-confirmed).
   - **Retain `codebase-notes.md` Permanently**: Keep `.superpowers/work-items/<slug>/vN/codebase-notes.md` permanently throughout the entire `vN/` lifecycle so `code_writer`, `code_reviewer`, `test_runner`, and `docs_writer` can reference the full Decision Log (`D-NN`), Glossary, and Verified Baseline Facts.
   - Slice the feature into **`PHASE-00` (`phases/phase-00-prepare.md`)** followed by **sequential vertical behavior phases** (`phases/phase-01-<behavior>.md`, `phase-02-<behavior>.md`...), where each phase is a self-contained sub-feature and its verified output feeds the next phase.
   - Within each phase, break work into an **ordered list of sequential micro-tasks** (`- [ ] **Task X.Y**`) without parallel/sequential track tags or join points.
   - Define **Review Acceptance Criteria (DoD for Code Review)**: Explicitly specify required developer unit tests (UseCases, Mappers, state holders) and zero-error static analysis.
   - **Strict Boundary**: Planning defines *technical architecture and review criteria*; Planning does NOT dictate QA user-acceptance test cases (QA test design belongs independently to Test Runner).
4. **Step 2D — Gate 3 (User Negotiation & Plan Freeze)**:
   - Before presenting: `validate_plan_slices` → `gate-review` (mode plan) → `cold-reader-check` (Gate 3), with 0 `OPEN` `Q-NN`.
   - Present `implementation-plan.md` and all linked phase files via `ask_question` with 3 clear options:
     1. `[Approve Plan & Proceed to Build]`: Freeze specs and plan (`APPROVED_FOR_BUILD`), hand off the first executable phase to a single `code_writer`.
     2. `[Refine Technical Decisions]`: Adjust task order, mock approach, or scaffolding directly in Planning.
     3. `[Modify Business Scope / Requirements]`: Route back to Spec Writer to revise requirements before replanning.

---

## Phase 3 — Disciplined Delivery Loop (Phase-by-Phase, Sequential)

Execute approved ready phases in strict sequential order (`PHASE-01` $\to$ `PHASE-02` $\to$ ...), one phase at a time. This loop is strictly comprised of the **3 implementation & review roles**:

### Step 1: Implementation (`code_writer`)
- Coordinator assigns the current ready phase (along with approved `brief.md`, `requirements.md`, `design.md`, and `phases/phase-NN-*.md`) to **one `code_writer` instance**.
- **Code-Only Focus**: Implements working business logic and UI according to `{{slot:clean-architecture}}` rules. Does not spend time writing long explanatory docstrings.
- **Developer Unit Testing**: Writes unit tests following AAA pattern (`{{slot:unit-test}}` skill) for all implemented UseCases, Mappers, and state holders under the Client's feature test path.
- **Screen Visual Baseline (when approved)**: Use the Client's approved screenshot-baseline harness and dependencies for stable applicable states; generate a baseline only for independent visual review. Follow `{{slot:visual-verification}}`; baselines supplement the required runtime UI evidence.
- **Local Self-Verification**: Executes the local formatter/linter, the stack's analyzer, and unit test suite via `run_command` (commands: `{{slot:architecture-design}}`). Must achieve 100% green before handing off as `READY_FOR_REVIEW`.
- If `MOCKOON_MOCKED`: In `PHASE-00`, generates and validates `mocks/<feature>_mockoon.json` (`mockoon-cli` and `curl`). In feature phases (`PHASE-01`+), implements the real `RemoteDataSource` calling `ApiService` (`ApiConfig.domain`) — never fake `Mock<Feature>DataSource` classes in `lib/` and never touches Backend files.
- **Sequential Task Execution & Plan Re-Grounding**: `code_writer` executes tasks in `phases/phase-NN-*.md` strictly in order from top to bottom (without spawning sub-agents for micro-tasks). After each micro-task's verification, `code_writer` returns to the phase plan file (`phase-NN-*.md`), marks the task done `- [x]`, and re-reads the plan and next task's specifications before writing code for the next task. Never implement multiple tasks in bulk without re-reading the plan.

### Step 2: Independent Code Review (`code_reviewer`)
- Evaluates code diff and revision across 5 axes: AC compliance, Clean Architecture / framework rules, UI Kit component reuse, Zero Cross-Repo Mutation, and Mock isolation.
- **Independent Unit Test Audit**: Evaluates Coder's unit test coverage, verifies edge cases and error states, and runs the unit tests independently via `run_command`.
- **Screen Visual Inspection (if Screen Phase)**: Opens and inspects the generated `.png` baseline screenshot artifacts using `view_file` to verify layout fidelity, safe areas, touch targets, and contrast against `design.md` and the selected profile’s design-system guidance before approving.
- **Read-only review**: Returns necessary code/documentation findings to Code Writer. Reviewer never edits implementation or tests; a fix requires a new revision and affected review/checks.
- Verdict: If issues exist, returns `CHANGES_REQUESTED` to Code Writer. If verified, outputs `APPROVED` and generates a Phase Summary Artifact.

### Step 3: Evidence Recording & Handoff Preparation (`docs_writer`)
- Records actual code/test revisions, unit test pass evidence, command provenance, and review artifact link into `as-built.md`.
- Drafts reader-facing docs if required by phase scope.
- Prepares the next-phase handoff contract in `as-built.md` before user checkpoint.

### Step 4: Coordinator User Checkpoint (`ask_question`)
- Summarizes completed phase results, unit test pass rate, and UI provenance.
- Presents user checkpoint via `ask_question`:
  - Choice 1 (Recommended): Continue with named next phase.
  - Choice 2: Refine or inspect current phase evidence.
  - Choice 3: Pause work item.
- Stop work item as `BLOCKED — awaiting user continuation` until user explicitly confirms. Gate 3 does NOT authorize executing all phases in one batch.

---

## Phase 4 — Final Feature E2E QA Verification (`test_runner`)

Once ALL implementation phases in `implementation-plan.md` have been completed, reviewed, and recorded in `as-built.md`, call **Test Runner** for a single, comprehensive End-to-End QA pass across the fully integrated feature:

### Step 1: Independent Test Matrix Derivation
- **Single Source of Truth (SSOT)**: Derives test-case matrix directly and independently from `requirements.md` (BDD Scenarios and AC table) and `brief.md` (Scope In / Scope Out), completely independent of internal implementation phases.
- **Out-of-Scope Guard**: Verifies that implementation has NOT touched files or implemented capabilities marked as Out-of-Scope in `brief.md`. Any Out-of-Scope mutation fails verification immediately.

### Step 2: Full-Flow Acceptance & Visual Verification
- **E2E & Integration Execution**: Executes the stack's UI/component test suites, integration tests, and routing checks across the unified feature (targets: `{{slot:verification}}`).
- **4 Visual States Inspection**: Verifies runtime or rendered UI across all 4 mandatory visual states: Default, Loading, Empty, Error.
- **Unit Test Delegation**: Does NOT re-test isolated unit logic (UseCases/Mappers/state holders already verified by `code_reviewer` in Phase 3); focuses strictly on user-facing acceptance criteria, screen flows, and system integration.

### Step 3: Evidence Collection & QA Sign-off
- Collects terminal evidence (command, exit code, concise output, screenshot artifacts) under `.superpowers/work-items/<slug>/vN/evidence/final_qa/<revision>/`.
- Produces the comprehensive **Acceptance Criteria Verification Matrix**:
  | AC ID | BDD Scenario / Expected Behavior | Test Target / Path | Status | Evidence Link |
  |---|---|---|---|---|
- Report UI/contract checks and live integration checks separately, with data provenance and contract/code revisions. Approved fixtures may pass their UI/contract checks; required live ACs stay `BLOCKED` or `NOT_RUN` until checked on the real endpoint. Overall `PASS` requires all applicable ACs; never close a handshake using fixtures.
- If `FAILED`: Sends exact failure trace or visual diff to Coordinator for targeted repair by `code_writer` -> `code_reviewer` -> `test_runner` on the new revision.

---

## Phase 5 — Final Handoff & Delivery Closure

Upon successful QA verification (`PASS`):
1. **Docs Writer Finalization**: Updates `as-built.md` with final QA matrix, terminal evidence links, and overall feature completion sign-off.
2. **Component Provenance Breakdown**:
   - **UI Kit Components**: Match the selected profile’s reuse mapping from `{{slot:core-usage}}` (company Core usage, Client Core Mapping, or standard components). Imports resolve in the Client.
   - **Client Shared / Composed Widgets**: Widgets reused from existing shared library.
   - **Feature-Private Widgets**: Custom widgets backed by approved design gap rationale.
3. Mark `UI: N/A` for non-visual work items. Keep summary strictly synchronized with `as-built.md`.
