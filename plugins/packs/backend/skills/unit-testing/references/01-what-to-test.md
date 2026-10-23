# 01 — What to test

Detail for [unit-testing](../SKILL.md). Rules U2, U3. Layer names follow `{{slot:clean-architecture}}`; the example paths (`app/domain/`, `app/application/`, `app/infrastructure/`, `app/api/`) are conventions the workspace may override with its real folders.

## Where cases come from

- Each changed behavior gets its **Pass/Default**, every **Fail** it handles and **Empty** where a collection or optional value exists, taken from the test-data table or verified API specification in `design.md`. Reason: cases invented while coding test what the code does, not what was agreed.
- A case listed below that the design does not need is not required; a design row not listed below still is.
- Test at the seams the design names (public use case / service method, schema, mapper, router, port). A test that needs a seam the design does not have is `NEEDS_CONTEXT` or `change-control`, not a new test-only hook in production code.
- Use the terms of the `codebase-notes.md` Glossary in test names, so a failure reads as a rule.

## Per-layer matrix (unit level: no database, no network)

| Layer / subject | Example path | Double | Required cases |
|---|---|---|---|
| Domain entity / value object / pure rule | `app/domain/` | none | Valid construction; each invariant violation raises the named domain error; boundary values (0, 1, max, empty string); each allowed and refused state transition |
| Use case / application service | `app/application/` (or `app/services/`) | Fakes of its ports: repository, unit of work, gateways, clock | Pass/Default returns the expected DTO and the fake holds the row; each refusal rule raises its domain error and leaves state unchanged; not found raises the agreed error (not `None` passed upward); actor B on actor A's object raises `Forbidden` / list for B shows only B's rows (real policy code); fake unit of work committed on success, **not** committed after an error; dependency failure mapped to the agreed domain error, nothing persisted |
| Pydantic schema (request / response) | `app/api/schemas/` (or `app/schemas/`) | none | Required field missing → `ValidationError` with the exact `loc`; bounds and formats the contract sets; extra fields refused where the model uses `extra="forbid"` (mass-assignment guard: `owner_id`, `role`, `status`); unknown enum value refused; `model_dump(mode="json", by_alias=True)` keys equal the contract keys; `None` handling as the contract says |
| Mapper (ORM row ↔ entity ↔ DTO) | `app/infrastructure/mappers/` | none (build the ORM object in memory, no session) | Full mapping of every field; optional / `None` fields; empty collections; unknown enum value; `Decimal` and aware-UTC `datetime` preserved |
| Router / endpoint (HTTP mapping only) | `app/api/` | Service doubled through `app.dependency_overrides`; authentication overridden, authorization real | Pass/Default status and body fields per contract; invalid body → 422 (FastAPI default) or the contract's 400 with the error shape of `api-contract-design`; each domain error reaches the global handler and maps to its status (404, 409, 403) without local remapping; empty list → 200 with `[]` or `items: []`, not 404; one test per protected route **without** the auth override expects 401 |
| Outbound adapter (HTTP client, LLM, ERP, payment) | `app/infrastructure/clients/` | `httpx.MockTransport`, one handler per scenario | 2xx parsed into the port's result type; each mapped 4xx/5xx → the port's error; `httpx.TimeoutException` → the port's timeout error; malformed JSON → the port's error, never a default object; request method, path and body the contract requires |

Never assert only `status_code == 200`. Reason: a handler returning the wrong object still returns 200.

Do not test Pydantic, FastAPI or SQLAlchemy themselves (that `int` parses `"3"`, that a route exists). Test the rules your code adds. Reason: those are change detectors of the library, not guards of your behavior.

## Minimum per changed behavior

- **Pass/Default** — the expected result, asserted field by field from the design literal.
- **Each handled Fail** — validation, not found, forbidden (real policy), conflict / business refusal, dependency failure: the exact domain error type, and that nothing was persisted or committed.
- **Empty / edges** — empty list, `None` / missing optional, zero, maximum (page size cap), malformed input, timezone-naive datetime where aware is required.

```python
# Shape - tests/unit/application/test_orders.py
async def test_cancel_order_when_already_shipped_raises_order_not_cancellable() -> None:
    repo = FakeOrderRepository([make_order(id=ORDER_1, status=OrderStatus.SHIPPED)])
    uow = FakeUnitOfWork()
    service = OrderService(repo=repo, uow=uow, clock=lambda: FIXED_NOW)

    with pytest.raises(OrderNotCancellable):
        await service.cancel(ORDER_1, actor=OWNER_A)

    assert (await repo.get(ORDER_1)).status is OrderStatus.SHIPPED
    assert uow.committed is False
```

## Bug fixes and review findings

1. Write the test that reproduces the faulty behavior, named after the behavior (`test_total_when_discount_exceeds_price_is_zero`), not the ticket number.
2. Run it red on the unfixed code and record the failure line (U3). Reason: the red run proves the defect was real.
3. Fix through `{{slot:root-cause-debugging}}`, run green, then the full unit suite.

If the defect lives only in SQL, a migration or a real transaction, the reproduction is an integration test (`{{slot:verification}}`); say so in the evidence instead of faking the database.

## Not unit-tested here

| Concern | Goes to |
|---|---|
| Repository queries, owner / tenant filters in SQL, constraints, `ON CONFLICT`, eager loading | Integration on real PostgreSQL — `{{slot:verification}}` |
| Alembic migrations, transaction isolation, locks | `{{slot:verification}}` |
| API authorization matrix (role × object × environment), contract compliance of live responses | `{{slot:verification}}`, `quality-acceptance` |

Full list and owners: [06 test boundaries](06-test-boundaries.md).
