# tests/unit/application/test_<feature>.py - service rules with fake ports; no database, no network.
# Shape only. Data comes from the Pass/Default, Fail and Empty rows of design.md; expected values are literals.
from datetime import UTC, datetime

import pytest

from app.application.<feature> import <Feature>Service
from app.domain.errors import <RefusalError>, Forbidden, NotFound
from tests.factories import make_<entity>
from tests.fakes import Fake<Feature>Repository, FakeUnitOfWork

FIXED_NOW = datetime(2026, 1, 15, 10, 0, tzinfo=UTC)


def _service(*rows):
    repo = Fake<Feature>Repository(list(rows))
    uow = FakeUnitOfWork()
    return <Feature>Service(repo=repo, uow=uow, clock=lambda: FIXED_NOW), repo, uow


async def test_<action>_with_default_data_returns_<result>() -> None:          # Pass/Default
    service, repo, uow = _service()

    result = await service.<action>(<pass_default_input>, actor=OWNER_A)

    assert result.<field> == <literal_from_design>
    assert uow.committed is True


async def test_<action>_when_<rule_broken>_raises_<refusal_error>() -> None:   # Fail
    service, repo, uow = _service(make_<entity>(<state_that_breaks_rule>))

    with pytest.raises(<RefusalError>):
        await service.<action>(<id>, actor=OWNER_A)

    assert uow.committed is False


async def test_<action>_when_missing_raises_not_found() -> None:               # Fail
    service, _, uow = _service()

    with pytest.raises(NotFound):
        await service.<action>(<unknown_id>, actor=OWNER_A)

    assert uow.committed is False


async def test_<action>_on_other_owner_raises_forbidden() -> None:              # authorization (real policy)
    service, _, uow = _service(make_<entity>(owner_id=OWNER_A))

    with pytest.raises(Forbidden):
        await service.<action>(<id>, actor=OWNER_B)

    assert uow.committed is False


async def test_list_<entities>_when_none_returns_empty_list() -> None:          # Empty
    service, _, _ = _service()

    assert await service.list_<entities>(actor=OWNER_A) == []
