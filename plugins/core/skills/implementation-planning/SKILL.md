---
name: implementation-planning
description: "Converts approved versioned requirements and architecture design into an executable implementation plan and behavior phase files."
---

# Implementation Planning & Task Breakdown

Guides the **Tech Lead (`planning`)** in converting an approved `requirements.md` (Gate 1), `codebase-notes.md`, and `design.md` (Gate 2, authored via `{{slot:architecture-design}}`) into an executable `implementation-plan.md` and sequential phase files (`phases/phase-NN-*.md`) in `.superpowers/work-items/<slug>/vN/` (or `docs/features/<module>/<feature>/vN/`).

## 1. Input Verification & Readiness Gate

Before formulating tasks, confirm all three inputs ([`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §1):
1. **Gate 1 Approval**: User-approved `requirements.md` (including `## Screens & Visual Sources` and `## Workflows` when UI is in scope) and `codebase-notes.md`.
2. **Gate 2 Approval**: User-approved `design.md` (`0 OPEN Q-NN` in `codebase-notes.md`).
3. **Codebase Readiness Scan**: Verified 4-area stack readiness (foundation/UI kit, routing, state/DI, reuse mapping) via `{{slot:architecture-design}}` and `{{slot:verification}}`.

## 2. Planning Protocol

1. **Mandatory `PHASE-00` (`phases/phase-00-prepare.md` — Prepare & Readiness Phase)**:
   - Always begin with `PHASE-00` (`phases/phase-00-prepare.md`), using `work-item-contract` → `templates/phase.md.tpl` (`AC IDs: NONE (readiness phase)`).
   - **Single home per fact**: Link Huly context in `codebase-notes.md` and the BE API / Mockoon contract in `design.md` without copying them ([`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §3).
   - Classify `PHASE-00` by API mode (`MOCKOON_MOCKED` → `[EXECUTE]` creating and verifying `mocks/<feature>_mockoon.json`, ticked `[x] PREPARED / COMPLETED` by `code_writer` and confirmed read-only by `code_reviewer`; `BE_API_READY` → `[INFO_NOTE]` pre-ticked `[x] PREPARED (INFO_READY)` or `[EXECUTE]` if live probe needed; `NO_EXTERNAL_API` → `[INFO_NOTE]` pre-ticked `[x] PREPARED (NO_EXTERNAL_API)`).
2. **Vertical Behavior Phase Slicing (`PHASE-01`, `PHASE-02`...)**:
   - Re-cut Huly sub-issues and specs into vertical user/test-observable behavior slices starting at `PHASE-01` (walking skeleton through highest risk first), never horizontal technical layers ([`01-readiness-and-phase-slicing.md`](references/01-readiness-and-phase-slicing.md) §2, §4).
   - **Strict Readiness Gate**: `PHASE-01+` may start only after `PHASE-00` carries one of the three accepted ticks defined in `work-item-contract` → `references/plan-and-task-contract.md`.
3. **Plan Sections & Ordered Single-Writer Tasks (`## Tasks`)**:
   - Author `implementation-plan.md` from `work-item-contract` → `templates/implementation-plan.md.tpl`, including `## Global constraints`, `## Review focus`, and `## Plan change log` ([`02-task-structure-and-regrounding.md`](references/02-task-structure-and-regrounding.md) §1).
   - Break each phase into sequential `- [ ] **Task X.Y**: <Title>` items for a single `code_writer` (no `[PARALLEL]` / `[SEQUENTIAL]` tracks or `Join points`) using the 6 mandatory task fields in `work-item-contract` → `references/plan-and-task-contract.md` §2 (`Scope / Files`, `Reused Components`, `Consumes`, `Produces`, `Acceptance Criteria` with `cwd`, and falsifiable `Expected`).
   - Right-size tasks, schedule prefactor tasks first inside the needing phase, apply `Expand → Migrate → Contract` for in-repo schema/contract evolution, and include **no transcribed code bodies** ([`02-task-structure-and-regrounding.md`](references/02-task-structure-and-regrounding.md) §3–§4).
4. **Task-by-Task Re-Grounding Loop & Commit Checkpoints**:
   - Structure tasks for the anti-bulk coding loop (`incremental-implementation`): after each task check (`MATCH` / `CODE_WRONG` / `PLAN_WRONG`), `code_writer` returns to `phases/phase-NN-*.md` on `MATCH` to tick `- [x]` and re-reads the phase plan before starting the next task ([`02-task-structure-and-regrounding.md`](references/02-task-structure-and-regrounding.md) §5).
   - Record the `git-preflight` branch decision (`D-NN`) and phase commit checkpoints in `implementation-plan.md` → `## Checkpoints and shared files`.
5. **100% `AC-NN`, `G-NN` & UI/UX Traceability + Review DoD**:
   - Map every `AC-NN` in `implementation-plan.md` → `## AC coverage` (`PLAN-V-006-AC-COVERAGE`), mirror the mapped IDs into each phase file's `- **AC IDs**:` bullet (`PLAN-V-006-AC-MISMATCH`), ensure every `G-NN` reaches at least one phase (`PLAN-V-010`), and cover all mapped `S-NN` / `C-NN` items ([`03-ac-coverage-and-review-dod.md`](references/03-ac-coverage-and-review-dod.md) §1).
   - Define the Developer Review DoD (0-error static analysis, unit/state tests via `{{slot:unit-testing}}`, and 4-state screen visual verification via `{{slot:visual-quality}}`) distinct from `test_runner`'s independent QA suite ([`03-ac-coverage-and-review-dod.md`](references/03-ac-coverage-and-review-dod.md) §2).
6. **Pre-Gate 3 Verification (`gate-review` `modes/plan.md`)**:
   - Run the 5-item author self-check, then execute `gate-review` (`modes/plan.md`) in strict 3-pass order: Pass 1 (`validate_plan_slices(plan_path="...")` = `PASS`), Pass 2 (Plan Checklist `P1`–`P5`, `BLOCKER` / `MAJOR` / `MINOR`), and Pass 3 (Fresh Cold-Reader Subagent Check playing `code_writer`), presenting Gate 3 only with `0 OPEN Q-NN` ([`03-ac-coverage-and-review-dod.md`](references/03-ac-coverage-and-review-dod.md) §3).

## 3. Gate 3 Approval Protocol & Post-Gate Change Control

Present `implementation-plan.md` and linked `phases/` to the user via `ask_question`:
1. **`[Approve Plan & Proceed to Build]`**: Freeze specs and plan (`APPROVED_FOR_BUILD`) and return `READY_FOR_BUILD` naming `PHASE-00` (if `[EXECUTE]`) or `PHASE-01` (if `PHASE-00` is `[INFO_NOTE]` with an accepted readiness tick).
2. **`[Refine Technical Decisions]`**: Update task order, fixtures, or Review DoD in `implementation-plan.md` / `phases/`, re-validate, and re-present Gate 3.
3. **`[Modify Business Scope / Requirements]`**: Halt and route back to `spec_writer` (Gate 1) before replanning.

After Gate 3, the plan changes only through `change-control`: `planning` amends `TASK_DETAIL` items and logs a row in `## Plan change log`; any frozen item (`work-item-contract` → `references/plan-and-task-contract.md` §4) is escalated to Gate 2 (`DESIGN_CHANGE`) or Gate 1 (`SCOPE_CHANGE`).

## Reference Guides

| Reference | Topic |
|---|---|
| [references/01-readiness-and-phase-slicing.md](references/01-readiness-and-phase-slicing.md) | 3-input readiness verification, Huly sub-issue re-cutting, mandatory `PHASE-00` API & Mockoon strategy, vertical behavior slicing (`PHASE-01`+), and Gate 1 consultation |
| [references/02-task-structure-and-regrounding.md](references/02-task-structure-and-regrounding.md) | Plan-level sections (`Global constraints`, `Review focus`, `Plan change log`), single-writer task breakdown, right-sizing & risk-first ordering, no-transcribed-code rule, and task-by-task re-grounding loop |
| [references/03-ac-coverage-and-review-dod.md](references/03-ac-coverage-and-review-dod.md) | 100% `AC-NN` / `G-NN` / UI-UX traceability (`PLAN-V-006`, `PLAN-V-010`), Developer Review DoD vs independent QA, 3-pass `gate-review` (`modes/plan.md`), and Gate 3 freeze & change control |
