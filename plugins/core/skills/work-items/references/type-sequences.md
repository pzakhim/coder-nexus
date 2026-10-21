# Type-specific sequence and evidence

Read only the row selected in the brief. These are dependency patterns, not compulsory phase counts.

| Type | Sequence | Decisive evidence |
|---|---|---|
| `feature` | Confirm goals → workflows + UI/UX design (approved `uiux.md` revision, UI-impact items) → requirements (behavior/permissions) → design → approved plan → smallest observable flow → errors/states → integration | Approved Gate 1–3 revisions (Gate 1 includes the approved UI/UX revision), AC scenarios, the stack's analyzer/test checks and required runtime UI states |
| `bugfix` | Reproduce expected vs actual → identify cause → narrow correction → regression | Reproduction fails before and focused regression passes after; nearby behavior remains intact |
| `refactor` | Capture public baseline → move coherent owner → compare contracts → remove obsolete path | Imports, routes, state, API, side effects and errors remain as approved |
| `optimization` | Measure representative baseline → change bottleneck → measure same workload | Target metric and correctness meet brief on comparable conditions |
| `migration` | Define old/new compatibility → prepare → cut over → verify/recover | Data/contract integrity and recovery check; irreversible step named |
| `maintenance` | Reproduce tool/build problem → adjust → repeat check | Affected tool or pipeline succeeds under the stated environment |
| `investigation` | Gather evidence → test hypotheses → report recommendation | Findings answer the decision question with sources and limits; code plan usually skipped |
| `documentation` | Verify source and reader task → write → check examples/links | Reader can follow accurate instructions; Docs Writer owns delivery |

For UI work, the approved `design-uiux/` revision is the visual input when it exists; the design names real visual input, Kit candidates, required states and target. For non-UI work, mark UI checks N/A with reason. A missing device, data source, service or baseline remains `BLOCKED` or `NOT_RUN`.
