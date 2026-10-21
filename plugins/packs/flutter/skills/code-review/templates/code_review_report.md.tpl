# Code Review Report

> **Feature/version:** {{FEATURE_VERSION}}
> **Phase / task:** {{TASK_ID}} — {{TASK_TITLE}}
> **Reviewed revision:** `{{REVISION_HASH}}` | **Branch:** `{{BRANCH_NAME}}`
> **Base revision:** `{{BASE_REVISION}}` | **Uncommitted scope included:** `{{UNCOMMITTED_SCOPE}}`
> **Date:** {{REVIEW_DATE}} | **Reviewer:** {{REVIEWER_ROLE}}
> **Overall verdict:** `{{OVERALL_VERDICT}}` <!-- APPROVED | CHANGES_REQUESTED | BLOCKED -->
> **Approved document revisions:** {{APPROVED_DOCUMENT_REVISIONS}}
> **Gate 1–3 approval references:** {{ACTUAL_APPROVAL_REFERENCES}}

## 1. Scope summary

- **Behavior phase:** {{SLICE_NAME}}
- **Changed files:** {{MODIFIED_FILES_COUNT}}
- **UI impact:** `{{UI_IMPACT}}` <!-- YES | NO -->
- **Planned checks:** {{PLANNED_CHECKS}}

{{#FILES}}
- `{{PATH}}` (layer: `{{LAYER}}`)
{{/FILES}}

## Acceptance criteria traceability

| AC | Implementation | Executable test or manual check | Evidence or gap | Review status |
|---|---|---|---|---|
{{AC_ROWS}}

## 2. Five-Axis Assessment

| Axis | Result | Evidence |
|---|---|---|
| Correctness | `{{CORRECTNESS_STATUS}}` | {{AC_PASS_COUNT}}/{{AC_TOTAL_COUNT}} ACs covered |
| Readability and simplicity | `{{SIMPLICITY_STATUS}}` | {{SIMPLICITY_NOTES}} |
| Clean Architecture and DI | `{{ARCHITECTURE_STATUS}}` | Hub: {{HUB_GATE_STATUS}}; analyzer: {{SYNTAX_STATUS}}; {{HUB_VIOLATIONS_COUNT}} findings; cross-file: {{CRX_STATUS}} |
| Security and data safety | `{{SECURITY_STATUS}}` | Actual secrets, parsing and data-handling checks |
| Performance and lifecycle | `{{PERFORMANCE_STATUS}}` | Resource ownership, disposal and render scope |

- **Analyzer command/result on reviewed tree:** {{ANALYZER_EVIDENCE}}
- **Full-module gate:** {{MODULE_GATE_AND_WARNING_RESOLUTION}} <!-- PASSED | FAILED | UNVERIFIED | N/A with reason -->

## 3. Bug hunt

> **Effort:** `{{BUG_HUNT_EFFORT}}` <!-- quick | standard | deep --> | **Summary:** {{BUG_HUNT_SUMMARY}}

| ID | Severity | Verdict | File:line | Defect | Failure scenario | Evidence | Fix direction |
|---|---|---|---|---|---|---|---|
{{BUG_HUNT_ROWS}}

- **Writer self-check PLAUSIBLE items resolved:** {{SELF_CHECK_FOLLOWUP}}

## 3b. Compliance findings

{{#HAS_FINDINGS}}
| Severity | File | Line | Rule | Finding | Suggested correction |
|---|---|---|---|---|---|
{{#FINDINGS}}
| `{{SEVERITY}}` | `{{FILE}}` | {{LINE}} | `{{RULE_ID}}` | {{MESSAGE}} | {{SUGGESTION}} |
{{/FINDINGS}}
{{/HAS_FINDINGS}}
{{^HAS_FINDINGS}}
No findings were observed in the reviewed scope.
{{/HAS_FINDINGS}}

### Checks not proven by the Hub

{{#UNSUPPORTED_CHECKS}}
- `{{CHECK}}`
{{/UNSUPPORTED_CHECKS}}

## 4. Runtime Visual Review Gate

- **Visual verdict:** `{{VISUAL_VERDICT}}` <!-- PASS | FAILED | BLOCKED | N/A -->
- **Target:** `{{TARGET_DEVICE}}` <!-- Chrome | iOS Simulator | Android Emulator -->
- **Evidence revision:** `{{REVISION_HASH}}`
- **Screenshot or recording:** `{{EVIDENCE_PATH}}`
- **Image inspection and Visual AC comparison:** {{IMAGE_INSPECTION}}
- **Runtime logs:** `{{RUNTIME_LOG_SUMMARY}}`

## 5. Verdict and handoff

- **Decision:** `{{OVERALL_VERDICT}}`
{{#IS_APPROVED}}
- [x] Pass this exact revision to `flutter-verification`; merge/readiness still depends on required verification PASS.
{{/IS_APPROVED}}
{{#IS_CHANGES_REQUESTED}}
- [ ] Send findings to `flutter-incremental-implementation`; a fix creates a new revision and invalidates affected earlier evidence.
{{/IS_CHANGES_REQUESTED}}
{{#IS_BLOCKED}}
- [ ] Record the unavailable source, service, environment or target; do not report PASS.
{{/IS_BLOCKED}}
