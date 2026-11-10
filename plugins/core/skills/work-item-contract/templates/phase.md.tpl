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

## Objective, approach & scope

- **Why (Objective)**: {{PhaseWhyBusinessProblemAndAcDecisionIds}}
- **In-phase execution architecture & approach**:
  - {{ExecutionFlowComponentsWiringDataFlowInThisPhase}}
  - Rejected alternative(s): {{RejectedOptionFromDnnAndReasonOrNONE}}
- **Scope in (Included in this phase)**:
  - {{ExplicitDeliverablesBehaviorsFilesAndUnitTestsInThisPhase}}
- **Scope out (Excluded from this phase — anti-overlap)**:
  - {{ExcludedItemOrAdjacentBehavior}} → {{OwningPhaseIdOrOutOfWorkItem}}
- **Cross-phase conflict & boundary check**:
  - Consumes from earlier phases: {{InterfacesModelsStateFromEarlierPhasesOrNONE}}
  - Produces for later phases: {{InterfacesModelsStateExposedToLaterPhasesOrNONE}}
  - Shared-file / scope conflict check: {{HowSharedFilesAndBoundariesAvoidOverlap}}
- **In-phase unit test plan (Mandatory)**:
  - Test file(s): `{{UnitTestFilePaths}}`
  - Named test cases (`Happy/Pass`, `Negative/Fail`, `Edge/Empty`): {{NamedUnitTestsCoveringPassFailEmpty}}

## Tasks

{{OrderedTasksWithFilesReusedComponentsConsumesProducesAcceptanceCriteriaAndExpected}}
<!-- Format for each ordered task:
- [ ] **Task X.Y**: <Task Title>
  - **Scope / Files**: `path/to/source_file`, `path/to/unit_test_file`
  - **Reused Components**: entries from the design's Core usage / Client Core Mapping table
  - **Consumes**: exact signatures from earlier tasks or existing code, or none
  - **Produces**: public symbols later tasks consume, or none
  - **Acceptance Criteria**: exact check command and its cwd running both static analysis and the task's named unit tests (Pass/Happy, Negative/Fail, Edge/Empty)
  - **Expected**: the observable result of that check (exit code, named unit test count passed, exact error text, response status)
Execution Rule:
1. A single `code_writer` executes tasks strictly in order from top to bottom.
2. Every logic-building task MUST include its developer unit tests (Happy/Pass, Negative/Fail, Edge/Empty) in the same task; never defer unit tests to a standalone test-only task or a later phase.
3. After each task: run Acceptance Criteria -> compare with Expected (MATCH / CODE_WRONG / PLAN_WRONG) -> on MATCH return to this file, tick `- [x]` -> re-read plan and next task specs before writing next task code.
4. PLAN_WRONG: stop and raise a plan change request (change-control); never edit the check or Expected.
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
