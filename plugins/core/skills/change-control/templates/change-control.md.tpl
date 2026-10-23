# {{PcrId}}: {{OneLineSummary}}

- **Raised by**: {{Role}} on {{Date}} (file written by the Code Writer, or by the coordinator from a Reviewer / Test Runner `PLAN_CONFLICT` row)
- **Work item / version / phase / task**: {{Slug}} / {{Version}} / {{PhaseId}} / {{TaskId}}
- **Revision**: {{CodeRevision}}; plan revision {{PlanRevision}}
- **Trigger**: {{PlanWrongMissingSymbolComponentMismatchDnnConflictFileOutsideScopeOrPlanConflictFinding}}
- **Blocked**: {{TasksOrPhaseWaitingOnThisRequest}}

## Expected vs reality

| Plan says (quote the task line, `D-NN` or constraint) | Reality |
|---|---|
| {{PlanText}} | {{ObservedFact}} |

## Evidence

| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
|---|---|---|---|---|---|
| {{Claim}} | {{CommandAndCwd}} | {{Revision}} | {{ExitCode}} | {{KeyOutput}} | {{Result}} |

## Options

| # | Option | Touches (task detail / design / scope) | Cost |
|---|---|---|---|
| 1 (Recommended) | {{Option1}} | {{Touches1}} | {{Cost1}} |
| 2 | {{Option2}} | {{Touches2}} | {{Cost2}} |

## Answer (Planning)

- **Class**: {{TASK_DETAIL_or_DESIGN_CHANGE_or_SCOPE_CHANGE}}
- **Status**: {{AMENDED_or_ESCALATED}}
- **Changed lines / target gate and Q-NN**: {{ExactChangedTaskLinesOrGateAndQueuedQuestion}}
- **Tasks unticked, evidence invalidated**: {{AffectedTasksOrNone}}
- **Plan change log row**: {{DateOfAppendedRowOrPendingUserApproval}}
