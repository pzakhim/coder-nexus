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
1. **Start Spec Writer** with the request, supplied files and the Huly task ID (read once by `huly-task-intake`, read-only; downloads in `.superpowers/sources/<ISSUE-ID>/`). Web Standard (React/Next.js/Vue) is TODO — not yet maintained.
2. **API source** has three values, recorded in `codebase-notes.md`: `BE_API_READY` (spec from Huly BE task, Swagger/OpenAPI or `.md`), `MOCKOON_MOCKED` (spec_writer locks business Input/Output; Planning designs the mock and `PHASE-00`) or `NO_EXTERNAL_API` (`PHASE-00` pre-ticked `[x] PREPARED (NO_EXTERNAL_API)`). With `MOCKOON_MOCKED`, approved Mockoon fixtures support UI/contract checks only and live integration stays pending until a real endpoint is verified; the mock's file, rules and smoke checks belong to `{{slot:verification}}` and the stack part of the Planning and Code Writer profiles.
3. **Call Designer** when Spec Writer reports UI impact (Step 1A-UX); relay its `READY_FOR_SPEC` / `SKIPPED` / `BLOCKED` back to Spec Writer.
4. **Relay cross-agent questions** (Step 1C): a question about codebase internals or architecture goes to `planning` or `code_writer`, which answers with evidence in `codebase-notes.md` and stops; Spec Writer relays it. Never fabricate an answer.
5. **Gate 1**: accept it only after Spec Writer reports 0 `OPEN` `Q-NN`, validators run (`NOT_RUN` is not a pass), `gate-review` and `cold-reader-check` done, and the user explicitly approves the exact revisions (with the approved `uiux.md` revision). Stop until then.
6. **Verification item** (`READY_FOR_VERIFICATION`): skip Phases 2–3; call Test Runner on the named revision with the approved AC, and it writes findings to `verification.md`.
7. **Escalated bug** (from `defect-resolution`, status `ESCALATED`): pass `.superpowers/debug/<bug-slug>/escalation-report.md` to Spec Writer as a supplied source. Its reproduction, root cause and impact are evidence to re-check, not approved requirements. Spec Writer settles the job type: `bugfix` when behavior must be restored, `feature` with `change-impact.md` when it must change. The debug folder stays read-only.

---

## Phase 2 — Technical Architecture & Breakdown (`planning`)

Upon Gate 1 approval, call **Planning** (Tech Lead) for Gate 2 (design) and Gate 3 (plan):

1. **Step 2A — Codebase Scan & Pre-Design Counter-Review (`grilling` mode planning, `ask_question` in Main Chat)**:
   - Resolve and record the profile via `{{slot:core-package-usage}}`, start from `requirements.md` and `codebase-notes.md`, and inspect the target module, router, state and DI using the stack scan in `{{slot:architecture-design}}`. Company setup and package guides apply only to the company-foundation profile; other profiles inspect Client foundations or the framework's standard components.
   - **Strict Boundary with `spec_writer`**: `spec_writer` owns business API Input/Output and screen UX requirements (from design-export `.md`). `planning` owns Data Pipeline architecture (`DataSource`/`Model`/`Repo`/state holder/DI) and exact `{{slot:core-package-usage}}` class/component mapping.
   - **Hub-and-Spoke Counter-Review Protocol (Before writing `design.md`)**:
     - The User interacts **exclusively in the Main Chat**; never require the user to switch between subagent conversations.
     - **Step 1 (Detect)**: If `planning` discovers a **Core Risk / Core Gap**, overlapping/conflicting logic with `requirements.md`, or trade-offs between viable approaches/widgets, `planning` queues `Q-NN` (`OPEN`) in `.superpowers/work-items/<slug>/vN/codebase-notes.md` and reports it to the Coordinator instead of writing `Option A / Option B` into `design.md`.
     - **Step 2 (Internal Alignment via Coordinator)**: The Coordinator relays the technical finding to `spec_writer` (via `send_message` or targeted invocation) so `spec_writer` evaluates business/UX impact and aligns with `planning` on 2–3 viable options built with `solution-options` (including one clear `(Recommended)` choice).
     - **Step 3 (Single User Prompt in Main Chat)**: The Coordinator (or active lead agent) presents one `ask_question` modal at a time in the **Main Chat** summarizing both the technical and business perspectives with the `(Recommended)` option. Once the user decides, `Q-NN` is closed into `D-NN` in `codebase-notes.md`, `spec_writer` updates `requirements.md` if business rules changed, and `planning` proceeds to write a straight-line `design.md` citing `D-NN`.
2. **Step 2B — API source strategy (`BE_API_READY` / `MOCKOON_MOCKED` / `NO_EXTERNAL_API`)**:
   - When the API is mocked, `planning` designs the mock and its test-data table in `design.md` and allocates **`PHASE-00` (`phase-00-prepare.md`)** to prepare it before feature phases (`PHASE-01`+) integrate through the real remote data access; the stack steps are in `{{slot:verification}}` and the Planning profile's stack part. Feature phases never add fake data sources to the Client source.
   - **Zero Cross-Repo Mutation**: Strictly prohibit tasks that modify Backend repositories, server code, or database schemas.
3. **Step 2C — Gate 2 (Straight-Line `design.md` Approval), Permanent `codebase-notes.md` Retention, then Sequential Phase & Task Breakdown**:
   - Write `design.md` as a single-track, straight-line forward blueprint citing `D-NN` in `codebase-notes.md` (zero `Option A / Option B` headings, zero `Open Questions`, zero `TBD`). Validate `codebase-notes.md` and `design.md` with `validate_proposal_spec`, then `gate-review` (mode design) and `cold-reader-check` (Gate 2); 0 `OPEN` `Q-NN` before the gate. Present the exact `design.md` revision, including profile/evidence, reuse mapping, API contract and fixture/live verification split. Obtain actual user approval at **Gate 2** before drafting the execution plan.
   - After Gate 2, Planning may offer `architecture-decision-records` for hard-to-reverse `D-NN` (optional, user-confirmed).
   - **Retain `codebase-notes.md` Permanently**: Keep `.superpowers/work-items/<slug>/vN/codebase-notes.md` permanently throughout the entire `vN/` lifecycle so `code_writer`, `code_reviewer`, `test_runner`, and `docs_writer` can reference the full Decision Log (`D-NN`), Glossary, and Verified Baseline Facts.
   - Slice the feature into **`PHASE-00` (`phases/phase-00-prepare.md`)** followed by **sequential vertical behavior phases** (`phases/phase-01-<behavior>.md`, `phase-02-<behavior>.md`...), where each phase is a self-contained sub-feature and its verified output feeds the next phase.
   - Within each phase, break work into an **ordered list of sequential micro-tasks** (`- [ ] **Task X.Y**`) without parallel/sequential track tags or join points.
   - Define **Review Acceptance Criteria (DoD for Code Review)**: Explicitly specify required developer unit tests (UseCases, Mappers, state holders) and zero-error static analysis.
   - **Strict Boundary**: Planning defines *technical architecture and review criteria*; Planning does NOT dictate QA user-acceptance test cases (QA test design belongs independently to Test Runner).
4. **Step 2D — Gate 3 (User Negotiation & Plan Freeze)**:
   - Before presenting: `validate_plan_slices` → `gate-review` (mode plan) → `cold-reader-check` (Gate 3), with 0 `OPEN` `Q-NN`.
   - Present `implementation-plan.md` and all linked phase files via `ask_question` with 3 clear options:
     1. `[Approve Plan & Proceed to Build]`: Record `APPROVED_FOR_BUILD` (specs and plan frozen); Planning returns `READY_FOR_BUILD` naming the first executable phase, and you assign one `code_writer`.
     2. `[Refine Technical Decisions]`: Adjust task order, mock approach, or scaffolding directly in Planning.
     3. `[Modify Business Scope / Requirements]`: Route back to Spec Writer to revise requirements before replanning.

---

## Phase 3 — Disciplined Delivery Loop (Phase-by-Phase, Sequential)

Execute approved ready phases in strict sequential order (`PHASE-01` $\to$ `PHASE-02` $\to$ ...), one phase at a time. This loop is strictly comprised of the **3 implementation & review roles**:

### Step 1: Implementation (`code_writer`)
- Coordinator assigns the current ready phase (with approved `brief.md`, `requirements.md`, `design.md`, `implementation-plan.md` and `phases/phase-NN-*.md`) to **one `code_writer` instance**. The Code Writer follows `incremental-implementation`: tasks strictly in order, each check triaged against its **Expected** (`MATCH` / `CODE_WRONG` / `PLAN_WRONG`), phase checks via `{{slot:verification}}`, a self `{{slot:bug-hunt}}`, and the hand-off at `vN/evidence/<phase-id>/<REVIEW_REVISION>/writer-handoff.md`. Do not restate or reorder that loop here.
- `PHASE-00 [EXECUTE]` prepares and smoke-tests what the stack rules say (`{{slot:verification}}`) and the Code Writer ticks it before hand-off; feature phases integrate only the real remote data access, never fake data sources in the Client source and never Backend files.
- The Code Writer returns `READY_FOR_REVIEW` (optional Concerns), `BLOCKED` or `NEEDS_CONTEXT`; route each as in **Routing** below.

### Step 2: Independent Code Review (`code_reviewer`)
- The Reviewer follows `review-workflow` on the exact `BASE_REVISION..REVIEW_REVISION`, read-only, re-running the hand-off's checks and AC commands, and writes `vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md`.
- Verdict `APPROVED` → Step 3 (Docs Writer) on the same tree; the Test Runner waits for Phase 4. `CHANGES_REQUESTED` → back to the same Code Writer with finding IDs and the round number (`review-resolution`). `BLOCKED` → resolve the named blocker before re-assigning.
- Every fix is a new revision; review and test evidence for the touched code no longer counts.

### Step 3: Evidence Recording & Handoff Preparation (`docs_writer`)
- Records actual code/test revisions, evidence rows, command provenance and the review report link into `as-built.md`.
- Drafts reader-facing docs if required by phase scope.
- Prepares the next-phase handoff contract in `as-built.md` before user checkpoint, then returns `RECORDED` (or `BLOCKED`); row shape in `handoff-and-status.md` §8.

### Routing (coordinator only)
Formats and status words: `work-item-contract` → `handoff-and-status.md`. All hand-offs go through you; no agent starts another.

| Returned | Your move |
|---|---|
| `NEEDS_CONTEXT` | Add exactly what was asked (from the approved documents or a relayed question), then re-assign. Never re-assign unchanged. |
| `BLOCKED` (environment, approval, external dependency, branch) | Resolve it or ask the user; never let a role work around it. |
| `BLOCKED` naming a `PCR-NN`, or a `PLAN_CONFLICT` / `SCOPE_CHANGE` row in a review or test report | For a report row, write `plan-changes/PCR-NN.md` from it (the Reviewer and Test Runner stay read-only). Send the request to Planning (`change-control`). The Code Writer waits. `AMENDED` → re-assign the phase from the first affected task and list the new `## Plan change log` rows at the next phase checkpoint. `ESCALATED` → ask the user at once with the `Q-NN`; Gate 2 (`DESIGN_CHANGE`) or Gate 1 via Spec Writer (`SCOPE_CHANGE`) re-approves before work resumes. |
| `CHANGES_REQUESTED` (review) | Back to the Code Writer. **Cap: 3 review rounds on the same phase**; after the third, escalate: a plan cause goes to Planning as a `PCR-NN`, anything else to the user with both positions. Nobody waives a finding. |
| `FAIL` / `CHANGES_REQUESTED` (Test Runner) | Each failing case goes to the Code Writer under the phase that owns its AC (`## AC coverage`), with its evidence; the fix goes through review again (new revision), then Test Runner re-tests affected cases. The owning phase's 3-round cap counts (`handoff-and-status.md` §2, Test Runner defect). |
| A third `PCR-NN` on the same task | To the user, whatever its class. |

Verification path per revision: Code Writer evidence → Code Reviewer re-runs it (`APPROVED`) → Docs Writer records it (`RECORDED`) → after the last phase, Test Runner `quality-acceptance` (`final_qa`) on the approved revision → Docs Writer records the verdict. Order: `handoff-and-status.md` §2. `NOT_RUN`, `BLOCKED` and `UNVERIFIED` never become PASS, `APPROVED` or `ACCEPTED` at any step.

### Step 4: Coordinator User Checkpoint (`ask_question`)
- Summarizes completed phase results, unit test pass rate, UI provenance, and any `AMENDED` `## Plan change log` rows since the last checkpoint (one line each).
- Presents user checkpoint via `ask_question`:
  - Choice 1 (Recommended): Continue with named next phase.
  - Choice 2: Refine or inspect current phase evidence.
  - Choice 3: Pause work item.
- Stop work item as `BLOCKED — awaiting user continuation` until user explicitly confirms. Gate 3 does NOT authorize executing all phases in one batch.

---

## Phase 4 — Final Feature E2E QA Verification (`test_runner`)

Once ALL implementation phases in `implementation-plan.md` have been completed, reviewed, and recorded in `as-built.md`, call **Test Runner** once (`final_qa`) on the final `APPROVED` revision for a comprehensive End-to-End QA pass across the fully integrated feature; a phase the plan marks for its own acceptance run gets an extra run after that phase is recorded. It follows `quality-acceptance`; do not restate its steps here. What you check before accepting its report:

- **Independence**: the test-case matrix comes from `requirements.md` (BDD scenarios, AC table, `## 1.` **Scope in** / **Scope out**; `brief.md` for a phase-free item), `design.md` state matrix and the approved `uiux.md`, never from plan tasks; developer unit tests are not re-run as acceptance; an Out-of-Scope mutation fails verification.
- **Evidence**: rows under `.superpowers/work-items/<slug>/vN/evidence/final_qa/<revision>/` (stack targets from `{{slot:verification}}`), all 4 visual states for UI items, and the per-AC table defined in `quality-acceptance` → "Per-AC results".
- UI/contract checks and live integration checks are reported separately, with data provenance and contract/code revisions. Approved fixtures may pass their UI/contract checks; required live ACs stay `BLOCKED` or `NOT_RUN` until checked on the real endpoint. Never close a handshake using fixtures.
- **Verdict**: `ACCEPTED` only when every applicable AC is `PASS`. On `CHANGES_REQUESTED` (any `FAIL`), route each failure to the Code Writer under its owning phase as in **Routing**: `code_writer` -> `code_reviewer` -> `docs_writer` -> `test_runner` on the new revision. On `BLOCKED`, resolve the blocker first.

---

## Phase 5 — Final Handoff & Delivery Closure

Upon successful QA verification (`ACCEPTED`):
1. **Docs Writer Finalization**: Updates `as-built.md` with final QA matrix, terminal evidence links, and overall feature completion sign-off.
2. **Component Provenance Breakdown**:
   - **UI Kit Components**: Match the selected profile’s reuse mapping from `{{slot:core-package-usage}}` (company Core usage, Client Core Mapping, or standard components). Imports resolve in the Client.
   - **Client Shared / Composed Widgets**: Widgets reused from existing shared library.
   - **Feature-Private Widgets**: Custom widgets backed by approved design gap rationale.
3. Mark `UI: N/A` for non-visual work items. Keep summary strictly synchronized with `as-built.md`.
