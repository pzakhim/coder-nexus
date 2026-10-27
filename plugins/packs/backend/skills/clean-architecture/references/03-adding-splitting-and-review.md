# 03 — Adding Features, Splitting Files, and Architecture Review Rubric

Step-by-step workflow for adding a new vertical slice, splitting oversized modules in coordination with `{{slot:clean-code}}`, and grading architectural findings.

---

## 1. Step-by-Step Feature / Endpoint Addition

Each step below is an incremental task in the approved phase (`incremental-implementation`). Skip steps the behavior does not require (**A10**—e.g., a new endpoint on an existing table skips Steps 1–2):

| # | Step | Target Files | Deterministic Task Check (`PASS` / `FAIL`) |
|---|---|---|---|
| **1** | **ORM Model** | `app/models/<resource>.py`, `app/models/__init__.py` | `uv run mypy app/models` |
| **2** | **Migration** | `alembic/versions/<rev>_<slug>.py` (`backend-database-migrations`) | `uv run alembic upgrade head && uv run alembic downgrade -1 && uv run alembic upgrade head` |
| **3** | **Repository** | `app/repositories/<resource>.py`, `tests/repositories/test_<resource>.py` | `uv run pytest tests/repositories/test_<resource>.py -q` |
| **4** | **Schemas** | `app/schemas/<resource>.py` | `uv run mypy app/schemas` |
| **5** | **Service** | `app/services/<resource>.py`, `tests/services/test_<resource>.py` | `uv run pytest tests/services/test_<resource>.py -q` |
| **6** | **Router & DI** | `app/api/routers/<resource>.py`, `app/api/deps.py`, `app/main.py` | `uv run pytest tests/api/routers/test_<resource>.py -q` |
| **7** | **Error Mapping** *(if new error class)* | `app/core/errors.py`, `app/api/error_handlers.py` | Failing-case router test + `uv run lint-imports` |

---

## 2. Splitting Oversized Files (`{{slot:clean-code}}` C6 Coordination)

Line and complexity thresholds are owned by `{{slot:clean-code}}` (`01-structure-naming-and-types.md`: functions ≤ 30 lines, files ≤ 300 lines). When a file exceeds its threshold or accumulates multiple reasons to change, split inside the task modifying that file:

| Oversized File | Split Target | Placement & Call-Site Rule |
|---|---|---|
| `app/api/routers/orders.py` | Sub-resource router `app/api/routers/order_lines.py` (`prefix="/orders/{order_id}/lines"`) | One router per URL prefix; include each in `app/main.py` |
| `app/services/orders.py` | Package `app/services/orders/` with cohesive use-case modules (`placement.py`, `cancellation.py`) and an **empty** `__init__.py` | Callers import from the defining module; `app/api/deps.py` provides one dependency builder per service class |
| `app/repositories/orders.py` | Per aggregate (`order_lines.py`), or read-heavy report queries into `app/repositories/order_reports.py` | Writes remain in the owning aggregate's repository |
| `app/schemas/orders.py` | Package `app/schemas/orders/` (`requests.py`, `responses.py`) | Schema class names remain unchanged so the public API contract does not change |
| `app/models/orders.py` | One module per ORM table | Register the new module in `app/models/__init__.py` |

- **No pass-through shims**: Update all callers in the same task and delete the old location (`{{slot:clean-code}}` C1, C16, C17).

---

## 3. Feature-First Workspaces

If the workspace's verified tree is `app/modules/<feature>/{router,schemas,service,repository,models}.py`:
- The layer ownership table in [01 — Layout & Layer Roles](01-layout-and-layer-roles.md) and the dependency matrix in [02 — Dependencies, DI & Transactions](02-dependencies-di-and-transactions.md) apply file-for-file inside each feature folder.
- Cross-feature communication goes exclusively through the other feature's service (**A8**).
- Configure `import-linter` with `containers = ["app.modules.<feature>", ...]`.

---

## 4. Unified Architecture Review Severity (`BLOCKER` / `MAJOR` / `MINOR`)

All architectural review findings use the unified scale from `shared_contracts/flags_and_statuses.md` §2:

| Severity | Backend Architectural Criteria | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | • Failed `uv run lint-imports`, `mypy`, or import-purity check (`FAIL`)<br>• Router importing `repositories`/`models` or calling `session.commit()` (**A2, A3**)<br>• Returning ORM models directly without Pydantic schema mapping (**A1**)<br>• Repository calling `commit()`/`rollback()` or service opening its own session (**A3, A4, A5**)<br>• `services`/`repositories`/`core` importing `fastapi`/`starlette` (**A6**)<br>• Reading `.env` or connecting to DB/HTTP at module import time (**A7**) | `CHANGES_REQUESTED` (blocks approval) |
| `MAJOR` | • Missing `lazy="raise"` or implicit lazy load hazard (**A9**)<br>• Single-implementation `Protocol` or speculative empty layer (**A10**)<br>• Unsplit >300-line module modified in task scope | Must be fixed in the same revision when inside task scope |
| `MINOR` | • Minor file or dependency alias naming polish within the right layer | Optional (never blocks approval) |
