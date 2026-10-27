---
skills:
  - backend-fastapi
  - backend-postgres
  - backend-database-migrations
  - backend-realtime
  - backend-api-contract-design
---
## Backend rules (Python + FastAPI + PostgreSQL)

- **Source and test folders**: `app/`, `tests/` (`tests/unit/`, `tests/integration/`), and `alembic/`.
- **Reproduction check**: a focused unit, repository, or in-process endpoint test under `tests/` (`httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")`) that fails for the reported reason, run non-interactively with `uv run pytest <test_path>::<test_name> -q` (and `uv run pytest <id> -vv -s --tb=long --showlocals --log-cli-level=DEBUG` to inspect the first chained exception frame under `app/`). Never pass `--pdb`, `--trace`, or `breakpoint()`.
- **Architecture profile**: take `architecture_profile.mode` from the `design.md` of the work item that built the service module; without one, resolve it from `.superpowers/setup.json` (`architecture_profile`) and `{{slot:architecture-design}}`. Record the mode in `brief.md` → `## 7` → **Architecture profile** and fix inside that profile's `{{slot:root-cause-debugging}}` and `{{slot:clean-architecture}}` rules.
- **Floors (at least L3)**:
  - any database schema change or new/modified Alembic migration under `alembic/versions/` (never run `metadata.create_all()` or ad-hoc DDL);
  - any breaking or visible change to a public endpoint's request, response, status code, or error code in `api_contract.json` or OpenAPI;
  - authentication, authorization, role-permission, or tenant/data-scope dependencies;
  - shared core utilities, middleware, database session/lifespan wiring, or exception handlers under `app/core/` or `app/common/`.
- **Temporary instrumentation (investigation mode)**: `logging` or `structlog` statements with a unique tag (`[DBG-<slug>]`) so every inserted line can be located and removed; **every** inserted line carries `[DBG-<slug>]` in the log string or as a trailing `# DBG-<slug>` comment; SQL query and N+1 inspection via `logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)` (`caplog`) and read-only `EXPLAIN (ANALYZE, BUFFERS)` via the Postgres MCP on a dev/test database (`DATABASE_URI` in `.env`, never production). Before returning `DIAGNOSED`, `rg -n "DBG-<slug>" app/ tests/` must return nothing and `uv run ruff check --select T10,T20 app tests` must exit `0`.
- **Local self-verification**: `uv run ruff format --check app tests`, `uv run ruff check app tests`, `uv run mypy app tests`, and `uv run pytest <touched_test_paths> -q` via `run_command`.
