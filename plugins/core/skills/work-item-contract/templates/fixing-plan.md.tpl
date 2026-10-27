# Fixing plan: {{BugTitle}}

- **Bug slug:** {{BugSlug}}
- **Level:** L2 (confirmed: {{UserResponseReference}})
- **Brief:** [brief.md](brief.md) at revision {{BriefRevision}}
- **Root cause:** {{OneLineRootCauseFromBrief}}

## Global constraints

- **In scope:** {{FilesFromBriefScope}}
- **Out of scope:** {{NeighbourCodeThatMustNotChange}}
- **Floors not to cross:** {{L3FloorsNearThisFix}}

## Review focus

{{WhatTheReviewerMustCheckOnPurpose_LayersTouchedSharedElementsNearbyFloorsRiskyPaths}}

## Tasks

{{OrderedTasks}}
<!-- Same task fields as work-item-contract plan-and-task-contract section 2:
- [ ] **Task X.Y**: <title>
  - **Scope / Files**: `path` (create / modify)
  - **Reused Components**: entries from existing code, or none
  - **Consumes**: exact existing signatures, or none
  - **Produces**: symbols a later task consumes, or none
  - **Acceptance Criteria**: exact check command and its cwd
  - **Expected**: the observable result of that check
The first task writes the failing regression test (red run and reason); the last task re-runs the reproduction check. -->

## Final checks

| Check | Command (cwd) | Expected |
|---|---|---|
| Reproduction | {{ReproductionCheck}} | {{PassesAfterFix}} |
| Regression test | {{RegressionTest}} | {{Passes}} |
| Verification | {{StackVerificationCommands}} | {{NoNewErrors}} |

## Plan change log

| Date | Change | Reason | Re-confirmed by user |
|---|---|---|---|
{{ChangesOrNone}}
