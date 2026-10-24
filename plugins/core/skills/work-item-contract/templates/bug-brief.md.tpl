# {{BugTitle}}

- **Bug slug:** {{BugSlug}}
- **Status:** {{NOT_REPRODUCED_or_TRIAGED_or_READY_FOR_TEST_or_READY_FOR_REVIEW_or_VERIFIED_FIXED_or_STILL_BROKEN_or_ESCALATED_or_BLOCKED}}
- **Source:** {{UserReportTicketOrLogReference}}
- **Found in:** {{EnvironmentAndAppVersionOrRevision}}
- **Branch:** {{BranchFromGitPreflight}}

## 1. Symptom

{{WhatTheUserSeesAndWhereInTheirWords}}

## 2. Expected and actual

- **Expected:** {{CorrectBehavior}} (source: {{SpecAcDecisionOrUserStatement}})
- **Actual:** {{ObservedBehavior}}

## 3. Reproduction

1. {{ReproductionSteps}}

- **Check:** `{{ReproductionCommandOrTestName}}` (cwd: `{{Directory}}`)
- **Before the fix:** {{RedResultAndEvidencePath_or_AttemptsWhenNotReproduced}}

## 4. Root cause

{{FileLineAndWhyItProducesTheActualBehaviorWithEvidence_or_NotConfirmed}}

## 5. Impact

| Area | Item | Evidence | Affected because |
|---|---|---|---|
{{ScreensFlowsApisDataSharedCodeRowsOrNone}}

## 6. Level decision

- **Proposed severity:** {{S1_to_S4}} - {{Reason}}
- **Proposed level:** {{L1_or_L2_or_L3}} - conditions matched: {{ConditionsFromDebugItemContract}}; floors hit: {{FloorsOrNone}}
- **User confirmation:** {{UserResponseReferenceAndConfirmedLevels_or_PENDING}}

## 7. Scope / Files

- **Architecture profile:** {{ProfileWhereTheStackDefinesOne_FromTheBuildingDesignOrResolved_or_NA}}

{{FilesToCreateOrModify_or_NoneForL3}}

## 8. Tasks and verification

{{L1TasksInPlanAndTaskContractFormat_or_SeeFixingPlanForL2_or_NoneForL3}}

## 9. Regression test

- **Test:** `{{RegressionTestPathAndName}}`
- **Red run (before the fix):** {{FailingResultAndReason}}
- **Green run (after the fix):** {{PassingResult}}

## 10. Result

- **Revisions:** `{{BASE_REVISION}}..{{FIX_REVISION}}`
- **Evidence:** `evidence/{{FIX_REVISION}}/`
- **Self bug-hunt (quick):** {{FindingsOrNone}}
- **Code review (L2):** {{APPROVED_or_CHANGES_REQUESTED_or_BLOCKED_or_NotApplicableForL1}} - round {{ReviewRoundNumber}} - `reviews/review_{{FIX_REVISION}}.md`
- **Test Runner:** {{VERIFIED_FIXED_or_STILL_BROKEN_or_PENDING}} - round {{RoundNumber}}
