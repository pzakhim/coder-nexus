# {{PhaseId}}: {{BehaviorTitle}}

> **Document type**: PHASE  
> **Feature**: {{module}}/{{feature}}  
> **Version**: {{Version}}  
> **Created**: {{CreatedDate}}  
> **Source references**: [requirements.md](../requirements.md), [design.md](../design.md)  
> **Status**: PENDING_REVIEW  
> **Approval reference**: NONE

- **Phase ID**: {{PhaseId}}
- **Execution Mode**: {{EXECUTE_OR_INFO_NOTE}}
- **Readiness / Completion Tick**: {{ReadinessCheckboxPreparedOrCompleted}}
- **Behavior**: {{ObservableBehavior}}
- **AC IDs**: {{AcIds}}
- **Depends on**: {{PhaseDependenciesOrNone}}
- **READY when**: {{ReadinessAndBlockers}}
- **Files**: {{CreateModifyReusePathsAndOwner}}
- **Owner**: {{AgentOrHumanOwner}}
- **Verification**: {{ActualCommandsAndEvidence}}
- **UI impact**: {{YES_OR_NO_WITH_REASON}}
- **Visual target/states**: {{TargetAndRequiredStatesOrReasonedNA}}
- **Test cases/data provenance**: {{AcScenarioRealDataSourceOrSafeInputExpectedResultAndTestPath}}
- **Golden baseline**: {{ApprovedBaselineAndComparisonCommandOrReasonedNA}}

## Tasks

{{OrderedTasksWithFilesReusedComponentsProducesAndAcceptanceCriteria}}
<!-- Format for each ordered task:
- [ ] **Task X.Y**: <Task Title>
  - **Scope / Files**: `path/to/file`
  - **Reused Components**: entries from the design's Core usage / Client Core Mapping table
  - **Produces**: public symbols later tasks consume, or none
  - **Acceptance Criteria**: Command or assertion to verify immediately (e.g. the stack's analyzer on `<path>`)
Execution Rule:
1. A single `code_writer` executes tasks strictly in order from top to bottom.
2. After each task: run Acceptance Criteria -> return to this file -> tick `- [x]` -> re-read plan and next task specs before writing next task code.
-->

## Code direction

{{DomainDataPresentationDiRouterChangesActuallyNeeded}}

## Design system source

{{VerifiedTokensComponentsFunctionsOrReasonedNA}}

## Done when

{{ObservableChecksAndEvidence}}

## Risks

{{RisksOrReasonedNone}}

A phase is a verifiable behavior, not a single technical layer. Do not create fake API/data paths or mark expected evidence PASS before execution.
