# 01 — Scope and candidates

Real defects are found in a fixed tree, in the callers of what changed, and by a systematic walk rather than an intuitive read. This file covers the steps before any candidate is judged.

## Fix the scope

- **Revision.** Record `BASE_REVISION` and `REVIEW_REVISION` from the hand-off header ([handoff-and-status](../../work-item-contract/references/handoff-and-status.md) §1), plus the staged, unstaged and untracked files that belong to the item (`git status --short`, `git diff --stat <BASE_REVISION>..<REVIEW_REVISION>`). Review exactly that tree. Reason: a finding must refer to code that will ship, not a moving target. The Code Writer's self-check runs on the phase diff before its commit; the Reviewer runs on the committed `REVIEW_REVISION` only.
- **Whole context.** Read each changed hunk with its whole enclosing function, class, router module or migration file. Reason: guards, early returns and `finally` blocks outside the hunk decide whether a suspicion is real.
- **Callers.** For each changed public symbol, find and read its callers. A broken caller outside the diff is in scope, because most regressions surface there, not in the changed lines. Public symbols in this stack:
  - function or method signature, return type, `None`-ability, raised exceptions (`HTTPException` status, domain errors, `NoResultFound`);
  - Pydantic model fields, aliases, defaults, `model_config` (`extra`, `populate_by_name`);
  - route path, method, status code, `response_model`, dependency (`Depends(...)`) signature;
  - SQLAlchemy model column, nullability, relationship loading, table / constraint name;
  - settings keys, event or message payloads, background task arguments.
- **Caller search** (read-only), from the repo root:
  - `rg -n -w "<symbol>" app tests` for Python references;
  - `rg -n "\"<json_key>\"|'<json_key>'" app tests` for serialized keys and aliases;
  - `rg -n "<path_fragment>" app tests` for route consumers and tests;
  - GitNexus `context` / `impact`, where configured, for call graphs.
  `app/`, `tests/unit/`, `tests/integration/` and `alembic/versions/` are conventional paths; use the workspace's real ones.

## Cold pass first

Hunt from the code **before** reading `requirements.md`, `design.md`, `api_contract.json`, the phase file or the hand-off's Concerns. Read them afterwards only to decide whether a suspicious behavior is intended (a `D-NN` decision or an AC) or a defect. Reason: knowing the intent makes the reader see what the code should do instead of what it does.

## Seven dimensions

Walk the scope once per dimension and write every suspicion as `file:line — hypothesis`. Reason: a walk per dimension finds what a single read skips. Prompts are starting points; dimension 6 holds the full stack list.

1. **Logic and data flow** — wrong comparison or operator, off-by-one in `offset` / slicing / `range`, inverted flag, wrong variable, value overwritten in a loop, truthiness used for "missing" (`if not qty` treats `0` as absent), `Decimal` vs `float`, `round()` banker's rounding, timezone or unit mismatch.
2. **Error and edge paths** — `None` or missing key, empty result (`scalars().first()` → `None`), first / last page, `scalar_one()` raising on 0 or 2 rows, failed or slow external call (`httpx` timeout, retry), partial success across several writes, validation bypassed on one path (a second endpoint or a background job writing the same data).
3. **State, async and lifecycle** — coroutine not awaited, blocking call inside `async def`, one `AsyncSession` used by concurrent tasks, attribute access after `commit()` (expired instance → lazy I/O), lazy relationship load in async code, work done after commit or after the session closed (`BackgroundTasks`), check-then-act races, lost updates, client or connection not closed on the error path, module-level mutable state shared across requests.
4. **Contract and caller breakage** — callers from the scope step now receive another type, `None`, exception or status code; a response field renamed, removed or changed in nullability against `api_contract.json` or `design.md`; a Pydantic alias, enum value or event payload no longer matching the consumer; an ORM model no longer matching the latest Alembic revision.
5. **Security, scope and data safety** — object-level authorization (the query filters by `owner_id` / `tenant_id`, not only the route having a user), mass assignment from a request body, SQL / shell / template built from request data, secrets or personal data in logs, exceptions or responses, unsafe parsing that silently substitutes a default. The rules for writing this safely belong to `{{slot:secure-coding-standards}}`; here you only hunt the breach.
6. **Stack and project patterns** — every row of [05-bug-patterns.md](05-bug-patterns.md) the changed code can hit.
7. **Test blind spots** — for each surviving candidate: would an existing test fail if it were real? Watch for tests that cannot fail here: a repository mocked so the SQL filter is never executed, a transaction-rollback fixture hiding a missing `commit()`, `dependency_overrides` replacing the very guard under review, an `async def` test that never ran because the pytest-asyncio mode or marker is missing. A defect without a failing test is still a defect; record the missing test with the finding.

`quick` effort runs dimensions 1–4 on the changed hunks only.

## Not candidates

Reuse, simplification or efficiency without a failure (a slower query that still returns the right rows within the contract, a duplicated helper) is not a defect. Note it, if worth it, as a `NOTE` line for `code-simplification`. Reason: the defect list must stay about defects. An N+1 that hangs or times out a realistic page is a defect, not a note.
