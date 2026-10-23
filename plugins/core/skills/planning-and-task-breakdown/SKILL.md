---
name: planning-and-task-breakdown
description: Converts approved versioned requirements and architecture design into an executable implementation plan and behavior phase files.
---

# Planning and Task Breakdown

This skill guides the **Tech Lead (Planning Agent)** in converting an approved `requirements.md` (Gate 1) and `design.md` (Gate 2, authored via `{{slot:architecture-design}}` skill) into an actionable `implementation-plan.md` and discrete phase files (`phases/phase-NN-*.md`) in `.superpowers/work-items/<slug>/vN/` or `${workspaceFolder}/docs/features/<module>/<feature>/vN/`.

## 1. Input Verification

Before formulating tasks, confirm:
1. **Gate 1 Approval**: Actual user approval of `requirements.md` (authored by Spec Writer).
2. **Gate 2 Approval**: Actual user approval of `design.md` (authored by Planning via `{{slot:architecture-design}}`).
3. Check sibling files: Both `requirements.md` and `design.md` must be present in `docs/features/<module>/<feature>/vN/` or the work item directory.

## 2. Planning Protocol

1. **Mandatory `PHASE-00` (`phases/phase-00-prepare.md` — Prepare & Readiness Phase)**:
   - Always begin the plan with `PHASE-00` (`phases/phase-00-prepare.md`). **One home per fact**: Huly and source context stay in `codebase-notes.md`, the BE API / Mockoon contract in `design.md`; `PHASE-00` links to them and holds only readiness checks and preparation tasks, so downstream agents (`code_writer`, `code_reviewer`, `test_runner`) never re-query Huly or read a stale copy.
   - Classify each item in `PHASE-00` as **`[EXECUTE]`** or **`[INFO_NOTE]`** with a Readiness Checklist (`- [ ]` / `- [x] PREPARED / COMPLETED`):
     - **If `MOCKOON_MOCKED` (`[EXECUTE]`)**: `PHASE-00` contains executable tasks for `code_writer` to create `mocks/<feature>_mockoon.json` (with all Pass/Default, Empty, and Fail rules from the `Mockoon Trigger & Test Data Table` in `design.md`), start `mockoon-cli`, verify via `curl`, and pass `code_reviewer` inspection. The `code_writer` ticks **`[x] PREPARED / COMPLETED`** in `phases/phase-00-prepare.md` and `implementation-plan.md` before its hand-off; the `code_reviewer` only confirms the tick and never edits plan documents.
     - **If `BE_API_READY` (`[INFO_NOTE]` or `[EXECUTE]` if live probe needed)**: Link the BE API section of `design.md` (endpoints, schemas, verification status against the user's spec). When no execution is needed, mark **`[INFO_NOTE]`** and pre-tick **`[x] PREPARED (INFO_READY)`**.
     - **If No External API (`[INFO_NOTE]`)**: Omit the API section in `PHASE-00`, record only links to `codebase-notes.md`, and pre-tick **`[x] PREPARED (NO_EXTERNAL_API)`**.
2. **Sequential Behavior Phase Slicing (`PHASE-01`, `PHASE-02`, `PHASE-03`...)**:
   - Follow [01_phase_slicing_rules.md](references/01_phase_slicing_rules.md). Slice by vertical observable behavior (each phase is a self-contained sub-feature), never by horizontal technical layers. Add Domain, Data, Presentation, and DI as required by each behavior.
   - **Strict Sequential Phase Order & Readiness Gate**: `PHASE-01`, `PHASE-02`, `PHASE-03`... only start after `PHASE-00` carries one accepted tick (**`[x] PREPARED / COMPLETED`**, `[x] PREPARED (INFO_READY)` or `[x] PREPARED (NO_EXTERNAL_API)`; `work-item-contract` → `plan-and-task-contract.md` → `PHASE-00` readiness tick), ensuring all data and API context are ready so `code_writer` never gets stuck due to missing information.
3. **Ordered Task Breakdown Within Each Phase (Single `code_writer` Execution)**:
   - Every phase MUST be broken down into an ordered list of discrete, bounded micro-tasks executed top-to-bottom by a single `code_writer` (do **not** split tasks into `[PARALLEL]` / `[SEQUENTIAL]` tracks or `Join points`).
   - Each task (`- [ ] **Task X.Y**: <Title>`) uses the task fields defined once in [plan-and-task-contract.md](../work-item-contract/references/plan-and-task-contract.md) §2: **Scope / Files**, **Reused Components**, **Consumes**, **Produces**, **Acceptance Criteria** (exact check + cwd) and **Expected** (its observable result). Do not restate or vary the format here. Reason: one home per format, so writer, reviewer and tester read the same fields.
4. **Plan Quality Rules**: Follow [04_plan_structure_and_task_rules.md](references/04_plan_structure_and_task_rules.md):
   - `implementation-plan.md` carries `## Global constraints`, `## Review focus` and, at the end, `## Plan change log` (format in [plan-and-task-contract.md](../work-item-contract/references/plan-and-task-contract.md) §1, §5; how to choose their content in [04](references/04_plan_structure_and_task_rules.md) §1).
   - **Right-size** tasks: one deliverable with its own check; fold setup/config into the task that needs it.
   - **Order**: after `PHASE-00`, the highest-risk behavior first; behavior-preserving prefactor tasks first inside the phase that needs them; storage or public-contract changes with live consumers follow expand → migrate → contract.
   - **No transcribed code**: tasks give file, signature and the values `requirements.md` / `design.md` pin, never full bodies.
5. **Agent Execution Loop & Plan Re-Grounding Contract**:
   - The breakdown structures tasks as ordered, single-objective units designed for the Code Writer's Task-by-Task Grounding Loop (in `incremental-implementation`).
   - Every task has an actionable checkbox `- [ ]`.
   - **Mandatory Re-Reading of Plan**: After finishing each micro-task and running its acceptance verification, `code_writer` MUST return to the phase file (`phases/phase-NN-*.md`), tick the completed task `- [x]`, re-read the plan to refresh context, and inspect the scope, mapped components, and acceptance criteria of the next task before starting it. Never execute multiple tasks in one bulk pass without returning to re-read the plan between tasks.
6. **AC Coverage Matrix**: Follow [02_ac_coverage_matrix.md](references/02_ac_coverage_matrix.md). Map every AC ID from `requirements.md` to an owning phase with decisive checks.
7. **Review DoD & Verification Strategy**: Follow [03_review_dod_and_testing.md](references/03_review_dod_and_testing.md). Specify developer unit tests (use cases, mappers, state-holder emissions covering the agreed Pass/Default and Fail cases) and a zero-error run of the stack's analyzer; the exact commands and test conventions come from `{{slot:unit-test}}` and `{{slot:verification}}`.
8. **Draft Plan & Phases**:
   - Write `implementation-plan.md` using [implementation-plan.md.tpl](../work-item-contract/templates/implementation-plan.md.tpl); keep every template heading.
   - Write `phases/phase-00-prepare.md` and `phases/phase-NN-<behavior>.md` using [phase.md.tpl](../work-item-contract/templates/phase.md.tpl) ensuring each task has status checkbox `- [ ]`, file scope, reused components, consumed and produced symbols, acceptance criteria and Expected.
9. **Validation**: Run `validate_plan_slices(plan_path="...")` to ensure document integrity and 100% AC coverage.
10. **Pre-Gate 3 Review** (after validation passes):
    - Run [gate-review](../gate-review/SKILL.md) with `modes/plan.md` (it starts from the validator result). Fix CRITICAL and HIGH findings in the plan; a finding only the user can settle becomes `Q-NN`.
    - Run [cold-reader-check](../cold-reader-check/SKILL.md) on `implementation-plan.md` and the phase files. Answer minor questions in the plan yourself and mark them as Planning's call; queue user's-call questions as `Q-NN` in `codebase-notes.md`, ask one at a time, close each into `D-NN`.
    - Present Gate 3 only with 0 `OPEN` `Q-NN`. Reason: a plan the Code Writer cannot follow without asking stops the build mid-phase.

## 3. Gate 3 Approval Protocol & Handoff

Present the plan and linked phases to the User via `ask_question`:
1. **[Approve Plan & Proceed to Build]**: User approves at Gate 3 $\implies$ specs and plan are frozen (`APPROVED_FOR_BUILD`); Planning returns `READY_FOR_BUILD` naming `PHASE-00` (if `[EXECUTE]`) or `PHASE-01` (if `PHASE-00` is `[INFO_NOTE]` and already carries `[x] PREPARED (INFO_READY)` or `[x] PREPARED (NO_EXTERNAL_API)`), and the coordinator assigns one Code Writer; the Code Reviewer checks each `## Review focus` line deliberately.
2. **[Technical Refinement]**: Adjust task order, mock fixtures, or DoD directly in `implementation-plan.md`.
3. **[Scope / Requirements Change]**: Route back to Spec Writer if business rules need revision before replanning.

After Gate 3 the plan changes only through [plan-change-request](../plan-change-request/SKILL.md): Planning amends `TASK_DETAIL` alone and logs it in `## Plan change log`; anything frozen ([plan-and-task-contract.md](../work-item-contract/references/plan-and-task-contract.md) §4) is escalated to Gate 2 or Gate 1.
