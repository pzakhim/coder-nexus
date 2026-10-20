# Implementation Plan: {{FeatureTitle}} — {{Version}}

> **Document type**: IMPLEMENTATION_PLAN  
> **Feature**: {{module}}/{{feature}}  
> **Version**: {{Version}}  
> **Created**: {{CreatedDate}}  
> **Source references**: [requirements.md](requirements.md), [design.md](design.md)  
> **Status**: PENDING_REVIEW  
> **Approval reference**: NONE

- **Gate 1 approval reference**: {{ActualRequirementsApproval}}
- **Gate 2 approval reference**: {{ActualDesignApproval}}

## AC coverage

| AC ID | Phase ID | Verification evidence required |
|---|---|---|
{{AcToPhaseRows}}

## Phase order (Starting with `PHASE-00` Prepare Phase)

Each phase file is linked under `phases/` relative to this plan. `PHASE-00` (`phases/phase-00-prepare.md`) consolidates Huly/API context once and must be ticked `[x] PREPARED / COMPLETED` before `PHASE-01, 02, 03...` begin.

| Phase ID | Mode (`[EXECUTE]` / `[INFO_NOTE]`) | Behavioral outcome / Consolidation | Phase file | Depends on | Readiness / Status | Owner |
|---|---|---|---|---|---|---|
{{PhaseRowsWithRelativeLinks}}

## Checkpoints and shared files

{{DependenciesSharedFileOrderAndCheckpoints}}

## Test and visual strategy

{{ActualWorkspaceCommandsTargetsAndStates}}

For UI phases, name each AC's real data source or safe input, expected visible state, screenshot target, and whether golden comparison applies. A golden requires a reviewed baseline and a Client-approved dev dependency; the pre-release command must not update goldens.

## Gate 3 approval

- **Decision summary**: {{UserFacingPlanSummary}}
- **Approved response**: NONE
- **Approved plan and phase revisions**: NONE

Each phase link must be relative to this version directory. Keep this approved plan stable while implementation progress and real results are recorded in `as-built.md`.
