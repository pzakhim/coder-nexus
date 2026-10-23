# Gate commands and results

Detail for [backend verification](../SKILL.md) §2–§3. Commands show the `uv run` prefix; use the prefix detected in [workspace detection](workspace-detection.md). cwd is the service root.

## G1 Format — `ruff format --check .`

| Exit | Output | Result |
|---|---|---|
| 0 | `N files already formatted` | PASS |
| 1 | `Would reformat: app/services/orders.py` | FAIL |
| 2 | invalid config / CLI / internal error | BLOCKED (quote the error) |

Run on the whole service, not only changed files, unless the workspace's own target scopes it. Reason: the gate is what CI will run. The formatter does not sort imports; that is ruff's `I` rules in G2.

## G2 Lint — `ruff check .`

| Exit | Output | Result |
|---|---|---|
| 0 | `All checks passed!` | PASS |
| 1 | `Found N errors.` with rule codes | FAIL |
| 2 | config or internal error | BLOCKED |

- Never add `--fix` in a verification run. Reason: verification must not change the tree it verifies; fixes are the Code Writer's, on a new revision.
- New `# noqa` or `per-file-ignores` in the diff are reviewed as findings (`backend-code-review`), not accepted as a pass.

## G3 Types — `mypy <package>`

| Exit | Output | Result |
|---|---|---|
| 0 | `Success: no issues found in N source files` | PASS |
| 1 | `Found N errors in M files` | FAIL |
| 2 | crash, bad config, missing module with no stubs config | BLOCKED |

- Target: the `files` / `packages` in `[tool.mypy]` when set, else the app package named in `pyproject.toml`. Whether `tests/` is type-checked follows the workspace config.
- Read the file count: a run that checked 3 files in a 200-file package has the wrong target.
- The plugins the workspace enables (`pydantic.mypy`) stay as configured; strictness is never lowered for a run.

## G4 Unit tests — `pytest tests/unit -q`

| Exit | Output | Result |
|---|---|---|
| 0 | `N passed` (read `skipped`, `xfailed`, `deselected`) | PASS when the phase's tests are among the passed |
| 1 | `N failed` | FAIL |
| 2 / 3 / 4 | interrupted, internal error, usage error (often a collection `ImportError`) | an import error in changed code is FAIL; a broken tool or config is BLOCKED |
| 5 | `no tests ran` | NOT_RUN |

Confirm with `-v` or `--collect-only -q` that the phase's test ids are collected when the count looks wrong. A skipped test that guards a phase AC makes that AC `NOT_RUN`.

## G5 Migrations — disposable database

```bash
# 1. a database created for this run (name from the agreed rule, e.g. <app>_verify_<sha>)
# 2. point Alembic at it through the variable alembic/env.py reads (from .env, never typed in evidence)
uv run alembic heads            # exactly one head, unless the plan approves a merge
uv run alembic upgrade head     # applies from empty to head
uv run alembic check            # models and migrations agree (Alembic >= 1.9)
```

| Step | PASS | FAIL | BLOCKED |
|---|---|---|---|
| `alembic heads` | one head | two heads with no approved merge migration | - |
| `upgrade head` | exit 0, last revision applied | migration error (SQL error, missing dependency) | database cannot be created or reached |
| `alembic check` | `No new upgrade operations detected.` | `New upgrade operations detected: …` | Alembic older than 1.9: record `NOT_RUN` for this step with the version |

- Round-trip (`downgrade -1` then `upgrade head`) and data backfill checks follow `backend-database-migrations` when the migration policy asks for reversibility.
- Never run G5 on a shared dev database another person uses, and never on production. Reason: a failing migration half-applied on a shared database blocks everyone.

## G6 Integration tests — `pytest tests/integration -q`

Same result table as G4. In addition:

- The test database URL passes the guard in the suite's `conftest.py` (`{{slot:unit-testing}}`). No guard in the workspace → G6 is `BLOCKED` until one exists. Reason: without it nothing stops a run against a real database.
- `ConnectionRefusedError` / `InvalidPasswordError` / `database "…" does not exist` raised in a fixture → BLOCKED (environment), with the error line.

## G7 Coverage — only with an existing threshold

Where to look: `[tool.coverage.report] fail_under` in `pyproject.toml`, `.coveragerc` `[report]`, `setup.cfg` `[coverage:report]`, or `--cov-fail-under` in `[tool.pytest.ini_options] addopts`.

```bash
uv run pytest --cov=<package> --cov-report=term-missing -q
```

| Outcome | Result |
|---|---|
| Total ≥ threshold, tests pass | PASS (quote `TOTAL … 87%` and the threshold) |
| `FAIL Required test coverage of 85% not reached` | FAIL |
| No threshold configured | no G7 row; never invent one |

Coverage proves lines ran, not that behavior is asserted; it never replaces the AC rows.

## G8 OpenAPI diff

```bash
# export the spec of REVIEW_REVISION (the app import must not need a live database)
uv run python -c "import json; from app.main import app; print(json.dumps(app.openapi(), indent=2, sort_keys=True))" > <evidence-dir>/openapi.review.json
# compare with the agreed contract (api_contract.json / openapi.json in the repo, or the export at BASE_REVISION)
oasdiff breaking <agreed.json> <evidence-dir>/openapi.review.json      # when oasdiff is installed
diff -u <agreed.json> <evidence-dir>/openapi.review.json               # otherwise; read every hunk
```

`<evidence-dir>` is the run's evidence folder (`vN/evidence/<phase-id>/<REVIEW_REVISION>/`), never a path inside the service source. Reason: verification must leave the tree it verifies unchanged.

| Outcome | Result |
|---|---|
| Every difference is named in `design.md` / the contract change for this phase | PASS |
| A removed or renamed path, field, enum value or status code; a field newly required in a request; a response field newly nullable — not in `design.md` | FAIL (breaking for the frontend client) |
| App cannot be imported without a running service or secrets | BLOCKED; report the import-time side effect to `{{slot:clean-code}}` (CC12) |

Contract rules (versioning, error envelope, naming) belong to [api-contract-design](../../api-contract-design/SKILL.md); this gate only shows whether the running code matches what was agreed.
