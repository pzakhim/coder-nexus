# 02 - Verification Before Reporting

Never report speculative defects without verifying their feasibility.

## 1. The Verification Standard

Before declaring a bug finding:
1. **Trace the Execution Flow:** Walk through the code path from input to execution. Confirm that the buggy condition is realistically reachable.
2. **Check Existing Defenses:** Verify that an upstream layer or validator doesn't already sanitize or guard the condition.
3. **Prove the Failure:**
   - For logic/parsing bugs: Verify by crafting a test case input that breaks the code.
   - For lifecycle leaks: Verify the absence of a `dispose()` or `cancel()` call in the state class.
   - For layout bugs: Check if constraints passed by parent widgets allow unconstrained expansion.

## 2. Confidence Grading

- **`CONFIRMED`:** Proven via trace, test case, or definitive code omission (e.g. missing `dispose()` or raw bang operator on nullable API response).
- **`PLAUSIBLE`:** High risk under specific edge conditions (e.g. race condition under extreme network latency).
