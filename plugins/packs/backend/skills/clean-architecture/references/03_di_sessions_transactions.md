# 03 — Dependency injection, sessions and transactions

## 1. One session per request (`yield` dependency)

```python
# app/db/session.py
async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    async with session_factory() as session:
        yield session
```

- `async with` closes the session after the request; an uncommitted transaction is rolled back on close. Reason: a failed request leaves nothing behind without any `except` block.
- No `try/except` that swallows errors around `yield`. If you must catch to log, re-raise. Reason: a swallowed exception becomes a 500 with no log (FastAPI docs, dependencies with yield).
- The factory comes from `app.state`, set in `lifespan` ([04_settings_and_startup.md](04_settings_and_startup.md)). Reason: no engine or settings read at import; tests swap the factory.
- Never a module-level `session = ...`, never one session passed to `asyncio.gather` tasks. Reason: `AsyncSession` is not safe for concurrent use; concurrent work opens its own session from the factory.

## 2. Wiring with `Annotated`

```python
# app/api/deps.py
SessionDep = Annotated[AsyncSession, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]

def get_order_service(session: SessionDep) -> OrderService:
    return OrderService(session)

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
```

FastAPI caches a dependency per request, so the router's `OrderServiceDep` and `CurrentUserDep` share the same `SessionDep`. That shared session is what makes the request one unit of work.

Unsafe vs safe:

```python
# Unsafe: class dependency, session opened by the service itself
class OrderService:
    def __init__(self) -> None:
        self.session = SessionLocal()          # hidden I/O, never closed on error

# Safe: the session is injected; the service is built by a function dependency
class OrderService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.orders = OrderRepository(session)
```

## 3. Transactions: the service owns the commit

| Layer | Does | Never |
|---|---|---|
| Router | Calls one service method | `commit`, `rollback`, `begin` |
| Service (method called by the router) | All writes, then `await self.session.commit()` once at the end | Commit halfway, then continue writing |
| Service (method called by another service) | Writes without committing; document "caller commits" in its docstring | Commit on behalf of the caller |
| Repository | `session.add`, `await session.flush()` (gets ids, surfaces constraint errors early) | `commit`, `rollback`, `close` |
| `get_session` | Closes the session (rolls back what was not committed) | Commit on exit |

Why the commit is not in `get_session` after `yield`: with the default request scope, exit code runs **after the response is sent**. A commit there could fail after the client already saw `201`. Committing inside the service means the response is built only after the data is durable.

```python
# app/services/orders.py
async def create_order(self, data: OrderCreate, actor: CurrentUser) -> OrderRead:
    ensure_can_create_order(actor, data.customer_id)       # PermissionDeniedError if not
    order = await self.orders.add(Order(customer_id=data.customer_id, status=OrderStatus.DRAFT))
    await self.audit.add(AuditEntry.created(order, actor))  # same transaction
    await self.session.commit()
    return OrderRead.model_validate(order)
```

If the audit insert fails, nothing was committed and the session closes with a rollback: no order without its audit row.

## 4. Errors cross layers as domain errors

```python
# app/repositories/orders.py
async def add(self, order: Order) -> Order:
    self.session.add(order)
    try:
        await self.session.flush()
    except IntegrityError as exc:
        raise ConflictError("order_already_exists") from exc   # adds behavior: translation
    return order
```

- `app/api/error_handlers.py` maps `ConflictError` → `409`, `NotFoundError` → `404`, `PermissionDeniedError` → `403`, each with the contract's error body ([api-contract-design](../../api-contract-design/SKILL.md)).
- Translating is the only reason to catch in a repository. Catch-all `except Exception` is allowed only in the error handler edge, and it logs (`{{slot:clean-code}}` CC9).

## 5. Loading relationships under async

- Relationships declare `lazy="raise"`. A repository that needs related rows loads them explicitly: `select(Order).options(selectinload(Order.lines))`.
- `async_sessionmaker(engine, expire_on_commit=False)`, so the service can map an object to its schema after `commit()` without a reload.
- Server-generated columns (timestamps, defaults) are fetched on flush via `eager_defaults` on the base mapper, or `await session.refresh(obj, attribute_names=[...])`.

Reason: an implicit lazy load under async raises `MissingGreenlet` at runtime; `lazy="raise"` turns it into an immediate, obvious error in tests. Query and index guidance: [postgres](../../postgres/SKILL.md).

## 6. Tests replace dependencies, not internals

```python
app.dependency_overrides[get_settings] = lambda: test_settings
```

The session in API tests comes from the test database's factory (set on `app.state` by the test lifespan or overridden through `get_session`). Never mock the service's authorization to make a test pass (`{{slot:unit-testing}}`).
