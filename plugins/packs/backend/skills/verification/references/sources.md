# Sources

Ideas adapted into [backend verification](../SKILL.md), rewritten in this repo's vocabulary (gates G1–G8, evidence rows, `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`, `REVIEW_REVISION`). The claim discipline itself lives in core `evidence-standard`. Internal base inputs, read-only: the previous `plugins/packs/backend/skills/verification/SKILL.md` (Test Runner boundary, AC mapping), `src/skill_factory/library/generators/create-unit-testing-skill/references/tooling-by-stack.md` (Python commands, "did it run?" column, coverage only if measured), `src/skill_factory/library/generators/create-database-migrations-skill/` (disposable-database verification).

| Source (pinned link or doc URL + date read) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `verification-before-completion/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion/SKILL.md) | 303k | Linter clean ≠ build/type clean; read the full output and the failure count; partial checks prove nothing | SKILL §2 "a later gate never replaces an earlier one", §3 reading results |
| same | 303k | Requirements are checked line by line, not inferred from "tests pass" | SKILL §3 (coverage never replaces AC rows), [gates G7](gates.md) |
| [wshobson/agents `python-testing-patterns/SKILL.md`](https://github.com/wshobson/agents/blob/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/python-development/skills/python-testing-patterns/SKILL.md) | 42k | `--cov-fail-under` and `--cov-report=term-missing` | [G7](gates.md) |
| [Ruff docs](https://docs.astral.sh/ruff/) and [Ruff formatter](https://docs.astral.sh/ruff/formatter/) (read 2026-10-23) | - | `ruff format --check` exit codes 0/1/2; formatter does not sort imports; config in `pyproject.toml` | [G1](gates.md), [G2](gates.md) |
| [mypy docs](https://mypy.readthedocs.io/en/stable/) (read 2026-10-23, docs version 2.4.0) | - | Config in `pyproject.toml` / `mypy.ini`; strictness flags are configuration, not per-run choices | [G3](gates.md) |
| [coverage.py configuration](https://coverage.readthedocs.io/en/latest/config.html) (read 2026-10-23) | - | `fail_under` in `[report]` (`[tool.coverage.report]` in `pyproject.toml`); config lookup order | [G7](gates.md), [detection](workspace-detection.md) |
| [pytest-asyncio configuration](https://pytest-asyncio.readthedocs.io/en/latest/reference/configuration.html) (read 2026-10-23) | - | Async settings live in `[tool.pytest.ini_options]` | [detection](workspace-detection.md) |
| [FastAPI: Async Tests](https://fastapi.tiangolo.com/advanced/async-tests/) (read 2026-10-23) | - | App-level tests run without a server through `ASGITransport` | SKILL §5 (developer tests vs acceptance) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Rationalization tables and "spirit over letter" wording | superpowers verification-before-completion | Already carried by core `evidence-standard` §5; a stack slot must not restate core rules |
| Verifying agent delegation through the VCS diff | superpowers verification-before-completion | Core `review-workflow` pass 1 owns re-checking another role's claims |
| A default coverage threshold (for example 80%) | wshobson python-testing-patterns | Verification proves the workspace's agreed bar; introducing or raising a threshold is a `D-NN` |
| `ruff check --fix` / `ruff format` (writing) during verification | Ruff docs | Verification must leave the tree unchanged; fixes are a new revision by the Code Writer |
| `Base.metadata.create_all` as migration proof | common practice | Does not run migrations; `alembic upgrade head` + `alembic check` on a disposable database does |
| Running migrations against the shared dev database to save time | common practice | Half-applied migrations block other people; only a disposable or test database |
