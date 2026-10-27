# 03 — Self-Check Commands & Review Severity (Python / FastAPI)

Consolidated pre-handoff CLI verification commands (**C14**) and the unified review grading rubric (`BLOCKER` / `MAJOR` / `MINOR`) from `shared_contracts/flags_and_statuses.md`.

---

## 1. Deterministic Pre-Handoff CLI Gates (`PASS` / `FAIL`)

Determine the runner prefix from the service root (`uv run` when `uv.lock` is present, `poetry run` when `poetry.lock` is present) and execute in sequence before reporting `READY_FOR_REVIEW`. Every check is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)** and must be recorded as an evidence row:

```bash
# 1. Code formatting check
uv run ruff format --check <changed_files>

# 2. Linter, naming, debug calls, and cyclomatic complexity
uv run ruff check <changed_files>

# 3. Static type checking
uv run mypy <changed_files_or_package>

# 4. Forbidden patterns & structure scan via ripgrep (C3, C4, C15, C17)
rg -n "print\(|breakpoint\(|import pdb|except Exception|except:|# type: ignore(?!\[)|from \S+ import \*" <changed_files>
rg -n "^[a-z_][a-z0-9_]*\s*(:\s*[^=]+)?=\s*(\{|\[|dict\(|list\(|set\()" <changed_files>

# 5. Export surface check (C17) on any touched __init__.py
rg -n "__all__" <changed_init_files>

# 6. Affected unit tests
uv run pytest <affected_test_files> -q
```

---

## 2. Unified Review Severity Scale (`BLOCKER` / `MAJOR` / `MINOR`)

Reviewers and authors grade all code findings using the single unified scale defined in `shared_contracts/flags_and_statuses.md` §2 and `work-item-contract` (`references/handoff-and-status.md` §9).

> Do **not** use `P1` / `P2` / `P3` for code findings. Tool gates (`ruff`, `mypy`, `lint-imports`, `pytest`) are strictly `PASS` (`exit 0`) or `FAIL` (`exit != 0`).

| Severity | Criteria | Review Verdict Impact |
|---|---|---|
| **`BLOCKER`** | 1. **Failed CLI Gate (`FAIL`)**: `ruff check`, `ruff format --check`, `mypy`, `lint-imports`, or `pytest` exits non-zero.<br>2. **Core Design Rule Violation**: Pass-through wrapper or compatibility alias (**C1**), dead/debug code (**C2, C3**), swallowed exception or unlogged broad catch (**C4**), broken workspace contract (**C11**), import-time I/O or env read (**C12**), skipped self-check (**C14**), mutable module global (**C15**), exposed internal helper or `utils.py` bucket (**C16**), or leaked/wildcard export (**C17**).<br>3. **Behavioral / Security Defect**: Broken `AC-NN`, data corruption, crash, or security vulnerability. | **`CHANGES_REQUESTED`** (blocks approval). |
| **`MAJOR`** | Maintainability or clarity issue not caught by linters: vague naming (**C5**), function/file exceeding size thresholds without decomposition (**C6**), scattered magic literals (**C7**), drive-by edit outside task scope (**C10**), or mutable value object where `frozen=True` belongs (**C13**). | Must be fixed in the same revision when inside the phase's `Scope / Files`; triggers `CHANGES_REQUESTED` if left unaddressed in touched files. |
| **`MINOR`** | Redundant "what" comment (**C8**) or optional readability polish. | Non-blocking (`Optional`); never blocks `APPROVED`. |

## 3. Review Scope Rule

- Evaluate **only** code modified in the current task or phase diff (`BASE_REVISION..REVIEW_REVISION`).
- Pre-existing legacy debt outside the diff is recorded as an informational note in `Concerns`, never as a blocking finding.
