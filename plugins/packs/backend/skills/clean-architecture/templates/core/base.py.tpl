# app/models/base.py - declarative base shared by every table.
#
# Rules:
# - The naming convention gives every index and constraint a stable name, so Alembic
#   autogenerate and downgrades refer to the same names on every database.
# - eager_defaults fetches server-generated columns (created_at, ids) on flush via RETURNING,
#   so services can map objects after commit without an extra query.
from typing import Any, ClassVar

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    __mapper_args__: ClassVar[dict[str, Any]] = {"eager_defaults": True}
