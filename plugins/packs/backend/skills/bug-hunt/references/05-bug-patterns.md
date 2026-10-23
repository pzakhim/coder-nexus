# 05 — Bug patterns (Python / FastAPI / SQLAlchemy async / Alembic)

Dimension 6 of the hunt. These are the failure modes generic advice misses and the ones most likely to cost data. Check only the rows the changed code can hit; each hit still needs a failure scenario and verification ([02](02-verify.md)). Paths such as `app/` and `alembic/versions/` are conventions the workspace may override.

## Async and event loop

| Looks like | Goes wrong when | Check |
|---|---|---|
| `repo.save(x)` / `session.commit()` without `await` | Returns a coroutine object; nothing is written, the request returns success | `uv run mypy` reports `[unused-coroutine]`; Python warns "coroutine … was never awaited" |
| `asyncio.create_task(...)` result not stored | The task can be garbage-collected before it finishes; errors are never seen | ruff `RUF006`; who awaits or holds the task? |
| `requests`, `time.sleep`, sync DB driver, heavy CPU or `open()` inside `async def` | Blocks the event loop; all concurrent requests stall | ruff `ASYNC` rules; use `httpx.AsyncClient`, `asyncio.sleep`, `run_in_threadpool` |
| `asyncio.gather(...)` over calls that share one `AsyncSession` | `AsyncSession` is not safe for concurrent use; errors or interleaved state | Each concurrent task needs its own session, or run sequentially |
| `asyncio.gather` without handling one failure | Other tasks keep running or half the writes land | Is partial success handled or rolled back? |
| `except BaseException` / bare `except:` in async code | Swallows `asyncio.CancelledError`; shutdown and timeouts hang | Catch `Exception`, re-raise cancellation |
| `httpx.AsyncClient()` created per call without `async with` | Connection leak under load | Client closed on every path, or one app-scoped client via `lifespan` |
| External call without a timeout (or `timeout=None`) | A slow provider hangs the worker | Explicit timeout and bounded retries |

## SQLAlchemy 2.x async sessions and queries

| Looks like | Goes wrong when | Check |
|---|---|---|
| `obj.relationship` accessed after the query in async code | Implicit lazy load raises `MissingGreenlet` | `selectinload` / `joinedload` in the query, or `lazy="raise"` to surface it in tests |
| Attribute read after `await session.commit()` | Default `expire_on_commit=True` expires the instance; the read needs I/O → `MissingGreenlet` | `async_sessionmaker(..., expire_on_commit=False)` or `await session.refresh(obj)` |
| `commit()` inside a repository method used by a multi-step use case | Earlier steps are committed when a later one fails: partial write | One transaction boundary per use case (`async with session.begin()` or a unit of work) |
| Work after commit that belongs in the transaction (outbox row, audit, balance update) | Crash between them leaves inconsistent data | Move it inside the transaction |
| Request-scoped session used from `BackgroundTasks` or a spawned task | The session is closed after the response | Background work opens its own session |
| Commit only in a `yield` dependency's teardown | Depending on the FastAPI version, the response may be sent before the commit, so a commit failure never reaches the client | Check the installed FastAPI version's teardown order; prefer committing in the use case |
| `select` then `insert` to enforce uniqueness | Concurrent requests both insert; `IntegrityError` becomes 500 | `UNIQUE` constraint plus `insert(...).on_conflict_do_nothing()` / catch `IntegrityError` → 409 |
| Read-modify-write of a counter, balance or status | Lost update between concurrent requests | `with_for_update()`, a version column, or an atomic `update(...).where(...)` |
| `scalar_one()` on a lookup by user input | `NoResultFound` / `MultipleResultsFound` → 500 instead of 404 | `scalar_one_or_none()` and an explicit 404 |
| `scalars().first()` where exactly one row is expected | A duplicate is silently ignored | `scalar_one_or_none()`, or a unique constraint |
| `text(f"... {value}")` or string-concatenated SQL / `order_by` from a query param | SQL injection | ruff `S608`; bound parameters; whitelist sort columns |
| Relationship loaded inside a loop over results | N+1 queries; page times out on realistic data | One query with `selectinload`; count queries in an integration test |

## FastAPI and Pydantic v2

| Looks like | Goes wrong when | Check |
|---|---|---|
| PATCH applies `body.model_dump()` | Omitted fields overwrite stored values with `None` / defaults: data loss | `model_dump(exclude_unset=True)` |
| `Model(**body.model_dump())` or `setattr` loop from the request | Client sets `owner_id`, `role`, `status`: mass assignment | Separate input schema without those fields |
| Field `x: str \| None = None` that the client must send | Omission is accepted silently and stored as `NULL` | Required fields have no default |
| Default `extra="ignore"` on input schemas | A misspelled field is dropped silently; the update does nothing | `model_config = ConfigDict(extra="forbid")` where the contract requires it |
| Route without `response_model`, returning an ORM object or dict | Internal fields (password hash, internal flags) leak; shape drifts from `api_contract.json` | Explicit `response_model` matching the contract |
| `HTTPException` raised inside `try: … except Exception:` | It is caught and turned into 500 or a fake success | Narrow the `except`, or re-raise `HTTPException` |
| `except Exception: return []` / `return None` | A failure looks like an empty success to the client | ruff `BLE001`, `S110`; log and raise, or map to the contract's error |
| Query param `limit: int` without bounds | Unbounded page loads the whole table | `Query(default=…, ge=1, le=…)` |
| Offset pagination without `ORDER BY` a unique key | Pages repeat or skip rows | Order by a unique column (or add `id` as tie-breaker) |
| Auth dependency present, query filters only by id | User B reads or edits user A's object (IDOR) | Every object query filters by owner / tenant; a test with a foreign object expects 404 |

## Python language and data

| Looks like | Goes wrong when | Check |
|---|---|---|
| Mutable default argument `def f(x=[])` / `{}` | State leaks across calls and requests | ruff `B006`; Pydantic field defaults are copied and are fine |
| Module-level dict / list cache, `@lru_cache` on a function taking user or tenant data | One user's or tenant's data served to another; unbounded growth | Cache key includes the scope; bounded size or no cache |
| `if not value:` for an optional number or string | `0`, `""`, `[]` treated as missing | `if value is None:` |
| `float` for money or quantities; `round()` on halves | Rounding errors; banker's rounding (`round(2.5) == 2`) | `Decimal` with `quantize(ROUND_HALF_UP)`, `Numeric` columns |
| `datetime.utcnow()` / `datetime.now()` / `date.today()` | Naive datetimes; asyncpg rejects mixing naive and aware values; "today" in the server zone | ruff `DTZ` rules; `datetime.now(UTC)`, `timestamptz` columns, the configured zone for business dates |
| Lambda or closure created in a loop | Late binding: every closure sees the last value | Bind as a default argument or use `functools.partial` |
| Secrets or tokens in settings printed / logged | Secret in logs | `SecretStr`; no `repr(settings)` in logs |

## Alembic migrations

| Looks like | Goes wrong when | Check |
|---|---|---|
| Autogenerated drop + add for a renamed column or table | Data in the old column is lost | Review the script; use `op.alter_column(..., new_column_name=...)` |
| `add_column(..., nullable=False)` without `server_default` on a populated table | Upgrade fails on existing rows | `server_default` or add nullable → backfill → set `NOT NULL` |
| Column dropped or renamed while the running version still reads it | The deployed app errors during rollout | Expand / contract across releases |
| `op.create_index` on a large hot table | Long lock blocks writes | `postgresql_concurrently=True` inside `op.get_context().autocommit_block()` |
| Data migration importing `app.models` | Model drift breaks old migrations later | Use `sa.table(...)` / `op.execute` with the schema at that revision |
| Two revisions with the same `down_revision` | Multiple heads; `upgrade head` fails | `uv run alembic heads` shows one head |
| Missing or wrong `downgrade()` | Rollback fails or loses data | Downgrade restores the previous schema, or the plan records it as irreversible |
| ORM model and migration disagree (nullability, type, constraint) | Runtime errors or missing constraints | `uv run alembic check` where configured; compare `--sql` output with the model |

## Project patterns

A Backend workspace adds its own rows here for its risk areas, each naming a real path: tenant / environment scoping of every query and cache, its authorization model (which dependency guards which routes), money and unit rules, external providers (timeouts, partial failures, provider errors leaked to users), and its migration / backfill practice. Until a workspace adds them, dimension 5 and the rows above cover these areas generically.

## Adding a pattern

When a bug escapes to review or production, add a row here (or in the workspace's own `bug-hunt` override) in the same change as its fix and its regression test. Reason: a pattern that escaped once will escape again unless the hunt names it.
