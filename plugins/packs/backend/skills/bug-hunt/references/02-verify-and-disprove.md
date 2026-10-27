# 02 — Verify and Disprove Candidates

> Topic: Adversarial disproof workflow, concrete failure scenarios, read-only CLI checks, and confidence grading (`H6`–`H8`)

A candidate that survives an honest attempt to refute it is worth the reader's time; everything else is noise. Verify every candidate from [01-scope-dimensions-and-patterns.md](01-scope-dimensions-and-patterns.md) before it becomes a finding.

## 1. Adversarial Disproof Steps per Candidate (`H6`–`H8`)

1. **Trace the Real Path (`H6`):** Walk from an entry point to the suspect line: a FastAPI route, a dependency, a background task, a CLI / worker job, an Alembic migration run, or a startup (`lifespan`) hook. On the way, read the guards, `Depends(...)` chain, Pydantic validation, defaults, exception handlers, middleware, and framework behavior. Do not assume what a library does; check its documented behavior or installed source (`uv run python -c "import inspect, <mod>; print(inspect.getsource(<obj>))"`).
2. **Write the Failure Scenario (`H7`):** State concrete values:
   ```text
   given <input/state> → when <action> → then <observed wrong result>
   ```
   Example: `given order 42 owned by user A → when user B calls GET /orders/42 with a valid token → then 200 with A's order, because get_order filters only by Order.id`.
3. **Run Read-Only CLI Checks (`H6`):** When a read-only command decides the question, run it and quote its exit code (`PASS` / `FAIL`) and key output:
   - Focused tests: `uv run pytest tests/unit/<file>.py -q` or `uv run pytest -q -k "<name>"`
   - Type checks: `uv run mypy <path>` (an un-awaited coroutine shows as `[unused-coroutine]`)
   - Lint: `uv run ruff check <path>` (`ASYNC`, `B006`, `BLE001`, `DTZ`, `RUF006`, `S608`)
   - Migrations: `uv run alembic heads`, `uv run alembic history -r <base>:<head>`, `uv run alembic upgrade <base>:<head> --sql` (renders SQL offline, touches no database), `uv run alembic check`
   - Git history: `git show <REVIEW_REVISION>:<path>`, `git log -L <start>,<end>:<path>`
   Never modify application code, tests, or migrations during the hunt, and never run a migration against a shared database.
4. **Classify Confidence (`H8`):**
   - `CONFIRMED` — the path is traced end-to-end and nothing on it prevents the failure, or a read-only command demonstrated it.
   - `PLAUSIBLE` — the failure depends on something not visible in the repository: production data shape, PostgreSQL isolation level or lock behavior under load, a provider's real response, or deployment settings. Name exactly what would confirm it.
   - **Rejected** — a guard, caller contract, database constraint, or framework behavior prevents it. Drop silently.

---

## 2. What Does Not Survive

- **No failure scenario → no finding.** "Might be fragile", "consider handling errors", "add logging", and style remarks are not findings.
- **Impossible input:** A scenario rejected earlier by Pydantic validation, a `CHECK` / `UNIQUE` / `NOT NULL` constraint, or an auth dependency on every route reaching the line is rejected.
- **Pure cleanup:** A scenario that only shows a slower or less tidy path with the right result is a `NOTE` (`H14`).

---

## 3. Typical Disproofs in Backend (Python / FastAPI / SQLAlchemy)

| Suspicion | Often Disproved By |
|---|---|
| "`None` reaches the query" | The Pydantic field is required and non-optional; FastAPI returns 422 before the handler runs |
| "Duplicate rows on retry" | A `UNIQUE` constraint plus `ON CONFLICT` / `IntegrityError` handling on the write |
| "Lazy load in async code" | The query uses `selectinload` / `joinedload`, or the relationship sets `lazy="raise"` / `"selectin"` |
| "Attribute expired after commit" | `async_sessionmaker` sets `expire_on_commit=False` |
| "Unauthorized object access" | A dependency loads the object filtered by the current user and the handler only uses that object |

Check the actual code for each disproof; an assumed disproof is as weak as an assumed finding.
