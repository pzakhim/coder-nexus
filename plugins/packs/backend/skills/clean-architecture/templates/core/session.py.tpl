# app/db/session.py - engine, session factory and the per-request session.
#
# Rules:
# - Nothing here runs at import: lifespan calls build_engine/build_session_factory.
# - One AsyncSession per request; never module-level, never shared across concurrent tasks.
# - get_session never commits: the service method called by the router owns the commit.
# - Closing the session rolls back anything not committed; exceptions are never swallowed.
from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import Settings


def build_engine(settings: Settings) -> AsyncEngine:
    # One DATABASE_URI (postgresql://...) serves the app, Alembic and the Postgres MCP;
    # the async driver is chosen here.
    url = make_url(settings.database_uri.get_secret_value()).set(drivername="postgresql+asyncpg")
    return create_async_engine(url, pool_pre_ping=True, pool_size=10, max_overflow=5, pool_recycle=1800, pool_timeout=10)


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    # expire_on_commit=False: services map objects to schemas after commit without a reload.
    return async_sessionmaker(engine, expire_on_commit=False)


def get_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    return request.app.state.session_factory


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    async with session_factory() as session:
        yield session
