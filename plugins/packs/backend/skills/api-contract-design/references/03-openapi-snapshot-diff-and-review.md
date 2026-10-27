# OpenAPI Snapshot, Diffing, Handshake & Review Gates

> Topic: Deterministic `contracts/openapi.json` export (`CT1`), base-vs-head OpenAPI diffing (`CT7`), `contracts/contract-change.md` classification, cross-repo `api_contract.json` handshake (`CT9`), binary `PASS`/`FAIL` CLI gates, and `BLOCKER`/`MAJOR`/`MINOR` review rubric.

## 1. Exporting the Committed OpenAPI Snapshot (`CT1`)

`contracts/openapi.json` is mandatory reviewable evidence — never ask a reviewer or frontend engineer to boot a local server and inspect `/docs` to discover what changed.

### Deterministic Export Script (`scripts/export_openapi.py`)

```python
from pathlib import Path
import json
from app.main import create_app


def export_openapi(output_path: Path = Path("contracts/openapi.json")) -> None:
    app = create_app()
    schema = app.openapi()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    export_openapi()
```

- **Why `sort_keys=True`**: Guarantees deterministic key ordering across Python invocations so `git diff contracts/openapi.json` highlights only real contract edits.
- **No side effects at import/export time**: `create_app()` must construct routers and OpenAPI schemas without opening live PostgreSQL/Redis connections.

---

## 2. Base vs. Head OpenAPI Diff Workflow (`CT7`)

Whenever any router, DTO, status code, security dependency, or exception envelope changes, compare the base branch contract against the head snapshot:

### Step 1 — Extract `contracts/openapi.base.json` from Git

```bash
git show origin/develop:contracts/openapi.json > contracts/openapi.base.json
```

*(Remove `contracts/openapi.base.json` before committing, or keep it in `.gitignore`.)*

### Step 2 — Run Structural & Breaking Diff

- **With `oasdiff` (preferred when installed)**:
  ```bash
  oasdiff breaking contracts/openapi.base.json contracts/openapi.json
  oasdiff changelog contracts/openapi.base.json contracts/openapi.json
  ```
- **With `jq` + `diff -u` (always available in standard toolchains)**:
  ```bash
  # Compare all (path, method, operationId, status codes) tuples:
  diff -u \
    <(jq -S '.paths | to_entries | map({path: .key, methods: (.value | to_entries | map({method: .key, op: .value.operationId, status: (.value.responses | keys)}))})' contracts/openapi.base.json) \
    <(jq -S '.paths | to_entries | map({path: .key, methods: (.value | to_entries | map({method: .key, op: .value.operationId, status: (.value.responses | keys)}))})' contracts/openapi.json)

  # Full normalized schema diff:
  diff -u <(jq -S . contracts/openapi.base.json) <(jq -S . contracts/openapi.json)
  ```

### Step 3 — Record `contracts/contract-change.md`

When `contracts/openapi.json` changes in a feature or bugfix branch, summarize the diff in `contracts/contract-change.md` (or in the phase handoff artifact):

```markdown
# Contract Change Summary

- **Classification**: `additive` | `breaking (approved by D-NN in design.md)`
- **Base Commit**: `<git-sha>`
- **Operations Added**:
  - `POST /api/v1/work-orders` (`work_orders_create`) — Scope: `work_orders:write`, Idempotency-Key: required
- **Operations Modified**:
  - `GET /api/v1/work-orders` (`work_orders_list`) — Added optional `priority` query filter
- **Breaking Changes**: None
- **Handshake Sync**: `api_contract.json` updated (`PASS`)
```

---

## 3. Cross-Repo Handshake (`api_contract.json`, `CT9`)

When the Backend service pairs with a mobile or web client workspace, keep `api_contract.json` synchronized per `shared_contracts/api_handshake_protocol.md`:

- Every endpoint entry in `api_contract.json` must match `contracts/openapi.json` on:
  - `method`, `path`, and `operation_id`
  - Authentication requirement and required scopes (`CT5`)
  - Request DTO field names, types, constraints, and `Idempotency-Key` header requirement (`CT2`, `CT10`)
  - Response DTO field names, types, nullability, and pagination wrapper (`CT2`, `CT6`)
  - Error status codes and `ErrorResponse` `error.code` values (`CT3`, `CT4`)
- For Server-Sent Events (SSE) or WebSocket channels paired with REST endpoints, cross-reference `backend-realtime` so event payload schemas are versioned alongside HTTP DTOs.

---

## 4. Deterministic CLI Verification Gates (`PASS` / `FAIL`)

All automated contract checks report strictly **`PASS`** or **`FAIL`** (`shared_contracts/flags_and_statuses.md`; `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`):

| Gate | Command | `PASS` Criterion | `FAIL` Resolution |
|---|---|---|---|
| **G1 — Snapshot Drift Gate** | `uv run python scripts/export_openapi.py && git diff --exit-code contracts/openapi.json` | Exit `0` — `contracts/openapi.json` matches live code | Re-export `contracts/openapi.json` and commit |
| **G2 — Raw Wire Model Scan** | `rg -n "response_model\s*=\s*(dict|Any|None)" app/ src/ -g "*.py"` | `0` unapproved matches | Declare explicit `*Response` Pydantic DTO (`CT2`) or `status_code=204, response_class=Response` |
| **G3 — Unbounded Pagination Scan** | `rg -n "limit:\s*int\s*=\s*(Query\(\s*\)|[0-9]+)" app/ src/ -g "*router*.py" -g "*routes*.py"` | `0` matches without `le=` upper bound | Add `Query(default=20, ge=1, le=100)` (`CT6`) |
| **G4 — Input `extra="forbid"` Check** | `rg -n "class .*Request\(BaseModel\)" -A 4 app/ src/ -g "*.py"` | Every `*Request` input DTO sets `extra="forbid"` (or inherits a `StrictRequestModel` base) | Add `model_config = ConfigDict(extra="forbid")` (`CT2`) |
| **G5 — Compatibility Diff Check** | `oasdiff breaking contracts/openapi.base.json contracts/openapi.json` (or `jq -S` diff) | Zero unapproved breaking changes | Revert breaking edit or document approved `D-NN` in `design.md` (`CT7`) |
| **G6 — Contract Test Suite** | `uv run pytest -q -k "contract or openapi"` | Exit `0` | Fix failing schema/contract tests |

---

## 5. Code Review Severity Rubric (`BLOCKER` / `MAJOR` / `MINOR`)

Reviewer findings use the unified 3-tier scale from `shared_contracts/flags_and_statuses.md` (never use `P0`–`P3`):

| Severity | Contract Finding Criteria |
|---|---|
| **`BLOCKER`** | • Unapproved breaking change (`CT7`) without `D-NN` in `design.md`.<br>• `contracts/openapi.json` is stale or uncommitted after route/DTO edits (`CT1`).<br>• Missing authentication/scope dependency (`Security(...)` / `Depends(...)`) or IDOR tenant leak where `tenant_id` is read from request body or omitted from SQL `WHERE` (`CT5`).<br>• SQLAlchemy ORM model, internal domain entity, or sensitive field exposed directly as `response_model` (`CT2`).<br>• `api_contract.json` out of sync with `contracts/openapi.json` on shared client endpoints (`CT9`). |
| **`MAJOR`** | • Route or exception handler returns ad-hoc `{"detail": "..."}` instead of `ErrorResponse` (`CT3`).<br>• Collection endpoint lacks `le=` upper bound on `limit` or lacks a unique tie-breaker column in `ORDER BY` (`CT6`).<br>• Non-idempotent state-changing `POST` endpoint lacks `Idempotency-Key` deduplication (`CT10`).<br>• Input `*Request` DTO omits `extra="forbid"` or bounds on string/list fields (`CT2`).<br>• Route omits explicit `status_code=`, `response_model=`, or `responses=` error declarations (`CT4`). |
| **`MINOR`** | • Missing or non-standard `operation_id` / `tags` (`CT9`).<br>• Missing OpenAPI field `description` or `examples` on public DTO properties.<br>• Deprecated field/endpoint (`deprecated=True`) missing `Sunset` header metadata (`CT8`). |

See [`references/01-conventions-schemas-and-idempotency.md`](01-conventions-schemas-and-idempotency.md) for DTO/pagination/idempotency implementations and [`references/02-compatibility-and-versioning.md`](02-compatibility-and-versioning.md) for auth scopes and compatibility policy.
