# app/schemas/{{resources}}.py - API contract for {{Resource}} (field names and types equal design.md).
#
# Rules:
# - Pydantic v2 only; never imports ORM classes (enums from app.models.enums are allowed).
# - No `...` defaults and no RootModel; constraints with Field(...).
# - Response schemas list exactly the exposed fields; from_attributes lets services map ORM objects.
# - Client-supplied input never carries ownership/scope fields the server derives (owner, tenant).
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import {{Resource}}Status


class {{Resource}}Create(BaseModel):
    model_config = ConfigDict(extra="forbid")

    note: str | None = Field(default=None, max_length=500)


class {{Resource}}Read(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: {{Resource}}Status
    created_at: datetime


class {{Resource}}Page(BaseModel):
    items: list[{{Resource}}Read]
    total: int
    limit: int
    offset: int
