---
name: implementation-planning
description: "Converts approved versioned requirements and architecture design into an executable implementation plan, behavior phase files, and Hybrid E2E test plan using a 3-step 2-Channel Gate 3 protocol (roadmap lock, adaptive detailing, final freeze)."
---

# Implementation Planning & Task Breakdown

Guides the **Tech Lead (`planning`)** in converting an approved `requirements.md` (Gate 1), `codebase-notes.md`, and `design.md` (Gate 2, authored via `{{slot:architecture-design}}`) into an executable `implementation-plan.md`, sequential phase files (`phases/phase-NN-*.md`), and the Master E2E Test Plan (`test-plan.md`, `E2E-01..E2E-N`) in `.superpowers/work-items/<slug>/vN/` (or `docs/features/<module>/<feature>/vN/`).

## 1. Input Verification & Readiness Gate

Before formulating tasks, confirm all three inputs ([`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §1):
1. **Gate 1 Approval**: User-approved `requirements.md` (including `## Screens & Visual Sources` and `## Workflows` when UI is in scope) and `codebase-notes.md`.
2. **Gate 2 Approval**: User-approved `design.md` (`0 OPEN Q-NN` in `codebase-notes.md`).
3. **Codebase Readiness Scan**: Verified 4-area stack readiness (foundation/UI kit, routing, state/DI, reuse mapping) via `{{slot:architecture-design}}` and `{{slot:verification}}`.

## 2. 3-Step Gate 3 Planning Protocol (2-Channel Grilling)

Follow **2-Channel Grilling** (`grilling` Law 4): present structured breakdowns in **session chat (`content`)** and use **short 1-line `ask_question` calls** (`(Recommended)` first). Follow the **3-step formula** (`1 + N + 1`, where `N = 0, 1, 2...` genuine decisions) — never dive head-first into detailing all X phases before locking the roadmap, and never force `X` mechanical ritual popups when a phase is already clear.

1. **Step 1 — High-Level X-Phase Roadmap Lock FIRST (Channel 1 + 1 `ask_question`)**:
   - Always start with mandatory **`PHASE-00`** (`phases/phase-00-prepare.md`, `templates/phase.md.tpl`, `AC IDs: NONE (readiness phase)`), linking Huly context in `codebase-notes.md` and BE API / Mockoon contracts in `design.md` without copying ([`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §3). Classify by API mode: `MOCKOON_MOCKED` → `[EXECUTE]` (ticked `[x] PREPARED / COMPLETED` by `code_writer`, confirmed read-only by `code_reviewer`); `BE_API_READY` → `[INFO_NOTE]` pre-ticked `[x] PREPARED (INFO_READY)` (or `[EXECUTE]` if live probe needed); `NO_EXTERNAL_API` → `[INFO_NOTE]` pre-ticked `[x] PREPARED (NO_EXTERNAL_API)`. `PHASE-01+` starts only after `PHASE-00` carries one of those three accepted ticks (`work-item-contract` → `references/plan-and-task-contract.md`).
   - Re-cut Huly sub-issues and approved specs into vertical behavior slices (`PHASE-01..NN`, walking skeleton / highest risk first, never horizontal layers; [`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §2, §4).
   - Present **only the high-level roadmap FIRST** in **Channel 1 session chat (`content`)**: *"Here is the X-phase roadmap"* — listing `PHASE-00` readiness + `PHASE-01..NN`, a brief summary of what each phase delivers (`AC-NN`, `G-NN`), explicit `Scope in / Scope out` (anti-overlap), and the **Hybrid E2E strategy choice**: **(a) Live `E2E-01..E2E-N` only** (executed read-only by `test_runner` via Antigravity `browser` subagent / `chrome-devtools` MCP or simulator/emulator) **OR (b) Live `E2E-01..E2E-N` + optional local `integration_test/` authoring tasks** assigned to `code_writer` inside the relevant phase(s).
   - Call **1 short 1-line `ask_question`** (`(Recommended)` first) to lock the roadmap direction and Hybrid E2E strategy **before** authoring detailed per-phase specs. Record confirmed choices as `D-NN` in `codebase-notes.md`.
2. **Step 2 — Detail Each Phase & `test-plan.md` + Ask `N` Real Questions Only When Needed (`N = 0, 1, 2...`)**:
   - After the user confirms the X-phase roadmap, author:
     - **`implementation-plan.md`** (`templates/implementation-plan.md.tpl`): `## Global constraints`, `## Review focus`, `## AC coverage` (100% `AC-NN` [`PLAN-V-006-AC-COVERAGE`], 100% `G-NN` [`PLAN-V-010`], mapped `S-NN`/`C-NN`), `## Phase order`, `## Checkpoints and shared files` (recording the `git-preflight` branch `D-NN` and phase commit checkpoints), `## Test and visual strategy` (Developer Review DoD: 0-error static analysis, unit/state tests, 4-state screen visual capture & `code_reviewer` multimodal `read_file` comparison), `## Gate 3 approval`, and `## Plan change log` ([`02-task-structure-and-regrounding.md`](references/02-task-structure-and-regrounding.md) §1, [`03-ac-coverage-and-review-dod.md`](references/03-ac-coverage-and-review-dod.md) §1–§2).
     - **All `phases/phase-NN-*.md` files** (`templates/phase.md.tpl`): mirrored `- **AC IDs**:` (`PLAN-V-006-AC-MISMATCH`), `## Objective, approach & scope`, `[+]/[M]` files, `Consumes ↔ Produces`, cross-phase conflict check, sequential single-writer tasks (`- [ ] **Task X.Y**: <Title>`, 6 mandatory fields, no `[PARALLEL]`/`[SEQUENTIAL]` tracks), **mandatory co-located in-phase unit tests** (`Happy/Pass`, `Negative/Fail`, `Edge/Empty`) in `Scope / Files` + `Acceptance Criteria`/`Expected` (plus explicit `integration_test/` files when confirmed in Step 1), and context-driven **`[REVIEW_CHECKPOINT: <Screen / Component / Feature unit>]`** placements ([`02-task-structure-and-regrounding.md`](references/02-task-structure-and-regrounding.md) §2–§4).
     - **Master E2E Test Plan (`test-plan.md`)**: Author `.superpowers/work-items/<slug>/vN/test-plan.md` (`templates/e2e-test-plan.md.tpl`) locking sequential Fail-Fast `E2E-01..E2E-N` scenarios (100% `AC-NN`) and Hybrid E2E execution targets ([`03-ac-coverage-and-review-dod.md`](references/03-ac-coverage-and-review-dod.md) §2).
   - **Adaptive Grilling (`N = 0, 1, 2...` real questions)**: While detailing phases, ask a 2-Channel `ask_question` **only** when a genuine cross-phase conflict, technical trade-off, checkpoint trade-off, or risk requires a user decision (recording each decision as `D-NN` in `codebase-notes.md`). **Skip** mechanical per-phase confirmation stops (`X` ritual popups) whenever a phase is already clear.
3. **Step 3 — Pre-Gate 3 Verification (`gate-review` `modes/plan.md`), Master Plan Report & Gate 3 Freeze (Channel 1 + 1 `ask_question`)**:
   - Run the author self-check, then 3-pass `gate-review` (`modes/plan.md`): Pass 1 (`validate_plan_slices` = `PASS`), Pass 2 (Plan Checklist `P1`–`P5`), Pass 3 (Fresh Cold-Reader via `invoke_subagent` or temporary `swarm{action:"add"}` helper playing `code_writer`), proceeding to Gate 3 only when `0 OPEN Q-NN` remain ([`03-ac-coverage-and-review-dod.md`](references/03-ac-coverage-and-review-dod.md) §3).
   - Present the consolidated **Master Plan Report** (`implementation-plan.md`, all `phases/`, and `test-plan.md` `E2E-01..E2E-N` + Hybrid E2E strategy) in **Channel 1 session chat (`content`)**, then call **1 short 1-line `ask_question`** to lock Gate 3 (§3).

## 3. Gate 3 Approval Paths & Post-Gate Change Control

Gate 3 final `ask_question` (`(Recommended)` first):
1. **`(Recommended) Approve Plan & Proceed to Build`**: Freeze specs, plan, and `test-plan.md` (`APPROVED_FOR_BUILD`) and return `READY_FOR_BUILD` naming `PHASE-00` (if `[EXECUTE]`) or `PHASE-01` (if `PHASE-00` carries an accepted readiness tick).
2. **`Refine Technical Decisions`**: Adjust task order, fixtures, Hybrid E2E tasks, Review DoD, or `E2E-NN` scenarios, re-validate, and re-present Gate 3.
3. **`Modify Business Scope / Requirements`**: Halt and route back to `spec_writer` (Gate 1) before replanning.

After Gate 3, the plan and `test-plan.md` change only through `change-control` (including `L3` `PCR-NN.md` escalations from `bug_fixer` in `final_qa`): `planning` amends `TASK_DETAIL` items and logs `## Plan change log`; frozen items escalate to Gate 2 (`DESIGN_CHANGE`) or Gate 1 (`SCOPE_CHANGE`), after which `code_writer` implements the updated task(s).

## Reference Guides

| Reference | Topic |
|---|---|
| [references/01-readiness-and-phase-slicing.md](references/01-readiness-and-phase-slicing.md) | 3-input readiness check, Huly sub-issue re-cutting, `PHASE-00` API & Mockoon strategy, vertical slicing, 3-step 2-Channel Gate 3 planning, and Gate 1 consultation |
| [references/02-task-structure-and-regrounding.md](references/02-task-structure-and-regrounding.md) | Plan-level sections, single-writer tasks, right-sizing & risk-first ordering, no-transcribed-code rule, and atomic-unit re-grounding loop |
| [references/03-ac-coverage-and-review-dod.md](references/03-ac-coverage-and-review-dod.md) | 100% `AC-NN` / `G-NN` / UI-UX traceability, Hybrid E2E & Review DoD, 3-pass `gate-review` (`modes/plan.md`), and Gate 3 freeze & change control |
