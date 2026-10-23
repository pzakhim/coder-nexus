# app/repositories/{{resources}}.py - queries for the {{Resource}} aggregate.
#
# Rules:
# - SQLAlchemy 2 select() style; bound parameters only, never string-built SQL.
# - flush() to get ids and surface constraint errors; never commit, rollback or close.
# - Catch only to translate (IntegrityError -> ConflictError); returns ORM objects to the service.
# - Every query that reads scoped data filters by the scope column it receives.
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError
from app.models.{{resources}} import {{Resource}}


class {{Resource}}Repository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_for_customer(self, {{resource}}_id: int, customer_id: int) -> {{Resource}} | None:
        statement = select({{Resource}}).where(
            {{Resource}}.id == {{resource}}_id, {{Resource}}.customer_id == customer_id
        )
        return await self.session.scalar(statement)

    async def list_for_customer(self, customer_id: int, limit: int, offset: int) -> Sequence[{{Resource}}]:
        statement = (
            select({{Resource}})
            .where({{Resource}}.customer_id == customer_id)
            .order_by({{Resource}}.id)
            .limit(limit)
            .offset(offset)
        )
        return (await self.session.scalars(statement)).all()

    async def add(self, {{resource}}: {{Resource}}) -> {{Resource}}:
        self.session.add({{resource}})
        try:
            async with self.session.begin_nested():
                await self.session.flush()
        except IntegrityError as exc:
            raise ConflictError("{{resource}}_conflict") from exc
        return {{resource}}
