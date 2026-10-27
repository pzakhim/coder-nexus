# 02 — Dependency Rules, DI Wiring, Sessions, Transactions, and Startup

Defines the inward dependency matrix, deterministic boundary checks (`import-linter` and `rg`), request-scoped `AsyncSession` & transaction rules, and `lifespan` / `Settings` purity.

---

## 1. Dependency Direction Matrix (**A1, A2, A6, A8**)

```text
main -> api (routers, deps, error_handlers) -> services -> repositories -> models
                       \-> schemas <-------------/            db.session, core: used by all
```

| Layer | May Import | Never Imports | Failure Prevented |
|---|---|---|---|
| `api/routers` | `api/deps`, `schemas`, service dependency aliases | `repositories`, `models`, `sqlalchemy` | Handlers bypassing service authorization and unit-of-work |
| `services` | `repositories`, `schemas`, `models`, `core/errors`, `integrations` | `fastapi`, `starlette`, `api/*` | Use cases becoming uncallable from workers, CLI, or unit tests |
| `repositories` | `models`, `core/errors`, `sqlalchemy` | `schemas`, `services`, `fastapi` | Persistence queries coupling to API response shapes |
| `models` | `models/base`, `models/enums`, `sqlalchemy` | `schemas`, `services`, `fastapi`, `pydantic` | Response changes forcing schema migrations or circular imports |
| `schemas` | `pydantic`, `models/enums` | `models` (ORM classes), `sqlalchemy`, `fastapi` | Database columns leaking into public API contracts |
| `core` | Standard library, `pydantic`, `pydantic-settings`, crypto/token libs | Any other `app.*` module, `fastapi` | Startup import cycles |

---

## 2. Deterministic Boundary Checks (`PASS` / `FAIL`)

### Primary Gate: `import-linter` (`uv run lint-imports`)
Configured in `pyproject.toml` and installed by default via `coder-nexus setup tools --pack backend`:

```toml
[tool.importlinter]
root_package = "app"
include_external_packages = true

[[tool.importlinter.contracts]]
name = "Layers: api above services above repositories above models"
type = "layers"
layers = ["app.main", "app.api", "app.services", "app.repositories", "app.models"]

[[tool.importlinter.contracts]]
name = "Services and core are framework-free"
type = "forbidden"
source_modules = ["app.services", "app.repositories", "app.models", "app.schemas", "app.core"]
forbidden_modules = ["fastapi", "starlette"]

[[tool.importlinter.contracts]]
name = "Storage does not know the API contract"
type = "forbidden"
source_modules = ["app.repositories", "app.models"]
forbidden_modules = ["app.schemas", "pydantic"]

[[tool.importlinter.contracts]]
name = "Schemas are plain data (enums excepted)"
type = "forbidden"
source_modules = ["app.schemas"]
forbidden_modules = ["app.models", "sqlalchemy"]
ignore_imports = ["app.schemas.* -> app.models.enums"]

[[tool.importlinter.contracts]]
name = "Core depends on nothing in app"
type = "forbidden"
source_modules = ["app.core"]
forbidden_modules = ["app.api", "app.services", "app.repositories", "app.models", "app.schemas", "app.db"]
```

### Fallback Gate: Ripgrep (`rg`) Boundary Audit
Each command below must produce **empty output** (`PASS`):

```bash
rg -n "^\s*(from|import) (fastapi|starlette)" app/services app/repositories app/models app/schemas app/core
rg -n "^\s*from app\.(repositories|models)(\.| )" app/api/routers
rg -n "^\s*from app\.schemas" app/repositories app/models
rg -n "^\s*from app\.models(\.| )" app/schemas | rg -v "app\.models\.enums"
rg -n "^\s*from app\.(api|services|repositories|models|schemas|db)" app/core
```

---

## 3. DI Wiring, Request-Scoped `AsyncSession`, and Transactions (**A3, A4, A5, A6, A9**)

### One Session per Request (`yield` Dependency — **A4, A5**)
```python
# app/db/session.py
async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    async with session_factory() as session:
        yield session

# app/api/deps.py
SessionDep = Annotated[AsyncSession, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]

def get_order_service(session: SessionDep) -> OrderService:
    return OrderService(session)

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
```
- Never wrap `yield session` in a `try/except` that swallows exceptions.
- Never instantiate `SessionLocal()` inside a service or share one `AsyncSession` across `asyncio.gather` tasks.

### Service Owns the Transaction Commit (**A3**)
| Layer | Permitted | Forbidden |
|---|---|---|
| **Router** | Calls one service method | `commit()`, `rollback()`, `begin()` |
| **Service (entry method)** | Executes writes across repositories, then calls `await self.session.commit()` once before returning | Committing mid-operation and continuing writes |
| **Service (called by another service)** | Executes writes without committing (document `"caller commits"`) | Committing on behalf of the outer service |
| **Repository** | `session.add()`, `await session.flush()`, translating `IntegrityError` → `ConflictError` | `commit()`, `rollback()`, `close()` |

### Explicit Relationship Loading (**A9**)
- Declare ORM relationships with `lazy="raise"`, configure `async_sessionmaker(engine, expire_on_commit=False)`, and load related rows explicitly in repositories with `selectinload()` (`backend-postgres`).

---

## 4. Settings, `lifespan`, and Import-Time Purity (**A7, A8**)

```python
# app/core/settings.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_uri: SecretStr
    environment: Literal["dev", "test", "staging", "production"]

@lru_cache
def get_settings() -> Settings:
    return Settings()

# app/main.py
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = build_engine(get_settings())
    app.state.session_factory = build_session_factory(engine)
    yield
    await engine.dispose()
```
- **Required settings have no fabricated defaults**: missing `DATABASE_URI` fails loudly at startup with `ValidationError`.
- **Secrets use `SecretStr`** and are unwrapped via `.get_secret_value()` only at the consumer boundary.
- **No module-level I/O**: never call `Settings()` or `create_async_engine()` at module top level; `env -i PATH="$PATH" uv run python -c "import app.main"` must exit `0`.
