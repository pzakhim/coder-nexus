# Safe patterns for common changes

Default shapes (PostgreSQL wording; adapt to the engine). The generated `02` keeps the ones the workspace needs, with its runner's syntax.

| Change | Safe pattern | Avoid |
|---|---|---|
| **Add a NOT NULL column** | Add nullable (or with a constant default where the engine adds it without rewrite) → backfill in batches → set `NOT NULL` after verifying no nulls | Adding `NOT NULL` without a default on a populated table |
| **Rename a column/table** | Add new → write to both (or a view) → backfill → switch reads → stop writing old → drop old in a later release | `RENAME` while old code still reads the old name |
| **Change a column type** | New column with the new type → backfill with explicit conversion → switch → drop old | In-place type change that rewrites a large table under lock |
| **Add an index** | `CREATE INDEX CONCURRENTLY` (outside a transaction); check it is valid afterwards | Plain `CREATE INDEX` on a busy table |
| **Add a unique/FK/check constraint** | Query for violations → fix data → add `NOT VALID` → `VALIDATE CONSTRAINT` | Adding a validated constraint blindly |
| **Drop a column/table** | Stop all reads/writes in code first (deployed) → drop in a later migration | Dropping while any running version still uses it |
| **Large backfill** | Batches by key range, scoped by tenant/environment, resumable, with progress logging; outside peak hours if needed | One huge `UPDATE` |
| **Enum / allowed values** | Add new value first; migrate rows; remove old value only after code no longer writes it | Removing a value still in use |
| **New table** | Create with constraints and indexes; include scope columns (tenant/environment) from the start | Adding scope columns later to a populated table |

## Rollout order (expand / contract)

```
1. Migration: expand (compatible with old and new code)
2. Deploy code that writes/reads the new structure (workers included)
3. Backfill
4. Deploy code that stops using the old structure
5. Migration: contract (drop old)
```
