# Test run report: {{Title}}

- **Run status:** {{COMPLETED_or_BLOCKED}} - {{OneLineReason}}
- **Counts:** PASS {{Pass}} / FAIL {{Fail}} / BLOCKED {{Blocked}} / NOT_RUN {{NotRun}}
- **Revision under test:** `{{Revision}}` (uncommitted scope: {{UncommittedScopeOrNone}})
- **Environment record:** {{TargetDeviceBuildServicesAccountsAndWhatThisRunStarted}}
- **Plan:** [test-plan.md](test-plan.md)

## Results

| ID | Result | Expected | Observed | Evidence | Label |
|---|---|---|---|---|---|
{{ResultRows_PASS_FAIL_BLOCKED_NOT_RUN__LabelExpectedInferredWhereUsed}}

## Failures

{{PerFailStepsExpectedVsActualEvidencePath_or_None}}

## Gaps

{{CasesWithNoAutomatedTest_or_None}}

## Limitations

{{StubbedProvidersMissingToolsNotRunReasons_or_None}}

## Suggested cases (not run)

{{AdditionalCasesTheScenarioDidNotCover_WithReason_or_None}}
