# 02 — Test Doubles, Fixtures & Assertion Quality (Flutter / Dart)

Rules **U1**, **U4**, **U5**, **U6**, **U7**, **U8**, **U9**, and **U11**.

---

## 1. Doubles Hierarchy in `mocktail`: `Real > Fake > Stub > Mock` (`U4`, `U5`, `U6`)

| Dependency | What to Use in `test/` | Forbidden (`BLOCKER` / `MAJOR`) |
|---|---|---|
| **Subject under test & pure collaborators (`Entity`, `ValueObject`, `Model`, `Mapper`, validator)** | **Real** implementation | Mocking the UseCase, Mapper, or Cubit under test (`U5`) |
| **Port boundaries (`Repository` in UseCase test, `UseCase` in Cubit test, `DataSource` in Repository test)** | `class MockX extends Mock implements X {}` (`mocktail`) | Calling live network, disk storage, or platform channels (`U4`) |
| **Custom parameter types passed to `any()` / `captureAny()`** | `class FakeXParams extends Fake implements XParams {}` registered via `registerFallbackValue(...)` in `setUpAll` | Leaving fallback unregistered (`mocktail` runtime error) |
| **Permission, role & input validation guards** | **Real** validation/guard code | Mocking a guard to bypass validation or permission checks (`U6`) |

---

## 2. Flutter / `bloc_test` / `mocktail` / Hybrid-E2E Contracts (`U1`, `U7`, `U8`, `U11`)

*(For workspace profile-specific result/use-case wrappers, see the active profile's `testing-contracts.md` guide.)*

- **Domain UseCase (`mocktail`)**: Stub the Repository port (`when(() => mockRepo.op(any())).thenAnswer(...)`), assert exact returned entity/failure, and verify single port invocation (`verify(() => mockRepo.op(tParams)).called(1)` + `verifyNoMoreInteractions(mockRepo)`).
- **Data Model & Mapper**: Use plain deterministic JSON maps in `test/fixtures/`. Assert every mapped field on complete payloads, missing/null optional fields, empty lists `[]`, and numeric coercion (`int` vs `double` vs numeric string), plus fail-fast refusal on missing mandatory fields.
- **Presentation Cubit / Bloc (`bloc_test`)**:
  - Assert `initial` state explicitly and close the Cubit in `tearDown(() => cubit.close())`.
  - Assert full emitted state sequences (`expect: () => const [Loading(), Loaded(items)]`, `[Loading(), Empty()]`, `[Loading(), Failure(message)]`) with concrete data values — never `isA<State>()` alone when state carries fields.
  - Verify validation guards reject bad input without calling downstream UseCases (`verifyNever(...)`).
- **Golden Tests (`golden_screenshot`, when approved)**: Cover all 4 visual states (`Loading`, `Content`, `Empty`, `Error`) with `await tester.loadAssets()` (`{{slot:visual-quality}}` `02-golden-screenshot-workflow.md`).
- **Optional Local `integration_test/` (Hybrid E2E)**: When scheduled in Gate 3 plan, initialize `IntegrationTestWidgetsFlutterBinding.ensureInitialized()`, drive full screen flows against approved `FE_MOCKOON` or safe test environments using deterministic widget `Key`s, and assert visible UI outcomes without hardcoding arbitrary `Future.delayed` sleeps (prefer `pumpAndSettle` or bounded polling helpers).

---

## 3. Right-Reason Red Failure, Independent Expectations & Mutation Check (`U7`, `U8`, `U14`)

| Red Run Output | Meaning | Action |
|---|---|---|
| `TestFailure` (`Expected: ... Actual: ...`) naming the missing behavior | **Right reason** | Write the minimal production code to make it pass |
| Test passes immediately (`+1: All tests passed!`) | Behavior already exists or assertion is tautological | Fix the test so it fails when the target behavior is absent |
| Compilation error, missing `registerFallbackValue`, `NullCheckError` in setup | **Not red yet** (broken test setup) | Fix the setup and re-run until the assertion itself fails |
| `No tests match regular expression` / skipped | **Not run (`NOT_RUN`)** | Fix `--plain-name` or file path; never record as red or green |

- **Independent Literal Expectations (`U8`):** Assert concrete expected literals from `design.md` (`equals(1500)`). Never write `expect(result, isNotNull)` or `expect(true, isTrue)` as the sole assertion.
- **Determinism (`U7`):** Inject `DateTime Function()` for time-sensitive logic, use `Random(seed)` for randomness, await all futures/streams, and close Cubits/controllers in `tearDown`.
- **Pre-Handoff Mental Mutation Check:** Verify at least one test fails if you flip a branch condition, return `Failure` instead of `Success`, omit a Cubit state emission, or drop a field in `toEntity()`.
