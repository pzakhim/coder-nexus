# FastAPI CLI Verification Gates and Review Checklist

> Topic: Deterministic pre-handoff CLI verification gates (`PASS` / `FAIL`) and `BLOCKER` / `MAJOR` / `MINOR` review severity rubric for FastAPI code.

All CLI gates and review severities follow `shared_contracts/flags_and_statuses.md`.

---

## 1. Pre-Handoff CLI Verification Checklist (`PASS` / `FAIL`)

Run every command using the workspace's lockfile prefix (`uv run`, `poetry run`, or `.venv/bin/`):

| # | Gate | Command | Pass Criteria (`PASS` / `FAIL`) |
|---|---|---|---|
| **1** | **FastAPI Version & Bundled Skill Probe** | `uv run python -c "import fastapi; print(fastapi.__version__)"` | `PASS` when version and bundled skill path (or `ABSENT` fallback) are recorded in `codebase-notes.md` |
| **2** | **Banned Override Scan (`O1`, `F5`, `F6`)** | `rg -n "sqlmodel|ORJSONResponse|UJSONResponse|on_event\(" app/` | `PASS` when output is empty (`0` matches) |
| **3** | **Layer Purity Scan (`O6`, `O7`)** | `rg -n "^\s*(from|import) (fastapi|starlette)" app/services app/repositories app/models app/schemas app/core` | `PASS` when output is empty (`0` matches) |
| **4** | **Router Direct Session/Commit Scan (`O6`)** | `rg -n "session\.(commit|rollback|execute|scalars|scalar|add)\(" app/api/` | `PASS` when output is empty (`0` matches in `app/api/routers/`) |
| **5** | **Linter & Type Checker (`O2`)** | `uv run ruff check . && uv run mypy app` | `PASS` when both exit `0` |

---

## 2. Review Severity Rubric (`BLOCKER` / `MAJOR` / `MINOR`)

| Severity | FastAPI Findings |
|---|---|
| **`BLOCKER`** | • Using `SQLModel` or returning raw SQLAlchemy ORM instances from routes/services (**O1, O8**)<br>• Querying `AsyncSession` or calling `session.commit()` directly inside an `APIRouter` handler (**O6**)<br>• Importing `fastapi` or `starlette` (e.g., `HTTPException`, `Request`) inside `app/services/`, `app/repositories/`, `app/models/`, or `app/core/` (**O7**)<br>• Sync `def` route calling async DB/service methods or blocking CPU/file I/O called directly inside `async def` (**O3**)<br>• Swallowing exceptions after `yield` in a session/resource dependency (**F3**)<br>• Adding `Asyncer` or any unapproved package without a `D-NN` (**O4**) |
| **`MAJOR`** | • Missing return type annotation (`-> SchemaRead`) on a path operation (**O8**)<br>• Using `@app.on_event("startup" / "shutdown")` instead of `lifespan=` (**F5**)<br>• Defining `prefix`/`tags` only on `include_router()` or using `@router.api_route(methods=[...])` (**F4**)<br>• Using deprecated `ORJSONResponse` / `UJSONResponse` or `RootModel` where `Annotated[list[T], Field(...)]` applies (**F6**) |
| **`MINOR`** | • Inline `Depends(...)` repetition in route signatures instead of a shared `Annotated` alias in `app/api/deps.py` (**F2**) |
