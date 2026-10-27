# 02 — Test Doubles, Fixtures & Assertion Quality (Backend / FastAPI)

Rules **U1**, **U4**, **U5**, **U6**, **U7**, **U8**, **U9**, and **U11**.

---

## 1. Doubles Hierarchy: `Real > Fake > Stub > Mock` (`U4`, `U5`, `U6`)

Move down the hierarchy only when the real dependency performs I/O, is non-deterministic, or has external side effects:

| Dependency | What to Use in `tests/unit/` | Forbidden (`BLOCKER` / `MAJOR`) |
|---|---|---|
| **Subject under test & pure domain collaborators (`Entity`, `ValueObject`, policy, mapper)** | **Real** implementation | Mocking or patching the class/function under test (`U5`) |
| **Application-owned `Protocol` ports (`Repository`, `UnitOfWork`, `Gateway`)** | **Hand-written Fake** implementing the `Protocol`, storing rows in a `dict`, raising the exact domain errors | Unspecced `MagicMock()` returning arbitrary attributes |
| **Outbound HTTP calls (`httpx.AsyncClient`)** | `httpx.MockTransport(handler)` — one explicit handler per scenario; unexpected URL raises `AssertionError` | Live network requests (`U4`) or monkeypatching `httpx` internals |
| **External third-party SDKs without transport hooks** | `unittest.mock.create_autospec(SdkClient, instance=True)` at the adapter boundary | Unspecced `Mock()` without `spec_set` / `create_autospec` |
| **Clock, UUIDs, randomness** | Injected `clock: Callable[[], datetime]` returning aware UTC `FIXED_NOW`; injected `id_factory`; `random.Random(seed)` | `datetime.now()` inside tested code, `time.sleep()` in tests (`U7`) |
| **Authorization, ownership & tenant-scope checks** | **Real** policy/guard code | Mocking a permission/tenant check to always allow (`U6`) |
| **Database (`AsyncSession`, SQL queries)** | Not in unit tests — services use `FakeRepository`; SQL queries belong in `tests/integration/` (`{{slot:verification}}`) | Mocking `AsyncSession.execute` in unit tests (`U6`) |

---

## 2. Reference Unit Test Patterns

### Pattern A — Hand-Written Port Fakes & Service Unit Test (`tests/fakes.py` & `tests/unit/application/test_orders.py`)

```python
# tests/fakes.py — satisfies OrderRepository Protocol & UnitOfWork Protocol
from uuid import UUID
from app.domain.orders import DuplicateOrderError, Order, OrderNotFoundError


class FakeOrderRepository:
    def __init__(self, initial: list[Order] | None = None) -> None:
        self._rows: dict[UUID, Order] = {o.id: o for o in (initial or [])}

    async def get_by_id(self, tenant_id: UUID, order_id: UUID) -> Order:
        order = self._rows.get(order_id)
        if order is None or order.tenant_id != tenant_id:
            raise OrderNotFoundError(order_id)
        return order

    async def save(self, order: Order) -> None:
        if order.id in self._rows and self._rows[order.id].version != order.version:
            raise DuplicateOrderError(order.id)
        self._rows[order.id] = order


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.committed: bool = False

    async def commit(self) -> None:
        self.committed = True
```

```python
# tests/unit/application/test_orders.py — Pass + Refusal + Cross-Tenant Isolation
import pytest
from app.application.orders import OrderService
from app.domain.orders import OrderNotCancellableError, OrderNotFoundError, OrderStatus
from tests.factories import FIXED_NOW, ORDER_1, TENANT_A, TENANT_B, make_actor, make_order
from tests.fakes import FakeOrderRepository, FakeUnitOfWork


async def test_cancel_order_when_pending_marks_cancelled_and_commits() -> None:
    # Arrange
    repo = FakeOrderRepository([make_order(id=ORDER_1, tenant_id=TENANT_A, status=OrderStatus.PENDING)])
    uow = FakeUnitOfWork()
    service = OrderService(repo=repo, uow=uow, clock=lambda: FIXED_NOW)

    # Act
    result = await service.cancel(order_id=ORDER_1, actor=make_actor(tenant_id=TENANT_A))

    # Assert
    assert result.status is OrderStatus.CANCELLED
    assert result.cancelled_at == FIXED_NOW
    assert uow.committed is True


async def test_cancel_order_when_already_shipped_raises_and_does_not_commit() -> None:
    # Arrange
    repo = FakeOrderRepository([make_order(id=ORDER_1, tenant_id=TENANT_A, status=OrderStatus.SHIPPED)])
    uow = FakeUnitOfWork()
    service = OrderService(repo=repo, uow=uow, clock=lambda: FIXED_NOW)

    # Act & Assert
    with pytest.raises(OrderNotCancellableError):
        await service.cancel(order_id=ORDER_1, actor=make_actor(tenant_id=TENANT_A))

    assert (await repo.get_by_id(TENANT_A, ORDER_1)).status is OrderStatus.SHIPPED
    assert uow.committed is False


async def test_cancel_order_when_other_tenant_raises_not_found() -> None:
    repo = FakeOrderRepository([make_order(id=ORDER_1, tenant_id=TENANT_A, status=OrderStatus.PENDING)])
    uow = FakeUnitOfWork()
    service = OrderService(repo=repo, uow=uow, clock=lambda: FIXED_NOW)

    with pytest.raises(OrderNotFoundError):
        await service.cancel(order_id=ORDER_1, actor=make_actor(tenant_id=TENANT_B))

    assert uow.committed is False
```

### Pattern B — FastAPI Router Unit Test via `ASGITransport` & `dependency_overrides`

Always use `httpx.AsyncClient(transport=ASGITransport(app=app))` in `async def` tests (never sync `TestClient` inside `async def`), keep authorization real, and clear `app.dependency_overrides` in a `finally` block:

```python
# tests/unit/api/routes/test_orders.py
from collections.abc import AsyncIterator
import httpx
import pytest
from httpx import ASGITransport
from app.api.deps import get_current_actor, get_order_service
from app.main import app
from tests.factories import ORDER_1, TENANT_A, make_actor, make_order
from tests.fakes import FakeOrderRepository, FakeUnitOfWork


@pytest.fixture
async def api_client() -> AsyncIterator[httpx.AsyncClient]:
    repo = FakeOrderRepository([make_order(id=ORDER_1, tenant_id=TENANT_A)])
    service = OrderService(repo=repo, uow=FakeUnitOfWork())
    app.dependency_overrides[get_order_service] = lambda: service
    app.dependency_overrides[get_current_actor] = lambda: make_actor(tenant_id=TENANT_A)
    try:
        async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.clear()


async def test_get_order_when_unauthenticated_returns_401() -> None:
    app.dependency_overrides.clear()
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/api/v1/orders/{ORDER_1}")
    assert response.status_code == 401
```

### Pattern C — Outbound HTTP Adapter Test via `httpx.MockTransport`

```python
# tests/unit/infrastructure/clients/test_erp.py
import httpx
import pytest
from app.infrastructure.clients.erp import ErpClient, ErpUpstreamError


async def test_fetch_stock_when_erp_returns_503_raises_erp_upstream_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET" and request.url.path == "/v1/stock/SKU-1":
            return httpx.Response(503, json={"detail": "maintenance"})
        raise AssertionError(f"Unexpected call: {request.method} {request.url}")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://erp.test") as http:
        client = ErpClient(http=http)
        with pytest.raises(ErpUpstreamError):
            await client.fetch_stock("SKU-1")
```

---

## 3. Right-Reason Red Failure, Independent Expectations & Mutation Check (`U7`, `U8`, `U14`)

| Red Run Output | Meaning | Action |
|---|---|---|
| `AssertionError` or `DID NOT RAISE <DomainError>` | **Right reason** | Write the minimal production code to make it pass |
| Test passes immediately | Behavior already exists or test is tautological | Fix the test so it fails when the target behavior is broken |
| `ImportError`, `NameError`, `AttributeError`, fixture error | **Not red yet** (broken test setup) | Fix the signature/import and re-run until the assertion fails |
| `0 items collected`, `skipped`, deselected (exit code 5) | **Not run (`NOT_RUN`)** | Fix the filter/path; never record as red or green |

- **Independent Literal Expectations (`U8`):** Assert expected values using concrete literals from `design.md` (`Decimal("15.00")`), never by copying the production calculation (`expected = sum(...)`) into the test.
- **Specific Exception Assertions (`U8`):** Use `with pytest.raises(SpecificDomainError)` around a single statement — never `pytest.raises(Exception)` (`ruff` `PT011`, `PT012`, `B017`). For Pydantic `ValidationError`, assert `exc.value.errors()[0]["loc"]` and `["type"]`, not prose messages.
- **Pre-Handoff Mental Mutation Check:** Verify at least one test fails if you: (1) flip a branch or refusal condition, (2) skip `uow.commit()` or commit on error, (3) remove a tenant/owner filter, or (4) return `[]` / `None`.
