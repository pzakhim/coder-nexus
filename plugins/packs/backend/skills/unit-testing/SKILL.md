---
name: unit-testing
description: Developer unit-test standard for a Backend (Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x async) service - when a failing test must come first and how to see it fail for the right reason, what to test per layer with the required Pass/Default, Fail and Empty cases, pytest layout and naming, hand-written fakes at port boundaries, httpx MockTransport and dependency_overrides, deterministic time and ids, specific assertions, focused and full pytest commands and red/green evidence rows. Use whenever the Code Writer writes or changes backend code that needs a test, fixes a bug or a review finding, when Planning names test paths, Acceptance Criteria and Expected red/green runs in a task, and when the Code Reviewer grades backend tests, even if the request only says "add tests", "pytest", "TDD" or "regression test". Not for integration against a real database, contract compliance or live API checks (those are verification and acceptance).
---

# Unit Testing — Backend (Python / FastAPI)

A test proves something only if you have seen it fail for the reason it exists. Reason: a test written after the code passes at once, so nobody knows whether it can detect the defect it claims to guard.

Baseline: pytest + pytest-asyncio, httpx `AsyncClient`, `unittest.mock` only at external edges, ruff, mypy, `uv`. Layout: flat. Paths such as `app/` and `tests/unit/` are conventions; the workspace's `pyproject.toml`, `conftest.py` files and existing test tree win.

## For every behavior change

1. Decide whether the test comes first (table below); the plan wins where a task says so explicitly.
2. Find the subject's layer and its required cases in [01 what to test](references/01-what-to-test.md); case data comes from the Pass/Default, Fail and Empty rows of `design.md`.
3. Put the test where [02 location and naming](references/02-location-and-naming.md) says, named by behavior.
4. **Name the break**, write one test, double only the port boundary ([03 doubles and fixtures](references/03-doubles-and-fixtures.md)).
5. Run it **red** with the focused command and check the failure reason ([04 test quality](references/04-test-quality.md#right-reason-failure)).
6. Write the least code that makes it pass; run it **green**, then the task's Acceptance Criteria ([05 running and evidence](references/05-running-and-evidence.md)).
7. Next behavior. One behavior per cycle; never all tests first and all code after. Reason: bulk tests describe imagined behavior and harden before the design has taught you anything. Clean-up belongs to `{{slot:code-simplification}}` at phase end, not to this loop.

## When the test comes first

| Change | Order | Reason |
|---|---|---|
| Domain rules, use cases / services, validation, calculations | Failing test first | Logic is where silent wrong results live |
| Pydantic schemas and mappers of a contract (ORM row ↔ entity ↔ DTO) | Failing test first | A wrong key, alias or null rule breaks the other side unseen |
| State transitions (status fields, workflows) | Failing test first | Missed transitions show up only on rare paths |
| **Every bug fix and every review finding fix** | Reproduce with a failing test first | The red run is the only proof the defect was real and is now gone |
| Changing existing code that has no test | Characterization test of current behavior first, then the change | Shows what the change really altered |
| Pure wiring (dependency providers, `include_router`, settings objects, module exports) | May follow; covered by phase checks of `{{slot:verification}}` | No logic of its own to drive |
| Alembic migrations, SQL queries, generated code | May follow; proven by integration checks (`{{slot:verification}}`) or the first consumer | A unit test cannot see the real database or generator |
| Config, docs, constants with no behavior | No test | Nothing observable to break |

"May follow" never means "may skip" when the task's Acceptance Criteria name a test. Production code written before a required failing test: set that change aside (`git stash` or revert the hunk), run the test red against the old code, then restore the change. Reason: without the red run the test is unproven.

## Rules

Severity for a broken rule is `P1`/`P2`/`P3`; defects found by a test use `BLOCKER`/`MAJOR`/`MINOR` + `CONFIRMED`/`PLAUSIBLE` ([handoff-and-status §9](../work-item-contract/references/handoff-and-status.md)).

| # | Rule | Why | Severity | Enforced by |
|---|---|---|---|---|
| U1 | Test behavior, not implementation: assert returns, raised errors, state and calls at port boundaries | Implementation-coupled tests break on every refactor and stop being trusted | P2 | Review |
| U2 | Pass/Default + every handled Fail + Empty/edges for each changed behavior | Happy-path-only suites pass while the code fails in production | P1 | Review |
| U3 | Every bug fix and finding fix starts with a red regression test | Without it the same bug returns silently | P1 | Review, red evidence row |
| U4 | No live network, database, file system or real clock in `tests/unit/` | Environment-dependent tests are slow, flaky or prove the environment | P1 | Review; `httpx.MockTransport` refuses unknown URLs |
| U5 | Double the port, never the subject; a double keeps the real contract | A mocked subject or loose fake passes whatever the code does | P1 | Review |
| U6 | Never mock authorization, data-scope rules or the database to make a test pass | Mocking the guard tests nothing about the guard and hides security regressions | P1 | Review |
| U7 | Deterministic: injected clock and ids, seeded randomness, awaited async, isolated state | Flaky tests train everyone to ignore red | P1 | Review |
| U8 | Specific assertions with independent literal expectations; no tautologies, no assertion-free tests | A weak or recomputed assertion passes on wrong output | P2 | Review; ruff `PT011`, `B017` where enabled |
| U9 | One behavior per test, Arrange-Act-Assert, `test_<behavior>_<condition>` name | A failing name reads as the broken rule | P2 | Review |
| U10 | Test path mirrors the source path | Tests nobody can find are not maintained | P2 | Review |
| U11 | Reuse the existing pytest setup, fixtures and fakes; no second framework or async plugin | Parallel setups diverge and double maintenance | P2 | Review |
| U12 | The new test must run: collected, not skipped, red then green | A test that never ran is not evidence | P1 | Evidence rows (`evidence-standard`) |
| U13 | State what unit tests did not prove | Over-claiming hides untested risk | P2 | [06 boundaries](references/06-test-boundaries.md) |
| U14 | Failing test first per the table above | Seeing it fail proves it can detect the defect | P2 | Red evidence row |

## Never

| Never | Reason |
|---|---|
| Edit an expectation, delete an assertion, add `skip`/`xfail` to match the code | Turns a found defect into a hidden one; if the design is wrong it is `PLAN_WRONG` ([plan-and-task-contract §3](../work-item-contract/references/plan-and-task-contract.md)) |
| Tautological asserts (expected recomputed like the code, only `is not None`) | Passes by construction, cannot disagree with the code |
| Change detectors (a constant's value, exact wording, private structure) | Fail on every decision, sleep through every defect |
| Assertions on the mock itself (`mock.assert_called()` with no arguments as the only check) | Proves the mock exists, says nothing about the code |
| Production methods or flags only tests use | Test needs leak into the shipped surface |
| Count a skipped, uncollected or not-run test as passing | A test that never ran is not evidence |

A green run that later fails in review or acceptance is `CODE_WRONG`: reproduce it with a failing test first, then `{{slot:root-cause-debugging}}`.

## Which file to read

| Doing | Read |
|---|---|
| Which cases to write per layer | [01-what-to-test.md](references/01-what-to-test.md) |
| Where the test goes, what it is called | [02-location-and-naming.md](references/02-location-and-naming.md) |
| Fakes, mocks, fixtures, async setup | [03-doubles-and-fixtures.md](references/03-doubles-and-fixtures.md) |
| Right-reason red, naming the break, assertions, determinism | [04-test-quality.md](references/04-test-quality.md) |
| Commands, "did it run?", evidence rows | [05-running-and-evidence.md](references/05-running-and-evidence.md) |
| What unit tests cannot prove, who covers it | [06-test-boundaries.md](references/06-test-boundaries.md) |
| Starter files | [templates/](templates/) |
| Where the ideas come from | [sources.md](references/sources.md) |

## Relationship with other skills

- Layers, ports and which boundary is doubled: `{{slot:clean-architecture}}`. Test code follows `clean-code` / `{{slot:clean-code}}` too.
- Task loop, focused task check and phase checks: `incremental-implementation`. Task fields and the red/green **Expected**: `work-item-contract`.
- Error codes and response shapes a router test asserts: `api-contract-design` (pack skill).
- Integration against PostgreSQL, contract compliance, live API: `{{slot:verification}}` and `quality-acceptance` (Test Runner).
- A seam the design does not have: `NEEDS_CONTEXT` or `change-control`, never a test-only hook.
