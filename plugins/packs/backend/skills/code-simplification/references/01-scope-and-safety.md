# 01 — Scope, Behavior Safety & Stop Criteria

Rules S1, S2, S3, S11, S12 and S13. Reason: simplifying at the wrong time, outside the diff or past the point where behavior changes turns a cleanup into an unreviewed feature change.

> **Workspace Convention Rule (`C11` — `EXTEND` vs `INIT`):**
> - **Existing project (`EXTEND`):** Simplify strictly toward the patterns, DI style (`Depends`), ORM query patterns, and error hierarchy already established in the workspace. Never introduce a second competing pattern inside a simplification pass.
> - **Greenfield project (`INIT`):** Follow the default Python 3.12+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x async patterns below.

## 1. When

| Situation | Simplify? |
|---|---|
| The phase's checks pass (`ruff check`, `mypy`, affected `pytest`) and the diff has a named smell | Yes, inside the changed code only — the simplicity pass of `incremental-implementation` |
| A review finding names unnecessary complexity in the phase's code | Yes, as the fix revision for that finding (`review-resolution`) |
| Checks are red | No: fix behavior first with `{{slot:root-cause-debugging}}` |
| The smell is outside the diff | No: record it in the hand-off's Concerns as a separate item |
| The code is already clear, or a later task in the plan rewrites it | No |
| Writing a new feature, endpoint or migration, or fixing a bug | No: that changes behavior and follows the plan, not this skill |

## 2. Scope

Only the files and lines changed in this phase. List them with:

```bash
git diff --name-only <base>...HEAD -- '*.py'
```

`<base>` is the branch point of the task. Conventional locations are `app/`, `tests/unit/`, `tests/integration/` and `alembic/versions/`; the workspace may use other paths.

- Inside the diff: avoidable complexity under any of the four lenses is fair game.
- Outside the diff: report it, never touch it. A drive-by change invalidates evidence for code nobody asked to change (`{{slot:clean-code}}` scope rule).
- Alembic revisions that already ran anywhere other than a local database are history: never "simplify" them; a new revision is planned work.
- Generated code (OpenAPI clients, protobuf stubs) is regenerated, not hand-simplified.

## 3. Before editing

Read, for the code you are about to change:

- **Callers**: `rg -n "<name>" app/ tests/`. Also search for string use (route names, `getattr`, settings keys, Celery/ARQ task names, `alembic` env imports) before deleting anything: dynamic use does not show in a symbol search.
- **FastAPI wiring**: `Depends(...)` chains, `dependency_overrides` in tests, lifespan handlers, middleware and exception handlers that turn exceptions into responses.
- **Side effects**: database writes, `session.commit()` / `flush()`, outbox or event publishing, cache writes, outbound HTTP calls, logging that audits.
- **Error paths**: which exception is raised, which handler maps it, which status code and body the client sees.
- **Lifecycle**: `AsyncSession` scope, `async with` blocks, background tasks, connection release.
- **Tests** that cover it (`tests/unit/`, `tests/integration/` by convention).

## 4. Must stay identical

Inputs · outputs and response models · HTTP status codes and error bodies · raised exceptions and messages · side effects and their order · number and order of SQL statements on a hot path · transaction boundaries (what commits or rolls back together) · state transitions · `await` points that release the event loop · performance limits.

Existing tests pass **unchanged**. The only allowed test edit is an import path after a move. Reason: a test edited in the same step as the code no longer proves the old behavior.

Python-specific traps:

- Replacing a manual loop with a comprehension keeps exceptions raised mid-loop and the order of results.
- `dict` → dataclass/Pydantic model changes equality, hashing and JSON output; check every consumer and the response schema.
- `functools.cache` on a function that reads settings, time, request or tenant data changes behavior; cache only pure functions.
- Removing an `await`ed call or moving a `commit()` changes transaction semantics even when tests pass with a single request.
- `asyncio.gather` over calls that share one `AsyncSession` is not safe: concurrency needs separate sessions, or it stays sequential.
- Merging two Pydantic models (create / update / response) changes the API contract and can open mass assignment; they are separate contracts.

## 5. One step at a time

After each simplification, run the workspace's checks (prefix with its runner, e.g. `uv run`, when it uses one). Each is `PASS` (`exit 0`) or `FAIL`:

```bash
ruff format --check <changed files>
ruff check <changed files>
mypy app
pytest <affected test files> -q
```

Keep each command and exit code as an evidence row (`evidence-standard`, handoff-and-status §4). Red after a step and the cause is not obvious → revert that step (§7).

## 6. Never

- Change a test to make the simplification pass.
- Remove Pydantic field constraints, validators, error mapping (exception handlers, `HTTPException` translation), authorization or tenant/data-scope filters, `Depends` boundaries, transactions or package contracts. Guards owned by `{{slot:secure-coding-standards}}` stay even when they look redundant.
- Leave a wrapper, alias or re-export (`from .new import X as OldX`, a shim module, an `__init__.py` re-export) after moving code: update every caller in the same step and delete the old name (`{{slot:clean-code}}` C1).
- Add a `# type: ignore` or `# noqa` to make a simplification pass: it hides the signal the check exists for.

## 7. Stop criteria

Past these points the change is design work that needs `change-control`, not simplification.

| Situation | Do instead |
|---|---|
| Behavior, an endpoint's request/response schema, a status code, an exception type or a DB schema would change | Stop; it is a contract change: `change-control` and the approval gate. API shape belongs to `api-contract-design` |
| A `D-NN` or a `{{slot:clean-architecture}}` port requires the abstraction | Leave it; mention it in Concerns if it looks unnecessary |
| The gain is cosmetic (renaming taste, reordering imports ruff already sorts, quote style) | Leave it |
| A hot path (query count, eager vs lazy loading, `await` points, batching) would change without a measurement | Measure first (query log, timing in an integration test) or leave it |
| The next step, or the right depth for an Altitude fix, needs code outside the diff | Record a separate item in Concerns |
| An Alembic revision that already ran outside a local database would be edited | Leave it; a new revision is planned work |
| A guard from `{{slot:secure-coding-standards}}` would be removed or merged away | Leave it |
| Checks turn red and the cause is not obvious | Revert the last step; do not debug a refactor |
| No named smell remains | Stop and report |
