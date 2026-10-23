# 02 — Location and naming

Detail for [unit-testing](../SKILL.md). Rules U9, U10. The paths are conventions; when the workspace already has a test tree, follow it and list any drift you find instead of mixing two layouts.

## Detect before writing

Read `pyproject.toml` (`[tool.pytest.ini_options]`), `pytest.ini` / `setup.cfg` if present, and every `conftest.py` first. The workspace's runner, markers, fixture names and folders win over every default here. Reason: two test styles in one repository means every new test is written and reviewed against the wrong rule.

## Where

| Source | Test | Level |
|---|---|---|
| `app/domain/orders.py` | `tests/unit/domain/test_orders.py` | unit, no doubles |
| `app/application/orders.py` | `tests/unit/application/test_orders.py` | unit, fakes at ports |
| `app/api/schemas/orders.py` | `tests/unit/api/schemas/test_orders.py` | unit, Pydantic only |
| `app/api/orders.py` (router) | `tests/unit/api/test_orders.py` | unit, service faked via overrides |
| `app/infrastructure/clients/erp.py` | `tests/unit/infrastructure/clients/test_erp.py` | unit, `httpx.MockTransport` |
| `app/infrastructure/repositories/orders.py` | `tests/integration/...` | not here — `{{slot:verification}}` |

- One test file per source module; the path mirrors the package below `app/`. Reason: the reviewer finds the guard for a changed line without searching.
- Shared fakes in `tests/fakes.py` (or `tests/fakes/`), data builders in `tests/factories.py`, shared unit fixtures in `tests/unit/conftest.py`. Reason: one fake per port, reused, keeps its contract in one place.
- Database fixtures live only under `tests/integration/conftest.py`. Reason: a unit test can then never reach a database by accident.
- Name test files `test_<module>.py`; pytest collects `test_*.py` by default. A file named `orders_test.py` is collected only if the workspace configured `python_files` for it.

## Names

- Function: `test_<behavior>_<condition>[_<result>]` with Glossary terms, e.g. `test_cancel_order_when_already_shipped_raises_order_not_cancellable`. Reason: a failing name reads as the broken rule.
- Group related tests of one subject with a plain `class TestOrderCancel:` only if the workspace already does; no `unittest.TestCase` subclasses in a pytest suite. Reason: `TestCase` disables fixtures and parametrization.
- Parametrized cases get readable ids: `@pytest.mark.parametrize("qty", [0, -1], ids=["zero", "negative"])`. Reason: `test_x[zero]` in the output names the failing row.
- Constants used across cases (`OWNER_A`, `ORDER_1`, `FIXED_NOW`) are module-level `UPPER_CASE`, named for their role, not `user1` / `data`.

## Known drift

Record inconsistent locations or names you find (two folders for the same layer, mixed `test_x.py` / `x_test.py`) in your hand-off notes; fix them only when a phase task touches those files. Reason: renaming tests outside the task's **Scope / Files** is unreviewed scope.
