# 01 — Per-Layer Test Matrix, Directory Tree & Naming (Backend / FastAPI)

Rules **U2**, **U3**, **U9**, **U10**, **U11**, and **U14**.

> **Workspace Convention Rule (`C11` / `U11` — `EXTEND` vs `INIT`):**
> - **Existing project (`EXTEND`):** Inspect `pyproject.toml` (`[tool.pytest.ini_options]`), `conftest.py`, existing `tests/` folders, shared fakes, and test naming conventions before writing any test. The workspace's established layout, runner (`uv run` / `poetry run`), and `asyncio_mode` (`auto` vs `strict`) always win. Record any legacy drift in `Concerns` without renaming files outside task scope.
> - **Greenfield project (`INIT`):** Use the default `tests/unit/` mirrored tree, `pytest` + `pytest-asyncio` (`asyncio_mode = "auto"`), and `test_<behavior>_<condition>` naming below.

---

## 1. Per-Layer Unit Test Matrix (No Database, No Live Network)

Every changed behavior must cover **Pass/Default**, **every handled Fail**, and **Empty / Edge** cases derived from the test-data rows and API specifications in `design.md`:

| Layer / Subject | Example Source Path | Boundary Doubled | Required Cases (Pass / Fail / Empty & Edge) |
|---|---|---|---|
| **Domain Entity / Value Object / Pure Policy** | `app/domain/orders.py` | **None** (100% pure Python) | Valid construction; each invariant violation raises the exact domain error; boundary values (`0`, `1`, max cap, empty string); each allowed and refused state transition |
| **Application Service / Use Case** | `app/application/orders.py` (or `app/services/orders.py`) | **Hand-written Fakes** of `Protocol` ports (`Repository`, `UnitOfWork`, `Gateway`, `clock`) | **Pass/Default** returns expected DTO and persists to fake repo with `uow.committed is True`; **Fail** (not found, conflict, validation, upstream error) raises exact domain error with `uow.committed is False` and state unchanged; **Authz/Scope** (actor B on actor A's resource) raises `ForbiddenError` / filters to actor B's tenant rows using **real** policy code |
| **Pydantic Schema (Request / Response)** | `app/api/schemas/orders.py` | **None** | Valid payload parses cleanly; missing required field or out-of-bounds value raises `ValidationError` (assert `errors()[0]["loc"]` and `["type"]`); unknown enum refused; extra fields (`role`, `tenant_id`, `status`) rejected when `extra="forbid"` (mass-assignment guard); `model_dump(mode="json", by_alias=True)` matches contract keys |
| **Data Mapper (`ORM ↔ Entity ↔ DTO`)** | `app/infrastructure/mappers/orders.py` | **None** (in-memory model instances, no `AsyncSession`) | Full field-by-field mapping; `None` optional fields; empty lists `[]`; `Decimal` precision and timezone-aware UTC `datetime` preserved |
| **FastAPI Router / Endpoint (HTTP Mapping)** | `app/api/routes/orders.py` | **Service doubled** via `app.dependency_overrides`; `get_current_actor` overridden for authn, **authorization real** | **Pass/Default** HTTP status code AND response JSON fields (never assert only `status_code == 200`); invalid payload → `422`/`400` error envelope; domain errors (`NotFoundError`, `ConflictError`, `ForbiddenError`) map to `404`/`409`/`403` via global exception handlers; empty list → `200` with `[]`; **1 test without auth override** → `401 Unauthorized` |
| **Outbound HTTP / SDK Adapter** | `app/infrastructure/clients/erp.py` | `httpx.MockTransport(handler)` (unknown URL raises `AssertionError`) | `2xx` parsed into port result type; mapped `4xx`/`5xx` → port domain error; `httpx.TimeoutException` → port timeout error; malformed JSON → port error (never silent fallback); request method, URL path, headers, and body verified |

Do not write change-detector tests for FastAPI, Pydantic, or SQLAlchemy internals (e.g., testing that `int` parses `"3"`). Test the business rules and boundary contracts your code adds.

---

## 2. Mirrored Test Directory Tree (`U10`)

One unit test file per source module, mirroring `app/` under `tests/unit/`. Database fixtures belong strictly in `tests/integration/conftest.py` so unit tests can never touch a database by accident:

```text
tests/
├── fakes.py                                 # Hand-written Protocol port fakes (FakeOrderRepository, FakeUnitOfWork)
├── factories.py                             # Deterministic data builders (make_order(**overrides))
├── unit/
│   ├── conftest.py                          # Unit-only fixtures (fixed UTC clock, ASGITransport client, override cleanup)
│   ├── domain/
│   │   └── test_orders.py                   # Mirrors app/domain/orders.py
│   ├── application/
│   │   └── test_orders.py                   # Mirrors app/application/orders.py
│   ├── api/
│   │   ├── schemas/
│   │   │   └── test_orders.py               # Mirrors app/api/schemas/orders.py
│   │   └── routes/
│   │       └── test_orders.py               # Mirrors app/api/routes/orders.py
│   └── infrastructure/
│       ├── mappers/
│       │   └── test_orders.py               # Mirrors app/infrastructure/mappers/orders.py
│       └── clients/
│           └── test_erp.py                  # Mirrors app/infrastructure/clients/erp.py
└── integration/                             # Owned by {{slot:verification}} (real PostgreSQL)
    └── conftest.py
```

---

## 3. Naming & Regression Rules (`U3`, `U9`)

- **File Naming:** `test_<module>.py` (default `pytest` discovery pattern).
- **Function Naming:** `test_<behavior>_<condition>_<expected_outcome>` using domain glossary terms:
  - `test_cancel_order_when_already_shipped_raises_order_not_cancellable`
  - `test_create_order_when_extra_tenant_id_supplied_raises_validation_error`
  - `test_list_orders_when_actor_is_other_tenant_returns_empty_list`
- **Parametrized Cases:** Always provide readable `ids=`:
  ```python
  @pytest.mark.parametrize("quantity", [0, -1, 10_001], ids=["zero", "negative", "above_max_cap"])
  def test_order_line_when_quantity_out_of_bounds_raises_invalid_quantity(quantity: int) -> None: ...
  ```
- **Constants:** Module-level `UPPER_SNAKE_CASE` named for their domain role (`TENANT_A`, `TENANT_B`, `ORDER_1`, `FIXED_NOW`), never `data1` or `test_user`.
- **Bug Fix & Review Finding Regression (`U3`):**
  1. Write a test named after the broken domain rule (never `test_bug_123`).
  2. Run it **red** on the unfixed code and record the failure row.
  3. Fix via `{{slot:root-cause-debugging}}`, run **green**, then run the module and unit suite.
