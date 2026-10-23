# 03 — Query plans and N+1 detection

A slow query is a defect like any other: the method is `root-cause-debugging` (reproduce, read the real evidence, one hypothesis at a time, regression check). This file adds the PostgreSQL tools.

## EXPLAIN ANALYZE workflow

1. **Reproduce on dev/test only**, with realistic volume. A plan on 20 rows says nothing about 2 million: seed or generate data at the expected scale first (fixture or a seed script in the workspace, never copied production data).
2. **Capture the exact SQL and parameters** the code emits:
   ```python
   test_engine = create_async_engine(url, echo=True)   # or logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
   print(stmt.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))  # for reading only
   ```
3. **Run the plan** in `psql` against the dev DB (or `explain_query` from postgres-mcp, [04](04-postgres-mcp.md)):
   ```sql
   EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) <the statement with real parameter values>;
   ```
   `ANALYZE` executes the statement. For `INSERT`/`UPDATE`/`DELETE` wrap it: `BEGIN; EXPLAIN ANALYZE …; ROLLBACK;` — and only on a disposable/dev database.
4. **Read it**, from the most expensive node outwards:

   | Sign in the plan | Usually means | Next step |
   |---|---|---|
   | `Seq Scan` on a large table with a selective `Filter` and many `Rows Removed by Filter` | Missing or unusable index | Index the filter columns ([02](02-schema-keys-and-indexes.md)); check the expression matches (e.g. `lower(email)`) |
   | Estimated `rows` far from actual `rows` | Stale or missing statistics | `ANALYZE <table>;` on dev, re-plan (vendored `monitor-vacuum-analyze.md`) |
   | `Sort` with `external merge Disk` | Sort exceeds `work_mem` | Index that delivers the order, or a smaller result set |
   | `Nested Loop` with a large outer side and an inner `Seq Scan` | Join column not indexed | Index the FK / join column |
   | High `Buffers: shared read` | Cold cache or too many pages touched | Narrower index, covering index, less data |
   | `Index Scan` but still slow on `OFFSET` pages | Deep offset pagination | Keyset pagination (vendored `data-pagination.md`) |

5. **Change one thing**, re-plan, and compare actual time and buffers. Hypothetical indexes (`explain_query` with hypothetical indexes, needs the `hypopg` extension) let you compare before writing a migration.
6. **Ship and record**: the index goes into an Alembic revision; the evidence rows show the plan's key line before and after (`Seq Scan … 840 ms` → `Index Scan using ix_orders_… 3 ms`) on the named database and revision. A plan excerpt is evidence for the performance claim only; tests remain the decisive check for behaviour.

Whole-workload view on dev/staging-like data: `pg_stat_statements` (vendored `monitor-pg-stat-statements.md`) or postgres-mcp `get_top_queries`, then `analyze_query_indexes` on the top statements.

## N+1 detection

N+1 = one query for the list, then one more per row (a lazy relationship, or a repository call inside a loop). In async SQLAlchemy a lazy load usually raises `MissingGreenlet`; with `awaitable_attrs` or per-row repository calls it silently multiplies round trips.

Guard it with a statement-count test on list endpoints and list services:

```python
# tests/support/query_counter.py
@contextmanager
def count_queries(engine: AsyncEngine) -> Iterator[list[str]]:
    statements: list[str] = []

    def before(conn, cursor, statement, parameters, context, executemany):
        statements.append(statement)

    event.listen(engine.sync_engine, "before_cursor_execute", before)
    try:
        yield statements
    finally:
        event.remove(engine.sync_engine, "before_cursor_execute", before)
```

```python
async def test_list_orders_query_count_does_not_grow_with_rows(client, engine, make_orders):
    await make_orders(count=2)
    with count_queries(engine) as few:
        await client.get("/orders")
    await make_orders(count=20)
    with count_queries(engine) as many:
        await client.get("/orders")
    assert len(many) == len(few)   # fails if a query runs per row
```

Fix by loading what the response needs in the query (`selectinload`/`joinedload`, or one batched `WHERE id = ANY(:ids)` query), never by caching inside a loop. Vendored detail: `data-n-plus-one.md`.

## Things that look like a fix but are not

- Raising `statement_timeout` to make a slow query pass. It hides the plan problem and holds connections longer.
- Adding an index without checking the plan uses it (wrong column order, function on the column, low selectivity).
- "It is fast on my machine": a plan on a near-empty table is not evidence; state the row counts used.
