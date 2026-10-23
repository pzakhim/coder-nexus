# 05 — Tools and commands

Rule D13 of [root-cause-debugging](../SKILL.md). Why this file exists: real commands and tracing tools turn the loop into actions. The commands assume a `uv`-managed project with `pyproject.toml`; when the workspace defines its own scripts (Makefile, `scripts/`, task commands in the plan), those win. Check commands for the task come from its Acceptance Criteria and `{{slot:verification}}`.

Run from: the service root (the directory holding `pyproject.toml`).

## pytest

| Need | Command |
|---|---|
| Reproduce one failure | `uv run pytest tests/unit/test_x.py::test_y -q` |
| Select by name | `uv run pytest -k "cancel and not paid" -q` |
| Stop at the first failure | `uv run pytest -x -q` |
| Rerun failed only | `uv run pytest --lf -q` (then `--ff` to run failures first in the full suite) |
| Verbose, stdout, full trace, locals | `uv run pytest <id> -vv -s --tb=long --showlocals` |
| Live logs | `uv run pytest <id> --log-cli-level=DEBUG` |
| Fail on un-awaited coroutines | `uv run pytest <id> -W error::RuntimeWarning` |
| Fixed order | `-p no:randomly` (only if `pytest-randomly` is installed) |
| Repeat to expose flakiness | `--count=50` (only if `pytest-repeat` is installed) |
| Run without the cache | `-p no:cacheprovider` |

`--pdb`, `--trace` and `breakpoint()` open an interactive prompt: an agent's `run_command` would hang waiting for input. Use them only in a human terminal session while debugging, and never commit a `breakpoint()` or `import pdb` (ruff T100). Agents use `--showlocals`, `-vv -s`, `caplog` and temporary tagged logging instead.

## Static checks on one file

| Need | Command |
|---|---|
| Lint | `uv run ruff check app/path/module.py` |
| Leftover debug code | `uv run ruff check --select T10,T20 <touched files>` |
| Types | `uv run mypy app/path/module.py` (`--no-incremental` if the cache is suspect) |

Read the rule code (`F821`, `B008`, mypy `[arg-type]`, …) and fix the cause, not the report.

## Database

| Need | How |
|---|---|
| See the SQL a test emits | `logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)` in the test, or `--log-cli-level=INFO`; `create_async_engine(url, echo=True)` only temporarily, never committed |
| Count statements (N+1) | Count `sqlalchemy.engine` log records via `caplog` around the call |
| Query plan | `EXPLAIN (ANALYZE, BUFFERS) <query>;` in `psql` against the **local/test** database. `ANALYZE` executes the query: wrap writes in `BEGIN; … ROLLBACK;`, never run it on a shared database |
| Migration state | `uv run alembic current`, `uv run alembic heads`, `uv run alembic history -v` |
| Model vs migration drift | `uv run alembic check` (Alembic ≥ 1.9) |

## HTTP

- In-process: `httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")` inside an async test; assert status **and** body. Why: no server, no port, deterministic.
- Against a local server you started: `curl -sS -i http://127.0.0.1:8000/<path>` or an `httpx` script; stop that server when done.

## Logs

- Local server you start yourself: `uv run uvicorn app.main:app --log-level debug` (module path is the conventional one; use the workspace's). Tracebacks of a `500` appear in this console, not in the response.
- In tests: `caplog` or `--log-cli-level=DEBUG`.
- Shared or deployed logs: read only through the access the workspace documents; never restart or reconfigure the service to get them.

## Bisect a regression

```bash
git worktree add ../bisect-wt <bad-sha>
cd ../bisect-wt
git bisect start <bad-sha> <good-sha>
git bisect run uv run pytest tests/unit/test_x.py::test_y -q
git bisect reset
cd - && git worktree remove ../bisect-wt
```

Only in a separate disposable worktree, never in the shared working tree with uncommitted work or someone else's checkout. The command must exit non-zero exactly on the failure (an unrelated import error marks commits bad); use exit code 125 in a wrapper script to skip unbuildable commits.

## Tracing

- If the workspace configures a code-intelligence tool (for example GitNexus: `query` for the error text, `context` for callers/callees, `impact` before editing a symbol, `detect_changes` before committing), its mandatory rules apply and come first.
- Fallback: `rg -n "<symbol>" app/ tests/` for callers, `rg -n "Depends\(<dep>\)" app/` for FastAPI dependency users, `git log -S "<symbol>" --oneline` for when it changed.
