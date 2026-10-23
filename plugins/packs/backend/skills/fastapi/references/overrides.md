# Overrides of the official FastAPI skill

Read against the official skill for the installed version (located in [../SKILL.md](../SKILL.md) §1; pinned copy `0.161.1` in [sources.md](sources.md)). Each override names what the official skill says (paraphrased, not copied), what we do, why, and the safe pattern next to the unsafe one. Anything not listed here is followed as the official skill says.

## O1. SQLAlchemy 2 async + repositories instead of SQLModel

- **Official**: prefer SQLModel so one class is both the table and the validation model.
- **We do**: SQLAlchemy 2 ORM (`DeclarativeBase`, `Mapped[...]`, `mapped_column`) with asyncpg, repository classes for queries, and separate Pydantic v2 schemas for request and response bodies.
- **Why**:
  1. The API contract and the table change for different reasons. A shared class means a new column can appear in a response, or a response field forces a migration. Separate schemas make every exposed field an explicit decision (`{{slot:secure-coding-standards}}`: no accidental exposure of hashes, internal flags or other tenants' ids).
  2. SQLAlchemy 2's typed ORM is checked by mypy without a plugin; async sessions, `selectinload` and `lazy="raise"` are first-class.
  3. It is the approved decision for this pack, and the migration tool (Alembic) is built on the same metadata.

```python
# Unsafe here: one class is table, input and output
class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int
    internal_note: str        # leaks in every response that returns Order

# Safe: table in app/models, contract in app/schemas
class Order(Base):                                  # app/models/orders.py
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    internal_note: Mapped[str | None]

class OrderRead(BaseModel):                         # app/schemas/orders.py
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_id: int                                # internal_note is not exposed
```

## O2. mypy instead of ty

- **Official**: use ty for type checking when available.
- **We do**: mypy, configured in `pyproject.toml` (`[tool.mypy]`, `plugins = ["pydantic.mypy"]`), run as `mypy app` (with the workspace prefix, for example `uv run mypy app`).
- **Why**: approved decision; one type checker in CI and review; the Pydantic plugin checks model constructors. If the workspace already runs ty and not mypy, that is a verified convention: raise it as a question at Gate 2 instead of adding a second checker.

## O3. `async def` on database paths

- **Official**: when unsure, write plain `def` path operations so blocking code runs in the threadpool.
- **We do**: every path operation and dependency that touches the database, a provider client or another awaitable is `async def`. Blocking libraries are never called directly inside it.
- **Why**: `AsyncSession` and asyncpg only work with `await`; a `def` handler cannot await the service. A blocking call inside `async def` stalls every request on the worker.

```python
# Unsafe: blocks the event loop for every concurrent request
@router.post("/{order_id}/invoice")
async def create_invoice(order_id: int, service: InvoiceServiceDep) -> InvoiceRead:
    pdf = render_pdf_blocking(order_id)            # CPU/file-bound call on the loop
    ...

# Safe: the blocking part runs in a worker thread (anyio ships with FastAPI)
pdf = await anyio.to_thread.run_sync(render_pdf_blocking, order_id)
```

A pure-CPU path operation that touches nothing async may stay `def`; that is the exception, not the default.

## O4. No Asyncer (or any new dependency) without a decision

- **Official**: prefer Asyncer for mixing sync and async code.
- **We do**: use what is installed (`anyio.to_thread.run_sync`). Adding Asyncer, or any package, needs a `D-NN` and a task that lists `pyproject.toml` and the lock file in **Scope / Files**.
- **Why**: a dependency is a supply-chain and maintenance decision (`{{slot:secure-coding-standards}}`), and a lock-file change outside the task's scope is unreviewed scope.

## O5. The workspace's package manager, not "uv if available"

- **Official**: use uv when it is available.
- **We do**: detect from the lock file (`uv.lock` → `uv run`, `poetry.lock` → `poetry run`, otherwise the venv interpreter) and use only that.
- **Why**: running a different manager rewrites or ignores the lock, so the reviewer cannot reproduce your checks.

## O6. Layering instead of queries in path operations

- **Official**: examples query the session directly inside the path operation (fine for a one-file example).
- **We do**: router → one service method → repositories → session. The router parses input, calls the service, returns its schema. The service owns business rules, authorization checks and the single commit. Repositories own `select()` statements and never commit. Layout and rules: `{{slot:clean-architecture}}`.
- **Why**: business rules in handlers cannot be reused by workers or tested without HTTP; scattered commits break the one-transaction-per-request rule.

```python
# Unsafe: query, rule and commit inside the handler
@router.post("/")
async def create_order(body: OrderCreate, session: SessionDep) -> OrderRead:
    if (await session.scalar(select(func.count()).where(Order.customer_id == body.customer_id))) > 10:
        raise HTTPException(409)
    order = Order(**body.model_dump()); session.add(order); await session.commit()
    return OrderRead.model_validate(order)

# Safe: the handler only delegates
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(body: OrderCreate, service: OrderServiceDep, user: CurrentUserDep) -> OrderRead:
    return await service.create_order(body, actor=user)
```

Also: the official dependency example uses the legacy `session.query(...)`. We use SQLAlchemy 2 style `select(...)` with `session.scalars()` / `session.execute()` in repositories.

## O7. Errors raised as domain errors, mapped once

- **Official docs** (tutorial): raise `HTTPException` from path operations in most cases.
- **We do**: services and repositories raise framework-free errors from `app/core/errors.py` (`NotFoundError`, `ConflictError`, `PermissionDeniedError`, ...). One set of exception handlers in `app/api/error_handlers.py` maps them to the status codes and error body agreed in the API contract ([api-contract-design](../../api-contract-design/SKILL.md)). Routers do not `try`/`except` to remap.
- **Why**: services must not import FastAPI (workers and tests call them), and one mapping keeps every endpoint's error body identical to the contract.

## O8. Return types, but never ORM objects

- **Official**: prefer a return type; use `response_model` when returning an internal object that must be filtered to the public schema.
- **We do**: services return the public Pydantic schema, so the router's return type and the returned value match and mypy checks them. We do not return ORM instances and rely on `response_model` filtering.
- **Why**: an ORM object leaving the service may trigger a lazy load outside the session (an error under async), and `-> Any` (needed with `response_model` on a different type) hides type errors from mypy. `response_model` stays available for the rare case the official skill describes, with a reason in the code.

## O9. Not used without a `D-NN`

| Feature | Why not by default |
|---|---|
| `app.frontend()` / `router.frontend()` static serving | This pack serves an API to the frontend client; serving built assets is a deployment decision outside the backend work item |
| Native OpenTelemetry auto-configuration | Export endpoints and headers are configuration and data-handling decisions; enable only when the workspace already configures telemetry or a `D-NN` adds it |
| Ruff's FastAPI rule set (`FAST`) | Good idea, but enabling it changes `pyproject.toml` lint config for the whole repo; propose it as a `D-NN`, never enable it inside an unrelated task |

## Adopted, with our stack's shape

| Rule | Our safe pattern |
|---|---|
| `Annotated` dependency aliases | `SessionDep = Annotated[AsyncSession, Depends(get_session)]` and `OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]`, both in `app/api/deps.py` (services never import FastAPI) |
| Function dependencies, not classes | `def get_order_service(session: SessionDep) -> OrderService: return OrderService(session)` instead of `Depends()` on the class |
| `yield` dependencies | `get_session` uses `async with session_factory() as session: yield session`; it never catches and drops an exception (the session closes and rolls back an uncommitted transaction) |
| Dependency `scope` | Keep the default `"request"` scope for the session. The commit happens inside the service before the response is built, so no write is confirmed to the client before it is durable |
| Router-level config | `router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(require_authenticated)])` |
| One method per function | `list_orders`, `create_order`, `get_order` - never `api_route(methods=[...])` |
| No `...`, no `RootModel` | `quantity: int = Field(gt=0)`; bulk input `Annotated[list[OrderLineIn], Field(min_length=1)]` |
| Native SSE | `@router.get("/stream", response_class=EventSourceResponse)` with an `async` generator yielding `ServerSentEvent`; auth, resume and fan-out rules in `backend-realtime` |
| `fastapi` CLI | `fastapi dev` (cwd: backend root) when `[tool.fastapi] entrypoint` is set; otherwise the launcher the workspace already uses |
| Lifespan | Engine and session factory created in `lifespan`, disposed after `yield`; no `@app.on_event` |
