# tests/unit/conftest.py - unit fixtures: fake service through dependency_overrides, no database, no network.
# Shape only: adapt module paths and dependency names to the workspace; keep the override reset.
from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.api.dependencies import get_current_user, get_order_service  # the exact functions the routes use
from tests.fakes import FakeOrderRepository, FakeUnitOfWork
from app.application.orders import OrderService

FIXED_NOW = ...  # datetime(2026, 1, 15, 10, 0, tzinfo=UTC)


@pytest.fixture
def order_repo() -> FakeOrderRepository:
    return FakeOrderRepository()


@pytest.fixture
def order_service(order_repo: FakeOrderRepository) -> OrderService:
    # Real service (real authorization policy) over fake ports.
    return OrderService(repo=order_repo, uow=FakeUnitOfWork(), clock=lambda: FIXED_NOW)


@pytest.fixture
async def client(order_service: OrderService) -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_order_service] = lambda: order_service
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def as_user():
    # Overrides authentication only; authorization stays in the real service.
    def _login(user) -> None:
        app.dependency_overrides[get_current_user] = lambda: user
    return _login
