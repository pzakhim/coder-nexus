## Phase gates - <phase-id> @ <REVIEW_REVISION>

Service root: `<services/api>` | Prefix: `<uv run | poetry run | python -m>` | Python `<x.y>` | ruff `<v>` | mypy `<v>` | pytest `<v>` | Alembic `<v>`
Test database: `<name only, no URL>` (guard rule: `<_test suffix | D-NN>`) | Disposable DB for G5: `<name>` created by `<who>`
Tree: `git status --short` → `<clean | listed scope>`

| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
|---|---|---|---|---|---|
| G1 format | `<prefix> ruff format --check .` (cwd `<root>`) | `<sha>` | | `<N files already formatted>` | |
| G2 lint | `<prefix> ruff check .` (cwd `<root>`) | `<sha>` | | `<All checks passed!>` | |
| G3 types | `<prefix> mypy <package>` (cwd `<root>`) | `<sha>` | | `<Success: no issues found in N source files>` | |
| G4 unit tests | `<prefix> pytest tests/unit -q` (cwd `<root>`) | `<sha>` | | `<N passed, M skipped>` | |
| G5 migrations | `<prefix> alembic heads && <prefix> alembic upgrade head && <prefix> alembic check` (disposable DB) | `<sha>` | | `<No new upgrade operations detected.>` | |
| G6 integration tests | `<prefix> pytest tests/integration -q` (cwd `<root>`) | `<sha>` | | `<N passed>` | |
| G7 coverage | `<prefix> pytest --cov=<package> --cov-report=term-missing -q` - only if `fail_under` exists | `<sha>` | | `<TOTAL ... NN% (threshold NN)>` | |
| G8 OpenAPI diff | export + `<oasdiff breaking | diff -u> <agreed.json> <evidence-dir>/openapi.review.json` | `<sha>` | | `<differences: only those in design.md>` | |

Result words: PASS / FAIL / BLOCKED / NOT_RUN. A gate that does not apply to this phase gets one line with the reason instead of a row. BLOCKED and NOT_RUN rows name the reason and the owner.
