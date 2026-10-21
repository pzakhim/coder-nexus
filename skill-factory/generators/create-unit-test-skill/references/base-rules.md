# Base rules (generic, every workspace)

Generalised from Coder Nexus `plugins/packs/backend/skills/unit-test`, `plugins/packs/flutter/skills/unit-test` and the unit-test practice of a real fullstack workspace. Each rule goes into the generated skill with the workspace's facts **and its reason**, adapted to its tools, or marked "not adopted" with a reason. If a gate already enforces a rule, cite the gate.

| # | Rule | Why | Default severity | Goes into |
|---|---|---|---|---|
| U1 | **Test behavior, not implementation.** Assert outputs, raised errors, emitted states and calls **at port boundaries**; not private helpers, call order inside the subject, or internal data shapes. | Implementation-coupled tests break on every refactor and stop being trusted. | P2 | 04 |
| U2 | **Happy + negative + edge for every changed behavior.** At least: the success path, each failure the code handles (validation, not found, forbidden, conflict, dependency failure), and boundaries (empty, null/missing, zero, max, malformed). | Happy-path-only suites pass while the code fails in production. | P1 | 01 |
| U3 | **Regression test for bug fixes.** A test that fails on the faulty behavior and passes after the fix, when practical. | Without it the same bug returns silently. | P2 | 01, 04 |
| U4 | **Isolated and fast.** No live network, database, file system, device plugins or real clock in unit tests; external dependencies are replaced at their boundary. | Slow or environment-dependent tests are skipped, flaky, or prove the environment instead of the code. | P1 | 03 |
| U5 | **Double the boundary, never the subject.** Fake or mock the port/adapter the subject depends on, keeping its real contract (return types, raised errors); never mock the function under test. | A mocked subject or an unrealistic double makes the test pass whatever the code does. | P1 | 03 |
| U6 | **Never mock authorization or the database to make a test pass.** Behavior that depends on them is covered by integration tests; unit tests use fakes that keep the rules. | Mocking the guard away tests nothing about the guard and hides security regressions. | P1 | 03, 06 |
| U7 | **Deterministic.** Control time, randomness, ordering and concurrency (injected clock, seeded random, awaited async). | Flaky tests train everyone to ignore red. | P1 | 04 |
| U8 | **Specific assertions.** Assert exact values, error types/messages and emitted states; no tautologies (`isNotNull` alone, `expect(true)`), no assertion-free tests. | A weak assertion passes on wrong output. | P2 | 04 |
| U9 | **One behavior per test, AAA structure, behavior-revealing name** (`test_<behavior>_<condition>` or the workspace's pattern). | Clear failures point to the broken behavior without debugging the test. | P2 | 02, 04 |
| U10 | **Location mirrors source;** follow the workspace's test tree and file naming. | Tests that cannot be found next to their code are not maintained. | P2 | 02 |
| U11 | **Reuse the existing setup.** Existing fixtures, factories, fakes and the one test framework already in use; no second framework, no global overrides (e.g. event loop). | Parallel setups diverge and double maintenance. | P2 | 03 |
| U12 | **The new test must run.** Confirm it appears in the runner output and passes; a skip, a missing dependency or "not collected" is not a pass. | A test that never runs is not evidence. | P1 | 05 |
| U13 | **Know the limits.** Unit results do not prove authorization at the API, SQL/migrations, server/client rendering or real integrations; say what is left to integration/E2E. | Over-claiming unit results hides untested risk from reviewers and testers. | P2 | 06 |
| U14 | **TDD when the plan asks.** Write the failing test first, see it fail for the right reason, then implement. | Seeing the test fail proves it can detect the bug. | P3 | 05 |

**Never "not adopted":** U2, U4, U5, U6, U12.

## Who does what (default)

| Role | Unit tests |
|---|---|
| Code Writer | Writes and runs them with each task; reports evidence |
| Code Reviewer | Grades assertions and coverage of cases; reruns the suite on the reviewed revision |
| Test Runner | Owns integration, contract, E2E and visual checks — not unit tests |

Keep the workspace's own roles and evidence locations when they exist (P5).
