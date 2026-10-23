# 03 — Fix and prevent

Rules D6-D9 and D11 of [root-cause-debugging](../SKILL.md). Why this file exists: a root-cause fix at the right layer with a regression test is the only fix that stays fixed; green-washing removes the protection that found the bug.

## Fix

1. **Regression test first** (`{{slot:unit-testing}}`). Turn the minimised case into a test at a seam that exercises the real bug pattern: a use-case/service test with a fake port for logic, a repository test against the test database for queries and constraints, an in-process `httpx.AsyncClient` test for routing, validation and serialization. Place it per convention (`tests/unit/`, `tests/integration/`; the workspace may override). Run it: it must **fail for the reported reason** (same exception or assertion), not for a typo or a missing fixture.
2. **Smallest change at the owning layer** (`{{slot:clean-architecture}}`), inside the task's Scope / Files. Typical owners: a validation rule → the Pydantic schema or domain entity; a business rule → the use case/service; a query or loading strategy → the repository; a schema mismatch → the model **and** an Alembic migration. Run the workspace's impact analysis before editing a shared symbol if its tracing tool requires it ([05](05-tools-and-commands.md)). Check the diff for the same mistake elsewhere. No unrelated refactor. Why: wrong-layer fixes re-break on the next change and bloat review.
3. **Prove it.** Run the test: it passes. Undo only the fix in the working tree, rerun (must fail), restore, rerun (must pass). Record both runs as evidence rows. Why: a red you never saw may never have been red.
4. Rerun the original un-minimised reproduction, the affected suite, `uv run ruff check`, `uv run mypy` on the touched files, and the task's check; triage against **Expected** again ([plan-and-task-contract §3](../../work-item-contract/references/plan-and-task-contract.md)).
5. Remove every temporary print, tagged log, `breakpoint()`, `import pdb` and `echo=True`; `rg -n "<tag>"` returns nothing and `uv run ruff check --select T10,T20 <touched files>` is clean.

**No correct seam** for a test (the bug only shows against a third-party service or a production-only configuration) → say so in the hand-off as a finding; do not write a shallow test that mocks the bug away and gives false confidence.

**Bad data entering through a boundary** → add validation at the boundary that owns it (usually the Pydantic request model or the entry use case), failing loudly with the existing error type. Do not add checks in every layer beyond the task scope; extra layers are a design change for Planning.

**Migration fixes.** Never edit a migration that may already be applied elsewhere; add a new revision with `uv run alembic revision -m "<why>"` and a working `downgrade`. Why: an edited applied revision silently diverges databases. A new or changed table, column or constraint is a schema change → `change-control` unless the task already approves it.

## Never

| Tempting shortcut | Why it is forbidden |
|---|---|
| Edit, delete, `@pytest.mark.skip` / `xfail` the failing test, or change its assertion or the **Expected** line | Hides the defect and removes the check that found it; a genuinely wrong test (contradicts the AC or a `D-NN`) is a plan change request (`change-control`) |
| `except Exception: pass`, `contextlib.suppress(Exception)`, returning `None`/`[]`/a default on failure | Turns a loud failure into silent wrong data |
| Fake data or a hardcoded fallback so the endpoint "works" | Fabricates success; the real source is still broken |
| `Any`, `# type: ignore`, `cast(...)`, `model_config = ConfigDict(extra="allow")`, a looser assertion (`in` instead of `==`, `status_code < 500`) | Lets the same bug through next time |
| `asyncio.sleep`, retry loops, bigger timeouts, `pytest-rerunfailures` to make a race or slow query pass | The race or the slow query is still there, only rarer |
| `# noqa`, removing a ruff rule or mypy flag in `pyproject.toml`, skipping a CI gate | Removes protection for everyone |
| Committing `breakpoint()`, `import pdb`, `print`, `echo=True` | Leaks data and noise; ruff T100/T201 flag them anyway |

Every fix is a **new revision**: earlier review and test evidence for the touched code is invalid until rerun.
