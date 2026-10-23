# 03 - Fixing the Root Cause & Preventing Regressions

Fix the underlying defect without patching around it or introducing new risks.

## 1. Principles of a Clean Fix

- **Fix the Source, Not the Symptom:**
  - If a variable is unexpectedly null, determine WHY it became null rather than scattering `?? ''` throughout the presentation layer.
  - If a widget overflows, adjust layout flex constraints rather than artificially shrinking font sizes.
- **Never Paper Over with Try-Catch:**
  - Wrapping a broken function in a broad `try-catch` block converts a reproducible bug into a silent corrupted state.

## 2. Regression Prevention

- The reproduction test written in step 1 becomes a permanent regression test in the test suite.
- Re-run the full module test suite:
  ```bash
  flutter test test/modules/<feature>/
  ```
- Ensure zero other tests were broken by the fix.
