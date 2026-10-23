---
name: unit-testing
description: Developer unit-test standard for Flutter Clean Architecture (UseCases, Cubit/Bloc, Data Mappers, Models, Data Sources) - test-first discipline (when failing test comes first), Arrange-Act-Assert, mocktail mocks and fakes, bloc_test state verification, boundary probing, and red/green evidence.
---

# Flutter Clean Architecture Unit Testing

A test proves behavior only if you have seen it fail for the reason it exists. Write isolated, deterministic developer unit tests that verify domain logic, state transitions, data conversions, and error handling.

Apply the approved profile through [core-package-usage](../flutter-core-package-usage/SKILL.md). Finding severities follow [work-item-contract handoff-and-status section 9](../work-item-contract/references/handoff-and-status.md).

## 1. When the Test Comes First (Test-First Matrix)

| Change | Order | Reason |
|---|---|---|
| Domain rules, UseCases (`UseCasePower<T, P>`), business validation | Failing test first | Logic is where silent defects and incorrect calculations live. |
| Cubit state machines and transitions (`bloc_test`) | Failing test first | State emission order and edge cases must be proven deterministically. |
| Data Mappers and Models (`fromJson`, `toJson`, `mapToEntity`) | Failing test first | Missing keys, null parsing errors, and type mismatches break screens. |
| **Every bug fix and review finding fix** | Reproduce with failing test first | A red run is the only proof the bug was real and is now resolved. |
| Changing legacy code lacking tests | Characterization test first | Establishes safety net before modifying existing behavior. |
| Pure UI layout & Widget assembly | May follow (widget/golden tests) | Verified via `{{slot:visual-quality}}` and manual layout inspection. |
| Route registration, DI registration (`getIt`) | May follow | Pure wiring covered by phase smoke checks. |

## 2. Core Testing Rules (U1–U14)

| # | Rule | Why | Severity | Reference |
|---|---|---|---|---|
| **U1** | **Test behavior, not implementation.** Assert emitted states, returned entities, and port interactions. | Implementation-coupled tests break on internal refactorings. | P2 | [01-what-to-test](references/01-what-to-test.md) |
| **U2** | **Pass, Fail, and Empty cases.** Never test only happy paths; cover HTTP 400, 401, 500, timeouts, and empty lists. | Happy-path-only suites pass while production fails under real conditions. | P1 | [04-test-quality](references/04-test-quality.md) |
| **U3** | **Red-to-Green on bug fixes.** Every bug fix starts with a failing regression test proving the failure. | Prevents silent regression of previously fixed defects. | P1 | [04-test-quality](references/04-test-quality.md) |
| **U4** | **100% Isolated & Fast.** Never call live HTTP endpoints, device disk, or OS plugins. | Live I/O makes unit tests slow, flaky, and environment-dependent. | P1 | [03-doubles-and-fixtures](references/03-doubles-and-fixtures.md) |
| **U5** | **Double the port, never the subject.** Mock repository interfaces with `mocktail`; test the real UseCase or Cubit. | Mocking the subject under test tests nothing about actual code execution. | P1 | [03-doubles-and-fixtures](references/03-doubles-and-fixtures.md) |
| **U6** | **Never mock security guards.** Do not mock authorization or data validation to force a test to pass. | Bypassing security checks in tests conceals authorization flaws. | P1 | [03-doubles-and-fixtures](references/03-doubles-and-fixtures.md) |
| **U7** | **Deterministic execution.** No dependency on system clocks, random values, or unawaited async operations. | Flaky tests erode team trust in test suites. | P1 | [04-test-quality](references/04-test-quality.md) |
| **U8** | **Specific assertions.** No shallow assertions (`expect(result, isNotNull)`); assert concrete values and failure states. | Vague assertions pass even when corrupted data is produced. | P2 | [04-test-quality](references/04-test-quality.md) |
| **U9** | **Arrange-Act-Assert (AAA).** Structure tests clearly with distinct setup, execution, and verification phases. | Standardized structure makes failure diagnosis immediate. | P2 | [04-test-quality](references/04-test-quality.md) |
| **U10** | **Path mirrors source.** Unit test path under `test/` must mirror `lib/` (e.g. `test/modules/<feature>/...`). | Undiscoverable tests are abandoned and rot over time. | P2 | [02-location-and-naming](references/02-location-and-naming.md) |
| **U11** | **Standard tooling.** Use `flutter_test`, `bloc_test`, and `mocktail`. Do not invent custom test runners. | Divergent test frameworks create fragmentation and maintenance overhead. | P2 | [03-doubles-and-fixtures](references/03-doubles-and-fixtures.md) |
| **U12** | **Tests must execute.** Ensure tests are collected and reported as passed evidence. | An unrun test provides zero verification value. | P1 | [05-running-and-evidence](references/05-running-and-evidence.md) |
| **U13** | **State testing boundaries.** Clearly distinguish unit tests from widget, integration, or visual tests. | Over-claiming unit coverage hides UI integration risks. | P2 | [06-test-boundaries](references/06-test-boundaries.md) |
| **U14** | **Test-first when required.** Follow the order table above; seeing red proves failure detectability. | Tests written after code often fail to detect real breaks. | P2 | [01-what-to-test](references/01-what-to-test.md) |

## 3. Starter Templates

Reference implementations are available under `templates/`:
- `templates/usecase_test.dart.tpl`
- `templates/mapper_test.dart.tpl`
- `templates/cubit_test.dart.tpl`
