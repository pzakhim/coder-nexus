# 01 — Alembic workflow

## Read the setup first

Record these facts in `codebase-notes.md` before writing a revision. Reread them on every new work item: setups change.

| Fact | Where | Why it matters |
|---|---|---|
| Command prefix | `uv.lock` → `uv run`; `poetry.lock` → `poetry run`; otherwise the project venv (`.venv/bin/alembic`) | Running a global `alembic` uses the wrong package versions |
| Backend root (cwd) | directory holding `alembic.ini` | Alembic resolves `script_location` from there |
| How the URL is loaded | `alembic/env.py` (`config.set_main_option`, settings object, `DATABASE_URL` env var) | Decides how you point a run at the disposable database without touching `.env` of a shared target |
| Async or sync `env.py` | `async_engine_from_config` + `connection.run_sync(do_run_migrations)` means async (template `alembic init -t async`) | Async env.py needs the `postgresql+asyncpg` URL; sync needs a sync driver |
| `target_metadata` | `env.py` imports the declarative `Base.metadata` — and every models module must be imported | A model not imported is invisible to autogenerate, which then proposes dropping its table |
| Transaction mode | `transaction_per_migration` in `context.configure` (default: one transaction for the whole run on PostgreSQL) | `autocommit_block()` commits whatever ran before it in that transaction |
| Revision file template | `file_template` in `alembic.ini` | Keep the existing naming; do not change it in a feature task |
| Hooks | `post_write_hooks` (ruff format), `process_revision_directives` (skip empty autogenerate), `compare_server_default` | Tells you what the generated file will look like and what autogenerate compares |
| Existing revisions | newest 3–5 files in `alembic/versions/` | Style (raw SQL vs `op.*`), naming of constraints, how data steps are written |

## Generate, then hand review

```bash
# cwd: backend root, DATABASE_URL pointing at the local/disposable DB already at head
uv run alembic upgrade head                      # autogenerate compares against the live schema
uv run alembic revision --autogenerate -m "add customer_id index to orders"
```

Then read every line of the new file:

| Autogenerate | Your review |
|---|---|
| Detects added/removed tables and columns, nullability, named indexes/uniques, foreign keys, type changes (`compare_type` on by default since 1.12) | Confirm each one is intended; delete unrelated drift (a model change from another branch) |
| Shows a **rename** as `drop_column` + `add_column` | Rewrite as `op.alter_column(..., new_column_name=...)` — or as expand/contract if the running version reads the old name ([02](02-safe-schema-changes.md)). A drop + add loses the data |
| Ignores anonymous constraints, named CHECK constraints (by default), server default changes (unless enabled), sequences, `EXCLUDE` | Add them by hand; name every constraint (naming convention in `backend-postgres`) |
| Emits plain `create_index` | On any populated table, rewrite as concurrent ([02](02-safe-schema-changes.md)) |
| Emits `nullable=False` on a new column of a populated table | Rewrite with a default or the three-step NOT NULL pattern |
| Emits enum type changes poorly | Write `ALTER TYPE … ADD VALUE` by hand; never drop a value still stored |
| Empty `upgrade()` | Delete the file unless the revision is intentionally data-only |

Autogenerate "is not intended to be perfect" (Alembic docs): the reviewed file, not the generated one, is what ships.

## Rules for every revision

| # | Rule | Reason |
|---|---|---|
| A1 | **One revision per logical change** (one expand step, one backfill, one contract step). A task may add one revision; a phase may add several in order. | Small revisions are reviewable, revertible and map to the plan's expand/backfill/contract steps. |
| A2 | **Message**: imperative, lower case, what changes — `add customer_id index to orders`, `backfill orders.currency`, `drop orders.legacy_status`. | The message becomes the file slug and the history line DevOps reads. |
| A3 | **Single linear chain.** `down_revision` points to the current head; `uv run alembic heads` shows one head before you hand off. | Multiple heads make `upgrade head` fail or run in an undefined order. |
| A4 | **Rebased onto a branch with a newer head?** If your revision was never applied to a shared environment, re-point its `down_revision` to the new head and re-verify. Create a merge revision (`alembic merge`) only when both branches are already applied somewhere shared, and say so in the hand-off. | Re-pointing keeps history linear; a merge is needed only when both orders already happened. |
| A5 | **Self-contained revisions.** Do not import application models or services; describe tables with `sa.table("orders", sa.column("id"), …)` or use `op.execute(sa.text(...))`. | Models change after the revision is written; an old revision importing today's model breaks a fresh install. |
| A6 | **Real `downgrade()`** that reverses the schema step. If the step destroys data (drop column/table, lossy type change), `downgrade()` restores the structure and the docstring plus the hand-off say "data not restored — irreversible step". | Verification runs `downgrade -1`; a fake or empty downgrade hides that recovery means a backup restore. |
| A7 | **Lock guard first.** Start `upgrade()` with `op.execute("SET LOCAL lock_timeout = '5s'")` (value per workspace) for DDL on existing tables. | A DDL statement waiting for a lock blocks every later query on that table; failing fast is safer than queueing ([02](02-safe-schema-changes.md)). |
| A8 | **Static DDL only.** Values in data statements are bind parameters (`sa.text(":v")`); no f-strings with runtime data. | Same injection rule as application code (`backend-postgres` PG6). |
| A9 | **No secrets, no environment-specific values** (hostnames, tenant ids of a real customer) in revisions. | Revisions run everywhere and are committed. |

## Commands reference (cwd: backend root)

| Purpose | Command | Safe for the agent? |
|---|---|---|
| Current revision of the DB in `DATABASE_URL` | `uv run alembic current` | Yes (read) — on local/disposable only |
| History / heads | `uv run alembic history -r-5:`, `uv run alembic heads` | Yes (reads files) |
| Apply / step back | `uv run alembic upgrade head`, `uv run alembic downgrade -1` | Local/disposable DB only |
| Models vs migrations drift | `uv run alembic check` | Local/disposable DB only |
| Show SQL without running | `uv run alembic upgrade <from>:<to> --sql` | Yes; useful for the hand-off and lock review |
| `alembic stamp`, `downgrade base`, dropping/recreating a database, `create_all` | — | Never on anything shared; on the disposable DB only when the verification recipe says so |

Before any command that writes, confirm the target is the local/disposable database (host is `localhost`, a compose service, or the test container), without printing the secret: see `backend-postgres` [04-postgres-mcp](../../postgres/references/04-postgres-mcp.md) for the host check.
