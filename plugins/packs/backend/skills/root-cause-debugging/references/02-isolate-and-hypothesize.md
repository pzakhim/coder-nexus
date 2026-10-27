# 02 — Isolate, Hypothesize & Symptom Matrix (Backend / FastAPI)

Rules **D4**, **D5**, **D6**, and **D11**.

---

## 1. Minimize & Isolate the Boundary (`D4`)

1. **Minimize the Case:** Strip request fields, fixtures, and steps one at a time while re-running the reproduction until every remaining element is load-bearing. The minimized case becomes the regression test (`D8`).
2. **Diff Since Last Green:** Check `git diff <last-green-sha> -- app/ tests/ alembic/` and `git diff <last-green-sha> -- uv.lock` (dependency drift in FastAPI, Pydantic, or SQLAlchemy).
3. **Boundary Binary Search:** Along a multi-layer path (`Router → Depends → Application Service → Repository → Database`), inspect the data entering and leaving each boundary once to find the exact hop where valid data turns into a wrong value or exception.

---

## 2. Ranked Falsifiable Hypotheses (`D5`, `D6`)

Write **3–5 ranked hypotheses** before editing code. Every hypothesis must state a **falsifiable prediction** ("if X is the cause, changing Y eliminates the failure"). Test the top hypothesis with a single probe, **one variable at a time**:

```text
H1 (rank 1): <suspected cause> | predicts: <changing Y removes the failure> | probe: <command or read> | result: CONFIRMED / RULED OUT
H2 (rank 2): <suspected cause> | predicts: <...> | probe: <...> | result: RULED OUT
Fix attempts: 1/3 <what changed> -> reproduction <PASS/FAIL>
```

When a hypothesis is `CONFIRMED`, ask "why" again and trace the bad value backwards caller-by-caller until you reach the layer that owns the invariant (`D6`), then search the diff (`rg -n`) for sibling occurrences of the same mistake.

---

## 3. Temporary Tagged Instrumentation & Cleanup (`D11`)

- Prefer non-invasive CLI flags first (`-vv -s --showlocals --tb=long`, `caplog`, `--log-cli-level=DEBUG`).
- When temporary logging is needed to inspect runtime values or async ordering, tag every statement with a unique marker (e.g., `logger.debug("[DEBUG-7f3a] order=%s", order.id)`) and never log secrets, tokens, or PII.
- **Mandatory Pre-Handoff Cleanup:** Before hand-off, delete all temporary logs and verify both `rg -n "DEBUG-7f3a" app tests` (0 matches) and `uv run ruff check --select T10,T20 app tests` (`PASS`).

---

## 4. Backend Symptom → First Moves → Typical Root Cause Matrix

| Symptom | First Moves | Typical Root Cause in FastAPI / SQLAlchemy Async |
|---|---|---|
| **Exception / Chained Traceback** | Inspect the first frame under `app/` above `direct cause`; check the variable that is `None` or invalid there | Missing `None`/empty guard, violated domain precondition, or changed upstream return type |
| **Wrong Value, No Exception** | Assert the expected value at the boundary closest to the output (response schema, service return, repo return); step back one layer | Wrong operator/branch, timezone-naive vs. aware UTC `datetime`, float vs. `Decimal` rounding, Pydantic `exclude_unset` / alias drop, or stale SQLAlchemy identity-map object without `refresh` |
| **`422 Unprocessable Entity`** | Read `response.json()["detail"]` (`loc`, `msg`, `type`) and compare against the Pydantic request schema | Field/alias mismatch, Pydantic v2 strict type rejection, or misplaced path/query/body parameter in router signature |
| **`500` with `MissingGreenlet`** | Locate the ORM relationship attribute access in the `app/` frame | Lazy-loaded SQLAlchemy relationship accessed outside async context (missing `selectinload` / `joinedload`) or after `AsyncSession` closed |
| **`RuntimeWarning: coroutine ... was never awaited`** | Re-run with `uv run pytest <id> -W error::RuntimeWarning` to turn the warning into a traceback at the exact line | Missing `await` on an async repository, service, or `AsyncSession` method |
| **`IntegrityError` / `UniqueViolation` / `ForeignKeyViolation`** | Read the constraint name in `orig`; inspect write order and input values | Missing domain existence/conflict check, wrong `flush()` order, or un-isolated test data colliding across tests |
| **`UndefinedTableError` / `UndefinedColumnError`** | Compare `uv run alembic current` vs. `uv run alembic heads` and ORM models | Unapplied migration on test DB (environment → `BLOCKED`) or ORM model out of sync with migration (code defect) |
| **Multiple Alembic Heads / Broken `downgrade`** | Run `uv run alembic heads` and `uv run alembic history -v` | Branches merged without `alembic merge`, or non-reversible `downgrade()` |
| **Flaky / Order-Dependent Test Failure** | Reproduce with `--randomly-seed=<seed>`; run alone vs. after the preceding test | Shared module-level state (`C15`), un-cleared `app.dependency_overrides`, missing per-test DB rollback, or mismatched `pytest-asyncio` loop scope |
| **Async Race / Concurrent Write Corruption** | Log entry/exit timestamps with `[DEBUG-xxxx]` across `await` points | Concurrent requests updating the same row without `SELECT ... FOR UPDATE` or optimistic version check, or `asyncio.gather` sharing one `AsyncSession` |
| **Slow Request / Timeout** | Count SQL statements via `sqlalchemy.engine` log records in `caplog` before editing code | N+1 query inside a loop, unbounded query missing pagination, or blocking sync I/O (`requests`, `time.sleep`) inside `async def` |
