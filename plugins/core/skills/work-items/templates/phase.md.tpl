# {{PhaseId}} — {{Behavior}}

- **Status:** TODO
- **Execution Mode:** {{EXECUTE_OR_INFO_NOTE}}
- **Readiness / Completion Tick:** {{ReadinessCheckboxPreparedOrCompleted}}
- **AC IDs:** {{AcIds}}
- **Goals:** {{GoalIdsServedByTheseAcs}}
- **Depends on:** {{EarlierPassedPhasesOrNone}}
- **Input/output contract:** {{VerifiedInputAndObservableOutput}}
- **Owned files:** {{BoundedClientPaths}}
- **Owner:** {{AssignedAgent}}
- **Ready when:** {{DependenciesAndApprovalReferences}}

## Tasks

{{OrderedTasksWithFilesReusedComponentsProducesAndAcceptanceCriteria}}
<!-- Format for each ordered task:
- [ ] **Task X.Y**: <Task Title>
  - **Scope / Files**: `path/to/file.ext`
  - **Reused Components**: entries from the approved reuse mapping
  - **Produces**: public symbols later tasks consume, or none
  - **Acceptance Criteria**: Command or condition to verify immediately
Execution Rule:
1. A single `code_writer` executes tasks strictly in order from top to bottom.
2. After each task: run Acceptance Criteria -> return to this file -> tick `- [x]` -> re-read plan and next task specs before writing next task code.
-->

## Pass gate

{{ActualAnalyzerTestsRuntimeVisualOrTypeSpecificEvidenceAndTarget}}
