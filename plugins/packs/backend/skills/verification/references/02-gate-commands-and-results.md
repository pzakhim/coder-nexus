# Gate Commands and Results (`G1`–`G8`)

> Topic: Detailed execution commands, exit codes, and `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` interpretation for `G1`–`G8`, `lint-imports`, and `pip-audit`.

Commands below show the `uv run` prefix; use the prefix detected in [01-workspace-detection-and-task-checks.md](01-workspace-detection-and-task-checks.md). Working directory (`cwd`) is the service root.

---

## G1: Format Check — `ruff format --check .`

| Exit Code | Output | Gate Result |
|---|---|---|
| `0` | `N files already formatted` | `PASS` |
| `1` | `Would reformat: app/services/orders.py` | `FAIL` |
| `2` | Invalid config / CLI / internal error | `BLOCKED` (quote exact error) |

- Run across the whole service root unless the workspace's own CI target scopes it.
- Formatter checks do not sort imports; import sorting belongs to Ruff's `I` rules in `G2`.

---

## G2: Static Lint — `ruff check .`

| Exit Code | Output | Gate Result |
|---|---|---|
| `0` | `All checks passed!` | `PASS` |
| `1` | `Found N errors.` with rule codes | `FAIL` |
| `2` | Configuration or internal tool error | `BLOCKED` |

- **Never pass `--fix`** during a verification run: verification must not mutate the working tree it verifies. Code fixes belong to Code Writer on a new revision.
- New `# noqa` or `per-file-ignores` added in the diff without justification are flagged in `{{slot:code-review}}` (`BLOCKER` / `MAJOR`).

---

## G3: Type Check — `mypy <package>`

| Exit Code | Output | Gate Result |
|---|---|---|
| `0` | `Success: no issues found in N source files` | `PASS` |
| `1` | `Found N errors in M files` | `FAIL` |
| `2` | Crash, bad config, or missing third-party stubs with no config | `BLOCKED` |

- Target the `files` / `packages` configured in `[tool.mypy]`, or else the application package named in `pyproject.toml`.
- Verify the file count in the output (`N source files`): checking 2 files in a 150-file service indicates a misconfigured target.
- Keep all workspace plugins (`pydantic.mypy`) and strictness settings intact; never lower strictness flags for a run.

---

## G4: Unit Tests — `pytest tests/unit -q`

| Exit Code | Output | Gate Result |
|---|---|---|
| `0` | `N passed` (inspect `skipped`, `xfailed`, `deselected`) | `PASS` only when the phase's new/updated tests are among the passed |
| `1` | `N failed` | `FAIL` |
| `2` / `3` / `4` | Interrupted, internal error, or collection `ImportError` | Import/syntax error in changed code is `FAIL`; broken environment/tool config is `BLOCKED` |
| `5` | `no tests ran` | `NOT_RUN` |

- Confirm with `-v` or `--collect-only -q` that the phase's test IDs were collected when the count looks unexpectedly low.
- A skipped test (`@pytest.mark.skip`) that guards a phase `AC-NN` renders that `AC-NN` **`NOT_RUN`**.

---

## G5: Migrations — Disposable Database

```bash
# 1. Point Alembic at a disposable database created for verification (e.g., <app>_verify_<sha>)
# 2. Never print the connection URL in logs or evidence
uv run alembic heads            # Must report a single head unless a merge migration is approved
uv run alembic upgrade head     # Applies cleanly from empty schema to head
uv run alembic check            # Verifies SQLAlchemy metadata matches Alembic heads (Alembic >= 1.9)
```

| Step | `PASS` | `FAIL` | `BLOCKED` / `NOT_RUN` |
|---|---|---|---|
| `alembic heads` | Exactly 1 head | Multiple heads without an approved merge | — |
| `alembic upgrade head` | Exit `0`, head revision applied | SQL error, constraint error, or broken migration script | `BLOCKED` if disposable DB cannot be created or reached |
| `alembic check` | `No new upgrade operations detected.` | `New upgrade operations detected: ...` (model drift) | `NOT_RUN` if Alembic `< 1.9` (record exact version) |

- Round-trip verification (`alembic downgrade -1 && alembic upgrade head`) and data-backfill checks follow [database-migrations](../../database-migrations/SKILL.md).
- Never execute `G5` against a shared dev database or production.

---

## G6: Integration Tests — `pytest tests/integration -q`

Uses the same exit-code table as `G4`, plus two mandatory database safety rules:
1. **Test Database Guard (`conftest.py`)**: The test suite must enforce a database URL/name guard (`{{slot:unit-testing}}`) that aborts immediately if pointed at a non-test database. If no guard exists in the workspace, `G6` is **`BLOCKED`** until one is added.
2. **Connection / Fixture Failures**: `ConnectionRefusedError`, `InvalidPasswordError`, or `database "..." does not exist` during fixture setup is **`BLOCKED`** (environment blocker), not a code `FAIL`.

---

## G7: Coverage — `pytest --cov=<package> --cov-report=term-missing -q`

Check `[tool.coverage.report] fail_under` in `pyproject.toml`, `.coveragerc`, `setup.cfg`, or `--cov-fail-under` in `[tool.pytest.ini_options] addopts`.

| Outcome | Gate Result |
|---|---|
| Tests pass and total coverage ≥ configured `fail_under` (or report generated cleanly when no threshold is configured) | `PASS` (record `TOTAL ... NN%` and configured threshold) |
| `FAIL Required test coverage of NN% not reached` | `FAIL` |

- Coverage proves lines executed, not that behavioral requirements are asserted; it never replaces per-AC verification rows.

---

## G8: OpenAPI Contract Diff

```bash
# Export the OpenAPI spec at REVIEW_REVISION to the evidence directory (never inside the service source tree)
uv run python -c "import json; from app.main import app; print(json.dumps(app.openapi(), indent=2, sort_keys=True))" > <evidence-dir>/openapi.review.json

# Compare against agreed baseline (openapi.json / api_contract.json or BASE_REVISION export)
oasdiff breaking <agreed.json> <evidence-dir>/openapi.review.json   # Preferred when oasdiff is installed
diff -u <agreed.json> <evidence-dir>/openapi.review.json            # Fallback; inspect every hunk
```

| Outcome | Gate Result |
|---|---|
| Every path, field, status code, and schema diff matches `design.md` | `PASS` |
| Undeclared breaking change (removed/renamed path, field, enum, status code; newly required request field; newly nullable response field) | `FAIL` |
| `app.main:app` cannot be imported without a live DB or external network call | `BLOCKED` (report import-time side effect as a `{{slot:clean-code}}` violation) |

---

## Supplementary Stack Gates (`lint-imports` & `pip-audit`)

- **Architecture Layer Contracts (`lint-imports`)**: When `[tool.importlinter]` is present in `pyproject.toml`, run `uv run lint-imports` (`PASS` on `0 broken contracts`, `FAIL` on any broken contract).
- **Dependency Vulnerability Audit (`pip-audit`)**: When `pyproject.toml` or lockfiles change, run `uvx pip-audit` or `uv run pip-audit` (`PASS` on 0 known vulnerabilities, `FAIL` on unmitigated CVE, `BLOCKED` if offline without vulnerability DB cache).
