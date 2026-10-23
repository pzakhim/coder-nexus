# 06 - Root-Cause Debugging Report Format

Summarize resolved defects in the task handoff following [work-item-contract handoff-and-status section 9](../../work-item-contract/references/handoff-and-status.md).

## 1. Structure

```text
### Root Cause Analysis: <Defect Title>
- **Symptom:** <Observed failure or error message>
- **Reproduction:** <Path to reproduction test>
- **Root Cause:** <Technical reason why the bug occurred>
- **Fix:** <What was changed to resolve it>
- **Prevention:** <Regression test added to prevent recurrence>
```

## 2. Example

```text
### Root Cause Analysis: Order List Screen stuck in loading on network timeout
- **Symptom:** Screen spinner never disappears when network drops.
- **Reproduction:** test/modules/orders/presentation/cubit/order_list_cubit_test.dart ("handles timeout")
- **Root Cause:** Cubit awaited repository without handling DataFailure case when ApiService timed out.
- **Fix:** Added failure pattern match to emit OrderListFailure state.
- **Prevention:** Added unit test asserting OrderListFailure state on DataFailure.
```
