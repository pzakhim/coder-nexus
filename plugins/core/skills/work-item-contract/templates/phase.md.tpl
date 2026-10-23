# {{PhaseId}}: {{BehaviorTitle}}

> **Document type**: PHASE  
> **Feature**: {{module}}/{{feature}}  
> **Version**: {{Version}}  
> **Created**: {{CreatedDate}}  
> **Source references**: [requirements.md](../requirements.md), [codebase-notes.md](../codebase-notes.md), [design.md](../design.md)  
> **Status**: PENDING_REVIEW  
> **Approval reference**: NONE

- **Phase ID**: {{PhaseId}}
- **Execution Mode**: {{EXECUTE_OR_INFO_NOTE}}
- **Readiness / Completion Tick**: {{ReadinessCheckboxPreparedOrCompleted}}
- **Behavior**: {{ObservableBehavior}}
- **AC IDs**: {{AcIds}}
- **Goals**: {{GoalIdsServedByTheseAcs}}
- **Depends on**: {{PhaseDependenciesOrNone}}
- **READY when**: {{ReadinessAndBlockers}}
- **Files**: {{CreateModifyReusePathsAndOwner}}
- **Owner**: {{AgentOrHumanOwner}}
- **Verification**: {{ActualCommandsAndEvidence}}
- **UI impact**: {{YES_OR_NO_WITH_REASON}}
- **Visual target/states**: {{TargetAndRequiredStatesOrReasonedNA}}
- **Test cases/data provenance**: {{AcScenarioRealDataSourceOrSafeInputExpectedResultAndTestPath}}
- **Screenshot baseline**: {{ApprovedBaselineAndComparisonCommandOrReasonedNA}}

## Tasks

{{OrderedTasksWithFilesReusedComponentsConsumesProducesAcceptanceCriteriaAndExpected}}
<!-- Format for each ordered task:
- [ ] **Task X.Y**: <Task Title>
  - **Scope / Files**: `path/to/file`
  - **Reused Components**: entries from the design's Core usage / Client Core Mapping table
  - **Consumes**: exact signatures from earlier tasks or existing code, or none
  - **Produces**: public symbols later tasks consume, or none
  - **Acceptance Criteria**: exact check command and its cwd (e.g. the stack's analyzer on `<path>`, a named test)
  - **Expected**: the observable result of that check (exit code, test count, exact error text, response status)
Execution Rule:
1. A single `code_writer` executes tasks strictly in order from top to bottom.
2. After each task: run Acceptance Criteria -> compare with Expected (MATCH / CODE_WRONG / PLAN_WRONG) -> on MATCH return to this file, tick `- [x]` -> re-read plan and next task specs before writing next task code.
3. PLAN_WRONG: stop and raise a plan-change-request; never edit the check or Expected.
Field rules: work-item-contract references/plan-and-task-contract.md.
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
