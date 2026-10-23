# 01 - Deterministic Reproduction & Reading Errors

A bug that cannot be reliably reproduced cannot be proven fixed.

## 1. Capturing Deterministic Reproduction

- **Unit Test Reproduction:**
  - If the bug is in business logic, state transitions, or data parsing, write a failing unit test in `test/modules/<feature>/` before modifying any production code.
  - The reproduction test must fail cleanly with the reported error.
- **Widget Test Reproduction:**
  - For layout overflow or UI event handling issues, write a `testWidgets(...)` scenario with fixed screen bounds.

## 2. Deciphering Flutter Stack Traces

1. **`NullCheckError: Null check operator used on a null value`:**
   - Cause: Unsafe `!` bang operator used on a null property.
   - Action: Inspect the stack trace for the exact line and replace with `?.` or guard clause.
2. **`A RenderFlex overflowed by xxx pixels on the bottom/right`:**
   - Cause: Unbounded children inside a `Row` or `Column` exceeding viewport constraints.
   - Action: Wrap expanding children in `Expanded` or `Flexible`, or wrap the column in `SingleChildScrollView`.
3. **`Unhandled Exception: type 'Null' is not a subtype of type 'String' in type cast`:**
   - Cause: Backend API returned `null` for a non-nullable model field in `fromJson`.
   - Action: Use `parseString(...)` from `app_util` with default fallback.
