# 03 — CLI Execution, Evidence, Boundaries & Review (Backend / FastAPI)

Rules **U12**, **U13**, and **U14**.

---

## 1. CLI Commands & Proving the New Test Ran (`U12`)

Run commands from the directory containing `pyproject.toml`. Use the workspace's configured runner (`uv run` by default; `poetry run` or activated `.venv` if the workspace uses them). Every command is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)**:

| Step | Command | What to Verify in Output |
|---|---|---|
| **1. Focused Red Run** | `uv run pytest tests/unit/application/test_orders.py::test_cancel_order_when_already_shipped_raises_and_does_not_commit -v` | Exits `1` with `AssertionError` or `DID NOT RAISE` (never exit `5` or `ImportError`) |
| **2. Focused Green Run** | `uv run pytest tests/unit/application/test_orders.py::test_cancel_order_when_already_shipped_raises_and_does_not_commit -v` | Exits `0`; output explicitly prints `...::test_<name> PASSED` |
| **3. Module Suite** | `uv run pytest tests/unit/application/test_orders.py -q` | Passed count increased by the exact number of added tests; `0 skipped` |
| **4. Full Unit Suite** | `uv run pytest tests/unit -q` | Full unit suite passes with `pytest-randomly` active (never pass `-p no:randomly` to hide order bugs) |
| **5. Lint & Types on Tests** | `uv run ruff format --check tests app && uv run ruff check tests app && uv run mypy app tests` | Zero lint, formatting, or static type errors in test or production code |

> **Reproducing a `pytest-randomly` Order Failure:** When a test fails under a specific random seed, copy the printed seed and reproduce deterministically with `uv run pytest tests/unit --randomly-seed=<seed> -q`, then fix the leaked state (`U7`).

---

## 2. Red-to-Green Evidence Rows & Result Triaging (`U12`, `U14`)

For every test-first task and every bug/finding fix, record both the Red and Green runs in the hand-off (`work-item-contract` `references/handoff-and-status.md` §4, `evidence-standard`):

| Claim | Command (+cwd) | Revision | Exit Code | Key Output | Result |
|---|---|---|---|---|---|
| `Task 2.1 red: shipped order cancellation not refused` | `uv run pytest tests/unit/application/test_orders.py::test_cancel_order_when_already_shipped_raises_and_does_not_commit -q` | `abc1234` | `1` | `Failed: DID NOT RAISE <class 'OrderNotCancellableError'>` | `FAIL` (expected red) |
| `Task 2.1 green: shipped order refusal verified` | `uv run pytest tests/unit/application/test_orders.py::test_cancel_order_when_already_shipped_raises_and_does_not_commit -q` | `def5678` | `0` | `1 passed in 0.08s` | `PASS` |

Compare actual output against the task's **Expected** outcome (`MATCH` / `CODE_WRONG` / `PLAN_WRONG` per `work-item-contract` `references/plan-and-task-contract.md` §3). Never edit an expectation, add `@pytest.mark.skip` / `xfail`, or weaken an assertion to force a green run. Non-executed checks must be reported as `NOT_RUN`, `BLOCKED`, or `UNVERIFIED` — never `PASS`.

---

## 3. Unit Test Boundaries (`U13`)

Always state what unit tests proved and what remains for downstream verification:

| Concern | Proven By | Owner |
|---|---|---|
| Domain invariants, service orchestration, Pydantic schemas, mappers, router HTTP mapping, outbound adapter parsing | **Developer Unit Tests** (`tests/unit/`, this skill) | Code Writer |
| SQL queries, tenant/owner `WHERE` filters in SQL, DB constraints, `ON CONFLICT`, eager loading / N+1 | **PostgreSQL Integration Tests** (`tests/integration/`, never SQLite — `{{slot:verification}}`) | Code Writer (when assigned an integration task) & Test Runner |
| Alembic migrations, transaction isolation, row locks, concurrent writes | **Migration & Integration Verification** (`{{slot:verification}}`) | Test Runner |
| Live API authorization matrix (`role × tenant × endpoint`) and end-to-end contract compliance | **Acceptance Verification** (`{{slot:verification}}`, `quality-acceptance`) | Test Runner |

Example hand-off boundary note:
> `Unit: 16 passed (domain, OrderService, schemas, router). Not covered by unit tests: SQL tenant filter in SqlAlchemyOrderRepository.list_for_tenant — covered by tests/integration/repositories/test_orders_repo.py.`

---

## 4. Review Severity (`BLOCKER` / `MAJOR` / `MINOR`)

Code Reviewers grade unit tests on the unified 3-tier scale (`shared_contracts/flags_and_statuses.md` §2):

| Severity | Finding | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | Any unit test, `ruff`, or `mypy` check `FAIL`s; new test not collected, skipped, or deselected (`U12`); bug/finding fix lacks red-to-green regression test (`U3`); subject under test mocked (`U5`); authorization/tenant guard or `AsyncSession` mocked to pass (`U6`); existing test weakened/edited to mask a bug | `CHANGES_REQUESTED` (blocks approval) |
| `MAJOR` | Missing required Pass/Default, handled Fail, or Empty/Edge case (`U2`); live network/DB/clock in `tests/unit/` (`U4`, `U7`); tautological or weak assertion (`is not None` alone, `pytest.raises(Exception)`) (`U8`); `app.dependency_overrides` not cleared; test path or setup violates workspace convention (`U10`, `U11`) | Must be fixed in the same phase scope |
| `MINOR` | Minor test naming improvement, AAA spacing, or local builder extraction (`U9`) | Optional (never blocks approval) |
