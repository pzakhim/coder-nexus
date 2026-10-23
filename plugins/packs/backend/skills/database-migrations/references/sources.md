# Sources

Ideas rewritten in this repo's vocabulary (phases, evidence rows, `BLOCKED`, `D-NN`). Links are pinned to a commit; docs pages show the date read.

| Source (pinned link or doc URL + date read) | Stars | Idea taken | Where used |
|---|---|---|---|
| Internal base: `src/skill_factory/library/generators/create-database-migrations-skill/` (`references/base-rules.md` M1–M14, `patterns.md`, `tooling-by-stack.md`, templates 01–05) | — | Real runner and target first; credentials are not authority; never deliver through reset/sync/seed; expand/backfill/contract; idempotent and immutable revisions; existing data and `NOT VALID`; locks and volume; scoped parameterised backfills; disposable-DB verification; backup and recovery; migration states; handoff packet fields | `SKILL.md`, all references, `templates/migration-handoff.md.tpl` |
| [wshobson/agents `plugins/framework-migration/skills/database-migration/SKILL.md`](https://github.com/wshobson/agents/blob/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/framework-migration/skills/database-migration/SKILL.md) — 2026-10-23 | 42k | Zero-downtime rename and type change as add → copy → switch → drop; data transformations in batches; every migration has a down path | [02](02-safe-schema-changes.md) Other changes, [03](03-data-backfills.md), [01](01-alembic-workflow.md) A6 |
| [supabase/agent-skills `references/schema-constraints.md`, `lock-short-transactions.md`](https://github.com/supabase/agent-skills/blob/c9be0e931b7930f7d02126d04774d904c381e7d7/skills/supabase-postgres-best-practices/SKILL.md) (vendored in `backend-postgres`) — 2026-10-23 | 2.9k | Constraints added safely in migrations; short transactions | [02](02-safe-schema-changes.md), [03](03-data-backfills.md) B3 |
| https://alembic.sqlalchemy.org/en/latest/autogenerate.html — 2026-10-23 | — | What autogenerate detects / cannot detect (renames, anonymous constraints, server defaults, sequences, EXCLUDE); `compare_type` default on since 1.12; name every constraint; `alembic check`; "not intended to be perfect" | [01](01-alembic-workflow.md) Generate, then hand review; [04](04-verification.md) V2 |
| https://alembic.sqlalchemy.org/en/latest/cookbook.html — 2026-10-23 | — | Async `env.py` (`async_engine_from_config`, `run_sync`, `alembic init -t async`); skip empty autogenerate via `process_revision_directives`; data migrations as separate script or `-x data=true` | [01](01-alembic-workflow.md) setup table, [03](03-data-backfills.md) where it runs |
| https://docs.sqlalchemy.org/en/20/dialects/postgresql.html — 2026-10-23 | — | `postgresql_concurrently=True` must run outside a transaction block | [02](02-safe-schema-changes.md) index pattern |
| https://www.postgresql.org/docs/current/sql-createindex.html — 2026-10-23 | — | `CONCURRENTLY` cannot run in a transaction block; two scans; a failure leaves an `INVALID` index to drop and rebuild or `REINDEX CONCURRENTLY` | [02](02-safe-schema-changes.md), [04](04-verification.md) V6 |
| https://www.postgresql.org/docs/current/explicit-locking.html — 2026-10-23 | — | Lock modes per command (ACCESS EXCLUSIVE for most ALTER TABLE forms, SHARE for CREATE INDEX, SHARE UPDATE EXCLUSIVE for concurrent builds and VALIDATE); waits are indefinite without a timeout | [02](02-safe-schema-changes.md) Lock awareness, A7 |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Authorised agent may apply to shared targets (generator M2 "apply only to targets the user authorised") | create-database-migrations-skill | Approved decision for this pack: shared environments are always applied by the user / DevOps; the agent hands off |
| Backup-table checkpoint (`CREATE TABLE users_backup AS SELECT …`) as rollback | wshobson/agents database-migration | Doubles storage and locks on large tables, copies personal data into an unmanaged table; recovery is the owner's backup/restore |
| Sequelize, TypeORM, Prisma examples; cross-ORM migration | wshobson/agents database-migration | Not this stack; Alembic only |
| Wrapping the whole migration in one transaction as the default rollback strategy | wshobson/agents database-migration | Correct for small DDL (Alembic already does it), wrong for concurrent indexes and large backfills, which must commit in steps |
| `pytest-alembic` as a required dependency | — | Adding a test library is a separate decision; used only if the workspace has it ([04](04-verification.md)) |
| Merge revisions as the normal way to resolve multiple heads | Alembic docs (branches) | Re-pointing an unshipped revision keeps the chain linear; merge only when both branches were applied somewhere shared (A4) |
| Squashing old revisions | — | Changes history other environments already ran; out of scope for feature work |
