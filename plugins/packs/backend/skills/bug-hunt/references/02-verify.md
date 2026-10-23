# 02 — Verify (try to disprove)

A candidate that survives an honest attempt to refute it is worth the reader's time; everything else is noise. Verify every candidate from 01 before it becomes a finding.

## Steps per candidate

1. **Trace the real path** from an entry point to the line: a FastAPI route, a dependency, a background task, a CLI / worker job, an Alembic migration run, a startup (`lifespan`) hook. On the way, read the guards, `Depends(...)` chain, Pydantic validation, defaults, exception handlers, middleware and framework behavior. Do not assume what a library does; check its documented behavior or the installed source (`uv run python -c "import inspect, <mod>; print(inspect.getsource(<obj>))"`). Reason: most false positives die on a guard or a framework rule the first read missed.
2. **Write the failure scenario** with concrete values:
   ```
   given <input/state> → when <action> → then <observed wrong result>
   ```
   Example: given order 42 owned by user A → when user B calls `GET /orders/42` with a valid token → then 200 with A's order, because `get_order` filters only by `Order.id`.
   Reason: a scenario is reproducible and turns directly into the regression test.
3. **Run a read-only command when it decides the question**, and quote its exit code and key output:
   - existing focused tests: `uv run pytest tests/unit/<file>.py -q` or `uv run pytest -q -k "<name>"`;
   - type checks: `uv run mypy <path>` (an un-awaited coroutine shows as `[unused-coroutine]`);
   - lint: `uv run ruff check <path>` (for example `ASYNC`, `B006`, `BLE001`, `DTZ`, `RUF006`, `S608` rule codes);
   - migrations: `uv run alembic heads`, `uv run alembic history -r <base>:<head>`, `uv run alembic upgrade <base>:<head> --sql` (renders SQL offline, touches no database), `uv run alembic check` where the workspace configures it;
   - history: `git show <REVIEW_REVISION>:<path>`, `git log -L <start>,<end>:<path>`.
   Use only the workspace's real commands; a command you did not run is not evidence (`evidence-standard`). Never modify application code, tests or migrations during the hunt, and never run a migration against a shared database. Writing a throw-away test is a fix step (Code Writer, after the hunt), not a verification step.
4. **Classify** (definitions in [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md)):
   - `CONFIRMED` — the path is traced end to end and nothing on it prevents the failure, or a command demonstrated it.
   - `PLAUSIBLE` — the failure depends on something you could not see: production data shape, PostgreSQL isolation level or lock behavior under load, a provider's real response, a dependency version's internals, deployment settings. Name exactly what would confirm it (a query, a log line, a version, a test against a real database).
   - Rejected — a guard, caller contract, database constraint or framework behavior prevents it. Drop it silently.

## What does not survive

- No failure scenario → no finding. "Might be fragile", "consider handling errors", "add logging" and style remarks are not findings.
- A scenario that needs an impossible input (rejected earlier by Pydantic validation, a `CHECK` / `UNIQUE` / `NOT NULL` constraint, or an auth dependency on every route that reaches the line) is rejected.
- A scenario that only shows a slower path with the right result is a `NOTE` (01 → "Not candidates").

## Typical disproofs in this stack

| Suspicion | Often disproved by |
|---|---|
| "`None` reaches the query" | The Pydantic field is required and non-optional; FastAPI returns 422 before the handler |
| "Duplicate rows on retry" | A `UNIQUE` constraint plus `ON CONFLICT` / `IntegrityError` handling on the write |
| "Lazy load in async code" | The query uses `selectinload` / `joinedload`, or the relationship is `lazy="raise"` / `"selectin"` |
| "Attribute expired after commit" | The `async_sessionmaker` sets `expire_on_commit=False` |
| "Unauthorized object access" | A dependency loads the object filtered by the current user and the handler only uses that object |

Check the actual code for each disproof; a disproof you assumed is as weak as a finding you assumed.
