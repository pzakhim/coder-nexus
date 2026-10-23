# app/api/routers/{{resources}}.py - HTTP edge for {{Resource}}.
#
# Rules:
# - Router-level prefix/tags/dependencies; one function per HTTP method; Annotated parameters.
# - Each handler: validated input -> one service method -> return its schema (return type declared).
# - No select(), commit(), permission logic or try/except remapping here (error_handlers maps errors).
# - async def: the service awaits the database.
from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from app.api.deps import CurrentUserDep, {{Resource}}ServiceDep
from app.schemas.{{resources}} import {{Resource}}Create, {{Resource}}Page, {{Resource}}Read

router = APIRouter(prefix="/{{resources}}", tags=["{{resources}}"])


@router.get("")
async def list_{{resources}}(
    service: {{Resource}}ServiceDep,
    actor: CurrentUserDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> {{Resource}}Page:
    return await service.list_{{resources}}(actor, limit=limit, offset=offset)


@router.get("/{{{resource}}_id}")
async def get_{{resource}}(
    {{resource}}_id: Annotated[int, Path(ge=1)], service: {{Resource}}ServiceDep, actor: CurrentUserDep
) -> {{Resource}}Read:
    return await service.get_{{resource}}({{resource}}_id, actor)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_{{resource}}(
    body: {{Resource}}Create, service: {{Resource}}ServiceDep, actor: CurrentUserDep
) -> {{Resource}}Read:
    return await service.create_{{resource}}(body, actor)
