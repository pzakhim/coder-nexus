---
name: postgres
description: PostgreSQL knowledge for the Python backend - SQLAlchemy 2 async with asyncpg (one AsyncSession per request, transactions in services, eager loading instead of lazy loads, pool sizing against max_connections, statement timeouts, parameterised queries), keys, timestamptz and indexes for every foreign key and filter, the EXPLAIN ANALYZE workflow, N+1 detection, safe use of the postgres-mcp server, and when to open which vendored Supabase Postgres rule. Use whenever a task writes or reviews a model, repository query, index, connection setting or slow-query fix against PostgreSQL, or uses the postgres MCP tools, even for a one-column change or a single query.
---

# PostgreSQL (SQLAlchemy 2 async + asyncpg)

Stack knowledge only. The process (tasks, checks, evidence, review, statuses) stays in core: `incremental-implementation`, `{{slot:unit-testing}}`, `{{slot:root-cause-debugging}}`, `evidence-standard`, `{{slot:secure-coding-standards}}`. Schema changes are delivered only through Alembic ([database-migrations](../database-migrations/SKILL.md)). Layer placement of sessions, repositories and services comes from `{{slot:clean-architecture}}`; FastAPI dependency mechanics from [fastapi](../fastapi/SKILL.md).

## 1. Read the workspace first

Before changing anything, record from the repository (not from memory):

| Fact | Where | Reason |
|---|---|---|
| PostgreSQL major version | `docker-compose*.yml`, CI service image, `SELECT version()` on the dev DB | Lock behaviour, `NULLS NOT DISTINCT`, `uuidv7()` availability depend on it |
| Engine and session setup | the module calling `create_async_engine` / `async_sessionmaker` | Pool size, `expire_on_commit`, timeouts are set once there |
| Session dependency | the `yield` dependency used by routes | Every rule in §2 hangs off it |
| Pooler in front of Postgres | `DATABASE_URL` host/port, infra docs (PgBouncer, a managed pooler) | Transaction pooling breaks asyncpg prepared statements |
| RLS in use | `ENABLE ROW LEVEL SECURITY` / `CREATE POLICY` in migrations | Decides whether the vendored `security-rls-*` rules apply at all |

## 2. Rules for SQLAlchemy 2 async + asyncpg

Detail, safe and unsafe code side by side: [references/01-async-sessions-and-pool.md](references/01-async-sessions-and-pool.md).

| # | Rule | Reason |
|---|---|---|
| PG1 | **One `AsyncSession` per request**, created by a `yield` dependency from one `async_sessionmaker`, closed in `finally`/`async with`. Never a module-level session, never one session shared across `asyncio.gather` tasks. | An `AsyncSession` is not safe for concurrent use; a shared session leaks state and transactions between requests. |
| PG2 | **Transactions belong to services** (`async with session.begin():` or one explicit `commit()` per use case). Repositories `add`/`flush`/query, never `commit`. Routes never commit. | One use case = one atomic unit; commits scattered in repositories leave half-written data when a later step fails. |
| PG3 | **No lazy loading in async paths.** Load relationships explicitly with `selectinload` (collections) or `joinedload` (many-to-one); set `lazy="raise"` on relationships; `expire_on_commit=False` on the sessionmaker. | An implicit lazy load in async code raises `MissingGreenlet` or hides an extra round trip per row (N+1). |
| PG4 | **Size the pool against `max_connections`.** `(pool_size + max_overflow) × processes (workers × replicas) + migrations/admin headroom < max_connections`. Use `pool_pre_ping=True`, a finite `pool_timeout`, `pool_recycle` below any proxy idle cut-off. | Each worker process owns its own pool; defaults (5 + 10) multiplied by workers exhaust the server. |
| PG5 | **Statement and lock timeouts on every connection** (`server_settings` → `statement_timeout`, `idle_in_transaction_session_timeout`); `lock_timeout` for DDL. | A runaway query or a forgotten open transaction holds locks and connections until someone notices. |
| PG6 | **Parameterised queries only**: ORM/Core expressions or `text()` with `:name` bind parameters. Never f-strings, `%`, or `.format()` into SQL; identifiers (sort columns) come from an allow-list. | String-built SQL is injection (`{{slot:secure-coding-standards}}` SC rules); bind parameters also let Postgres reuse plans. |
| PG7 | **Behind a transaction-mode pooler**, disable asyncpg's statement cache (`prepared_statement_cache_size=0` in the URL plus unique statement names) or use session pooling. | Prepared statements are per server connection; the pooler hands you another one and the call fails. |

## 3. Schema rules

Detail: [references/02-schema-keys-and-indexes.md](references/02-schema-keys-and-indexes.md).

- Keys: `BIGINT GENERATED ALWAYS AS IDENTITY` (`Identity()`) for internal ids; `UUID` when ids are exposed or generated outside the DB (time-ordered v7 where available). Follow the workspace's existing choice. Reason: identity is compact and ordered; random UUIDv4 keys scatter index inserts.
- Time: `TIMESTAMP WITH TIME ZONE` (`DateTime(timezone=True)`), stored UTC, server default `now()`. Reason: naive timestamps lose the offset and compare wrongly across zones.
- Money and exact values: `Numeric(p, s)`; strings: `Text`/`String` with a `CHECK` if a limit is a business rule; `JSONB` only for genuinely optional attributes.
- **An index for every foreign key column and every column used in a filter, join or sort** on a non-trivial table, as a composite in query order when filters combine. Reason: Postgres never indexes the referencing side of a foreign key; unindexed filters become sequential scans as data grows.
- Every constraint has a name via `MetaData(naming_convention=...)`. Reason: Alembic cannot track anonymous constraints.
- New columns and tables change only through an Alembic revision, never `metadata.create_all()` or the MCP server outside tests.

## 4. Query plans and N+1

Workflow and how to read a plan: [references/03-query-plans-and-n-plus-one.md](references/03-query-plans-and-n-plus-one.md).

1. Reproduce the slow call on the dev/test DB with realistic row counts; capture the emitted SQL (`echo=True` on a test engine or the SQL log) and its parameters.
2. `EXPLAIN (ANALYZE, BUFFERS)` the exact statement; find the node with the largest actual time or rows mismatch.
3. Propose an index or query change; check it with `explain_query` hypothetical indexes (§5) or on the disposable DB.
4. Ship the index through an Alembic revision (`CREATE INDEX CONCURRENTLY`, `backend-database-migrations`); re-run the plan and record before/after as evidence rows.

N+1 is detected by counting statements in a test (event listener on `before_cursor_execute`) for a list endpoint with several rows: the count must not grow with the number of rows.

## 5. postgres-mcp (shipped by this pack)

Full rules: [references/04-postgres-mcp.md](references/04-postgres-mcp.md). In short:

- Runs as `postgres-mcp --access-mode=restricted` (read-only transactions, execution time limit). Never switch it to `unrestricted`.
- `DATABASE_URI` comes from the workspace `.env` (ignored by git), pointing at a **dev or test** database with a read-only role. Never paste or echo its value.
- **Never production.** If the host is not a known local/dev/test host (`localhost`, `127.0.0.1`, a compose service name, a host the user named as dev/test), stop and ask the user before calling any tool.
- Use `list_schemas`, `list_objects`, `get_object_details`, `explain_query` (with hypothetical indexes), `analyze_query_indexes`, `analyze_workload_indexes`, `get_top_queries`, `analyze_db_health` for facts and index advice.
- `execute_sql` is for read-only inspection only. Schema changes go through Alembic; data fixes through a reviewed migration or service code.
- MCP output is evidence of a fact on that database at that time, not proof the code is correct: the decisive check is still a command in the task.

## 6. Vendored rule library (Supabase, MIT)

[vendor/supabase-postgres-best-practices/](vendor/supabase-postgres-best-practices/SKILL.md) is copied unchanged ([NOTICE](vendor/supabase-postgres-best-practices/NOTICE)). Open only the file the task needs. Where a vendored rule and this skill disagree, this skill and the core skills win.

| Task touches | Open (under `vendor/supabase-postgres-best-practices/references/`) |
|---|---|
| A new filter, join or sort; slow query | `query-missing-indexes.md`, `query-composite-indexes.md`, `query-partial-indexes.md`, `query-covering-indexes.md`, `query-index-types.md` |
| Pool, workers, pooler, prepared statements | `conn-pooling.md`, `conn-limits.md`, `conn-idle-timeout.md`, `conn-prepared-statements.md` |
| New table or column type, keys, foreign keys | `schema-data-types.md`, `schema-primary-keys.md`, `schema-foreign-key-indexes.md`, `schema-lowercase-identifiers.md`, `schema-constraints.md` |
| Very large or time-series tables | `schema-partitioning.md` (only with a design decision `D-NN`) |
| Locks, long transactions, queues, deadlocks | `lock-short-transactions.md`, `lock-deadlock-prevention.md`, `lock-skip-locked.md`, `lock-advisory.md` |
| List endpoints, bulk writes, upserts | `data-n-plus-one.md`, `data-pagination.md`, `data-batch-inserts.md`, `data-upsert.md` |
| Diagnosing performance | `monitor-explain-analyze.md`, `monitor-pg-stat-statements.md`, `monitor-vacuum-analyze.md` |
| Search or JSONB filters | `advanced-full-text-search.md`, `advanced-jsonb-indexing.md` |
| Database roles and grants | `security-privileges.md` |
| Row-Level Security | `security-rls-basics.md`, `security-rls-performance.md` — **only if the workspace already uses RLS** (§1) |

Applicability limits:

- RLS, `auth.uid()`, `auth.*` functions, `anon` / `authenticated` roles and Supabase dashboard or pooler notes apply **only when the workspace uses RLS / Supabase**. Otherwise authorization stays in the service layer per `{{slot:secure-coding-standards}}`; do not introduce RLS without a design decision.
- Extension-based advice (`pg_uuidv7`, `pg_stat_statements`, `hypopg`) needs the extension to exist; adding one is a migration and a design decision, not a side effect.
- Raw SQL examples show the target shape; in application code write them as SQLAlchemy expressions with bind parameters (PG6).
- `_contributing.md`, `_template.md`, `_sections.md` are authoring files of the vendored library; no task needs them.

## Sources

[references/sources.md](references/sources.md)
