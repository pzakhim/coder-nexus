# app/models/{{resources}}.py - ORM table for {{Resource}}.
#
# Rules:
# - SQLAlchemy 2 typed mapping (Mapped[...], mapped_column); never imports schemas, Pydantic or FastAPI.
# - Relationships use lazy="raise"; repositories load them explicitly with selectinload().
# - Ownership / data-scope columns (owner, tenant, environment) are NOT NULL when the design says so.
# - Add the module to app/models/__init__.py; the table is created only by an Alembic revision.
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import {{Resource}}Status

if TYPE_CHECKING:  # avoids an import cycle between table modules
    from app.models.customers import Customer


class {{Resource}}(Base):
    __tablename__ = "{{resources}}"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    status: Mapped[{{Resource}}Status]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    customer: Mapped["Customer"] = relationship(lazy="raise")
