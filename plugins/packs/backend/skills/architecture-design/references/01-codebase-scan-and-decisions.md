# 01 — Backend Codebase Scan and Decision Rules

> Topic: Read-only 7-anchor Backend codebase scan, Scope Classification, and Socratic grilling / D-NN decision rules (`AD1`–`AD3`)

Every scan command runs read-only from the backend root (the directory containing `pyproject.toml`). Never edit files, install packages, run migrations, or write to a database during the scan. Record every verified finding in `codebase-notes.md` → `## 3. Verified Baseline Facts` with its file path (`AD1`).

## 1. Project & Tooling Scan

| Look at | Command | What to Record in `codebase-notes.md` |
|---|---|---|
| **Package manager & prefix** | `ls uv.lock poetry.lock requirements*.txt 2>/dev/null` | `uv run` / `poetry run` / `.venv/bin/` prefix for all commands |
| **Python & framework versions** | `sed -n '/^\[project\]/,/^\[/p' pyproject.toml` | Versions of FastAPI, Pydantic, SQLAlchemy, Alembic, `asyncpg`, `httpx`, `pytest-asyncio`, `import-linter` |
| **Tool configurations** | `rg -n "^\[tool\.(ruff|mypy|pytest|importlinter|fastapi)" pyproject.toml` | Ruff rule sets, mypy strictness, `asyncio_mode`, test paths |
| **App start & Docker** | `Dockerfile`, `docker-compose*.yml`, `Makefile`, `README.md` | Dev and test startup commands |

---

## 2. Application Structure Scan

| Look at | Command / Path | What to Record in `codebase-notes.md` |
|---|---|---|
| **App factory & lifespan** | `rg -n "FastAPI\(" app/` | `create_app` vs module-level app; `lifespan=` resources (DB engine, `httpx` client, Redis) |
| **Routers & prefixes** | `rg -n "APIRouter\(|include_router" app/` | URL prefixes (`/api/v1`), tags, router-level dependencies |
| **Dependencies & DI** | `rg -n "Depends\(" app/ \| head -n 40` | Session/UoW dependency, auth guard (`get_current_user`), service builders, `Annotated` aliases |
| **Error handling** | `rg -n "exception_handler|HTTPException" app/` | Domain exception classes, HTTP error envelope shape, status code mappings |
| **Settings** | `rg -n "BaseSettings" app/` and `.env.example` | Setting field names only (**never record secret values**), `DATABASE_URI` key, provider keys |
| **Auth & data scope** | Auth dependency & security module | Credential type (JWT, cookie, API key), roles/capabilities, how `owner_id` / `tenant_id` scope is resolved |
| **Services / Use cases** | `ls app/services/` (or module use cases) | Where business rules and transaction `commit()` calls live today |
| **Repositories & models** | `ls app/models/ app/repositories/`; `rg -n "select\(" app/` | SQLAlchemy 2.0 `select()` style, eager-loading strategy (`selectinload`), columns, FKs, unique constraints |
| **Outbound providers & realtime** | `rg -n "httpx|EventSourceResponse|StreamingResponse|WebSocket" app/` | External HTTP clients, timeouts, SSE/WebSocket channels |

**Workspace Convention Rule (`AD2` — `INIT` vs `EXTEND` vs `CORE IMPACT`):**
- `INIT`: New service or standalone domain module — apply the pack's full Clean Architecture layout (`{{slot:clean-architecture}}`).
- `EXTEND`: Adding endpoints, fields, or rules to an existing domain — follow the existing module's folder layout, base classes, and naming conventions (`C11`).
- `CORE IMPACT`: Modifying shared settings, DB engine/session lifecycle, auth dependencies, global error handlers, or shared tables — record blast radius across all consumers.

---

## 3. Database, Migrations & Test Harness Scan

| Look at | Command / Path | What to Record in `codebase-notes.md` |
|---|---|---|
| **Alembic setup** | `alembic.ini`, `alembic/env.py` | Target metadata, async vs sync migration engine, DB URL source |
| **Migration head(s)** | `uv run alembic heads` | Current head revision (multiple heads is a `BLOCKED` condition to resolve before planning migrations) |
| **Test harness** | `tests/conftest.py`; `rg -n "ASGITransport|TestClient" tests/` | Real PostgreSQL test DB vs SQLite; transaction rollback vs truncation; `httpx.AsyncClient(transport=ASGITransport(app=app))` vs `TestClient`; auth token fixtures |

---

## 4. When to Open a `Q-NN` and Record a `D-NN` Decision (`AD3`)

1. Record a decision (`D-NN`) in `codebase-notes.md` **only** when all three hold:
   - Two independently built parts (two phases, a service and a repository, this Backend API and the Frontend client) could otherwise choose incompatibly.
   - The answer is not already settled by the existing codebase conventions.
   - It represents a genuine architectural or contract trade-off.
2. **Backend divergence points that always require a `D-NN` when new:** error envelope & error codes, pagination shape (offset vs cursor), ID type (`UUID` vs `BIGINT`), timestamp format & timezone (`UTC`), auth scheme & capability guards, tenant/owner scope column, and database enum storage strategy.
3. Queue each open trade-off as `Q-NN` (`OPEN`) in `codebase-notes.md` (`## 0. Question Queue`), present 2–3 options with `(Recommended)` first via `grilling` (`01-solution-options-and-divergent-pass.md`) / `ask_question` **one question at a time**, and close the user's answer into `D-NN` (`Owner: planning`) before rendering `design.md`.
