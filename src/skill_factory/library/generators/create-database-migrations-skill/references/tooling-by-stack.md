# Runners, commands and engine notes

Always read the workspace's real runner and scripts first; these are only orientation.

| Runner | Files | Typical commands | Notes |
|---|---|---|---|
| Alembic (SQLAlchemy) | `alembic.ini`, `migrations/versions/*.py` | `alembic revision -m "…"`, `alembic upgrade head`, `alembic current`, `alembic history` | Autogenerate output must be reviewed by hand; concurrent indexes need `with op.get_context().autocommit_block()` |
| Django | `<app>/migrations/*.py` | `manage.py makemigrations`, `migrate`, `showmigrations`, `sqlmigrate` | `atomic = False` for concurrent operations; `RunPython` for data with a reverse function |
| Prisma | `prisma/schema.prisma`, `prisma/migrations/` | `prisma migrate dev` (local only), `prisma migrate deploy` (shared targets), `prisma migrate status` | Never `migrate reset` or `db push` against shared databases |
| TypeORM | `migrations/*.ts` | `typeorm migration:generate`, `migration:run`, `migration:revert` | Disable `synchronize` outside local |
| golang-migrate | `migrations/NNN_*.up.sql` / `.down.sql` | `migrate up`, `migrate version` | Dirty state needs a manual `force` after investigation |
| Custom SQL runner | e.g. `schema/manifest.json`, a loader module, numbered `.sql` files | Workspace `make` targets (migrate, status, validate, backup) | Read what it replays and in which order; it may not track checksums |

## Engine lock notes

| Engine | Watch out |
|---|---|
| PostgreSQL 11+ | `ADD COLUMN … DEFAULT <constant>` is fast; volatile defaults rewrite. `CREATE INDEX CONCURRENTLY` cannot run in a transaction. `NOT VALID` + `VALIDATE CONSTRAINT` avoids long locks. `ALTER TYPE` of a column usually rewrites. |
| MySQL 8 (InnoDB) | Prefer `ALGORITHM=INSTANT/INPLACE, LOCK=NONE` where supported; large tables may need online schema-change tools (by DevOps). |
| SQLite | Many `ALTER`s require table rebuilds; fine for local only. |

## Commands that are never a delivery path

Anything that resets, recreates, syncs/clones or seeds data (`migrate reset`, `db push`, `flush`, "db-sync", "bootstrap") — name the workspace's own ones in `01`.
