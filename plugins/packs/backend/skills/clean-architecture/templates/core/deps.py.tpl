# app/api/deps.py - shared Annotated dependencies and service builders.
#
# Rules:
# - Function dependencies build services; services never import FastAPI.
# - FastAPI caches dependencies per request, so every service in one request shares
#   the same session: one unit of work, committed by the service method the router calls.
# - Tests replace a dependency with app.dependency_overrides, never by patching internals.
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.api.auth import get_current_user  # the workspace's auth dependency (FastAPI side)
from app.core.security import CurrentUser  # framework-free actor type
from app.core.settings import Settings, get_settings
from app.db.session import get_session, get_session_factory
from app.services.{{resources}} import {{Resource}}Service

SessionDep = Annotated[AsyncSession, Depends(get_session)]
SessionFactoryDep = Annotated[async_sessionmaker[AsyncSession], Depends(get_session_factory)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]


def get_{{resource}}_service(session: SessionDep) -> {{Resource}}Service:
    return {{Resource}}Service(session)


{{Resource}}ServiceDep = Annotated[{{Resource}}Service, Depends(get_{{resource}}_service)]
