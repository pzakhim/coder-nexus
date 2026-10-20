---
name: planning-and-task-breakdown
description: Converts approved versioned requirements and architecture design into an executable implementation plan and behavior phase files.
---

# Planning and Task Breakdown

This skill guides the **Tech Lead (Planning Agent)** in converting an approved `requirements.md` (Gate 1) and `design.md` (Gate 2, authored via `{{slot:architecture-design}}` skill) into an actionable `implement-plan.md` and discrete phase files (`phases/phase-NN-*.md`) in `.superpowers/work-items/<slug>/vN/` or `${workspaceFolder}/docs/features/<module>/<feature>/vN/`.

## 1. Input Verification

Before formulating tasks, confirm:
1. **Gate 1 Approval**: Actual user approval of `requirements.md` (authored by Spec Writer).
2. **Gate 2 Approval**: Actual user approval of `design.md` (authored by Planning via `{{slot:architecture-design}}`).
3. Check sibling files: Both `requirements.md` and `design.md` must be present in `docs/features/<module>/<feature>/vN/` or the work item directory.

## 2. Planning Protocol

1. **Mandatory `PHASE-00` (`phases/phase-00-prepare.md` — Prepare & Context/API Consolidation Phase)**:
   - Always begin the plan with `PHASE-00` so all Huly task context (fetched once) and external BE API / Mockoon details are consolidated in one place (`phases/phase-00-prepare.md`) and downstream agents (`code_writer`, `code_reviewer`, `test_runner`) never re-query Huly or hunt for scattered specs.
   - Classify each item in `PHASE-00` as **`[EXECUTE]`** or **`[INFO_NOTE]`** with a Readiness Checklist (`- [ ]` / `- [x] PREPARED / COMPLETED`):
     - **If `MOCKOON_MOCKED` (`[EXECUTE]`)**: `PHASE-00` contains executable tasks for `code_writer` to create `mocks/<feature>_mockoon.json` (with all Pass/Default, Empty, and Fail rules from the `Mockoon Trigger & Test Data Table` in `design.md`), start `mockoon-cli`, verify via `curl`, and pass `code_reviewer` inspection. Once completed and reviewed, tick **`[x] PREPARED / COMPLETED`** in `phases/phase-00-prepare.md` and `implement-plan.md`.
     - **If `BE_API_READY` (`[INFO_NOTE]` or `[EXECUTE]` if live probe needed)**: Consolidate the BE API endpoints, schemas, and verification status against the user's spec. When no execution is needed, mark **`[INFO_NOTE]`** and pre-tick **`[x] PREPARED (INFO_READY)`**.
     - **If No External API (`[INFO_NOTE]`)**: Omit the API section in `PHASE-00`, record only the consolidated context note, and pre-tick **`[x] PREPARED (NO_EXTERNAL_API)`**.
2. **Sequential Behavior Phase Slicing (`PHASE-01`, `PHASE-02`, `PHASE-03`...)**:
   - Follow [01_phase_slicing_rules.md](references/01_phase_slicing_rules.md). Slice by vertical observable behavior (each phase is a self-contained sub-feature), never by horizontal technical layers. Add Domain, Data, Presentation, and DI as required by each behavior.
   - **Strict Sequential Phase Order & Readiness Gate**: `PHASE-01`, `PHASE-02`, `PHASE-03`... only start after `PHASE-00` is ticked **`[x] PREPARED / COMPLETED`**, ensuring all data and API context are ready so `code_writer` never gets stuck due to missing information.
3. **Ordered Task Breakdown Within Each Phase (Single `code_writer` Execution)**:
   - Every phase MUST be broken down into an ordered list of discrete, bounded micro-tasks executed top-to-bottom by a single `code_writer` (do **not** split tasks into `[PARALLEL]` / `[SEQUENTIAL]` tracks or `Join points`).
   - Each task (`- [ ] **Task X.Y**: <Title>`) MUST explicitly specify:
     * **Scope / Files**: Exact file paths and class names created or modified.
     * **Reused Components**: Exact entries from the approved reuse mapping (`Core usage` / `Client Core Mapping` in `design.md`) that this task must use.
     * **Produces**: Public symbols/signatures that subsequent tasks in the phase consume (or `none`).
     * **Acceptance Criteria**: Exact command or assertion to verify that specific task immediately upon completion (e.g. the stack's analyzer on `<path>`, a targeted unit test).
4. **Agent Execution Loop & Plan Re-Grounding Contract**:
   - The breakdown structures tasks as ordered, single-objective units designed for the Code Writer's Task-by-Task Grounding Loop (in `incremental-implementation`).
   - Every task has an actionable checkbox `- [ ]`.
   - **Mandatory Re-Reading of Plan**: After finishing each micro-task and running its acceptance verification, `code_writer` MUST return to the phase file (`phases/phase-NN-*.md`), tick the completed task `- [x]`, re-read the plan to refresh context, and inspect the scope, mapped components, and acceptance criteria of the next task before starting it. Never execute multiple tasks in one bulk pass without returning to re-read the plan between tasks.
5. **AC Coverage Matrix**: Follow [02_ac_coverage_matrix.md](references/02_ac_coverage_matrix.md). Map every AC ID from `requirements.md` to an owning phase with decisive checks.
6. **Review DoD & Verification Strategy**: Follow [03_review_dod_and_testing.md](references/03_review_dod_and_testing.md). Specify developer unit tests (use cases, mappers, state-holder emissions covering the agreed Pass/Default and Fail cases) and a zero-error run of the stack's analyzer; the exact commands and test conventions come from `{{slot:unit-test}}` and `{{slot:verification}}`.
7. **Draft Plan & Phases**:
   - Write `implement-plan.md` using [templates/implement-plan.md.tpl](../feature-planner/templates/versioned_implementation_plan.md.tpl).
   - Write `phases/phase-00-prepare.md` and `phases/phase-NN-<behavior>.md` using [templates/phase.md.tpl](../feature-planner/templates/phase.md.tpl) ensuring each task has status checkbox `- [ ]`, file scope, reused components, produced symbols, and acceptance criteria.
8. **Validation**: Run `validate_plan_slices(plan_path="...")` to ensure document integrity and 100% AC coverage.

## 3. Gate 3 Approval Protocol & Handoff

Present the plan and linked phases to the User via `ask_question`:
1. **[Approve Plan & Proceed to Build]**: User approves at Gate 3 $\implies$ Freeze specs and plan (`APPROVED_FOR_BUILD`), hand off `PHASE-00` (if `[EXECUTE]`) or `PHASE-01` (if `PHASE-00` is `[INFO_NOTE]` and already ticked `[x] PREPARED`) to a single `code_writer`.
2. **[Technical Refinement]**: Adjust task order, mock fixtures, or DoD directly in `implement-plan.md`.
3. **[Scope / Requirements Change]**: Route back to Spec Writer if business rules need revision before replanning.
