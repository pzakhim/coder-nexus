# Sources

Our files rewrite ideas in this repo's vocabulary (tasks, evidence rows, `BLOCKED`, `D-NN`). The vendored library under `vendor/` is copied unchanged under its MIT license. Links are pinned to a commit; docs pages show the date read.

| Source (pinned link or doc URL + date read) | Stars | Idea taken | Where used |
|---|---|---|---|
| [supabase/agent-skills `skills/supabase-postgres-best-practices/SKILL.md`](https://github.com/supabase/agent-skills/blob/c9be0e931b7930f7d02126d04774d904c381e7d7/skills/supabase-postgres-best-practices/SKILL.md) + `references/*.md` (same sha), [LICENSE](https://github.com/supabase/agent-skills/blob/c9be0e931b7930f7d02126d04774d904c381e7d7/LICENSE) — 2026-10-23 | 2.9k | **VENDOR**: 31 rule files plus 3 authoring files, copied unchanged; prefix categories used for routing | `vendor/supabase-postgres-best-practices/`, `SKILL.md` §6 |
| [wshobson/agents `plugins/database-design/skills/postgresql-table-design/SKILL.md`](https://github.com/wshobson/agents/blob/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/database-design/skills/postgresql-table-design/SKILL.md) — 2026-10-23 | 42k | Identity over serial, UUID only when needed; `timestamptz`/`numeric`/`text` type table; FK columns are never auto-indexed; `NULLS NOT DISTINCT`; enums only for stable sets | `SKILL.md` §3, [02](02-schema-keys-and-indexes.md) |
| [crystaldba/postgres-mcp `README.md`](https://github.com/crystaldba/postgres-mcp/blob/15c8e33353546148acc2d8bd784551cf3905d1e2/README.md) — 2026-10-23 | 3.4k | Tool list; restricted mode = read-only transactions + execution time limit, rejects `COMMIT`/`ROLLBACK`; read-only role recommended; `hypopg` and `pg_stat_statements` prerequisites; credentials in config are a weak point | `SKILL.md` §5, [04](04-postgres-mcp.md) |
| https://docs.sqlalchemy.org/en/20/core/pooling.html — 2026-10-23 | — | `AsyncAdaptedQueuePool` default for async engines; `pool_size` 5 + `max_overflow` 10 defaults; `pool_pre_ping`, `pool_recycle`, `pool_timeout`; dispose after fork; `NullPool` | [01](01-async-sessions-and-pool.md) Engine, Pool sizing |
| https://docs.sqlalchemy.org/en/20/dialects/postgresql.html — 2026-10-23 | — | `postgresql_concurrently`, `postgresql_where`, `postgresql_include`, `Identity()`; asyncpg dialect URL parameters (`prepared_statement_cache_size`, `prepared_statement_name_func`) | [01](01-async-sessions-and-pool.md) PG7, [02](02-schema-keys-and-indexes.md) |
| https://magicstack.github.io/asyncpg/current/ and its FAQ — 2026-10-23 | — | Prepared statements break under PgBouncer transaction/statement mode (`statement_cache_size=0` or session mode); `IN $1` is invalid, use `= ANY($1)`; `server_settings` | [01](01-async-sessions-and-pool.md) PG6, PG7 |
| https://www.postgresql.org/docs/current/explicit-locking.html — 2026-10-23 | — | Lock levels; waits are indefinite unless a timeout is set | [01](01-async-sessions-and-pool.md) Timeouts |
| Internal: `plugins/packs/backend/skills/code-review/references/bug_patterns.md`, `src/skill_factory/library/generators/create-clean-architecture-skill/stacks/python-fastapi.md` | — | Sessions injected through `Depends`, never opened inside use cases; multi-table writes in one transaction; N+1 inside loops; naive vs aware datetimes; floats for money | [01](01-async-sessions-and-pool.md) PG1–PG3, [02](02-schema-keys-and-indexes.md) types, [03](03-query-plans-and-n-plus-one.md) N+1 |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Load the vendored skill as its own top-level skill | supabase/agent-skills | It would trigger on every Postgres task with RLS/Supabase advice that does not apply to most workspaces; routing through `SKILL.md` §6 keeps the applicability limits in front of the agent |
| Editing vendored files to remove Supabase-specific notes | supabase/agent-skills | VENDOR means unchanged (license and future re-sync); limits are stated in our `SKILL.md` instead |
| RLS as the default authorization mechanism | supabase/agent-skills `security-rls-basics.md` | Our authorization lives in the service layer (`{{slot:secure-coding-standards}}`); RLS only where the workspace already uses it or a `D-NN` decides it |
| Text-based time-prefixed primary keys | supabase/agent-skills `schema-primary-keys.md` | Wider index, type confusion; identity or UUIDv7 cover the needs |
| `--access-mode=unrestricted` for development | crystaldba/postgres-mcp README | Schema and data change only through Alembic and code; the agent needs read access for facts and plans only |
| SSE transport / shared MCP server | crystaldba/postgres-mcp README | One local stdio server per workspace keeps `DATABASE_URI` local |
| Partitioning, TimescaleDB, extension catalog | wshobson/agents table design | Rarely needed; partitioning needs a design decision and stays behind the vendored `schema-partitioning.md` pointer |
| SQLModel | — | Approved stack is SQLAlchemy 2 async + repository layer |
