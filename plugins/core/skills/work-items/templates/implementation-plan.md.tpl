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

## AC coverage

| AC ID | Phase ID | Verification evidence required | Goal |
|---|---|---|---|
{{AcToPhaseRows}}

Every confirmed goal in `requirements.md` → `## 0. Goals` is delivered by at least one phase (validator `PLAN-V-010`).

## Phase order (Starting with `PHASE-00` Prepare Phase)

Each phase file is linked under `phases/` relative to this plan. `PHASE-00` (`phases/phase-00-prepare.md`) records readiness (linking Huly context in `codebase-notes.md` and the API contract in `design.md`, never copying them) and must be ticked `[x] PREPARED / COMPLETED` before `PHASE-01, 02, 03...` begin.

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

Each phase link must be relative to this version directory. Keep this approved plan stable while implementation progress and real results are recorded in `as-built.md`.
