# 03 — Data backfills

A backfill changes existing rows so a new structure becomes correct. It is the step most likely to rewrite the wrong data or hold a lock for minutes.

## Choose where the backfill runs

| Size (rows touched, from `reltuples` or a count on a representative DB) | Where | Reason |
|---|---|---|
| Small (finishes in seconds; workspace threshold, e.g. ≤ 10 000 rows) | Inside the revision: `op.execute(sa.text(...))` | Ships with the schema step; one transaction is acceptable |
| Large, or touching a hot table | A separate, idempotent backfill command in the codebase (e.g. `uv run python -m app.scripts.backfill_order_currency --batch-size 1000`), run between the expand and contract revisions | A single `UPDATE` of millions of rows holds row locks, bloats the table and replicates as one huge transaction; it also cannot be resumed |
| Optional data step the operator may skip | Alembic `-x data=true` switch (`context.get_x_argument(as_dictionary=True).get("data")`) | Only when the workspace already uses this convention |

The plan names the backfill as its own task with its own check; for shared environments it is part of the hand-off, run by the user / DevOps.

## Rules

| # | Rule | Reason |
|---|---|---|
| B1 | **Scoped.** Every `UPDATE`/`DELETE` has a `WHERE` that names exactly the rows to change, including the data scope (tenant, environment, owner) when the target value depends on it. | An unscoped statement rewrites every customer's data. |
| B2 | **Idempotent and resumable.** Select only rows still needing work (`WHERE currency IS NULL`), so a rerun after a crash continues instead of redoing or double-applying. | Backfills get interrupted; the second run must be safe. |
| B3 | **Batched by key range**, one short transaction per batch, with a configurable batch size and an optional pause between batches. | Short transactions release locks and let vacuum keep up (vendored `lock-short-transactions.md` in `backend-postgres`). |
| B4 | **Bind parameters** for every value; no string-built SQL. | Same injection rule as application code. |
| B5 | **Self-contained logic.** No import of today's models or services in a revision; a standalone backfill command may use the repository layer only if that layer is stable for the old and new schema. | Old revisions must keep working on a fresh install. |
| B6 | **Progress and counts logged, never row contents.** Log batch number, rows updated, last key. | Operators need to see progress; row contents can be personal data. |
| B7 | **Invariant query defined up front** (e.g. `SELECT count(*) FROM orders WHERE currency IS NULL` must be `0`) and run after the backfill. | It is the proof the contract step is safe, and the postcheck in the hand-off. |
| B8 | **Concurrent writers handled.** Code deployed in step 2 already writes the new column, so rows created during the backfill are correct; otherwise rerun until the invariant holds. | A one-pass backfill misses rows inserted while it ran. |

## Batched backfill (inside a revision, moderate size)

```python
from alembic import op
import sqlalchemy as sa

BATCH = 1000

def upgrade() -> None:
    conn = op.get_bind()
    with op.get_context().autocommit_block():          # each batch commits on its own
        last_id = 0
        while True:
            ids = conn.execute(
                sa.text(
                    "SELECT id FROM orders WHERE id > :last AND currency IS NULL "
                    "ORDER BY id LIMIT :batch"
                ),
                {"last": last_id, "batch": BATCH},
            ).scalars().all()
            if not ids:
                break
            conn.execute(
                sa.text(
                    "UPDATE orders o SET currency = t.currency FROM tenants t "
                    "WHERE o.tenant_id = t.id AND o.id = ANY(:ids) AND o.currency IS NULL"
                ),
                {"ids": ids},
            )
            last_id = ids[-1]

def downgrade() -> None:
    pass  # data step: the expand revision's downgrade removes the column; nothing to undo here
```

```python
# unsafe: one transaction over the whole table, no scope join, not resumable
op.execute("UPDATE orders SET currency = 'EUR'")
```

A data-only revision with an empty `downgrade()` must say so in a comment, as above; a downgrade that silently does nothing for a schema step is not allowed ([01](01-alembic-workflow.md) A6).

## Large backfill as a command

Same loop as above in a module under the backend's scripts/CLI location (`backend-clean-architecture`), plus:

- `--dry-run` that only counts rows to change;
- `--batch-size` and `--sleep-ms` options;
- exit code non-zero on error, with the last processed key printed so it can resume;
- a unit or integration test on the disposable DB with rows in several tenants, asserting other tenants' rows are unchanged.

Verification of both forms is in [04](04-verification.md).
