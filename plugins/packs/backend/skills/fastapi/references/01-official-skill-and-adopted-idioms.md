# Official Bundled FastAPI Skill Discovery and Adopted Idioms

> Topic: Discovering `fastapi/.agents/skills/fastapi/` inside the workspace's installed environment, fallback to pinned `0.161.1`, and adopted FastAPI rules (`F1`–`F6`).

Rules **F1**, **F2**, **F3**, **F4**, **F5**, and **F6**.

---

## 1. Locating the Bundled Official FastAPI Skill (`F1`, `O5`)

Always run inside the workspace's own Python environment, detected from its lockfile (`uv.lock` → `uv run`, `poetry.lock` → `poetry run`, `.venv/` → `.venv/bin/python`):

```bash
# Run from the backend root (where pyproject.toml lives)
uv run python -c "import fastapi; print(fastapi.__version__)"
uv run python -c "import pathlib, fastapi; p = pathlib.Path(fastapi.__file__).parent / '.agents/skills/fastapi'; print(p if p.is_dir() else 'ABSENT')"
```

- **When a directory path is printed**:
  - Read `<path>/SKILL.md` and only the `<path>/references/*.md` files relevant to the current task (`dependencies.md`, `path-operations.md`, `pydantic.md`, `responses.md`, `streaming.md`, `other-tools.md`).
  - Record the installed FastAPI version and bundled skill path in `codebase-notes.md` (`## 3. Verified Baseline Facts`).
- **When `ABSENT` is printed** (older FastAPI version prior to bundled `.agents/skills/fastapi`):
  - Apply the adopted rules in §2 below (aligned with FastAPI `0.161.1`) and record `"bundled fastapi skill ABSENT; installed fastapi is X.Y.Z"` in `codebase-notes.md`.
  - Before using newer APIs (such as `fastapi.sse` or `Depends(..., scope=...)`), probe their existence in the installed version (`uv run python -c "import fastapi.sse"`).
- **When `import fastapi` fails**:
  - Treat as an environment setup blocker (`{{slot:root-cause-debugging}}`), never guess the installed version.

---

## 2. Adopted Official Rules in Our Layered Architecture (`F2`–`F6`)

Follow these official FastAPI conventions, shaped to fit `{{slot:clean-architecture}}`:

| Rule | Adopted FastAPI Pattern | Implementation in This Pack |
|---|---|---|
| **F2: `Annotated` Dependency Aliases** | Declare dependencies with `Annotated[Type, Depends(fn)]` using function dependencies (not class dependencies) | Define reusable aliases (`SessionDep`, `CurrentUserDep`, `OrderServiceDep`) in `app/api/deps.py`. Never define FastAPI dependencies inside `app/services/` or `app/repositories/`. |
| **F3: `yield` Cleanup Safety** | Use `yield` dependencies with `async with` / `try...finally` cleanup; never swallow exceptions after `yield` | `get_session` uses `async with SessionFactory() as session: yield session` so uncommitted work rolls back and exceptions propagate to `app/api/error_handlers.py`. Keep default `"request"` scope; commit inside the service before returning. |
| **F4: `APIRouter` Contract** | Declare `prefix`, `tags`, and shared `dependencies` on `APIRouter(...)`, not on `include_router()`; one HTTP verb per function | `router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(require_authenticated)])`. Never use `@router.api_route(methods=[...])`. |
| **F5: `lifespan` & Settings** | Manage startup/shutdown resources via `FastAPI(lifespan=...)` (never `@app.on_event`) and inject settings via cached `get_settings()` | Initialize DB engine / HTTPX clients in `lifespan` and dispose after `yield`. |
| **F6: Pydantic v2, Responses & HTTPX** | Avoid `...` defaults, `RootModel`, and deprecated `ORJSONResponse` / `UJSONResponse`; use `EventSourceResponse` for SSE and `httpx.AsyncClient` / `ASGITransport` | Use `Field(gt=0)` and `Annotated[list[Item], Field(min_length=1)]`. Declare explicit return types (`-> OrderRead`) so Pydantic v2 serializes in Rust. |
