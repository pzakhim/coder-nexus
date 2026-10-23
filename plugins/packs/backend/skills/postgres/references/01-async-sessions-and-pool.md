# 01 — Async sessions, transactions and the pool

Rules PG1–PG7 from [SKILL.md](../SKILL.md) with code. Names (`get_session`, `app/db/session.py`) are examples: use the workspace's own module and names, recorded in `codebase-notes.md`.

## Engine and sessionmaker (once per process)

```python
# app/db/session.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(
    settings.database_url,            # postgresql+asyncpg://… from settings / .env, never a literal
    pool_size=settings.db_pool_size,  # see "Pool sizing"
    max_overflow=settings.db_max_overflow,
    pool_timeout=10,                  # fail fast instead of queueing forever
    pool_pre_ping=True,               # drop connections the server or a proxy closed
    pool_recycle=1800,                # below any proxy / load-balancer idle cut-off
    connect_args={
        "server_settings": {
            "statement_timeout": "15000",                     # ms; per-workspace value
            "idle_in_transaction_session_timeout": "30000",
            "application_name": "api",
        },
    },
)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
```

- `expire_on_commit=False`: after commit, attributes stay loaded. Reason: with the default, the next attribute access after `commit()` triggers a refresh, which is an implicit I/O call in async code.
- `create_async_engine` uses `AsyncAdaptedQueuePool` by default (SQLAlchemy pooling docs). Reason to keep it: the plain `QueuePool` is not asyncio-safe.
- Worker processes (gunicorn/uvicorn workers, multiprocessing) create the engine after fork, or call `engine.dispose(close=False)` in the child. Reason: pooled connections must never be shared across processes.
- Tests that create an event loop per test use a test engine built in a fixture (or `NullPool`) and `await engine.dispose()` at teardown. Reason: connections bound to a closed loop raise "attached to a different loop".

## One session per request (PG1)

```python
# unsafe: one session for the whole app, shared by concurrent requests
session = SessionFactory()

async def list_orders():
    return (await session.scalars(select(Order))).all()
```

```python
# safe: a yield dependency; the session is closed even when the handler raises
async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
```

- Never pass one `AsyncSession` into several `asyncio.gather` branches. Reason: an `AsyncSession` is a single connection/transaction and is not safe for concurrent tasks; run the queries sequentially or give each task its own session from `SessionFactory`.
- Background tasks and workers open their own session; they never reuse the request's (it is closed when the response is sent).

## Transactions in services (PG2)

```python
# unsafe: repository commits; a failure in step 2 leaves step 1 committed
class OrderRepository:
    async def add(self, order: Order) -> None:
        self.session.add(order)
        await self.session.commit()
```

```python
# safe: repository adds/flushes, the service owns the unit of work
class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, order: Order) -> Order:
        self.session.add(order)
        await self.session.flush()      # gets the id, stays inside the caller's transaction
        return order

class PlaceOrder:
    def __init__(self, session: AsyncSession, orders: OrderRepository, stock: StockRepository) -> None:
        self.session, self.orders, self.stock = session, orders, stock

    async def __call__(self, cmd: PlaceOrderCommand) -> Order:
        async with self.session.begin():          # commit on success, rollback on any exception
            await self.stock.reserve(cmd.items)
            return await self.orders.add(Order.from_command(cmd))
```

- Keep transactions short: no outbound HTTP call, file upload or `await asyncio.sleep` inside `session.begin()`. Reason: the transaction holds row locks and a pooled connection for the whole wait (vendored `lock-short-transactions.md`).
- `session.begin()` fails if a transaction was already autobegun by an earlier query on the same session. If the service must read before writing, put the read inside the same `begin()` block.
- Lock rows you will update in the same transaction (`select(...).with_for_update()`), in a consistent order across code paths (vendored `lock-deadlock-prevention.md`).

## No lazy loading (PG3)

```python
# unsafe: each order.customer access is a lazy load → MissingGreenlet in async, or N+1
orders = (await session.scalars(select(Order))).all()
return [OrderOut(id=o.id, customer=o.customer.name) for o in orders]
```

```python
# safe: explicit eager loading chosen per query
stmt = (
    select(Order)
    .options(joinedload(Order.customer), selectinload(Order.lines))
    .where(Order.tenant_id == tenant_id)
    .order_by(Order.created_at.desc(), Order.id.desc())
    .limit(page_size)
)
orders = (await session.scalars(stmt)).unique().all()
```

- `joinedload` for many-to-one / one-to-one (one row per parent); `selectinload` for collections (one extra `IN` query, no row multiplication).
- Declare relationships with `lazy="raise"` so a forgotten option fails loudly in tests instead of silently issuing queries. Reason: the failure shows up at review time, not under production load.
- `AsyncAttrs` / `awaitable_attrs` is allowed only for a deliberate single-object access, never in a loop.

## Pool sizing (PG4)

```
per process:  pool_size + max_overflow
total:        (pool_size + max_overflow) × uvicorn/gunicorn workers × replicas
              + background workers' pools + Alembic/admin headroom (≥ 3)
must be  <    max_connections − superuser_reserved_connections
```

Read `max_connections` with `SHOW max_connections;` on the dev DB (or the postgres MCP `analyze_db_health`), and the worker count from the run command. Record the arithmetic in the design when it changes. Behind PgBouncer or a managed pooler, the limit that matters is the pooler's pool size. Vendored detail: `conn-limits.md`, `conn-pooling.md`, `conn-idle-timeout.md`.

## Timeouts (PG5)

- `statement_timeout` via `server_settings` (above) as the default; raise it per statement only for a known long report: `await session.execute(text("SET LOCAL statement_timeout = '60s'"))` inside that transaction.
- `idle_in_transaction_session_timeout` kills sessions that opened a transaction and stopped. Reason: they block vacuum and hold locks.
- `lock_timeout` belongs to migrations (`backend-database-migrations`), so DDL fails fast instead of queueing behind traffic.

## Parameterised SQL (PG6)

```python
# unsafe: injection, and a new plan per value
await session.execute(text(f"SELECT * FROM orders WHERE status = '{status}' ORDER BY {sort}"))
```

```python
# safe: bind parameters; identifiers from an allow-list
SORTABLE = {"created_at": Order.created_at, "total": Order.total}
column = SORTABLE.get(sort)
if column is None:
    raise InvalidSort(sort)
stmt = select(Order).where(Order.status == status).order_by(column.desc())
# raw text() when unavoidable:
await session.execute(text("SELECT id FROM orders WHERE status = :status"), {"status": status})
```

A list of values in raw SQL uses `= ANY(:ids)` (asyncpg rejects `IN $1`); in the ORM use `.in_(ids)`.

## Poolers and prepared statements (PG7)

asyncpg caches prepared statements per connection. Through PgBouncer in transaction or statement mode they fail with `prepared statement "__asyncpg_stmt_…__" does not exist / already exists`. Options, in order: use session pooling or connect directly; otherwise add `?prepared_statement_cache_size=0` to the URL and pass a unique `prepared_statement_name_func` in `connect_args` (SQLAlchemy asyncpg dialect docs), and keep SQLAlchemy's own pool small or `NullPool`. Vendored detail: `conn-prepared-statements.md`.
