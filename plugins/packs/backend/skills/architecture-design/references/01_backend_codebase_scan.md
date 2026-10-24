# 01 — Backend codebase scan

Read-only scan of the backend before Gate 2. Every command runs from the backend root (the directory with `pyproject.toml`). Nothing here edits files, installs packages, runs migrations or writes to a database. Each finding goes to `codebase-notes.md` → `## 3. Verified Baseline Facts` with the path it came from; anything you could not verify stays out of `design.md` or becomes a `Q-NN`.

## 1. Project and tools

| Look at | Command | Record |
|---|---|---|
| Package manager | `ls uv.lock poetry.lock requirements*.txt 2>/dev/null` | `uv` / `poetry` / pip + venv, and the prefix every later command uses (`uv run`, `poetry run`, `.venv/bin/`) |
| Python and dependency versions | `sed -n '/^\[project\]/,/^\[/p' pyproject.toml`; `uv run python -c "import fastapi, pydantic, sqlalchemy; print(fastapi.__version__, pydantic.VERSION, sqlalchemy.__version__)"` | Versions; whether `asyncpg`, `alembic`, `pydantic-settings`, `httpx`, `pytest-asyncio`, `import-linter` are present |
| Official FastAPI skill | `backend-fastapi` §1 | Path of the bundled skill, or "pinned copy, installed X.Y.Z" |
| Lint, format, type, test config | `rg -n "^\[tool\.(ruff|mypy|pytest|importlinter|fastapi)" pyproject.toml` | Ruff rule sets, mypy strictness and plugins, `asyncio_mode`, test paths, entrypoint |
| How the app starts | `[tool.fastapi]` entrypoint, `Dockerfile`, `docker-compose*.yml`, `Makefile`, `README` | The real start command for dev and tests |

## 2. Application structure

| Look at | Where | Record |
|---|---|---|
| App factory and lifespan | `rg -n "FastAPI\(" app/`; open the file | `create_app` or module-level app; `lifespan=` or `on_event`; what is created at startup (engine, clients) |
| Routers | `rg -n "APIRouter\(" app/`; `rg -n "include_router" app/` | Prefix and tags per router, version prefix (`/api/v1`) if any, router-level dependencies |
| Dependencies | `app/api/deps.py` or `rg -n "Depends\(" app/ \| head -40` | Session dependency, auth dependency (`get_current_user`), service builders, `Annotated` aliases |
| Error handling | `rg -n "exception_handler|HTTPException" app/` | Error classes, the current error body shape, which status codes are mapped where |
| Settings | `app/core/settings.py` (or `rg -n "BaseSettings" app/`), `.env.example` | Field names (never values), required vs defaulted, `DATABASE_URI` name, provider key names |
| Auth model | The auth dependency and `app/core/security.py` | Credential type (bearer JWT, session cookie, API key), roles, how the actor's scope (owner, tenant, environment) is resolved |
| Services | `ls app/services/` | Where business rules and commits live today (or that they live in routers - record it, do not fix it) |
| Repositories and queries | `ls app/repositories/`; `rg -n "select\(|session\.query" app/ \| head -40` | SQLAlchemy 2 `select` vs legacy `query`, eager loading style, raw SQL |
| Models | `ls app/models/`; open `base.py` and the tables the work item touches | Columns, types, nullability, FKs, unique constraints, scope columns, relationships and their `lazy` setting, naming convention |
| Outbound providers | `rg -n "httpx|requests\." app/` | Provider clients, base-URL settings, timeouts, sandbox vs production keys |
| Realtime | `rg -n "EventSourceResponse|StreamingResponse|WebSocket" app/` | Existing streams, their auth and event format (`backend-realtime`) |

If the layout differs from `{{slot:clean-architecture}}` (feature folders, `crud/` instead of `repositories/`), record the real layout as the convention the design follows.

## 3. Database and migrations

| Look at | Command | Record |
|---|---|---|
| Alembic setup | `alembic.ini`, `alembic/env.py` | Which metadata `env.py` imports, async or sync engine in `env.py`, where the URL comes from |
| History | `uv run alembic heads`; `uv run alembic history \| head -20` | Current head(s); more than one head is a blocker to raise before planning migrations |
| Live schema (optional, dev database only) | Postgres MCP in restricted (read-only) mode, `backend-postgres` | Tables, indexes, row counts of the tables a migration will touch (lock and volume risk). Never point it at production; never change schema through it |

`alembic heads` reads files only. Do not run `alembic upgrade`, `current` against a shared database, or any write during the scan.

## 4. Tests

| Look at | Where | Record |
|---|---|---|
| Layout | `ls tests/`; `find tests -name conftest.py` | Mirror of `app/` or by type (unit/integration) |
| Database in tests | `conftest.py` | Real PostgreSQL test database or SQLite; created by `alembic upgrade head` or `create_all`; transaction-per-test rollback or truncation |
| HTTP client | `rg -n "ASGITransport|TestClient" tests/` | `httpx.AsyncClient` with `ASGITransport`, or `TestClient` |
| Auth in tests | fixtures named like `auth_headers`, `user_token`, factories | How a test acts as each role; where test credentials come from (fixtures, `.env.test`), never their values |
| Baseline run (optional) | `uv run pytest -q` | Pass/fail count before the change, so later failures are attributable. A failing baseline is recorded, not fixed |

## 5. Output of the scan

- `codebase-notes.md` `## 3. Verified Baseline Facts`: one line per fact with its path or command.
- `## 4. Constraints`: versions, the package manager prefix, the test database rule, "no production database access".
- `## 0. Question Queue`: each conflict or choice found (`Q-NN`, `OPEN`), asked one at a time.
- Nothing about values of secrets: names of variables only.
