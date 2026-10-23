# Implementation Plan: {{FeatureTitle}} — {{Version}}

> **Document type**: IMPLEMENTATION_PLAN  
> **Feature**: {{module}}/{{feature}}  
> **Version**: {{Version}}  
> **Created**: {{CreatedDate}}  
> **Source references**: [requirements.md](requirements.md), [codebase-notes.md](codebase-notes.md), [design.md](design.md)  
> **Status**: PENDING_REVIEW  
> **Approval reference**: NONE

- **Gate 1 approval reference**: {{ActualRequirementsApproval}}
- **Gate 2 approval reference**: {{ActualDesignApproval}}

## Global constraints

{{ExactSpecValuesWithSourceIdsOrNone}}

## Review focus

{{UpToFiveUncoveredInputsWithOwningTaskOrNoneFoundAfterCheckingEveryAcAndBr}}

## AC coverage

| AC ID | Phase ID | Verification evidence required | Goal |
|---|---|---|---|
{{AcToPhaseRows}}

Every confirmed goal in `requirements.md` → `## 0. Goals` is delivered by at least one phase (validator `PLAN-V-010`).

## Phase order (Starting with `PHASE-00` Prepare Phase)

Each phase file is linked under `phases/` relative to this plan. `PHASE-00` (`phases/phase-00-prepare.md`) records readiness (linking Huly context in `codebase-notes.md` and the API contract in `design.md`, never copying them) and must be ticked `[x] PREPARED / COMPLETED`, `[x] PREPARED (INFO_READY)` or `[x] PREPARED (NO_EXTERNAL_API)` before `PHASE-01, 02, 03...` begin (`work-item-contract` → `references/plan-and-task-contract.md` → `PHASE-00` readiness tick).

| Phase ID | Mode (`[EXECUTE]` / `[INFO_NOTE]`) | Behavioral outcome / Readiness | Phase file | Depends on | Readiness / Status | Owner |
|---|---|---|---|---|---|---|
{{PhaseRowsWithRelativeLinks}}

## Checkpoints and shared files

{{DependenciesSharedFileOrderAndCheckpoints}}

## Test and visual strategy

{{ActualWorkspaceCommandsTargetsAndStates}}

For UI phases, name each AC's real data source or safe input, expected visible state, screenshot target, and whether baseline screenshot comparison applies. A screenshot baseline requires a reviewed baseline and a Client-approved dev dependency; the pre-release command must not update baselines.

## Gate 3 approval

- **Decision summary**: {{UserFacingPlanSummary}}
- **Approved response**: NONE
- **Approved plan and phase revisions**: NONE

Each phase link must be relative to this version directory. Keep this approved plan stable while implementation progress and real results are recorded in `as-built.md`; after Gate 3 only amendments logged below are allowed (`work-item-contract` → `references/plan-and-task-contract.md` §4–5).

## Plan change log

> Append-only. Never edit or delete a row. Planning reads every row before amending.

| Date | Trigger (task, finding) | Class | What changed | Bad state avoided | Authority |
|---|---|---|---|---|---|
| {{CreatedDate}} | None yet | - | - | - | - |
