# Diagnosis: {{Title}}

- **Slug:** {{BugSlug}}
- **Kind:** {{Bug_or_Trace}}
- **Status:** {{DIAGNOSED_or_NOT_REPRODUCED_or_BLOCKED}}
- **Revision investigated:** `{{Revision}}`
- **Environment:** {{EnvironmentDeviceOrTargetAndAppVersion}}

## 1. Question

{{SymptomExpectedAndActual_or_WhatTheUserWantsToUnderstandAboutTheFeature}}

## 2. Scenario

1. {{ReproductionStepsOrScenarioToRun}}

- **Check:** `{{CommandOrTestOrManualRun}}` (cwd: `{{Directory}}`)

## 3. Temporary instrumentation

| File:line | What it logs | Removed |
|---|---|---|
{{InstrumentationRows_or_None}}

- **Before:** `git status` / `git diff` of the instrumented files: {{StartingState}}
- **After removal:** {{SameStateAsBeforeWithEvidence}}

## 4. Captured output

{{KeyLogLinesTracesOrResponsesMaskedWithEvidencePaths}}

## 5. Findings

{{Bug_RootCauseFileLineAndMechanism_or_NotConfirmed__Trace_TheObservedFlowStepByStep}}

## 6. Impact

| Area | Item | Evidence | Affected because |
|---|---|---|---|
{{ScreensFlowsApisDataSharedCodeRows_or_NoneForATrace}}

## 7. Next step

{{FixThroughDefectResolution_or_NoActionNeeded_or_OpenQuestions}}
