# 05 — Self-check

Execute these checks on the files changed in the task or phase before reporting `READY_FOR_REVIEW`. An unrun check cannot be reported as passed (`evidence-standard`).

## Runner detection

Determine the command prefix from the service root (where `pyproject.toml` resides):

| Found | Prefix |
|---|---|
| `uv.lock` | `uv run` |
| `poetry.lock` | `poetry run` |
| `requirements*.txt` | Active virtualenv (`python -m` or direct executable) |

## Self-check commands

Run these checks in sequence from the service root:

1. **Code formatting**:
   ```bash
   uv run ruff format --check <changed_files>
   ```

2. **Linting and style rules**:
   ```bash
   uv run ruff check <changed_files>
   ```

3. **Type checking**:
   ```bash
   uv run mypy <changed_files_or_package>
   ```

4. **Forbidden patterns grep check**:
   ```bash
   # Check for debug calls, bare except, and wildcard imports
   rg -n "print\(|breakpoint\(|import pdb|except Exception|except:|# type: ignore(?!\[)|from \S+ import \*" <changed_files>

   # Check for mutable module-level dictionaries or lists (C15)
   rg -n "^[a-z_][a-z0-9_]*\s*(:\s*[^=]+)?=\s*(\{|\[|dict\(|list\(|set\()" <changed_files>
   ```
   *Note: Module-level `__all__ = [...]` and `logger = ...` are legitimate false positives.*

5. **Unit tests for affected components**:
   ```bash
   uv run pytest <affected_test_files> -q
   ```

## Evidence reporting

- Each executed check must be recorded as one evidence row in the hand-off per [handoff-and-status §4](../../work-item-contract/references/handoff-and-status.md).
- Status must reflect real outcomes: `PASS` when exit code is 0; `FAIL` if violations are found; `NOT_RUN` if the tool is unconfigured or absent. Never claim `PASS` for an unrun check.
