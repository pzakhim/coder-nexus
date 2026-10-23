# Sources

Ideas adapted into [unit-testing](../SKILL.md), rewritten in this repository's vocabulary (design Pass/Default, Fail and Empty rows, seams named in `design.md`, **Expected** triage, evidence rows, `NOT_RUN` / `BLOCKED`).

## Internal base inputs (read-only)

| Input | Taken | Where |
|---|---|---|
| Skill Factory generator `create-unit-testing-skill` (`references/base-rules.md` U1–U14, `cases-by-layer.md` Backend table, `tooling-by-stack.md` Python row, `templates/`) | Rule table, per-layer matrix, file shape 01–06, commands and "did it run?" | SKILL rules, [01](01-what-to-test.md)–[06](06-test-boundaries.md) |
| Core skill `test-first` (removed; merged here) | When the test comes first, red/green loop, name the break, right-reason table, independent expectations, doubles order, never list, mutation check, set-aside rule | SKILL "For every behavior change", "When the test comes first", "Never"; [04](04-test-quality.md); [03](03-doubles-and-fixtures.md) |
| Previous Backend `unit-testing` skill | Mandatory negative cases (validation, auth, not found, dependency failure, rollback) | [01](01-what-to-test.md) matrix |
| Backend `unit-test` draft (branch `wip/phase2-backend`) | Detect-before-writing, layout, pytest-asyncio settings, fakes vs `MagicMock`, `httpx.MockTransport`, dependency overrides, factories, determinism, commands; service and router templates | [02](02-location-and-naming.md), [03](03-doubles-and-fixtures.md), [05](05-running-and-evidence.md), [templates/](../templates/) |

## External sources

| Source (link pinned) | Idea taken | Where used |
|---|---|---|
| [obra/superpowers `test-driven-development/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/test-driven-development/SKILL.md) | Watch it fail for the expected reason; least code to pass; code before the test does not skip the red run; reproduce bugs red first | SKILL loop and table, [right-reason](04-test-quality.md#right-reason-failure) |
| [obra/superpowers `writing-good-tests.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/test-driven-development/writing-good-tests.md) | Name the break; no change detectors; no assertions on mocks; complete data shapes; mutation check | [04](04-test-quality.md), [03](03-doubles-and-fixtures.md) |
| [mattpocock/skills `engineering/tdd`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/tdd/SKILL.md) | Agreed seams; vertical slices; glossary vocabulary; verify through the interface; mock only at system boundaries | SKILL loop, [01](01-what-to-test.md), [04](04-test-quality.md) |
| [addyosmani/agent-skills `test-driven-development`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/test-driven-development/SKILL.md) | Real > fake > stub > mock; when not to test (config, docs) | [03](03-doubles-and-fixtures.md), SKILL table |
| [pytest: How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) | Function scope default, yield teardown, `conftest.py` sharing, factories as fixtures, autouse is implicit | [02](02-location-and-naming.md), [03](03-doubles-and-fixtures.md) |
| [pytest: `pytest.raises`](https://docs.pytest.org/en/stable/how-to/assert.html) and exit codes | Specific exceptions, `match=`; exit code 5 = no tests collected | [04](04-test-quality.md), [05](05-running-and-evidence.md) |
| [pytest-asyncio configuration](https://pytest-asyncio.readthedocs.io/en/latest/reference/configuration.html) | `asyncio_mode` (default `strict`) | [03](03-doubles-and-fixtures.md#async-setup) |
| [FastAPI: Async Tests](https://fastapi.tiangolo.com/advanced/async-tests/), [Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) | `AsyncClient` + `ASGITransport`; lifespan not run; overrides keyed by the original dependency and reset | [03](03-doubles-and-fixtures.md#router-tests-through-overrides) |
| [HTTPX: Transports](https://www.python-httpx.org/advanced/transports/) | `MockTransport` handlers, `ASGITransport(raise_app_exceptions=False)` | [03](03-doubles-and-fixtures.md) |
| [Python `unittest.mock`: autospeccing](https://docs.python.org/3/library/unittest.mock.html#autospeccing) | `create_autospec` / `spec_set` so renamed methods fail | [03](03-doubles-and-fixtures.md) |
| [Ruff rules `PT`, `B017`](https://docs.astral.sh/ruff/rules/) | `pytest.raises` too broad (`PT011`), multiple statements in the block (`PT012`), `assertRaises(Exception)` (`B017`) | SKILL U8, [04](04-test-quality.md) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| "No production code without a failing test" for every change, exceptions only by asking | superpowers TDD | Wiring, migrations and generated code have better checks; the plan and the SKILL table decide |
| Delete code written before the test | superpowers TDD | Set aside, run red, restore reaches the same proof without wasting approved-scope work |
| Refactor step inside each cycle | superpowers, addyosmani TDD | Clean-up is a separate pass (`{{slot:code-simplification}}`) at phase end so behavior change and refactoring stay apart for review |
| Confirm seams with the user before each test | mattpocock tdd | Seams are agreed once in `design.md` at Gate 2; a missing seam goes through `NEEDS_CONTEXT` / `change-control` |
| Test pyramid percentages, coverage targets | addyosmani TDD, common practice | Test levels come from the plan's test strategy; a coverage gate only where the workspace already configures one |
| `@pytest.mark.anyio` | FastAPI Async Tests docs | The baseline runner is pytest-asyncio; two async plugins make collection depend on plugin order |
| `freezegun` as the default way to fix time | common practice | An injected clock is explicit; freezegun only when already installed |
| `skip` / `xfail` for unfinished features or known bugs | common practice | Not evidence; a known bug is reproduced red and fixed |
| Repository tests, database fixtures (test-database guard, `alembic upgrade head`, per-test savepoint rollback), SQLite for tests | Backend draft | Real-database work is integration, owned by `{{slot:verification}}`; SQLite is never a stand-in for PostgreSQL |
| SSE / WebSocket test shapes | Backend draft | Protocol-specific; left to a later realtime skill |
| UI layout row and `visual-quality` slot | core `test-first` | A Backend service has no UI layout |
