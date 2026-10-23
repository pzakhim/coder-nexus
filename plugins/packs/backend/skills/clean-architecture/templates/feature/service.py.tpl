# app/services/{{resources}}.py - use cases for {{Resource}}.
#
# Rules:
# - Never imports FastAPI/Starlette; raises errors from app.core.errors.
# - The method the router calls owns the transaction: all writes, then one commit at the end.
# - Authorization and data scope are checked here, from the actor, never from client input.
# - Returns response schemas; ORM objects do not leave the service.
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.core.security import CurrentUser  # the workspace's authenticated-actor type
from app.models.enums import {{Resource}}Status
from app.models.{{resources}} import {{Resource}}
from app.repositories.{{resources}} import {{Resource}}Repository
from app.schemas.{{resources}} import {{Resource}}Create, {{Resource}}Page, {{Resource}}Read


class {{Resource}}Service:
    def __init__(self, session: AsyncSession, repository: {{Resource}}Repository | None = None) -> None:
        self.session = session
        self.{{resources}} = repository or {{Resource}}Repository(session)

    async def get_{{resource}}(self, {{resource}}_id: int, actor: CurrentUser) -> {{Resource}}Read:
        {{resource}} = await self.{{resources}}.get_for_customer({{resource}}_id, actor.customer_id)
        if {{resource}} is None:
            # Same error for "missing" and "belongs to someone else": no existence leak.
            raise NotFoundError("{{resource}}_not_found")
        return {{Resource}}Read.model_validate({{resource}})

    async def list_{{resources}}(self, actor: CurrentUser, limit: int, offset: int) -> {{Resource}}Page:
        rows = await self.{{resources}}.list_for_customer(actor.customer_id, limit, offset)
        return {{Resource}}Page(
            items=[{{Resource}}Read.model_validate(row) for row in rows],
            total=len(rows),
            limit=limit,
            offset=offset,
        )

    async def create_{{resource}}(self, data: {{Resource}}Create, actor: CurrentUser) -> {{Resource}}Read:
        {{resource}} = await self.{{resources}}.add(
            {{Resource}}(customer_id=actor.customer_id, status={{Resource}}Status.DRAFT, note=data.note)
        )
        await self.session.commit()
        return {{Resource}}Read.model_validate({{resource}})
