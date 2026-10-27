# Escalation: {{BugTitle}}

- **Bug slug:** {{BugSlug}}
- **Severity:** {{S1_to_S4}}
- **Level:** L3 (confirmed: {{UserResponseReference}})
- **Brief:** [brief.md](brief.md)
- **Code changed:** none

## 1. Symptom, expected and actual

- **Symptom:** {{WhatTheUserSees}}
- **Expected:** {{CorrectBehavior}} (source: {{SpecAcDecisionOrUserStatement}})
- **Actual:** {{ObservedBehavior}}

## 2. Reproduction

1. {{ReproductionSteps}}

- **Check:** `{{ReproductionCommandOrTestName}}` (cwd: `{{Directory}}`) - evidence: `{{EvidencePath}}`
- **Triage test (removed from the tree):** {{ReproductionTestPathAndContent_or_None}}

## 3. Root cause

{{FileLineAndWhyWithEvidence_or_NotConfirmedWithHypothesesTestedAndResults}}

## 4. Impact

| Area | Item | Evidence | Affected because |
|---|---|---|---|
{{ScreensFlowsApisDataSharedCodeRows}}

## 5. L3 conditions hit

{{ConditionsFromDebugItemContractSection3AndFloorsHitWithEvidence}}

## 6. Suggested work item

- **Type:** {{bugfix_or_feature_WithReason}}
- **Needs `change-impact.md`:** {{YES_or_NO_WithReason}}

## 7. Open questions for Spec Writer

{{QuestionsTheSpecMustAnswer_or_None}}
