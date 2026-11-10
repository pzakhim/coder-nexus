---
name: implementation-planning
description: "Converts approved versioned requirements and architecture design into an executable implementation plan and behavior phase files."
---

# Implementation Planning & Task Breakdown

Guides the **Tech Lead (`planning`)** in converting an approved `requirements.md` (Gate 1), `codebase-notes.md`, and `design.md` (Gate 2, authored via `{{slot:architecture-design}}`) into an executable `implementation-plan.md`, sequential phase files (`phases/phase-NN-*.md`), and the Master E2E Test Plan (`test-plan.md`, `E2E-01..E2E-N`) in `.superpowers/work-items/<slug>/vN/` (or `docs/features/<module>/<feature>/vN/`).

## 1. Input Verification & Readiness Gate

Before formulating tasks, confirm all three inputs ([`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §1):
1. **Gate 1 Approval**: User-approved `requirements.md` (including `## Screens & Visual Sources` and `## Workflows` when UI is in scope) and `codebase-notes.md`.
2. **Gate 2 Approval**: User-approved `design.md` (`0 OPEN Q-NN` in `codebase-notes.md`).
3. **Codebase Readiness Scan**: Verified 4-area stack readiness (foundation/UI kit, routing, state/DI, reuse mapping) via `{{slot:architecture-design}}` and `{{slot:verification}}`.

## 2. Interactive Phase-by-Phase Planning Protocol (Never Plan in a Silent Monologue)

1. **Step 1 — Master Phase Slicing Direction & Cross-Phase Conflict Alignment (`ask_question` Before Detailed Phase Planning)**:
   - Re-cut Huly sub-issues and approved specs into a proposed vertical behavior roadmap starting with `PHASE-00` (`phases/phase-00-prepare.md`) followed by `PHASE-01`, `PHASE-02`... (walking skeleton through highest risk first, never horizontal layers; [`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §2, §4).
   - **Ask the User for Planning Direction First**: Before writing out detailed phase files, present in the chat the proposed **Master Phase Slicing Strategy** (number of phases, order of phases, which `AC-NN` / `G-NN` each phase owns, preliminary `Scope in` vs `Scope out` per phase, and cross-phase shared-file/dependency analysis) and call `ask_question` with `(Recommended)` first so the user confirms or adjusts how the plan is sliced (`D-NN` in `codebase-notes.md`).
2. **Step 2 — Mandatory `PHASE-00` (`phases/phase-00-prepare.md` — Prepare & Readiness Phase)**:
   - Always begin with `PHASE-00` (`phases/phase-00-prepare.md`), using `work-item-contract` → `templates/phase.md.tpl` (`AC IDs: NONE (readiness phase)`).
   - **Single home per fact**: Link Huly context in `codebase-notes.md` and the BE API / Mockoon contract in `design.md` without copying them ([`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §3).
   - Classify `PHASE-00` by API mode (`MOCKOON_MOCKED` → `[EXECUTE]` creating and verifying `mocks/<feature>_mockoon.json`, ticked `[x] PREPARED / COMPLETED` by `code_writer` and confirmed read-only by `code_reviewer`; `BE_API_READY` → `[INFO_NOTE]` pre-ticked `[x] PREPARED (INFO_READY)` or `[EXECUTE]` if live probe needed; `NO_EXTERNAL_API` → `[INFO_NOTE]` pre-ticked `[x] PREPARED (NO_EXTERNAL_API)`).
   - **Strict Readiness Gate**: `PHASE-01+` may start only after `PHASE-00` carries one of the three accepted ticks defined in `work-item-contract` → `references/plan-and-task-contract.md`.
3. **Step 3 — Interactive Phase-by-Phase Planning Loop (`Plan PHASE-01` → User Confirmation → `Plan PHASE-02` → ...)**:
   - **Do NOT generate all `phases/phase-01..NN.md` files autonomously in one batch.** Work interactively with the user one phase at a time (`i = 1..N`) ([`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §4):
     1. **Synthesize & Report `PHASE-i` to the User**: Before locking `phases/phase-0i-*.md`, present a clear breakdown of `PHASE-i` in chat:
        - **Why (Objective) & Vertical Behavior Slice**: What `PHASE-i` solves (`AC-NN`, `G-NN`, `D-NN`) and the observable input → output.
        - **In-Phase Execution Architecture & Approach**: Exact execution flow inside `PHASE-i`, components/classes/files (`[+]`, `[M]`), and `Consumes` ↔ `Produces` interfaces.
        - **Explicit `Scope in` vs `Scope out` (Anti-Overlap Boundary)**:
          - **Scope in**: Deliverables, files, and unit tests owned by `PHASE-i`.
          - **Scope out**: Adjacent behaviors/files explicitly excluded from `PHASE-i`, each naming its owning `PHASE-k` (or `Out of work item`) so phases never overlap or drift.
        - **Cross-Phase Conflict & Boundary Check**: Analyze `PHASE-i` against already-planned `PHASE-1..i-1` and upcoming `PHASE-(i+1)..N` (shared files, state keys, interface handoffs) to surface and resolve any conflict before locking the phase.
        - **Ordered Tasks, Mandatory In-Phase Unit Tests & Context-Driven `[REVIEW_CHECKPOINT]` Placement**: List the tasks for `PHASE-i` (with unit test files + named `Happy/Pass`, `Negative/Fail`, `Edge/Empty` unit tests co-located inside each logic task), and evaluate where inside `PHASE-i` a **Screen (`S-NN`), Component (`C-NN`), UI tweak, or sub-feature** materializes on UI and should be reviewed immediately (`- [ ] **[REVIEW_CHECKPOINT: ...]**` placed right after that task — whether after 1 task or 2–3 tasks, never fixed by task count).
     2. **Consult & Lock `PHASE-i` with the User (`ask_question`)**: Call `ask_question` to confirm `PHASE-i`'s execution architecture, `Scope in / Scope out`, conflict resolution, unit test plan, and `[REVIEW_CHECKPOINT]` placement with the user. Write `phases/phase-0i-*.md` (`## Objective, approach & scope` + `## Tasks`) once confirmed, and **only after finishing the plan for `PHASE-i` proceed to plan `PHASE-(i+1)` with the user**.
4. **Step 4 — Plan Sections, Ordered Single-Writer Tasks & Mandatory In-Phase Unit Tests (`## Tasks`)**:
   - Author `implementation-plan.md` from `work-item-contract` → `templates/implementation-plan.md.tpl`, including `## Global constraints`, `## Review focus`, and `## Plan change log` ([`02-task-structure-and-regrounding.md`](references/02-task-structure-and-regrounding.md) §1).
   - Break each phase into sequential `- [ ] **Task X.Y**: <Title>` items for a single `code_writer` (no `[PARALLEL]` / `[SEQUENTIAL]` tracks or `Join points`) using the 6 mandatory task fields in `work-item-contract` → `references/plan-and-task-contract.md` §2 (`Scope / Files`, `Reused Components`, `Consumes`, `Produces`, `Acceptance Criteria` with `cwd`, and falsifiable `Expected`).
   - **Mandatory In-Phase Unit Tests**: Every logic-building task MUST include its developer unit test file in `Scope / Files` and run its named unit tests (Happy/Pass, Negative/Fail, Edge/Empty) in `Acceptance Criteria` + `Expected`. Never defer unit tests to a standalone test-only task or a separate testing phase ([`02-task-structure-and-regrounding.md`](references/02-task-structure-and-regrounding.md) §2–§4).
5. **Step 5 — Task-by-Task Re-Grounding Loop & Commit Checkpoints**:
   - Structure tasks for the anti-bulk coding loop (`incremental-implementation`): after each task check (`MATCH` / `CODE_WRONG` / `PLAN_WRONG`), `code_writer` returns to `phases/phase-NN-*.md` on `MATCH` to tick `- [x]` and re-reads the phase plan before starting the next task ([`02-task-structure-and-regrounding.md`](references/02-task-structure-and-regrounding.md) §5).
   - Record the `git-preflight` branch decision (`D-NN`) and phase commit checkpoints in `implementation-plan.md` → `## Checkpoints and shared files`.
6. **Step 6 — 100% `AC-NN`, `G-NN` & UI/UX Traceability + Review DoD + Master E2E Test Plan (`test-plan.md`)**:
   - Map every `AC-NN` in `implementation-plan.md` → `## AC coverage` (`PLAN-V-006-AC-COVERAGE`), mirror the mapped IDs into each phase file's `- **AC IDs**:` bullet (`PLAN-V-006-AC-MISMATCH`), ensure every `G-NN` reaches at least one phase (`PLAN-V-010`), and cover all mapped `S-NN` / `C-NN` items ([`03-ac-coverage-and-review-dod.md`](references/03-ac-coverage-and-review-dod.md) §1).
   - Define the Developer Review DoD (0-error static analysis, in-phase unit/state tests via `{{slot:unit-testing}}`, and 4-state screen visual verification via `{{slot:visual-quality}}`) for `code_writer` / `code_reviewer`, **AND author `.superpowers/work-items/<slug>/vN/test-plan.md`** (`work-item-contract` → `templates/e2e-test-plan.md.tpl`) defining ordered end-to-end scenarios (`- [ ] **E2E-01**` .. `- [ ] **E2E-N**`) covering 100% of `AC-NN` for `test_runner`'s Fail-Fast loop with `bug_fixer` and `planning` ([`03-ac-coverage-and-review-dod.md`](references/03-ac-coverage-and-review-dod.md) §2).
7. **Step 7 — Pre-Gate 3 Verification (`gate-review` `modes/plan.md`) & Gate 3 Master Plan Report**:
   - Run the author self-check, then execute `gate-review` (`modes/plan.md`) in strict 3-pass order: Pass 1 (`validate_plan_slices(plan_path="...")` = `PASS`), Pass 2 (Plan Checklist `P1`–`P5`, `BLOCKER` / `MAJOR` / `MINOR`), and Pass 3 (Fresh Cold-Reader Subagent Check playing `code_writer`), presenting Gate 3 (`implementation-plan.md`, `phases/`, and `test-plan.md`) with a full **Master Plan & Phase Breakdown Report** in chat only when `0 OPEN Q-NN` remain ([`03-ac-coverage-and-review-dod.md`](references/03-ac-coverage-and-review-dod.md) §3).

## 3. Gate 3 Approval Protocol & Post-Gate Change Control

Present `implementation-plan.md`, linked `phases/`, and `test-plan.md` (`E2E-01..E2E-N`) to the user via `ask_question`:
1. **`[Approve Plan & Proceed to Build]`**: Freeze specs, plan, and E2E test plan (`APPROVED_FOR_BUILD`) and return `READY_FOR_BUILD` naming `PHASE-00` (if `[EXECUTE]`) or `PHASE-01` (if `PHASE-00` is `[INFO_NOTE]` with an accepted readiness tick).
2. **`[Refine Technical Decisions]`**: Update task order, fixtures, Review DoD, or `E2E-NN` scenarios in `implementation-plan.md` / `phases/` / `test-plan.md`, re-validate, and re-present Gate 3.
3. **`[Modify Business Scope / Requirements]`**: Halt and route back to `spec_writer` (Gate 1) before replanning.

After Gate 3, the plan and `test-plan.md` change only through `change-control` (including `L3` `PCR-NN.md` escalations raised by `bug_fixer` when an `E2E-i` scenario fails during `final_qa`): `planning` amends `TASK_DETAIL` items and logs a row in `## Plan change log`; any frozen item (`work-item-contract` → `references/plan-and-task-contract.md` §4) is escalated to Gate 2 (`DESIGN_CHANGE`) or Gate 1 (`SCOPE_CHANGE`).

## Reference Guides

| Reference | Topic |
|---|---|
| [references/01-readiness-and-phase-slicing.md](references/01-readiness-and-phase-slicing.md) | 3-input readiness verification, Huly sub-issue re-cutting, mandatory `PHASE-00` API & Mockoon strategy, vertical behavior slicing (`PHASE-01`+), and Gate 1 consultation |
| [references/02-task-structure-and-regrounding.md](references/02-task-structure-and-regrounding.md) | Plan-level sections (`Global constraints`, `Review focus`, `Plan change log`), single-writer task breakdown, right-sizing & risk-first ordering, no-transcribed-code rule, and task-by-task re-grounding loop |
| [references/03-ac-coverage-and-review-dod.md](references/03-ac-coverage-and-review-dod.md) | 100% `AC-NN` / `G-NN` / UI-UX traceability (`PLAN-V-006`, `PLAN-V-010`), Developer Review DoD vs independent QA, 3-pass `gate-review` (`modes/plan.md`), and Gate 3 freeze & change control |
