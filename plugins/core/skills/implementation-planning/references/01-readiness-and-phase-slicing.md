# 01 — Codebase Readiness, PHASE-00 & Vertical Phase Slicing

> Topic: 3-input readiness verification, Huly sub-issue re-cutting, mandatory `PHASE-00` API & Mockoon strategy, vertical behavior slicing (`PHASE-01`+), and Gate 1 on-demand consultation.

## 1. Three Input Verification & Codebase Readiness Scan

Before formulating `implementation-plan.md` or any phase file, `planning` must verify three complete inputs:
1. **Gate 1 Approval (Requirements, Screens & Workflows)**: Actual user approval of `requirements.md` and `codebase-notes.md` (or `brief.md` for phase-free items).
2. **Gate 2 Approval (Architecture & Design System)**: Actual user approval of `design.md` (authored via `{{slot:architecture-design}}`), with `0 OPEN Q-NN` remaining in `codebase-notes.md`.
3. **Codebase Readiness Scan (4-Area Stack Checklist)**: Verify what exists vs what must be built by consulting `codebase-notes.md` (`## 3. Verified Baseline Facts & Cross-Agent Notes`) and the codebase-scan guidance in `{{slot:verification}}` and `{{slot:architecture-design}}`:
   - **Foundation & UI kit**: Confirm the resolved architecture/foundation profile via `{{slot:architecture-design}}`. Only a failed setup required by the active profile blocks on foundation dependencies; never invent missing package APIs.
   - **Routing & Screen Registry**: Inspect the repository's router configuration. If a route definition is missing for a new or modified screen, include registration inside the phase task that delivers that screen.
   - **State Management & DI**: Confirm the repository's active state-holder and dependency-injection conventions.
   - **Reuse before build**: Follow the `Core usage` / component mapping table in `design.md`: reuse a fitting foundation/core API first, else an existing target-module component, else a shared workspace folder only when two or more modules need it.

---

## 2. Huly Sub-Issues as Planning Input

When a work item originates from a Huly parent issue, its sub-issues are **planning input**, not a 1:1 phase list:
- Sub-issues are frequently split horizontally by role (e.g., API, UI, design) or author. Copying them 1:1 produces unobservable horizontal layers.
- Re-cut in-scope sub-issues into vertical behavior slices (`PHASE-01`, `PHASE-02`...) ordered by dependency and risk.
- Maintain traceability in `implementation-plan.md` (`| Huly ID | AC-NN | Phase |`): every in-scope child issue appears in at least one phase, and closed or out-of-scope children are recorded explicitly as out of scope in `codebase-notes.md`.

---

## 3. Mandatory `PHASE-00` (`phases/phase-00-prepare.md`) & API Strategy

Read plugin-root `shared_contracts/api_handshake_protocol.md`. **`PHASE-00` (`phases/phase-00-prepare.md`) is ALWAYS the prepare and readiness phase**; feature behavior phases ALWAYS start at **`PHASE-01`** (never label Mockoon or readiness preparation as `PHASE-01`).

1. **Single Home Per Fact (Link, Never Copy)**:
   - Huly task details and baseline codebase facts stay in `codebase-notes.md`.
   - External API contracts, endpoint schemas, and the `Mockoon Trigger & Test Data Table` stay in `design.md`.
   - `PHASE-00` links to `codebase-notes.md` and `design.md` and holds only readiness checks and preparation tasks so downstream agents (`code_writer`, `code_reviewer`, `test_runner`) never re-query Huly or read stale duplicated specs.
2. **Three API Readiness Modes**:
   - **`MOCKOON_MOCKED` (`[EXECUTE]`)**: When Backend endpoints do not yet exist or are incomplete, `PHASE-00` contains executable tasks for `code_writer` to create `mocks/<feature>_mockoon.json` implementing all agreed **Pass/Default** (`200`), **Empty** (`200`), and **Fail** (`400`/`422`/`500`) rules from `design.md`, boot `mockoon-cli`, and verify responses via `curl`. Before handing off `PHASE-00`, `code_writer` ticks **`[x] PREPARED / COMPLETED`** in both `phases/phase-00-prepare.md` and `implementation-plan.md`; `code_reviewer` inspects the evidence read-only and confirms the tick without editing plan files.
   - **`BE_API_READY` (`[INFO_NOTE]` or `[EXECUTE]` if live probe needed)**: Links the verified BE API contract in `design.md`. When no preparation command is needed, mark **`[INFO_NOTE]`** and pre-tick **`[x] PREPARED (INFO_READY)`**.
   - **`NO_EXTERNAL_API` (`[INFO_NOTE]`)**: When the feature has no external API dependency, omit the API section in `PHASE-00`, link `codebase-notes.md`, and pre-tick **`[x] PREPARED (NO_EXTERNAL_API)`**.
3. **Handshake & Zero Cross-Repo Mutation Guardrails**:
   - Explicitly approved contract-derived fixtures support UI and contract checks only; record fixture provenance and contract revision separately from live integration evidence. Required live ACs remain `BLOCKED` or `NOT_RUN` until exercised against the real endpoint.
   - In Client source code, always call the real remote data source wired to the configured API base URL — **never create fake mock data source classes, hardcoded fallback business records, or production success fallbacks in Client source**. Switching from Mockoon to live BE changes only `.env` configuration.
   - **Zero Cross-Repo Mutation**: Never plan tasks that modify another repository's server code, API handlers, or database schemas.

---

## 4. Vertical Behavior Phase Slicing (`PHASE-01`, `PHASE-02`...) & Phase File Contract

Each feature phase (`PHASE-01`, `PHASE-02`...) delivers **one user-observable or test-observable behavior** end to end, cutting vertically through only the layers that behavior requires.

**Self-check before writing a phase**: *"When this phase is done, what can I run or show that I could not before?"* If the answer is *"a class exists"* or *"the Domain/Data layer is done"*, it is a horizontal slice — re-cut it.

### Wrong (Horizontal Layer Slicing)

| Phase | Content | Observable? |
|---|---|---|
| `01` | Entities, repository contract, use cases | No |
| `02` | Models, data source, repository implementation, mocks | No |
| `03` | State holder, screen, components | Only now |

### Right (`PHASE-00` Prepare Phase + Vertical Behavior Phases)

| Phase | Mode (`[EXECUTE]` / `[INFO_NOTE]`) | Behavior / Readiness | Layers / Files Touched |
|---|---|---|---|
| `PHASE-00` (`phase-00-prepare.md`) | **`[EXECUTE]`** (if `MOCKOON_MOCKED`) or **`[INFO_NOTE]`** (if `BE_API_READY` / `NO_EXTERNAL_API`) | Link Huly context (`codebase-notes.md`) and API contract (`design.md`). If `MOCKOON_MOCKED`, create & verify `mocks/<feature>_mockoon.json`. Tick accepted readiness status when done. | `phases/phase-00-prepare.md`, `mocks/<feature>_mockoon.json` (if `MOCKOON_MOCKED`) |
| `PHASE-01` | `[EXECUTE]` | Walking skeleton: open screen and render `<feature>` list (Loading → Default content) | Entity + repo contract + remote data source/model/repo impl for list call + state holder + screen + route + DI + unit tests |
| `PHASE-02` | `[EXECUTE]` | Empty and error states with retry | State + screen visual states + state/widget tests; no new data layer code |
| `PHASE-03` | `[EXECUTE]` | Tap an item → detail screen | Detail call through required layers + detail screen + route + tests |
| `PHASE-04` | `[EXECUTE]` | Submit form action with validation errors | Write call + request model + form components + state action + tests |

### Slicing & Sequencing Rules
- **Strict Readiness Gate**: Feature phases (`PHASE-01`+) start only after `PHASE-00` carries one of the three accepted ticks defined in `work-item-contract` → `references/plan-and-task-contract.md` (`[x] PREPARED / COMPLETED`, `[x] PREPARED (INFO_READY)`, or `[x] PREPARED (NO_EXTERNAL_API)`).
- **Walking Skeleton in `PHASE-01`**: `PHASE-01` is thin but complete from API (or Mockoon HTTP server) to pixels/output, scheduled through the highest-risk integration (`02-task-structure-and-regrounding.md` §3).
- **No Placeholder Code**: Every phase file lists **only** the files that behavior needs. Never create empty classes, unused models, or dead DI registrations for later phases; shared pieces belong to the first phase that needs them and are extended by later phases.
- **UI-Only Phases Are Valid**: A phase that adds a layout refinement or new screen state without new Domain/Data work is a valid vertical slice.

### Phase File Contract (`validate_plan_slices` `PLAN-V-007`..`009`)
Every phase file under `phases/phase-NN-<behavior-slug>.md` is authored from `work-item-contract` → `templates/phase.md.tpl` and enforced by `validate_plan_slices`:
- Relative link under `phases/` that resolves to an existing file (`PLAN-V-007-NO-PHASES`, `PLAN-V-007-TRAVERSAL`, `PLAN-V-007-MISSING`).
- Header metadata: `Document type: PHASE` and `Version: vN` matching `implementation-plan.md` (`PLAN-V-008-VERSION`), with zero unfilled `{{...}}` placeholders (`PLAN-V-008-PLACEHOLDER`).
- Unique `Phase ID: PHASE-NN` (`PLAN-V-008-ID`), `Execution Mode` (`[EXECUTE]` or `[INFO_NOTE]`), and `Readiness / Completion Tick`.
- Mandatory metadata bullets (`PLAN-V-008-METADATA`): `Behavior`, `AC IDs` (`NONE (readiness phase)` for `PHASE-00`), `Goals`, `Depends on` (must reference only earlier declared phases or `NONE`; `PLAN-V-009-DEPENDENCY`), `READY when`, `Files`, `Owner`, `Verification`, `UI impact`, and `Visual target/states`.
- Mandatory body headings (`PLAN-V-008-SECTION`): `## Tasks`, `## Code direction`, `## Design system source`, `## Done when`, and `## Risks`.

---

## 5. On-Demand Consultation During Gate 1

Agents run only when the Coordinator invokes them; `planning` does not listen to `spec_writer` in the background.
1. **Focused Consult Call**: When `spec_writer` needs a verified codebase fact during Gate 1 (e.g., *"does module X exist?"*, *"does the UI kit provide a date-range picker?"*, *"is foundation setup READY?"*), the Coordinator invokes `planning` with that single question.
2. **Evidence-Backed Answer & Stop**: `planning` inspects the repository and foundation guides, appends the question, answer, and file/guide evidence path to `.superpowers/work-items/<slug>/vN/codebase-notes.md` (`## 3. Verified Baseline Facts & Cross-Agent Notes`), and stops immediately without drafting `design.md` or `implementation-plan.md` before Gate 1 is approved.
3. **Reuse at Gate 2 & Gate 3**: At Gate 2, `planning` starts from `codebase-notes.md` instead of re-scanning from scratch, keeping `codebase-notes.md` permanently across the `vN/` lifecycle.
