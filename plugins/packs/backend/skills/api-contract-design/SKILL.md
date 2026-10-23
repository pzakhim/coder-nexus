---
name: api-contract-design
description: How a Python + FastAPI service keeps its HTTP API contract - openapi.json generated from the app (app.openapi()) is the contract, saved as a revision-bound snapshot under the work item's contracts/ folder (and the repository path when the workspace commits one), diffed against the base revision on every change with breaking-vs-additive rules and the One-Version Rule; separate input and output Pydantic schemas, one error envelope, status codes, pagination, auth declared per endpoint, stable operationIds and tags for generated clients, deprecation and versioning; how the snapshot feeds the frontend handshake (api_contract.json review, READY_FOR_MOCK, LIVE_DEPLOYED) and mock servers; and contract tests. Use when Spec Writer reviews a frontend API request, when Planning writes the API section of design.md, when the Code Writer adds or changes an endpoint, schema, status code or error, when the Code Reviewer grades API conformity, and whenever someone asks whether a change is breaking.
---

# Backend API Contracts (FastAPI + OpenAPI)

An extra skill of the backend pack. The process (gates, task format, evidence, review) stays in the core skills; the lifecycle between workspaces stays in the installed plugin's `shared_contracts/api_handshake_protocol.md`. This skill adds how a FastAPI service produces, changes and proves its contract.

Detail: [conventions](references/conventions.md) · [snapshot and diff](references/openapi-snapshot-and-diff.md) · [compatibility](references/compatibility.md). Realtime channels (SSE, WebSocket) are documented through [realtime](../realtime/SKILL.md).

## 1. What the contract is

| Artifact | Role | Owner |
|---|---|---|
| `design.md` → API section | The **approved intent** at Gate 2: endpoints, schemas, status codes, auth, examples. Written before code | Planning |
| `openapi.json` generated from the app at a stated revision | The **delivered contract**: what the code really accepts and returns | Code Writer generates; Code Reviewer regenerates and compares |
| `contracts/openapi.base.json` + `contracts/contract-change.md` | The change set: base snapshot and the classified diff | Code Writer |
| Frontend `api_contract.json` / `api_gap_report.md` | A **request** from the frontend client (`DRAFT_BY_FE`), never a source of truth for the backend | Frontend; reviewed by Spec Writer |

`openapi.json` is generated, never hand-edited. Reason: a hand-written spec drifts from the code the first time someone forgets to update it; generation makes drift impossible and turns every contract change into a visible diff.

## 2. Rules

| # | Rule | Reason |
|---|---|---|
| CT1 | Contract first: the endpoint, its schemas, status codes and auth are in the approved `design.md` before the task that builds it | Frontend and backend never guess each other; an endpoint the plan does not name is a `change-control` request |
| CT2 | Every path operation has an explicit return type or `response_model` that is a named Pydantic model (or a list of one); never `dict`, `Any` or an ORM object as the documented type | Only named models produce a typed schema in `openapi.json`, filter output fields and give generated clients real types |
| CT3 | Input and output are separate models (`OrderCreate`, `OrderUpdate`, `OrderRead`); inputs use `extra="forbid"` | Mass assignment and accidental exposure are prevented by construction (`{{slot:secure-coding-standards}}`) |
| CT4 | One error envelope, defined once and declared on routers through `responses=`; every documented status in `design.md` appears in `openapi.json` | Clients handle errors in one place; an undeclared status is invisible to generated clients |
| CT5 | Auth is declared through security dependencies so each operation in `openapi.json` carries `security`; public endpoints are listed as public in `design.md` | The contract shows who may call what; a missing `security` is either a public endpoint on purpose or a bug |
| CT6 | `operationId`s and tags are stable: set by the workspace's `generate_unique_id_function` (or FastAPI's default) and never changed casually | Generated clients name methods after them; a rename breaks every client build |
| CT7 | Every change regenerates `openapi.json` and records a classified diff against the base revision ([compatibility](references/compatibility.md)) | A breaking change must be seen and approved, not discovered by the frontend at runtime |
| CT8 | Prefer addition over modification; a breaking change needs an approved `D-NN`, a compatible path, deprecation and a handshake notice; keep one live version (One-Version Rule) | Installed clients keep working; parallel versions multiply maintenance |
| CT9 | Contract evidence states its source: generated from revision `<sha>`, served by `<environment>`, or mock | Fixture or mock success is never live success (handshake evidence policy) |

## 3. By role

- **Spec Writer**: review a frontend draft against the current `openapi.json` (generate it first). Every field, type, status or auth difference becomes a `Q-NN`; feasibility, data scopes and RBAC go into `requirements.md` / `codebase-notes.md`.
- **Planning**: fill the API section of `design.md`; classify each planned change (additive / breaking) up front. When the item changes existing endpoints, add a `PHASE-00` `[EXECUTE]` task that captures `contracts/openapi.base.json` at `BASE_REVISION`. Task checks name real commands with cwd, e.g. `uv run pytest tests/contract -q` (cwd: service root), with **Expected** stating the status codes and schema names.
- **Code Writer**: build the models and routes to the design, then regenerate the snapshot and the diff ([snapshot and diff](references/openapi-snapshot-and-diff.md)); an unplanned diff line is a defect or a `change-control` request, never a silent snapshot update.
- **Code Reviewer**: regenerate `openapi.json` from `REVIEW_REVISION` independently and compare it with the hand-off snapshot and with `design.md`; check CT1–CT9.
- **Test Runner**: compare live responses with the snapshot of the deployed revision, with real auth per role (`quality-acceptance`).

## 4. Commands (detect the runner first)

Detect the runner from the workspace: `uv.lock` → `uv run`, `poetry.lock` → `poetry run`, otherwise the active virtualenv. Find the app import path in the run command (`uvicorn app.main:app`, `fastapi run`, Dockerfile, Procfile, README).

```bash
# generate (cwd: service root)
uv run python -c "import json,sys; from app.main import app; json.dump(app.openapi(), sys.stdout, indent=2, sort_keys=True); print()" > <contracts>/openapi.json
# operations without security (must match the public list in design.md)
jq -r '.paths | to_entries[] | .key as $p | .value | to_entries[] | select(.value.security == null) | "\(.key | ascii_upcase) \($p)"' <contracts>/openapi.json
```

If the app cannot be imported (missing settings, import error), the snapshot is `BLOCKED` with the error; never write the spec by hand instead.

## Related core skills

[work-item-contract](../work-item-contract/SKILL.md) · [implementation-planning](../implementation-planning/SKILL.md) · [evidence-standard](../evidence-standard/SKILL.md) · [review-workflow](../review-workflow/SKILL.md) · [change-control](../change-control/SKILL.md) · [quality-acceptance](../quality-acceptance/SKILL.md).
