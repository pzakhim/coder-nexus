# Base Unit Testing Rules (Universal)

Universal rules for developer unit tests across any technology stack. Every rule goes into the generated skill with the workspace's verified facts **and its rationale**, adapted to its tools, or cited where an automated CLI gate enforces it. All rules are **Mandatory Compliance** (there is no per-rule `P1`/`P2`/`P3` severity column).

| # | Rule | Why | Goes into |
|---|---|---|---|
| **U1** | **Test behavior, not implementation.** Assert outputs, raised errors, emitted states, and calls **at port boundaries**; never private helpers, internal call order, or private data fields. | Implementation-coupled tests break on every safe refactor and erode trust in the suite. | `SKILL`, `02` |
| **U2** | **Pass/Default + every handled Fail + Empty/Edge for each changed behavior.** Cover the success path, each failure the code handles (validation, not found, forbidden, conflict, dependency failure), and boundaries (empty, null/missing, zero, max, malformed). | Happy-path-only suites pass while production fails on real inputs. | `SKILL`, `01` |
| **U3** | **Red-to-Green regression test for every bug fix and review finding fix.** Write a test that fails on the faulty behavior first, record the red run, then fix the code and run green. | Without a red run on the unfixed code, nothing proves the test can detect the defect. | `SKILL`, `01`, `03` |
| **U4** | **Isolated and fast.** Zero live network, database, file system, OS/device plugins, or real wall clock in unit tests; replace external dependencies at their port boundary. | Environment-dependent tests are slow, flaky, or test infrastructure instead of logic. | `SKILL`, `02` |
| **U5** | **Double the port boundary, never the subject.** Use fakes or mocks for the port/adapter the subject depends on, preserving its real contract (return types, raised errors, full data shapes); never mock the class or function under test. | Mocking the subject or using a loose double makes tests pass regardless of production bugs. | `SKILL`, `02` |
| **U6** | **Never mock authorization, data-scope guards, or the database to make a test pass.** Keep policy/permission checks real in unit tests; cover SQL queries and schema constraints in integration tests. | Mocking a security guard away tests nothing about the guard and hides regressions. | `SKILL`, `02`, `03` |
| **U7** | **Deterministic execution.** Control time, IDs, randomness, ordering, and async completion (injected clock/ID factory, seeded random, awaited async, isolated per-test state). | Flaky tests train developers to ignore red builds. | `SKILL`, `02` |
| **U8** | **Specific assertions with independent expectations.** Assert exact values, error types/codes, and emitted state sequences from literal design expectations; never recompute expected values using production logic, and never write tautologies (`isNotNull` alone, `assert True`) or assertion-free tests. | Weak or recomputed assertions pass on corrupted output. | `SKILL`, `02` |
| **U9** | **One behavior per test, Arrange-Act-Assert (AAA), behavior-revealing name.** Separate Arrange, Act, and Assert; name each test for the behavior, condition, and expected outcome. | Clear failures point straight to the broken rule without debugging the test. | `SKILL`, `01`, `02` |
| **U10** | **Test path mirrors source path.** Place each unit test in the test tree mirroring its source module path and naming convention. | Tests nobody can locate next to their source module are neither run nor maintained. | `SKILL`, `01` |
| **U11** | **Reuse the workspace's existing test setup.** Use the workspace's installed test runner, async plugin, fixtures, builders, and port fakes; never introduce a competing test framework or global state override. | Parallel test setups diverge and double maintenance overhead (`EXTEND` vs `INIT`). | `SKILL`, `01`, `02` |
| **U12** | **Every new test must execute.** Confirm the test is collected, not skipped/deselected, fails for the expected reason on red, and passes on green. | An uncollected, skipped, or unrun test is `NOT_RUN`, never `PASS`. | `SKILL`, `03` |
| **U13** | **State unit test boundaries explicitly.** Report what unit tests proved and what remains for integration, contract, E2E, or visual verification. | Over-claiming unit test coverage hides untested SQL, wiring, or rendering risks. | `SKILL`, `03` |
| **U14** | **Failing test first when required.** Write the failing test before production code for domain rules, use cases/services, schemas/mappers, state machines, and all bug/finding fixes. | A test written after code passes immediately without proving it can catch a break. | `SKILL`, `01`, `03` |

**Mandatory rules (never "not adopted"):** `U2`, `U4`, `U5`, `U6`, `U12`.

---

## Unified Tool Gate (`PASS` / `FAIL`) & Review Severity (`BLOCKER` / `MAJOR` / `MINOR`)

CLI test and linter commands are strictly binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`; non-executed checks use `NOT_RUN`, `BLOCKED`, or `UNVERIFIED` per `shared_contracts/flags_and_statuses.md` §1). Reviewers grade unit test findings on the unified 3-tier scale (`shared_contracts/flags_and_statuses.md` §2):

| Severity | Finding | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | Unit test suite `FAIL`s; new test not collected/skipped (`U12`); bug/finding fix lacks red-to-green regression test (`U3`); mocked subject under test (`U5`) or mocked authorization/security guard (`U6`); edited/weakened existing test to mask a defect | `CHANGES_REQUESTED` (blocks approval) |
| `MAJOR` | Missing required Pass/Default, handled Fail, or Empty/Edge case (`U2`); live network/DB/clock in unit test (`U4`, `U7`); tautological or non-specific assertion (`U8`); test placed outside mirrored path or violating workspace convention (`U10`, `U11`) | Must be fixed before handoff |
| `MINOR` | Minor test naming polish, AAA spacing, or local fixture extraction opportunity (`U9`) | Optional improvement (never blocks approval) |

---

## Default Role Ownership

| Role | Responsibility |
|---|---|
| **Code Writer** | Writes and runs unit tests with each task (red → green); records exact CLI commands and exit codes in the hand-off |
| **Code Reviewer** | Grades case coverage (`U2`), doubles boundaries (`U5`, `U6`), and assertion strength (`U8`); reruns the suite on `REVIEW_REVISION` |
| **Test Runner** | Owns integration, contract, E2E, and visual acceptance checks — cites developer unit tests as input but never counts them as acceptance |
