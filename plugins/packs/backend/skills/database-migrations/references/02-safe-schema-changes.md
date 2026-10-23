# 02 — Designing safe schema changes

PostgreSQL 11+ behaviour. Check the workspace's major version ([postgres](../../postgres/SKILL.md) §1) before relying on a version-specific shortcut.

## Expand → backfill → contract

The plan decides which phase holds which step ([implementation-planning](../../implementation-planning/SKILL.md), exception "expand → migrate → contract"). This is what each step means for the database:

```
1. expand    revision: add new structure, compatible with old AND new code   (nullable column, new table, index)
2. code      deploy code that writes both / reads new with fallback          (API and every worker)
3. backfill  move existing rows, batched and scoped                           (03-data-backfills.md)
4. code      deploy code that stops using the old structure
5. contract  revision: tighten (NOT NULL, VALIDATE) and drop the old structure — later phase or later vN (D-NN)
```

Each step is its own revision and its own check. The hand-off states which step this revision is and what must be deployed before the next one.

## Lock awareness

Most `ALTER TABLE` forms take `ACCESS EXCLUSIVE`: they block reads and writes for their duration, and while they **wait** for a lock every later query on the table queues behind them. So a "fast" ALTER behind one long transaction is an outage.

| Statement | Lock | Blocks | Duration |
|---|---|---|---|
| `ADD COLUMN` nullable, or with a constant default (PG11+) | ACCESS EXCLUSIVE | everything | metadata only, instant once acquired |
| `ADD COLUMN … DEFAULT <volatile>` (e.g. `gen_random_uuid()`, `clock_timestamp()`) | ACCESS EXCLUSIVE | everything | **table rewrite** |
| `ALTER COLUMN TYPE` (most changes) | ACCESS EXCLUSIVE | everything | **rewrite + index rebuild** |
| `SET NOT NULL` | ACCESS EXCLUSIVE | everything | full scan, unless a valid `CHECK (col IS NOT NULL)` exists (PG12+) |
| `CREATE INDEX` | SHARE | writes | full build |
| `CREATE INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | other DDL, vacuum only | longer, two scans; **not in a transaction** |
| `ADD CONSTRAINT … NOT VALID` (FK / CHECK) | short ACCESS EXCLUSIVE / SHARE ROW EXCLUSIVE | briefly | no scan |
| `VALIDATE CONSTRAINT` | SHARE UPDATE EXCLUSIVE | other DDL only | scan, reads and writes continue |

Always: `SET LOCAL lock_timeout` at the top of the revision (rule A7 in [01](01-alembic-workflow.md)); estimate the row count (`SELECT reltuples::bigint FROM pg_class WHERE relname = 'orders'` on a representative DB) and write it in the hand-off.

## Patterns (Alembic)

### Add an index to a populated table

```python
# unsafe: SHARE lock blocks all writes for the whole build
op.create_index("ix_orders_customer_id", "orders", ["customer_id"])
```

```python
# safe: concurrent, outside the migration transaction, rerunnable
def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_orders_customer_id")  # removes an INVALID leftover
        op.create_index("ix_orders_customer_id", "orders", ["customer_id"], postgresql_concurrently=True)

def downgrade() -> None:
    with op.get_context().autocommit_block():
        op.drop_index("ix_orders_customer_id", table_name="orders", postgresql_concurrently=True)
```

- `autocommit_block()` commits what ran before it; put a concurrent index in its own revision. Reason: a failure after the commit leaves the earlier statements applied but the revision unrecorded.
- A failed concurrent build leaves an `INVALID` index; `IF NOT EXISTS` would then skip it silently. Drop and rebuild instead (as above), and check validity in verification ([04](04-verification.md)).
- Unique index the same way (`unique=True`); to turn it into a constraint: `ALTER TABLE orders ADD CONSTRAINT uq_orders_number UNIQUE USING INDEX ix_orders_number`.

### Add a NOT NULL column

```python
# unsafe on a populated table: fails (existing rows are NULL) or rewrites with a volatile default
op.add_column("orders", sa.Column("currency", sa.Text(), nullable=False))
```

```python
# safe A — constant default exists for all rows (PG11+: no rewrite)
op.add_column("orders", sa.Column("currency", sa.Text(), nullable=False, server_default="EUR"))
```

```python
# safe B — value must be computed per row: expand / backfill / contract
# rev 1 (expand)
op.add_column("orders", sa.Column("currency", sa.Text(), nullable=True))
# rev 2 (backfill, see 03)
# rev 3 (contract) — avoid the long SET NOT NULL scan
op.execute("SET LOCAL lock_timeout = '5s'")
op.execute("ALTER TABLE orders ADD CONSTRAINT ck_orders_currency_not_null CHECK (currency IS NOT NULL) NOT VALID")
op.execute("ALTER TABLE orders VALIDATE CONSTRAINT ck_orders_currency_not_null")
op.alter_column("orders", "currency", nullable=False)          # PG12+: uses the valid CHECK, no scan
op.drop_constraint("ck_orders_currency_not_null", "orders", type_="check")
```

### Add a foreign key or CHECK constraint to existing data

```python
# first: count violations on a representative DB and fix them (backfill or data decision with the user)
op.execute("SET LOCAL lock_timeout = '5s'")
op.execute(
    "ALTER TABLE orders ADD CONSTRAINT fk_orders_customer_id_customers "
    "FOREIGN KEY (customer_id) REFERENCES customers (id) NOT VALID"
)
op.execute("ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_customer_id_customers")
```

`NOT VALID` enforces the constraint for new writes immediately; `VALIDATE` checks old rows without blocking writes. On a large table put `VALIDATE` in a separate revision so the short-lock step and the long scan are applied separately. Index the FK column too (`backend-postgres`).

### Other changes

| Change | Safe pattern | Avoid |
|---|---|---|
| Rename a column used by running code | Add new column → write both → backfill → read new → stop writing old → drop old (contract) | `alter_column(new_column_name=...)` while any deployed version reads the old name |
| Change a column type | New column with the new type → backfill with explicit cast → switch → drop old | In-place `ALTER COLUMN TYPE` on a large table (rewrite under ACCESS EXCLUSIVE). Exceptions without rewrite: `varchar(n)` → `text`, widening `varchar` |
| Drop a column or table | Code stops reading and writing it and is deployed → drop in a later revision; remove it from the model first so autogenerate stays clean | Dropping in the same release that stops using it |
| Add an enum value | `op.execute("ALTER TYPE order_status ADD VALUE IF NOT EXISTS 'refunded'")` in an `autocommit_block()` on PG < 12 | Removing or renaming a value still stored or still written by any deployed version |
| New table | Create with PK, named constraints, FK indexes and scope column (`tenant_id`) from the start | Adding scope columns later to a populated table |
| Server default change | Explicit `op.alter_column(..., server_default=...)`; autogenerate does not see it unless `compare_server_default` is on | Assuming the model's `default=` (Python-side) changes the database |

## Sensitive data

A revision that copies, transforms or exposes personal data (new column holding PII, moving data between tables, removing masking) is flagged in the hand-off per `{{slot:secure-coding-standards}}` SC11. Never log row contents in a data step.
