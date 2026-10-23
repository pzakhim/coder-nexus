# 04 - Test Quality & Edge Probing

High-quality unit tests rigorously probe boundaries and provide definitive proof of correctness.

## 1. AAA Pattern (Arrange - Act - Assert)

Every unit test must have three explicit, clearly separated phases:
1. **Arrange:** Set up test dependencies, configure mock returns, instantiate subject under test.
2. **Act:** Call the single method or trigger the specific Cubit action.
3. **Assert:** Check returned results, emitted states, and mock interactions.

## 2. Eliminating Tautologies & Shallow Assertions

- **Forbidden:**
  - `expect(result, isNotNull);` - Passes even if `result` contains completely broken or empty data.
  - `expect(true, isTrue);` - Tautological assertion proving nothing.
- **Required:**
  - Assert exact failure messages: `expect(result.message, equals('Order not found'));`.
  - Assert specific error types and codes.
  - Assert exact emitted state sequences in `bloc_test`.

## 3. Boundary & Edge Case Probing

Every model, mapper, and usecase test suite must probe:
- **Null handling:** Omitted optional fields in JSON maps.
- **Empty collections:** Empty lists `[]` vs lists with elements.
- **Numeric limits:** Zero `0`, negative numbers, floating point parsing.
- **String variations:** Empty strings `""`, strings with whitespace, special Unicode characters.
