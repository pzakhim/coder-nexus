# 04 — Settings, lifespan and startup

## 1. One settings object, read through a cached dependency

```python
# app/core/settings.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_uri: SecretStr
    environment: Literal["dev", "test", "staging", "production"]
    order_page_size_max: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

| Rule | Why |
|---|---|
| Required values have **no default** (`database_uri`, `environment`) | A missing variable fails at startup with a `ValidationError` naming the field, instead of running against a guessed database (no fake fallbacks) |
| Secrets are `SecretStr` and read with `.get_secret_value()` only where they are used | `repr()`, logs and error pages print `**********` instead of the value |
| No `settings = Settings()` at module level; call `get_settings()` | Settings are read when the app starts, not when a module is imported; tests replace them with `app.dependency_overrides[get_settings]` or `Settings(...)` kwargs |
| Variable names follow the workspace's `.env` / `.env.example`. The pack's Postgres MCP reads `DATABASE_URI`, so a new service uses that name too | One variable, one meaning for the app, Alembic and the MCP (`backend-postgres`) |
| `extra="ignore"` only when the shared `.env` carries variables for other tools; otherwise keep the default (`forbid`) | `forbid` catches typos in `.env`; `ignore` is needed when the MCP or other tools share the file |
| A new setting is added to `.env.example` with a placeholder, never a real value, in the same task | The next developer and the reviewer see every required variable; no secret in git |

Source priority (pydantic-settings): constructor kwargs > environment variables > `.env` file > defaults. A test that sets `os.environ` after `get_settings()` was cached sees the old value: call `get_settings.cache_clear()` or override the dependency.

## 2. Lifespan owns resources

```python
# app/main.py
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = build_engine(get_settings())
    app.state.session_factory = build_session_factory(engine)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(orders.router)
    register_error_handlers(app)
    return app


app = create_app()
```

- Before `yield`: engine, session factory, shared `httpx.AsyncClient` for providers. After `yield`: dispose and close them. Reason: one place opens and closes every long-lived resource; `engine.dispose()` prevents "event loop is closed" warnings and leaked connections.
- No `@app.on_event("startup")`. When `lifespan=` is passed, startup/shutdown events are not called at all, so mixing them silently drops code.
- `create_app()` reads nothing from the environment; `lifespan` does, when the server starts. Reason: importing `app.main` in a test, in Alembic or in the CLI does not connect anywhere (core `clean-code` CC12).
- The engine URL uses the async driver: `make_url(settings.database_uri.get_secret_value()).set(drivername="postgresql+asyncpg")` inside `build_engine`, so one `DATABASE_URI` (`postgresql://...`) serves the app, Alembic and the MCP.

## 3. No I/O at import, minimal `__init__.py`

| Allowed at module level | Not allowed at module level |
|---|---|
| Constants used by two or more functions, `router = APIRouter(...)`, `app = create_app()`, type aliases (`SessionDep`) | `Settings()`, `create_async_engine(...)`, opening files, HTTP calls, reading `os.environ`, starting tasks |

`__init__.py` files are empty. The one exception is `app/models/__init__.py`, which imports every model module so `Base.metadata` is complete for Alembic autogenerate and relationship strings resolve:

```python
# app/models/__init__.py
from app.models import customers, orders  # noqa: F401  (registers tables on Base.metadata)
```

No re-exports such as `from app.services.orders import OrderService` in `app/services/__init__.py`: callers import from the defining module (core `clean-code` CC2, CC5).

## 4. Checks

| Check (cwd: backend root) | Expected |
|---|---|
| `python -c "import app.main"` with an empty environment (`env -i PATH="$PATH" .venv/bin/python -c "import app.main"`) | Exit 0: importing does not read settings or connect |
| `fastapi dev` or the workspace launcher with `.env` present | Server starts; `GET /docs` returns 200 |
| Same launcher without `DATABASE_URI` | Startup fails with a `ValidationError` naming `database_uri` (no silent default) |
