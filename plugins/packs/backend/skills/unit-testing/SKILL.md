---
name: unit-testing
description: Developer unit-test standard for a Backend (Python 3.12+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x async) service - test-first discipline (red-to-green loop), per-layer test matrix (Pass/Default, Fail, Empty/Edge cases), mirrored pytest layout and naming, hand-written fakes at Protocol port boundaries, httpx.MockTransport and FastAPI dependency_overrides, deterministic clocks and IDs, specific assertions, focused and full pytest commands, and red/green evidence rows. Use whenever writing or changing backend code that needs unit tests, fixing a bug or review finding, planning test tasks, or reviewing backend unit tests.
---

# Unit Testing — Backend (Python / FastAPI)

A test proves behavior only if you have seen it fail for the reason it exists. Every unit test in `tests/unit/` must be 100% isolated from live networks, databases, filesystems, and system clocks, deterministic across randomized test order (`pytest-randomly`), and verified via CLI.

All CLI test gates (`PASS` / `FAIL`) and review severities (`BLOCKER` / `MAJOR` / `MINOR`) follow `shared_contracts/flags_and_statuses.md` and `work-item-contract` (`references/handoff-and-status.md` §9).

---

## 1. CLI Test & Quality Gates (`PASS` / `FAIL`)

Installed and verified via `coder-nexus setup tools --pack backend` (`pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-randomly`, `httpx`, `ruff`, `mypy`). Every command below is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)**:

| Gate | Command | Purpose |
|---|---|---|
| **Focused Red / Green Run** | `uv run pytest tests/unit/<path>/test_<module>.py::test_<name> -v` | Run one test case to verify red failure reason and green fix (**U12**, **U14**) |
| **Module Unit Suite** | `uv run pytest tests/unit/<path>/test_<module>.py -q` | Verify all unit tests for the touched module after a task |
| **Full Unit Suite** | `uv run pytest tests/unit -q` | Verify the full unit suite (with `pytest-randomly` active) at phase end |
| **Coverage Report** | `uv run pytest tests/unit --cov=app --cov-report=term-missing -q` | Inspect uncovered branches in touched modules |
| **Static Analysis on Tests** | `uv run ruff check tests app && uv run mypy app tests` | Enforce clean-code linting and static types on test files (**U11**) |

---

## 2. When the Test Comes First (Red-to-Green Order)

| Change Type | Order | Reason |
|---|---|---|
| **Domain rules, application services / use cases, validation, calculations** | Failing test first | Business logic is where silent wrong results live |
| **Pydantic schemas and mappers (`ORM row ↔ Entity ↔ DTO`)** | Failing test first | Missing keys, alias drift, or null rules break contracts silently |
| **State transitions & FastAPI router error mapping** | Failing test first | Missed transitions and HTTP status mappings fail on rare paths |
| **Every bug fix and every review finding fix** | Reproduce with failing test first | A red run on unfixed code is the only proof the defect was real and is now gone |
| **Changing existing code that has no test** | Characterization test first | Locks in current behavior before altering the implementation |
| **Pure DI wiring (`Depends` providers, `include_router`, settings)** | May follow | Covered by phase checks of `{{slot:verification}}` |
| **Alembic migrations & SQL repository queries** | Integration test (`{{slot:verification}}`) | Unit tests never mock `AsyncSession` or run against SQLite |

---

## 3. Core Unit Testing Rules (Mandatory Compliance)

| Rule | Principle | Why | Reference |
|---|---|---|---|
| **U1** | **Test behavior, not implementation.** Assert return values, raised domain errors, state changes, and calls at `Protocol` port boundaries; never private `_helpers` or internal call order. | Implementation-coupled tests break on safe refactors. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U2** | **Pass/Default + every handled Fail + Empty/Edge.** Cover success, each handled domain error (validation, not found, forbidden, conflict, upstream error), and empty/null/boundary inputs. | Happy-path-only suites pass while production fails on real inputs. | [01-test-matrix-and-structure](references/01-test-matrix-and-structure.md) |
| **U3** | **Red-to-Green regression test for bug/finding fixes.** Reproduce the defect with a failing test first, record the red row, then fix and run green. | Prevents silent regression of fixed defects. | [01-test-matrix-and-structure](references/01-test-matrix-and-structure.md) |
| **U4** | **100% Isolated and fast.** Zero live network, PostgreSQL/SQLite database, filesystem, or real `datetime.now()` in `tests/unit/`. | Live I/O makes unit tests slow, flaky, and environment-dependent. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U5** | **Double the port boundary, never the subject.** Use hand-written fakes implementing the `Protocol` port; never mock the service/function under test. | Mocking the subject or using loose `MagicMock()` passes regardless of bugs. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U6** | **Never mock authorization, tenant/owner guards, or `AsyncSession`.** Keep policy/permission checks real; test SQL queries in `tests/integration/` on real PostgreSQL. | Mocking security guards or SQL sessions hides auth and query defects. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U7** | **Deterministic execution.** Inject `clock` (`Callable[[], datetime]` UTC), ID factories, and seeded `random.Random`; await all coroutines; clear `dependency_overrides` per test. | Flaky or order-dependent tests erode trust in the suite. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U8** | **Specific assertions with independent expectations.** Assert exact fields, `pytest.raises(SpecificError)`, and Pydantic `loc`/`type` against design literals; never only `is not None` or `assert True`. | Weak or recomputed assertions pass on wrong output (`ruff` `PT011`, `B017`). | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U9** | **One behavior per test, AAA structure, `test_<behavior>_<condition>` name.** Separate Arrange, Act, Assert; use readable `ids=` on `@pytest.mark.parametrize`. | Failing test names read directly as the broken business rule. | [01-test-matrix-and-structure](references/01-test-matrix-and-structure.md) |
| **U10** | **Test path mirrors `app/` source path.** Place unit tests under `tests/unit/<layer>/<test_module>.py` mirroring `app/`. | Undiscoverable tests are neither run nor maintained. | [01-test-matrix-and-structure](references/01-test-matrix-and-structure.md) |
| **U11** | **Reuse workspace pytest setup.** Follow existing `pyproject.toml`, `conftest.py`, fakes, and builders (`EXTEND` vs `INIT`); never mix `pytest-asyncio` with `anyio` or `unittest.TestCase`. | Competing test setups break collection and double maintenance. | [02-doubles-fixtures-and-quality](references/02-doubles-fixtures-and-quality.md) |
| **U12** | **Every new test must execute.** Verify `-v` collection, non-skipped execution (exit code 5 = no tests ran), right-reason red, and green pass. | An uncollected or skipped test is `NOT_RUN`, never `PASS`. | [03-execution-boundaries-and-review](references/03-execution-boundaries-and-review.md) |
| **U13** | **State unit test boundaries.** Explicitly report what unit tests proved and what belongs to PostgreSQL integration (`{{slot:verification}}`). | Over-claiming unit results hides untested SQL and migration risk. | [03-execution-boundaries-and-review](references/03-execution-boundaries-and-review.md) |
| **U14** | **Failing test first per the order table.** Run the new test red before writing production code (or `git stash` production code to verify red). | Seeing red proves the test can detect the defect. | [03-execution-boundaries-and-review](references/03-execution-boundaries-and-review.md) |

---

## 4. Reference Guides

| Topic | Reference |
|---|---|
| `EXTEND` vs `INIT` rule, per-layer Pass/Fail/Empty matrix, `tests/unit/` directory tree (`├──`/`└──`), and naming conventions | [01 — Test Matrix & Structure](references/01-test-matrix-and-structure.md) |
| `Real > Fake > Stub > Mock` policy, `FakeRepository`/`ASGITransport`/`MockTransport` code templates, AAA, independent expectations, right-reason red, and determinism | [02 — Doubles, Fixtures & Quality](references/02-doubles-fixtures-and-quality.md) |
| Focused/full `pytest` commands, proving tests ran, Red-to-Green evidence rows, unit test boundaries, and `BLOCKER`/`MAJOR`/`MINOR` review grading | [03 — Execution, Boundaries & Review](references/03-execution-boundaries-and-review.md) |

---

## 5. Relationship with Other Skills

- **Layer boundaries & `Protocol` ports to double**: `{{slot:clean-architecture}}`.
- **Code craft & static checks on test code**: `{{slot:clean-code}}` and `{{slot:code-simplification}}`.
- **Security & tenant-scope guards never mocked away**: `{{slot:secure-coding-standards}}` and `api-contract-design`.
- **Task loop & Red-to-Green execution**: `incremental-implementation` and `{{slot:root-cause-debugging}}`.
- **PostgreSQL integration, migrations, and live API verification**: `{{slot:verification}}` and `quality-acceptance`.
