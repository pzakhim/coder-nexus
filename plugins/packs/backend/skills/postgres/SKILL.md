---
name: postgres
description: "PostgreSQL & SQLAlchemy 2 async (`asyncpg`) standard for the Python Backend — `PG1`–`PG7` async session/transaction/eager-loading/pool/timeout rules, schema keys (`Identity()` / `UUIDv7`), `DateTime(timezone=True)`, mandatory FK and filter indexing, `EXPLAIN (ANALYZE, BUFFERS)` and N+1 detection, safe `postgres-mcp --access-mode=restricted` usage (`MCP1`–`MCP9`), and routing into the vendored `supabase-postgres-best-practices` rule library."
---

# PostgreSQL (SQLAlchemy 2 Async + `asyncpg` + `postgres-mcp`)

Authoritative PostgreSQL standard for the Python Backend Pack. Combines **SQLAlchemy 2 Async (`asyncpg`) rules (`PG1`–`PG7`)**, **read-only `postgres-mcp` guardrails (`MCP1`–`MCP9`)**, and **curated routing into the vendored MIT `supabase-postgres-best-practices` library** ([vendor/supabase-postgres-best-practices/](vendor/supabase-postgres-best-practices/SKILL.md)). Schema DDL is delivered strictly via Alembic (`backend-database-migrations`).

## 1. Baseline Facts to Record First (`codebase-notes.md`)

| Fact | Where to Inspect | Why It Matters |
|---|---|---|
| **PostgreSQL major version** | `docker-compose*.yml`, CI service image, or `SELECT version()` on dev DB | Governs `NULLS NOT DISTINCT` (PG 15+) and native `uuidv7()` (PG 18+) availability |
| **Engine & sessionmaker** | Module calling `create_async_engine` / `async_sessionmaker` | Configures `pool_size`, `max_overflow`, `expire_on_commit=False`, and `server_settings` timeouts |
| **Session dependency** | `yield` dependency in `app/api/deps.py` (`get_session`) | Enforces one `AsyncSession` per request (**PG1**) |
| **Connection pooler** | `DATABASE_URI` host/port or infra docs (PgBouncer / managed pooler) | Transaction-mode pooling requires disabling `asyncpg` prepared statement cache (**PG7**) |
| **Row-Level Security (RLS)** | `ENABLE ROW LEVEL SECURITY` / `CREATE POLICY` in `alembic/versions/` | Determines whether vendored `security-rls-*` rules apply (default is service-layer auth) |

## 2. Mandatory PostgreSQL & SQLAlchemy 2 Async Rules (`PG1`–`PG11` & `MCP1`–`MCP9`)

| ID | Rule | Reference |
|---|---|---|
| **PG1** | **One `AsyncSession` per request** via a `yield` dependency (`async with SessionFactory() as session:`); never share one session across `asyncio.gather` tasks. | [01](references/01-async-sessions-and-pool.md) |
| **PG2** | **Transactions belong to Services** (`async with session.begin():` or single `commit()`); repositories only `add`/`flush`/query and never `commit()`. | [01](references/01-async-sessions-and-pool.md) |
| **PG3** | **Zero lazy loading in async paths** — set `expire_on_commit=False` on `async_sessionmaker`, `lazy="raise"` on relationships, and load explicitly via `selectinload` / `joinedload`. | [01](references/01-async-sessions-and-pool.md) |
| **PG4** | **Size connection pool against `max_connections`** (`(pool_size + max_overflow) * workers * replicas + headroom < max_connections`) with `pool_pre_ping=True`. | [01](references/01-async-sessions-and-pool.md) |
| **PG5** | **Enforce `statement_timeout` and `idle_in_transaction_session_timeout`** on every connection via `server_settings`. | [01](references/01-async-sessions-and-pool.md) |
| **PG6** | **Parameterized SQL only** — SQLAlchemy expressions or `text()` with `:param` binds (`= ANY(:ids)` for lists) and allow-listed sort columns; never f-strings. | [01](references/01-async-sessions-and-pool.md) |
| **PG7** | **Disable `asyncpg` statement cache behind transaction-mode poolers** (`prepared_statement_cache_size=0`). | [01](references/01-async-sessions-and-pool.md) |
| **PG8** | **Named constraints (`MetaData(naming_convention=...)`) & proper types** (`Identity()` or `UUIDv7` keys, `DateTime(timezone=True)` UTC, `Numeric(p,s)` for money). | [02](references/02-schema-keys-and-indexes.md) |
| **PG9** | **Index every foreign key and every filter/join/sort column** (composite in query order; `CREATE INDEX CONCURRENTLY` on populated tables via Alembic). | [02](references/02-schema-keys-and-indexes.md) |
| **PG10** | **Prove query plans (`EXPLAIN (ANALYZE, BUFFERS)`) and guard list endpoints against N+1** (`count_queries` statement-count test). | [03](references/03-query-plans-and-n-plus-one.md) |
| **PG11 / MCP1–9** | **Use `postgres-mcp` strictly in `--access-mode=restricted` against dev/test DBs only** — never connect to production, never echo `DATABASE_URI`, and never run DDL outside Alembic. | [04](references/04-postgres-mcp.md) |

## 3. Vendored Supabase Postgres Rule Library (`vendor/supabase-postgres-best-practices/`)

Open only the vendored file matching your task under [vendor/supabase-postgres-best-practices/](vendor/supabase-postgres-best-practices/SKILL.md) ([NOTICE](vendor/supabase-postgres-best-practices/NOTICE)). Where a vendored file conflicts with `PG1`–`PG11`, this skill wins:

| Task Concern | Vendored Reference Files (`vendor/supabase-postgres-best-practices/references/`) |
|---|---|
| **Missing / Composite / Partial / Covering Indexes** | `query-missing-indexes.md`, `query-composite-indexes.md`, `query-partial-indexes.md`, `query-covering-indexes.md`, `query-index-types.md` |
| **Connection Pooling & Prepared Statements** | `conn-pooling.md`, `conn-limits.md`, `conn-idle-timeout.md`, `conn-prepared-statements.md` |
| **Schema Data Types, Primary Keys & Foreign Keys** | `schema-data-types.md`, `schema-primary-keys.md`, `schema-foreign-key-indexes.md`, `schema-lowercase-identifiers.md`, `schema-constraints.md` |
| **Locks, Short Transactions, Queues & Deadlocks** | `lock-short-transactions.md`, `lock-deadlock-prevention.md`, `lock-skip-locked.md`, `lock-advisory.md` |
| **N+1, Keyset Pagination, Batch Inserts & Upserts** | `data-n-plus-one.md`, `data-pagination.md`, `data-batch-inserts.md`, `data-upsert.md` |
| **Performance Diagnostics (`EXPLAIN`, `pg_stat_statements`, Vacuum)** | `monitor-explain-analyze.md`, `monitor-pg-stat-statements.md`, `monitor-vacuum-analyze.md` |
| **Full-Text Search, JSONB GIN Indexes & Partitioning** | `advanced-full-text-search.md`, `advanced-jsonb-indexing.md`, `schema-partitioning.md` (requires `D-NN`) |
| **Privileges & Row-Level Security (RLS)** | `security-privileges.md`; `security-rls-basics.md` & `security-rls-performance.md` (**only** if the workspace uses RLS per §1) |

## 4. Reference Guides

| Topic | Reference File |
|---|---|
| `AsyncSession` lifecycle, service transactions, `lazy="raise"`, pool sizing, timeouts, parameterized SQL (`PG1`–`PG7`) | [01-async-sessions-and-pool.md](references/01-async-sessions-and-pool.md) |
| Constraint naming convention, keys (`Identity` / `UUIDv7`), column types (`timestamptz`, `Numeric`), and indexing (`PG8`–`PG9`) | [02-schema-keys-and-indexes.md](references/02-schema-keys-and-indexes.md) |
| `EXPLAIN (ANALYZE, BUFFERS)` workflow and `count_queries` N+1 regression testing (`PG10`) | [03-query-plans-and-n-plus-one.md](references/03-query-plans-and-n-plus-one.md) |
| Safe `postgres-mcp --access-mode=restricted` rules (`MCP1`–`MCP9`), CLI/MCP verification gates (`PASS` / `FAIL`), and `BLOCKER` / `MAJOR` / `MINOR` review grading | [04-postgres-mcp.md](references/04-postgres-mcp.md) |
