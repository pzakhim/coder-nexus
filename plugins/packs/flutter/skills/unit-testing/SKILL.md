---
name: unit-testing
description: Developer unit-test standard for a Flutter / Dart app - test-first discipline (red-to-green loop), per-layer test matrix (Domain UseCases/Entities, Data Models/Mappers/DataSources, Presentation Cubit/Bloc/Notifier with Pass/Default, Fail, and Empty/Edge cases), mirrored test/ layout and naming, mocktail mocks and fakes at port boundaries, bloc_test state verification, deterministic clocks and async execution, specific assertions, focused and module flutter test commands, and red/green evidence rows. Use whenever writing or changing Flutter/Dart code that needs unit tests, fixing a bug or review finding, planning test tasks, or reviewing Flutter unit tests.
---

# Unit Testing — Flutter / Dart

A test proves behavior only if you have seen it fail for the reason it exists. Every unit test in `test/` must be 100% isolated from live HTTP endpoints, device storage, platform channels, and system clocks, deterministic across runs, and verified via CLI.

All CLI test gates (`PASS` / `FAIL`) and review severities (`BLOCKER` / `MAJOR` / `MINOR`) follow `shared_contracts/flags_and_statuses.md` and `work-item-contract` (`references/handoff-and-status.md` §9).

---

## 1. CLI Test & Quality Gates (`PASS` / `FAIL`)

Installed and verified via `coder-nexus setup tools --pack flutter` (`flutter_test`, `bloc_test`, `mocktail`, `flutter analyze`, `dart_code_linter`). Every command below is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)**:

| Gate | Command | Purpose |
|---|---|---|
| **Focused Red / Green Run** | `flutter test test/modules/<feature>/<layer>/<file>_test.dart --plain-name "<test name>"` | Run one test case to verify red failure reason and green fix (**U12**, **U14**) |
| **Module Unit Suite** | `flutter test test/modules/<feature>/` | Verify all unit tests for the touched feature module after a task |
| **Full Unit Suite** | `flutter test` | Verify the full unit suite at phase end before hand-off |
| **Static Analysis on Tests** | `dart format --output=none --set-exit-if-changed lib test && flutter analyze` | Enforce clean-code formatting and static analysis on test files (**U11**) |

---

## 2. When the Test Comes First (Red-to-Green Order)

| Change Type | Order | Reason |
|---|---|---|
| **Domain rules, UseCases, business validation, calculations** | Failing test first | Domain logic is where silent defects and calculation bugs live |
| **Cubit / Bloc / Notifier state machines and transitions (`bloc_test`)** | Failing test first | State emission order, loading/error states, and edge cases must be proven deterministically |
| **Data Models and Mappers (`fromJson`, `toJson`, `toEntity`)** | Failing test first | Missing JSON keys, null parsing errors, and type mismatches break screens at runtime |
| **Remote / Local DataSources (HTTP/storage mapping)** | Failing test first | Status code mapping and timeout/error translation must be verified at the adapter boundary |
| **Every bug fix and every review finding fix** | Reproduce with failing test first | A red run on unfixed code is the only proof the bug was real and is now resolved |
| **Changing legacy code lacking tests** | Characterization test first | Locks in existing behavior before modifying code |
| **Pure UI layout, widget styling & route/DI wiring** | May follow | Verified via `{{slot:visual-quality}}` and phase smoke checks (`{{slot:verification}}`) |

---

## 3. Core Unit Testing Rules (Mandatory Compliance)

| Rule | Principle | Why | Reference |
|---|---|---|---|
| **U1** | **Test behavior, not implementation.** Assert returned results/entities, emitted state sequences, and port calls; never private `_helpers` or internal fields. | Implementation-coupled tests break on safe refactorings. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U2** | **Pass/Default + every handled Fail + Empty/Edge.** Cover success, each handled error (400/401/403/404/500, timeout, validation), and empty/null/boundary inputs. | Happy-path-only suites pass while production fails on edge inputs. | [01-test-matrix-and-structure](references/01-test-matrix-and-structure.md) |
| **U3** | **Red-to-Green regression test for bug/finding fixes.** Reproduce the failure red first, record the red row, then fix and run green. | Prevents silent regression of fixed defects. | [01-test-matrix-and-structure](references/01-test-matrix-and-structure.md) |
| **U4** | **100% Isolated and fast.** Zero live HTTP calls, disk I/O, platform channels, or real `DateTime.now()` in unit tests. | Live I/O makes unit tests slow, flaky, and device-dependent. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U5** | **Double the port boundary, never the subject.** Mock or fake repository/usecase/client interfaces with `mocktail`; always test the real UseCase, Mapper, or Cubit. | Mocking the subject tests nothing about actual code execution. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U6** | **Never mock security or validation guards.** Keep permission/role checks and input validators real in unit tests. | Bypassing security or validation checks in tests conceals flaws. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U7** | **Deterministic execution.** Inject clocks (`DateTime Function()`), seeded `Random`, and controlled streams/futures; close Cubits/controllers in `tearDown`. | Flaky tests erode team trust in test suites. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U8** | **Specific assertions with independent expectations.** Assert exact entities, failure codes/messages, and `blocTest` state sequences against design literals; never `isNotNull` alone. | Shallow assertions pass even when corrupted data is emitted. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U9** | **One behavior per test, AAA structure, behavior-revealing name.** Group by class (`group('<Class>', ...)`), separate Arrange/Act/Assert, and name tests for behavior + condition. | Standardized structure makes failure diagnosis immediate. | [01-test-matrix-and-structure](references/01-test-matrix-and-structure.md) |
| **U10** | **Test path mirrors `lib/` source path.** Place unit tests under `test/modules/<feature>/...` mirroring `lib/modules/<feature>/...`. | Undiscoverable tests are abandoned and rot over time. | [01-test-matrix-and-structure](references/01-test-matrix-and-structure.md) |
| **U11** | **Reuse workspace test setup.** Use `flutter_test`, `bloc_test`, `mocktail`, and the active workspace profile's contracts (`EXTEND` vs `INIT`). | Competing test setups fragment the suite. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U12** | **Every new test must execute.** Verify collection, non-skipped execution, right-reason red, and `+N` green count. | An unrun or skipped test is `NOT_RUN`, never `PASS`. | [03-execution-boundaries-and-review](references/03-execution-boundaries-and-review.md) |
| **U13** | **State unit test boundaries.** Distinguish unit tests from widget/golden (`{{slot:visual-quality}}`) and integration (`{{slot:verification}}`) tests. | Over-claiming unit coverage hides UI and API integration risks. | [03-execution-boundaries-and-review](references/03-execution-boundaries-and-review.md) |
| **U14** | **Failing test first per the order table.** Run the new test red before writing production code (or stash production code to verify red). | Seeing red proves the test can detect real breaks. | [03-execution-boundaries-and-review](references/03-execution-boundaries-and-review.md) |

---

## 4. Reference Guides

| Topic | Reference |
|---|---|
| `EXTEND` vs `INIT` rule, per-layer Pass/Fail/Empty matrix, `test/` directory tree (`├──`/`└──`), and naming conventions | [01 — Test Matrix & Structure](references/01-test-matrix-and-structure.md) |
| `mocktail` `Mock`/`Fake` policy, UseCase/Mapper/Cubit (`blocTest`) code templates, AAA, independent expectations, right-reason red, and determinism | [02 — Doubles, Fixtures & Quality](references/02-doubles-fixtures-and-quality.md) |
| Focused/module `flutter test` commands, proving tests ran, Red-to-Green evidence rows, unit test boundaries, and `BLOCKER`/`MAJOR`/`MINOR` review grading | [03 — Execution, Boundaries & Review](references/03-execution-boundaries-and-review.md) |
<!-- {{profile_references}} -->

---

## 5. Relationship with Other Skills

- **Layer boundaries & ports to double**: `{{slot:clean-architecture}}`.
- **Code craft & static checks on test code**: `{{slot:clean-code}}` and `{{slot:code-simplification}}`.
- **Security guards never mocked away**: `{{slot:secure-coding-standards}}`.
- **Task loop & Red-to-Green execution**: `incremental-implementation` and `{{slot:root-cause-debugging}}`.
- **Runtime integration & visual verification**: `{{slot:verification}}` and `{{slot:visual-quality}}`.
