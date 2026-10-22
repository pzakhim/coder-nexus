# Bug patterns by stack (+ project patterns)

The generated `05-bug-patterns.md` = applicable stack patterns below **+ project patterns** derived from the workspace. Each pattern is one row: *looks like* → *goes wrong when* → *check*.

## Python / FastAPI / SQLAlchemy async

- Coroutine called without `await` (returns a coroutine object, nothing happens).
- Work after `uow.commit()` that should be inside the transaction, or commit inside a repository.
- `except Exception` returning a default → failure looks like an empty success.
- Mutable default arguments; module-level state shared across requests.
- SQL built with f-strings / string concatenation.
- Pydantic model with `exclude_unset`/defaults hiding a missing field the client must send.
- Datetime naive vs aware mix; `date.today()` instead of the configured timezone.
- Pagination: off-by-one on `offset`, missing stable `ORDER BY`.

## TypeScript / React / Next.js

- `useEffect` with missing dependencies or a fetch without cancellation/stale-response guard.
- State updated from a response after tenant/environment/route changed.
- Double submit: button not disabled while the mutation runs.
- Server-only module or secret imported into a client component.
- `key` from array index in lists that reorder.
- `===` vs `==`, `NaN` from `parseInt` on user input, `0`/`""` treated as missing.
- Error caught and turned into an empty list / success shape.
- Cached authenticated response without scope in the cache key.

## Flutter / Dart

- `setState`/emit after `dispose`/`close`; `BuildContext` used across an async gap.
- Stream subscription or controller not cancelled.
- `late` field read before initialisation.
- JSON parsing assuming non-null / exact numeric type.

## Go

- Loop variable captured by goroutines (pre-1.22); goroutine leak on early return; missing `defer rows.Close()`; error shadowed by `:=`; nil map write.

## Deriving project patterns

From `CLAUDE.md`, `AGENTS.md`, architecture docs, and bug-fix commits (`git log --grep='fix'`), write patterns for the workspace's risk areas, for example:

| Risk area | Pattern to write |
|---|---|
| Multi-tenant / multi-environment data | A query or cache without the tenant/environment filter; a write to the wrong environment |
| Governed content (drafts, releases, approvals) | A mutation outside the allowed state (e.g. outside a draft change set) |
| Authorization model | A route/use case without the capability guard; UI hiding used as the only check |
| Money / quantities / units | Float arithmetic, rounding at the wrong step, unit mix |
| Migrations / backfills | Non-idempotent migration, long lock on a hot table, missing default for existing rows |
| External providers (ERP, LLM, payment) | Timeout without retry limit, partial failure treated as success, provider error leaked to users |

Each project pattern names a real path where it applies (or could).
