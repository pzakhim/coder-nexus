# 02 — Isolate and hypothesize

Rules D4-D6 of [root-cause-debugging](../SKILL.md). Why this file exists: a small search space and one falsifiable hypothesis at a time find the cause fastest.

## Minimise

Cut input fields, fixtures, callers, config and steps one at a time, rerunning the reproduction after each cut. Done when every remaining element is load-bearing. Why: the minimised case becomes the regression test.

## Isolate

- What changed since the last green run: `git diff <last-green-sha> -- app/ tests/ alembic/`, `git log -p -- <path>`.
- Dependency drift: compare `uv.lock` between green and red (`git diff <last-green-sha> -- uv.lock`). A changed SQLAlchemy, Pydantic or FastAPI version is a hypothesis, and upgrading/pinning is a dependency change for `change-control`.
- Regressions with unknown cause: `git bisect run` **only in a separate disposable worktree**, never in the shared working tree with uncommitted work ([05](05-tools-and-commands.md)). Why: bisect checks out other commits.
- Callers and call paths: the workspace's code-intelligence tool if configured, else `rg -n "<symbol>" app/ tests/` ([05](05-tools-and-commands.md) "Tracing").
- Multi-component path (router → dependency → use case/service → repository → database): log what enters and leaves each boundary once (tagged, see below), find the boundary where good data turns bad, then investigate only that component.

## Hypothesize

Write **3-5 ranked hypotheses** before testing any. Each must be falsifiable: "if X is the cause, changing Y makes the failure disappear". A hypothesis without a prediction is discarded. Test the top one with the smallest probe, **one variable at a time**. Why: several changes at once make every result ambiguous.

```
H1 (rank 1): <suspected cause> | predicts: <changing Y removes the failure> | probe: <command or read> | result: CONFIRMED / RULED OUT
H2 (rank 2): ...
Fix attempts: 1/3 <what changed> -> reproduction <PASS/FAIL>
```

When one is confirmed, ask "why" again and trace the bad value backwards caller by caller until you reach where it originates; then look for the same mistake elsewhere in the diff. Ruled-out hypotheses go into the report ([06](06-report.md)); they save the reviewer the same detour.

## Temporary instrumentation

- Prefer non-invasive probes first: `-vv -s --showlocals --tb=long`, `caplog`, `--log-cli-level=DEBUG`, SQL echo via logging ([05](05-tools-and-commands.md)).
- When you must add output, use `logging.getLogger(__name__).debug(...)` or `print` with a unique tag, e.g. `[DEBUG-7f3a]`, and log no secrets, tokens or personal data.
- Before hand-off `rg -n "DEBUG-7f3a"` returns nothing, and `uv run ruff check --select T10,T20 <touched files>` is clean (T100 `breakpoint()`/`pdb`, T201 `print`). Why: untagged prints survive into review and leak data.

## Symptom → first moves

| Symptom | First moves | Typical cause in a FastAPI / SQLAlchemy async service |
|---|---|---|
| Exception / traceback | First frame under `app/`; the value that is wrong there; trace it back | Missing `None`/empty handling, wrong assumption about a caller, changed contract or schema |
| Wrong value, no error | Assert the expected value at the boundary nearest the output (response model, repository return); walk back one layer | Wrong condition/operator, timezone-naive vs aware `datetime`, `Decimal`/float rounding, Pydantic model dropping a field (`exclude_unset`, alias mismatch), stale identity-map object after an update without `refresh` |
| `422 Unprocessable Entity` | Read `detail[].loc/msg/type`; compare request body with the Pydantic model | Field name/alias mismatch, strict type in Pydantic v2 (no implicit coercion where v1 had it), wrong body/query/path declaration |
| `500` with `MissingGreenlet` | Find the attribute access in the frame | Lazy-loaded relationship touched outside `await` (missing `selectinload`/`joinedload`), or access after the session closed |
| `RuntimeWarning: coroutine … was never awaited`, result is a coroutine | Rerun with `-W error::RuntimeWarning` to fail at the line | Missing `await` |
| `IntegrityError`, `UniqueViolationError`, `ForeignKeyViolationError` | Read the constraint name; check the data and the order of writes | Missing existence check, wrong flush order, test data colliding across tests |
| `UndefinedTableError` / `UndefinedColumnError` | `uv run alembic current` vs `uv run alembic heads` | Migration not applied (environment → `BLOCKED`) or model and migration out of sync (code) |
| Multiple Alembic heads, failing `upgrade`/`downgrade` | `uv run alembic heads`, `uv run alembic history -v` | Two branches merged without a merge revision; non-reversible `downgrade`; data migration assuming rows exist |
| Regression ("it worked before") | Diff since last green, `uv.lock` diff, differential run, bisect in a worktree | A change elsewhere in the diff, a caller now passing other data, a dependency upgrade |
| Flaky / intermittent | Rerun N times; run alone vs after others (`-p no:randomly`); look at fixture scope | Shared session/engine across tests, missing transaction rollback per test, `event loop is closed` from mismatched pytest-asyncio loop scope, real time/random, network |
| Async ordering / race | Tagged temporary logs with timestamps at each boundary; check every `await` | Concurrent requests updating the same row without a lock or version check, work after commit, `asyncio.gather` sharing one `AsyncSession` |
| Works locally, fails in CI | Diff Python version, env vars, timezone/locale, database version, parallelism | Environment drift (often `BLOCKED`, not code) |
| ruff / mypy error | Read the first error and its rule code; fix the type at the source | Contract change, wrong import, `Optional` not narrowed |
| Slow request / timeout | Measure first (timing around the suspect, SQL echo to count statements, `EXPLAIN ANALYZE`), then change one thing | N+1 queries from lazy loads in a loop, missing index, unbounded query without pagination, blocking sync call (`requests`, `time.sleep`, sync driver) inside an `async def` |
| Only with real data | Capture the failing input (redacted); add it as a test case | Unexpected shape, encoding, very large values, `NULL` in a column assumed non-null |
