# 02 — Safe Schema Changes (`Expand → Backfill → Contract`) and Data Backfills (`B1`–`B8`)

> Topic: PostgreSQL 11+ lock matrix, zero-downtime `Expand → Backfill → Contract` rollout, `CREATE INDEX CONCURRENTLY`, safe `NOT NULL` and `NOT VALID` constraints, and batched/tenant-scoped data backfills (`B1`–`B8`).

---

## 1. Zero-Downtime `Expand → Backfill → Contract` Rollout

Because old and new API/worker instances run side by side during deployments, never combine `expand` and `contract` in a single revision:

```text
1. EXPAND    (Revision 1): Add new structure compatible with old & new code (nullable column, new table, concurrent index)
2. CODE      (Deploy 1):   Deploy API & workers that write both / read new with fallback
3. BACKFILL  (Revision 2 or CLI script): Backfill existing rows in batched, tenant-scoped transactions
4. CODE      (Deploy 2):   Deploy API & workers that stop reading/writing the old structure
5. CONTRACT  (Revision 3): Tighten constraints (NOT NULL, VALIDATE) and drop legacy column/table (after prior steps are VERIFIED_IN_TARGET)
```

---

## 2. PostgreSQL Lock Matrix & Safe DDL Patterns

Most `ALTER TABLE` statements acquire `ACCESS EXCLUSIVE`, blocking all reads and writes — and while waiting for that lock, every subsequent query on the table queues behind the `ALTER`:

| Statement | PostgreSQL Lock | Blocks | Safe Pattern |
|---|---|---|---|
| `ADD COLUMN` nullable or constant `server_default` (PG 11+) | `ACCESS EXCLUSIVE` | Everything (metadata-only, instant once acquired) | Precede with `SET LOCAL lock_timeout = '5s'` |
| `ADD COLUMN ... DEFAULT <volatile>` (`gen_random_uuid()`, `clock_timestamp()`) | `ACCESS EXCLUSIVE` | Everything (**full table rewrite**) | Add nullable → backfill in batches → set default for new rows |
| `ALTER COLUMN TYPE` (most changes) | `ACCESS EXCLUSIVE` | Everything (**table rewrite + index rebuild**) | Expand new column → dual-write & backfill → cutover → contract |
| `SET NOT NULL` | `ACCESS EXCLUSIVE` | Full table scan unless a valid `CHECK (col IS NOT NULL)` exists (PG 12+) | Add `CHECK (col IS NOT NULL) NOT VALID` → `VALIDATE CONSTRAINT` → `SET NOT NULL` → drop `CHECK` |
| `CREATE INDEX` | `SHARE` | All writes for full build | Use `CREATE INDEX CONCURRENTLY` inside `autocommit_block()` |
| `ADD CONSTRAINT ... NOT VALID` + `VALIDATE CONSTRAINT` | Brief `SHARE ROW EXCLUSIVE`, then `SHARE UPDATE EXCLUSIVE` | DDL only (reads & writes continue during `VALIDATE`) | Add `NOT VALID` first, then `VALIDATE CONSTRAINT` |

### Safe Pattern A — Concurrent Index in Its Own Revision
```python
def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_orders_customer_id")  # Clean up any prior INVALID build
        op.create_index("ix_orders_customer_id", "orders", ["customer_id"], postgresql_concurrently=True)

def downgrade() -> None:
    with op.get_context().autocommit_block():
        op.drop_index("ix_orders_customer_id", table_name="orders", postgresql_concurrently=True)
```

### Safe Pattern B — Computed `NOT NULL` Column Without Full-Table Exclusive Scan (PG 12+)
```python
# Revision 3 (Contract, after Expand + Backfill confirmed 0 NULL rows):
def upgrade() -> None:
    op.execute("SET LOCAL lock_timeout = '5s'")
    op.execute("ALTER TABLE orders ADD CONSTRAINT ck_orders_currency_not_null CHECK (currency IS NOT NULL) NOT VALID")
    op.execute("ALTER TABLE orders VALIDATE CONSTRAINT ck_orders_currency_not_null")
    op.alter_column("orders", "currency", nullable=False)  # Instant on PG 12+ when valid CHECK exists
    op.drop_constraint("ck_orders_currency_not_null", "orders", type_="check")
```

---

## 3. Data Migration & Backfill Rules (`B1`–`B8`)

| Size (Estimated Rows via `reltuples`) | Where to Execute Backfill | Why |
|---|---|---|
| **Small (`<= 10,000` rows, finishes in seconds)** | Inside a dedicated data revision (`alembic/versions/..._backfill_*.py`) using batched `autocommit_block()` | Ships in the revision chain without holding a multi-minute lock |
| **Large (`> 10,000` rows) or Hot Table** | Standalone idempotent CLI module (`uv run python -m app.scripts.backfill_<name> --dry-run` / `--batch-size 1000 --sleep-ms 50`) | Avoids long-running migration transactions, table bloat, and replication lag; supports pause/resume by DevOps |

### Mandatory Rules for Every Data Backfill (`B1`–`B8`)
1. **B1 (Scoped)**: Every `UPDATE` / `DELETE` filters by explicit tenant/organization/owner scope (`WHERE o.tenant_id = t.id ...`).
2. **B2 (Idempotent & Resumable)**: Select only rows still needing migration (`WHERE currency IS NULL`) so re-runs after interruption are safe.
3. **B3 (Batched by Key Range)**: Process in small key-ordered batches (`WHERE id > :last AND currency IS NULL ORDER BY id LIMIT :batch`), committing each batch independently.
4. **B4 (Parameterized SQL Only)**: Bind all values (`:last`, `:batch`, `= ANY(:ids)`); never use f-strings.
5. **B5 (Self-Contained)**: Never import live ORM models inside an Alembic revision.
6. **B6 (Log Counts, Never PII)**: Log batch number, updated row count, and last ID — never log customer row contents (`{{slot:secure-coding-standards}}`).
7. **B7 (Invariant Query Defined Up Front)**: Define the exact verification query (`SELECT count(*) FROM orders WHERE currency IS NULL` → expected `0`) and include it in `migration-handoff.md`.
8. **B8 (Concurrent Writers Handled)**: Deploy dual-write code before running the backfill so newly inserted rows already populate the new column.

```python
# Safe batched backfill inside a dedicated Alembic data revision:
BATCH = 1000

def upgrade() -> None:
    conn = op.get_bind()
    with op.get_context().autocommit_block():
        last_id = 0
        while True:
            ids = conn.execute(
                sa.text("SELECT id FROM orders WHERE id > :last AND currency IS NULL ORDER BY id LIMIT :batch"),
                {"last": last_id, "batch": BATCH},
            ).scalars().all()
            if not ids:
                break
            conn.execute(
                sa.text(
                    "UPDATE orders o SET currency = t.default_currency FROM tenants t "
                    "WHERE o.tenant_id = t.id AND o.id = ANY(:ids) AND o.currency IS NULL"
                ),
                {"ids": list(ids)},
            )
            last_id = ids[-1]

def downgrade() -> None:
    pass  # Data-only step: expand revision's downgrade drops the column
```
