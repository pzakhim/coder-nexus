# app/main.py - application assembly only.
#
# Rules:
# - create_app() reads no settings and opens no connection; lifespan does, at server start.
# - Every router is included here, imported as its module (each module defines `router`).
# - No @app.on_event: with lifespan= set, startup/shutdown events are never called.
# - pyproject.toml: [tool.fastapi] entrypoint = "app.main:app" (when the workspace has no other launcher).
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.error_handlers import register_error_handlers
from app.api.routers import {{resources}}
from app.core.settings import get_settings
from app.db.session import build_engine, build_session_factory


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = build_engine(get_settings())
    app.state.session_factory = build_session_factory(engine)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router({{resources}}.router)
    register_error_handlers(app)
    return app


app = create_app()
