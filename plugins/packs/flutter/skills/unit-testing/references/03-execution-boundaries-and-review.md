# 03 — CLI Execution, Evidence, Boundaries & Review (Flutter / Dart)

Rules **U12**, **U13**, and **U14**.

---

## 1. CLI Commands & Proving the New Test Ran (`U12`)

Run commands from the Flutter project root (where `pubspec.yaml` lives). Every command is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)**:

| Step | Command | What to Verify in Output |
|---|---|---|
| **1. Focused Red Run** | `flutter test test/modules/orders/presentation/cubit/order_list_cubit_test.dart --plain-name "emits [OrderListLoading, OrderListFailure] when useCase fails"` | Exits `1` with `TestFailure` (`Expected: ... Actual: ...`), not a compile error or `No tests match` |
| **2. Focused Green Run** | `flutter test test/modules/orders/presentation/cubit/order_list_cubit_test.dart --plain-name "emits [OrderListLoading, OrderListFailure] when useCase fails"` | Exits `0`; prints `+1: All tests passed!` |
| **3. Module Suite** | `flutter test --reporter=expanded test/modules/orders/` | Lists every test name explicitly; passed count `+N` increased by the number of added tests; `0 skipped` |
| **4. Full Unit Suite** | `flutter test` | Full test suite passes with zero failures |
| **5. Static Checks on Tests** | `dart format --output=none --set-exit-if-changed lib test && flutter analyze` | Zero formatting or analyzer issues in `lib/` and `test/` |

---

## 2. Red-to-Green Evidence Rows & Result Triaging (`U12`, `U14`)

For every test-first task and every bug/finding fix, record both the Red and Green runs in the hand-off (`work-item-contract` `references/handoff-and-status.md` §4, `evidence-standard`):

| Claim | Command (+cwd) | Revision | Exit Code | Key Output | Result |
|---|---|---|---|---|---|
| `Task 2.1 red: OrderListCubit failure state not emitted` | `flutter test test/modules/orders/presentation/cubit/order_list_cubit_test.dart --plain-name "emits [OrderListLoading, OrderListFailure] when useCase fails"` | `abc1234` | `1` | `Expected: [OrderListLoading, OrderListFailure], Actual: [OrderListLoading]` | `FAIL` (expected red) |
| `Task 2.1 green: OrderListCubit failure state verified` | `flutter test test/modules/orders/presentation/cubit/order_list_cubit_test.dart --plain-name "emits [OrderListLoading, OrderListFailure] when useCase fails"` | `def5678` | `0` | `+1: All tests passed!` | `PASS` |

Compare actual output against the task's **Expected** outcome (`MATCH` / `CODE_WRONG` / `PLAN_WRONG` per `work-item-contract` `references/plan-and-task-contract.md` §3). Never edit an expectation, pass `skip: true`, or weaken an assertion to force a green run. Non-executed checks must be reported as `NOT_RUN`, `BLOCKED`, or `UNVERIFIED` — never `PASS`.

---

## 3. Unit Test Boundaries (`U13`)

Always state what unit tests proved and what remains for downstream verification:

| Concern | Proven By | Owner |
|---|---|---|
| Domain entities/validators, UseCase orchestration, Model/Mapper serialization, DataSource status mapping, Cubit/Bloc state transitions | **Developer Unit Tests** (`test/`, this skill) | Code Writer |
| Widget rendering, responsive layout, theme tokens, touch targets, visual states against `requirements.md` (`S-NN`), `design.md` (`## UI/UX mapping`), and Figma reference renders (`<stem>-SNN.png`) | **Visual & Widget Verification** (`{{slot:visual-quality}}`) | Code Writer (self-check) & Test Runner |
| Live backend API contract compatibility, navigation flows, platform plugins (camera, biometrics, secure storage) on emulator/device | **Integration & Acceptance Verification** (`{{slot:verification}}`, `quality-acceptance`) | Test Runner |

Example hand-off boundary note:
> `Unit: 12 passed (OrderModel, GetOrdersUseCase, OrderListCubit). Not covered by unit tests: OrderListScreen responsive layout and pull-to-refresh gesture — covered by visual-quality and integration verification.`

---

## 4. Review Severity (`BLOCKER` / `MAJOR` / `MINOR`)

Code Reviewers grade unit tests on the unified 3-tier scale (`shared_contracts/flags_and_statuses.md` §2):

| Severity | Finding | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | Any `flutter test` or `flutter analyze` check `FAIL`s; new test not collected or marked `skip: true` (`U12`); bug/finding fix lacks red-to-green regression test (`U3`); subject under test mocked (`U5`); security/validation guard mocked away (`U6`); existing test weakened/edited to mask a bug | `CHANGES_REQUESTED` (blocks approval) |
| `MAJOR` | Missing required Pass/Default, handled Fail, or Empty/Edge case (`U2`); live HTTP/storage/clock in unit test (`U4`, `U7`); tautological or shallow assertion (`expect(x, isNotNull)` alone, `isA<State>()` without checking state fields) (`U8`); Cubit not closed in `tearDown`; test path or profile contract violated (`U10`, `U11`) | Must be fixed in the same phase scope |
| `MINOR` | Minor `group`/`test` description polish, AAA spacing, or shared fixture extraction (`U9`) | Optional (never blocks approval) |
