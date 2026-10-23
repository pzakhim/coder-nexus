# 04 — Verification on a disposable database

Only a real upgrade, with data, on a database you may destroy shows what a shared environment will do. Every command below produces an evidence row (`work-item-contract` hand-off and status §4) on the exact revision; a command that did not run is `NOT_RUN`, an unreachable database is `BLOCKED`.

## The disposable database

Use what `PHASE-00` prepared, in this order of preference:

1. The workspace's test database service (`docker compose up -d db-test` or similar) with its own database name.
2. A throwaway database on the local server: `createdb app_migration_check` / `dropdb app_migration_check` (local server only).
3. A container started by the test suite (testcontainers) when the workspace already uses it.

Point Alembic at it the way `env.py` reads the URL (for example `DATABASE_URL=postgresql+asyncpg://…/app_migration_check` from `.env.test`), never by editing the shared `.env`. Confirm the host is local before the first write (host check in `backend-postgres` [04](../../postgres/references/04-postgres-mcp.md)). The database must be on the same PostgreSQL major version as production (`docker-compose` image tag); lock and default behaviour differ between versions.

## Recipe (cwd: backend root)

| # | Check | Command | Expected | Proves |
|---|---|---|---|---|
| V1 | Clean install | fresh DB → `uv run alembic upgrade head` | exit 0; last line names the new revision | The whole chain still applies from zero (catches revisions that import models) |
| V2 | One head, no drift | `uv run alembic heads`; `uv run alembic check` | one head; `No new upgrade operations detected.` | Models and migrations agree; nothing left un-migrated |
| V3 | Upgrade **with data** | `uv run alembic downgrade -1` (or a DB restored to the previous head) → load representative rows (fixture/seed script, several tenants, NULLs and edge values, duplicates if adding a unique constraint) → `uv run alembic upgrade head` | exit 0 | The step works on existing rows, not just an empty table |
| V4 | Data invariants | the invariant queries from the design/backfill (`SELECT count(*) … WHERE currency IS NULL` → `0`; rows of other tenants unchanged) | stated values | The backfill did exactly what was intended |
| V5 | Reversible | `uv run alembic downgrade -1` then `uv run alembic upgrade head` | exit 0 both; for an irreversible data step the structure returns and the hand-off says data is not restored | `downgrade()` is real; a rerun of upgrade is safe |
| V6 | Index validity | `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;` | no rows | No `INVALID` index left by a concurrent build |
| V7 | Lock review | `uv run alembic upgrade <prev>:<new> --sql` and read it | every statement matches a safe pattern in [02](02-safe-schema-changes.md); `lock_timeout` present | The SQL DevOps will run is the SQL you reviewed |
| V8 | Behaviour | `uv run pytest tests/<affected> -q` against the migrated DB | named tests pass | API and workers work on the new schema |

Large backfill command: run it with `--dry-run`, then for real, then again (must report 0 rows changed: idempotent), and run V4.

## Optional automated migration tests

If the workspace already has migration tests (for example `pytest-alembic` or a `tests/migrations/` suite running upgrade/downgrade per revision), run them as an extra check: `uv run pytest tests/migrations -q`. Do not add a new testing library in a feature task; propose it as a separate item.

## What is not proof

| Looks like proof | Why it is not |
|---|---|
| "The app started" / startup ran migrations | Says nothing about data, invariants or downgrade; may have run against the wrong DB |
| A row in `alembic_version` | Only says Alembic recorded a revision, not that every statement did what was intended |
| `alembic upgrade --sql` alone | Offline SQL generation runs nothing |
| A run on an empty database | Existing-row problems (NULLs, duplicates, locks) only appear with data |
| Output from another revision or another database | Evidence is bound to the exact revision and target |

## Cleanup

Drop the throwaway database or stop only the containers you started ([quality-acceptance](../../quality-acceptance/SKILL.md) environment rules E2: never stop what someone else started). Keep the command output as evidence.
