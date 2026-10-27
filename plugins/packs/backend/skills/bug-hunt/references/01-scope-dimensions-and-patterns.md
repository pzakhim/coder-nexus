# 01 — Scope, Dimensions, and Backend Bug Patterns

> Topic: Fixed revision scope, caller search, cold pass, the 7 defect dimensions, and Python/FastAPI/SQLAlchemy/Alembic failure patterns (`H1`–`H5`)

## 1. Fix the Scope (`H2`, `H3`)

- **Revision (`H2`):** Record `BASE_REVISION` and `REVIEW_REVISION` from the hand-off header ([handoff-and-status](../../work-item-contract/references/handoff-and-status.md) §1), plus staged, unstaged, and untracked files belonging to the item (`git status --short`, `git diff --stat <BASE_REVISION>..<REVIEW_REVISION>`). Review exactly that tree. The Code Writer's self-check runs on the phase diff before commit; the Reviewer runs on the committed `REVIEW_REVISION` only.
- **Whole Context (`H3`):** Read each changed hunk with its whole enclosing function, class, router module, or migration file so guards, early returns, and `finally` blocks outside the hunk are visible.
- **Callers (`H3`):** For each changed public symbol, find and read its callers. A broken caller outside the diff is in scope because most regressions surface there:
  - Function or method signature, return type, `None`-ability, raised exceptions (`HTTPException` status, domain errors, `NoResultFound`).
  - Pydantic model fields, aliases, defaults, `model_config` (`extra`, `populate_by_name`).
  - Route path, method, status code, `response_model`, dependency (`Depends(...)`) signature.
  - SQLAlchemy model column, nullability, relationship loading, table / constraint name.
  - Settings keys, event or message payloads, background task arguments.
- **Caller Search (Read-Only):**
  - `rg -n -w "<symbol>" app tests` for Python references.
  - `rg -n "\"<json_key>\"|'<json_key>'" app tests` for serialized keys and aliases.
  - `rg -n "<path_fragment>" app tests` for route consumers and tests.
  - GitNexus `context` / `impact`, where configured, for call graphs.

---

## 2. Cold Pass First (`H4`)

Hunt from the code **before** reading `requirements.md`, `design.md`, `api_contract.json`, the phase file, or the hand-off's Concerns. Read them afterwards only to decide whether a suspicious behavior is intended (a `D-NN` decision or an AC) or a defect.

---

## 3. The Seven Defect Dimensions (`H5`)

Walk the scope once per dimension and write every suspicion as `file:line — hypothesis`:

1. **Logic and data flow** — wrong comparison or operator, off-by-one in `offset` / slicing / `range`, inverted flag, wrong variable, value overwritten in a loop, truthiness used for "missing" (`if not qty` treats `0` as absent), `Decimal` vs `float`, `round()` banker's rounding, timezone or unit mismatch.
2. **Error and edge paths** — `None` or missing key, empty result (`scalars().first()` → `None`), first / last page, `scalar_one()` raising on 0 or 2 rows, failed or slow external call (`httpx` timeout, retry), partial success across several writes, validation bypassed on one path (a second endpoint or a background job writing the same data).
3. **State, async, and lifecycle** — coroutine not awaited, blocking call inside `async def`, one `AsyncSession` used by concurrent tasks, attribute access after `commit()` (expired instance → lazy I/O), lazy relationship load in async code, work done after commit or after the session closed (`BackgroundTasks`), check-then-act races, lost updates, client or connection not closed on the error path, module-level mutable state shared across requests.
4. **Contract and caller breakage** — callers from the scope step now receive another type, `None`, exception, or status code; a response field renamed, removed, or changed in nullability against `api_contract.json` or `design.md`; a Pydantic alias, enum value, or event payload no longer matching the consumer; an ORM model no longer matching the latest Alembic revision.
5. **Security, scope, and data safety** — object-level authorization (the query filters by `owner_id` / `tenant_id`, not only the route having a user), mass assignment from a request body, SQL / shell / template built from request data, secrets or personal data in logs, exceptions, or responses, unsafe parsing that silently substitutes a default.
6. **Stack and project patterns** — every row in Section 4 below that the changed code can hit.
7. **Test blind spots** — for each surviving candidate: would an existing test fail if it were real? Watch for tests that cannot fail here: a repository mocked so the SQL filter is never executed, a transaction-rollback fixture hiding a missing `commit()`, `dependency_overrides` replacing the very guard under review, an `async def` test that never ran because the pytest-asyncio mode or marker is missing. Record the missing test with the finding.

`quick` effort runs dimensions **1–4** on changed hunks only.

---

## 4. Backend Bug Patterns (Dimension 6)

### 4.1 Async and Event Loop

| Looks like | Goes wrong when | Check |
|---|---|---|
| `repo.save(x)` / `session.commit()` without `await` | Returns a coroutine object; nothing is written, request returns success | `uv run mypy` reports `[unused-coroutine]` |
| `asyncio.create_task(...)` result not stored | Task can be garbage-collected before completion; errors lost | `ruff` `RUF006`; verify who awaits or holds the task |
| `requests`, `time.sleep`, sync DB driver, heavy CPU, or `open()` inside `async def` | Blocks the event loop; all concurrent requests stall | `ruff` `ASYNC` rules; use `httpx.AsyncClient`, `asyncio.sleep`, `run_in_threadpool` |
| `asyncio.gather(...)` over calls sharing one `AsyncSession` | `AsyncSession` is not safe for concurrent tasks; interleaved state/errors | Each concurrent task needs its own session, or run sequentially |
| `asyncio.gather` without handling partial failure | Other tasks keep running or half the writes land | Verify partial success handling or rollback |
| `except BaseException` / bare `except:` in async code | Swallows `asyncio.CancelledError`; shutdown and timeouts hang | Catch `Exception`, re-raise cancellation |
| `httpx.AsyncClient()` created per call without `async with` | Connection leak under load | Client closed on every path, or one app-scoped client via `lifespan` |
| External call without a timeout (or `timeout=None`) | Slow provider hangs the worker | Explicit timeout and bounded retries |

### 4.2 SQLAlchemy 2.x Async Sessions and Queries

| Looks like | Goes wrong when | Check |
|---|---|---|
| `obj.relationship` accessed after query in async code | Implicit lazy load raises `MissingGreenlet` | `selectinload` / `joinedload` in the query, or `lazy="raise"` |
| Attribute read after `await session.commit()` | Default `expire_on_commit=True` expires instance; read triggers I/O → `MissingGreenlet` | `async_sessionmaker(..., expire_on_commit=False)` or `await session.refresh(obj)` |
| `commit()` inside a repository method used by a multi-step use case | Earlier steps are committed when a later one fails: partial write | One transaction boundary per use case (`async with session.begin()` or UoW) |
| Work after commit that belongs in the transaction (outbox, audit, balance) | Crash between them leaves inconsistent data | Move inside the transaction |
| Request-scoped session used from `BackgroundTasks` or spawned task | Session is closed after the response | Background work opens its own session |
| `select` then `insert` to enforce uniqueness | Concurrent requests both insert; `IntegrityError` becomes 500 | `UNIQUE` constraint plus `on_conflict_do_nothing()` / catch `IntegrityError` → 409 |
| Read-modify-write of a counter, balance, or status | Lost update between concurrent requests | `with_for_update()`, version column, or atomic `update(...).where(...)` |
| `scalar_one()` on a lookup by user input | `NoResultFound` / `MultipleResultsFound` → 500 instead of 404 | `scalar_one_or_none()` and explicit 404 |
| `text(f"... {value}")` or string-concatenated SQL / `order_by` | SQL injection | `ruff` `S608`; bound parameters; whitelist sort columns |
| Relationship loaded inside a loop over results | N+1 queries; page times out on realistic data | Single query with `selectinload` |

### 4.3 FastAPI and Pydantic v2

| Looks like | Goes wrong when | Check |
|---|---|---|
| PATCH applies `body.model_dump()` | Omitted fields overwrite stored values with `None` / defaults | `model_dump(exclude_unset=True)` |
| `Model(**body.model_dump())` or `setattr` loop from request | Client sets `owner_id`, `role`, `status`: mass assignment | Separate input schema without privileged fields |
| Field `x: str \| None = None` that client must send | Omission accepted silently and stored as `NULL` | Required fields have no default |
| Route without `response_model`, returning ORM object or dict | Internal fields leak; shape drifts from `api_contract.json` | Explicit `response_model` matching contract |
| `HTTPException` raised inside `try: … except Exception:` | Caught and turned into 500 or fake success | Narrow `except`, or re-raise `HTTPException` |
| `except Exception: return []` / `return None` | Failure looks like an empty success to the client | `ruff` `BLE001`, `S110`; raise or map to domain error |
| Query param `limit: int` without bounds | Unbounded page loads whole table | `Query(default=…, ge=1, le=…)` |
| Offset pagination without `ORDER BY` a unique key | Pages repeat or skip rows | Order by a unique column (or add `id` as tie-breaker) |
| Auth dependency present, query filters only by `id` | User B reads or edits user A's object (IDOR) | Every object query filters by owner / tenant |

### 4.4 Python Language and Data

| Looks like | Goes wrong when | Check |
|---|---|---|
| Mutable default argument `def f(x=[])` / `{}` | State leaks across calls and requests | `ruff` `B006` |
| Module-level dict/list cache or `@lru_cache` on user/tenant data | Cross-tenant data leak; unbounded memory growth | Cache key includes scope; bounded size |
| `if not value:` for optional number or string | `0`, `""`, `[]` treated as missing | `if value is None:` |
| `float` for money or quantities; `round()` on halves | Rounding errors; banker's rounding (`round(2.5) == 2`) | `Decimal` with `quantize(ROUND_HALF_UP)`, `Numeric` columns |
| `datetime.utcnow()` / `datetime.now()` / `date.today()` | Naive datetimes rejected by `asyncpg` on `timestamptz` | `ruff` `DTZ` rules; `datetime.now(UTC)` |
| Secrets or tokens in settings printed / logged | Secret leaked in logs | `SecretStr`; never log `repr(settings)` |

### 4.5 Alembic Migrations

| Looks like | Goes wrong when | Check |
|---|---|---|
| Autogenerated drop + add for a renamed column or table | Data in old column is lost | Use `op.alter_column(..., new_column_name=...)` |
| `add_column(..., nullable=False)` without `server_default` | Upgrade fails on populated table | `server_default` or nullable → backfill → `NOT NULL` |
| Column dropped/renamed while running app still reads it | Deployed app errors during rollout | Expand / contract across releases |
| `op.create_index` on a large hot table | Long lock blocks writes | `postgresql_concurrently=True` inside `autocommit_block()` |
| Data migration importing `app.models` | Model drift breaks historical migrations later | Use `sa.table(...)` / `op.execute` |
| Two revisions with the same `down_revision` | Multiple heads; `upgrade head` fails | `uv run alembic heads` shows one head |

---

## 5. Non-Candidates (`H14`)

Reuse, simplification, or minor efficiency opportunities without a failure (a slower query that still returns the right rows within contract, or a duplicated helper) are not defects. Record them only as `NOTE` lines for `code-simplification`.
