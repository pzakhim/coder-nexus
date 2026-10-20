# Flutter Verification Report

> **Task:** {{TASK_ID}} — {{TASK_TITLE}}
> **Base revision:** `{{BASE_REVISION}}`
> **Review revision:** `{{REVIEW_REVISION}}`
> **Review report:** `{{REVIEW_REPORT_PATH}}`
> **Overall result:** `{{OVERALL_RESULT}}` <!-- PASS | FAILED | BLOCKED | NOT_RUN -->
> **Approved document revisions:** {{APPROVED_DOCUMENT_REVISIONS}}
> **Gate 1–3 approval references:** {{ACTUAL_APPROVAL_REFERENCES}}
> **Uncommitted scope reviewed:** {{UNCOMMITTED_SCOPE}}

## Environment

| Item | Evidence |
|---|---|
| Client workspace | `{{WORKSPACE_PATH}}` |
| Hub source revision | `{{HUB_REVISION}}` |
| Installed plugin version | `{{PLUGIN_VERSION}}` |
| Flutter/FVM version | `{{FLUTTER_VERSION}}` |
| Platform/device | `{{PLATFORM_DEVICE}}` |
| Flavor/entrypoint | `{{FLAVOR_ENTRYPOINT}}` |
| Working tree | `{{GIT_STATUS}}` |

## Executed checks

Planned checks: {{PLANNED_CHECKS}}. Record `NOT_RUN` or `BLOCKED` for every required check without current evidence.

| Check | Command / observation | CWD | Exit code | Result | Evidence |
|---|---|---|---:|---|---|
{{CHECK_ROWS}}

## Test cases

| AC | Scenario | Check scope (UI/contract or live integration) | Data source / fixture + contract revision | Expected result | Test path / target state | Result | Evidence |
|---|---|---|---|---|---|---|---|
{{CASE_ROWS}}

Fixture-backed PASS applies only to its labeled UI/contract check. Required live integration rows remain BLOCKED/NOT_RUN until exercised against the real endpoint. Overall PASS requires every applicable AC.

## Acceptance criteria traceability

| AC | Implementation | Observable check | Evidence | Result | Limitation |
|---|---|---|---|---|---|
{{AC_ROWS}}

## Runtime visual verification

- UI impact: `{{UI_IMPACT}}`
- Required states: {{REQUIRED_STATES}}
- Visual report/artifacts: {{VISUAL_EVIDENCE}}
- Screenshot review: {{SCREENSHOT_REVIEW_AND_PRESENTATION}}
- Golden baseline and comparison: {{GOLDEN_BASELINE_AND_RESULT_OR_NA}}
- Result: `{{VISUAL_RESULT}}` <!-- PASS | FAILED | BLOCKED | NOT_RUN | N/A -->

## Handoff

{{HANDOFF}}

If code changes after this report, invalidate the affected rows and repeat code/UI review plus verification on the new revision.
