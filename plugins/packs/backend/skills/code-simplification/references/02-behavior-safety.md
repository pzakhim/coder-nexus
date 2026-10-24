# 02 — Behavior safety

Rules SM1, SM2, SM6 and SM7. Reason: a "simplification" that changes behavior is an unreviewed feature change.

## Before editing

Read, for the code you are about to change:

- **Callers**: `rg -n "<name>" app/ tests/`. Also search for string use (route names, `getattr`, settings keys, Celery/ARQ task names, `alembic` env imports) before deleting anything: dynamic use does not show in a symbol search.
- **FastAPI wiring**: `Depends(...)` chains, `dependency_overrides` in tests, lifespan handlers, middleware and exception handlers that turn exceptions into responses.
- **Side effects**: database writes, `session.commit()` / `flush()`, outbox or event publishing, cache writes, outbound HTTP calls, logging that audits.
- **Error paths**: which exception is raised, which handler maps it, which status code and body the client sees.
- **Lifecycle**: `AsyncSession` scope, `async with` blocks, background tasks, connection release.
- **Tests** that cover it (`tests/unit/`, `tests/integration/` by convention).

## Must stay identical

Inputs · outputs and response models · HTTP status codes and error bodies · raised exceptions and messages · side effects and their order · number and order of SQL statements on a hot path · transaction boundaries (what commits or rolls back together) · state transitions · `await` points that release the event loop · performance limits.

Existing tests pass **unchanged**. The only allowed test edit is an import path after a move. Reason: a test edited in the same step as the code no longer proves the old behavior.

Watch the Python-specific traps:

- Replacing a manual loop with a comprehension keeps exceptions raised mid-loop and the order of results.
- `dict` → dataclass/Pydantic model changes equality, hashing and JSON output; check every consumer and the response schema.
- `functools.cache` on a function that reads settings, time, request or tenant data changes behavior; cache only pure functions.
- Removing an `await`ed call or moving a `commit()` changes transaction semantics even when tests pass with a single request.
- Merging two Pydantic models (create / update / response) changes the API contract and can open mass assignment; they are separate contracts.

## One step at a time

After each simplification, run the workspace's checks (prefix with its runner, e.g. `uv run`, when it uses one):

```bash
ruff format <changed files>
ruff check <changed files>
mypy app
pytest <affected test files> -q
```

Keep each command and exit code as an evidence row (`evidence-standard`, handoff-and-status §4). Red after a step and the cause is not obvious → revert that step ([04](04-stop-criteria.md)).

## Never

- Change a test to make the simplification pass.
- Remove Pydantic field constraints, validators, error mapping (exception handlers, `HTTPException` translation), authorization or tenant/data-scope filters, `Depends` boundaries, transactions or package contracts. Guards owned by `{{slot:secure-coding-standards}}` stay even when they look redundant.
- Leave a wrapper, alias or re-export (`from .new import X as OldX`, a shim module, an `__init__.py` re-export) after moving code: update every caller in the same step and delete the old name (`{{slot:clean-code}}` wrapper and alias rules).
- Add a `# type: ignore` or `# noqa` to make a simplification pass: it hides the signal the check exists for.
