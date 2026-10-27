# 03 — Root-Cause Fix, Escalation, Report & Review (Backend / FastAPI)

Rules **D6**, **D7**, **D8**, **D9**, **D10**, **D11**, **D12**, and **D14**.

---

## 1. Root-Cause Fix & Red-to-Green Regression Prevention (`D7`, `D8`, `D9`)

1. **Regression Test First (`D8`, `{{slot:unit-testing}}`):** Turn the minimized case into a test at the seam that owns the behavior:
   - Domain/application logic → unit test with `FakeRepository` (`tests/unit/`).
   - SQL query, constraint, or eager loading → integration test on PostgreSQL test DB (`tests/integration/`, `{{slot:verification}}`).
   - Routing, `Depends`, Pydantic validation, or exception handler mapping → in-process `httpx.AsyncClient(transport=ASGITransport(app=app))` test.
   Run it **red** first and verify it fails for the exact reported reason.
2. **Smallest Fix at the Owning Layer (`D7`, `{{slot:clean-architecture}}`):** Apply the minimal fix inside the task's **Scope / Files** (validation rule → Pydantic schema or domain entity; business rule → application service; SQL/loading → repository; schema drift → ORM model + new Alembic revision). Never edit an already-applied migration; create a new revision if approved by the task. Check the diff for sibling bugs (`D6`).
3. **Prove Red → Green → Undo-Red → Green:** Run the regression test (`PASS`), temporarily undo only the production fix in the working tree to confirm it fails (`FAIL`), restore the fix, and re-run (`PASS`). Record both runs as evidence rows.
4. **Full Verification & Cleanup (`D11`):** Re-run the original reproduction, the affected test suite, `uv run ruff check app tests`, `uv run mypy app tests`, and verify `rg -n "DEBUG-"` + `uv run ruff check --select T10,T20 app tests` return clean (`PASS`).

### Never Green-Wash (`D9` — Automatic `BLOCKER`)

| Forbidden Shortcut | Why It Is Forbidden |
|---|---|
| Editing, deleting, `@pytest.mark.skip` / `xfail`, or weakening a test assertion / **Expected** line | Hides the defect and removes the guard that caught it (wrong test spec → `change-control`) |
| `except Exception: pass`, `contextlib.suppress(Exception)`, or returning `None`/`[]` on failure | Turns a reproducible failure into silent corrupted data (`{{slot:clean-code}}` `C4`) |
| Hardcoded fallback or mock business data in production code | Fabricates success while the real path remains broken |
| `Any`, `# type: ignore`, `cast(...)`, `ConfigDict(extra="allow")`, or `status_code < 500` assertions | Disables static/contract safety and lets the bug through next time |
| `asyncio.sleep`, blind retry loops, or `pytest-rerunfailures` to mask races or slow queries | Leaves the race condition or N+1 bottleneck in production |
| `# noqa`, disabling `ruff`/`mypy` rules in `pyproject.toml`, or committing `print`/`breakpoint()` | Removes static protection for the entire repository |

---

## 2. Environment (`BLOCKED`) vs. Code & Escalation (`D10`, `D12`)

Never patch production code to work around a broken environment, and never stop, restart, or reconfigure a shared stack (PostgreSQL, Docker Compose, staging server) you did not start:

| Environment Sign | Diagnostic Check | Report Action |
|---|---|---|
| `ConnectionRefusedError`, `OSError: Connect call failed`, `CannotConnectNowError` | `pg_isready -h <host> -p <port>` or `lsof -i :5432` | `BLOCKED` — PostgreSQL unreachable |
| Startup `ValidationError` / `KeyError` on settings (`DATABASE_URL`, secret key) | Check variable names only (never print values) | `BLOCKED` — missing environment variable or credential |
| `UndefinedTableError` / `UndefinedColumnError` when ORM models and migrations agree | `uv run alembic current` vs. `uv run alembic heads` | `BLOCKED` — migrations not applied on target DB |
| `ModuleNotFoundError` / `ImportError` for declared dependency, lockfile drift | `uv sync --locked --dry-run` and `uv run python -V` | `BLOCKED` — stale/drifted virtualenv |
| Port already in use | `lsof -i :<port>` | `BLOCKED` — another process owns the port |
| Suspected stale cache (`.pytest_cache`, `.mypy_cache`) | Re-run with `-p no:cacheprovider` and `uv run mypy --no-incremental` | If still failing, treat as code defect; otherwise note cache cleanup |

- **3-Attempt Time-Box (`D12`):** After **3 failed fix attempts** (where the reproduction still fails), **stop immediately**. Return `BLOCKED` with the Debug Report block below showing `Root cause: unknown`, the 3 ruled-out hypotheses, and missing evidence.
- **Back to the Gate (`change-control`):** Stop and escalate if the fix requires:
  - Editing files outside the task's **Scope / Files** or correcting a broken plan check (`TASK_DETAIL`)
  - Changing an endpoint path, status code, request/response schema, DB schema, `pyproject.toml` dependency, or layer boundary (`DESIGN_CHANGE`)
  - Changing user-visible behavior or approved Acceptance Criteria (`SCOPE_CHANGE`)

---

## 3. Hand-Off Debug Report Format (`D14`)

Include this block in the Code Writer / Bug Fixer hand-off (or `FIXED` finding response) with redacted outputs (`<REDACTED>`):

```text
Symptom:      <what failed and where; reported by task check / reviewer / bug-hunt / tester / user>
Triage:       CODE_WRONG (task <id>, Expected: <...>)
Reproduction: uv run pytest <id> -q (cwd: <service root>) @ <revision> -> exit 1 (<key output>)
Root cause:   <exact defect at app/<file>.py:<line> and why it occurred>
Fix:          <what changed at which owning layer and why>
Regression:   <tests/...::test_name> -> FAIL (exit 1) with fix undone, PASS (exit 0) with fix
Evidence:     <rows per evidence-standard: regression red/green, original repro, suite, ruff, mypy>
Ruled out:    H2 (<why>), H3 (<why>)
Debug tags:   rg -n "DEBUG-" app tests -> 0 matches; uv run ruff check --select T10,T20 app tests -> PASS
```

---

## 4. Review Severity (`BLOCKER` / `MAJOR` / `MINOR`)

Code Reviewers grade debugging fixes on the unified 3-tier scale (`shared_contracts/flags_and_statuses.md` §2):

| Severity | Finding | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | Any green-washing (`D9`); missing Red-to-Green regression test (`D8`) where a seam exists; leftover `[DEBUG-xxxx]`, `print()`, or `breakpoint()` (`D11`); edited applied Alembic migration; unapproved contract/schema/dependency change (`D12`); any check `FAIL`s | `CHANGES_REQUESTED` (blocks approval) |
| `MAJOR` | Symptom patched in router/caller instead of the owning root-cause layer (`D6`, `D7`); sibling bug in the same diff left unfixed (`D6`); missing or incomplete Debug Report block (`D14`) | Must be fixed in the same phase scope |
| `MINOR` | Minor regression test naming or report formatting improvement | Optional (never blocks approval) |
