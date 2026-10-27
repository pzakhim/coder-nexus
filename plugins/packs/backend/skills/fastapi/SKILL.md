---
name: fastapi
description: "Use the official FastAPI agent skill bundled inside the installed `fastapi` package (`fastapi/.agents/skills/fastapi/`) together with the Backend Pack's Clean Architecture overrides (`O1`–`O8`: SQLAlchemy 2 async + separate Pydantic v2 schemas instead of SQLModel, `Router -> Service -> Repository` delegation, `async def` handlers, domain error handlers, and `mypy`), enforced by `PASS` / `FAIL` CLI gates and `BLOCKER` / `MAJOR` / `MINOR` review grading."
---

# FastAPI — Official Bundled Skill + Clean Architecture Overrides

FastAPI ships its own official agent skill inside the installed Python package (`fastapi/.agents/skills/fastapi/`). That bundled skill is the authority on **FastAPI framework syntax and API usage**, while this Backend Pack governs **Clean Architecture boundaries, async database safety, and verification gates**.

## 1. Source Precedence (Highest Wins)

| Priority | Source | Governs |
|---|---|---|
| **1** | Core handshake contracts (`shared_contracts/flags_and_statuses.md`) & pack slots (`{{slot:clean-architecture}}`, `{{slot:clean-code}}`, `{{slot:secure-coding-standards}}`) | Layer boundaries, gates (`PASS` / `FAIL`), and review severities (`BLOCKER` / `MAJOR` / `MINOR`) |
| **2** | Approved `design.md`, `implementation-plan.md`, and recorded decisions (`D-NN`) | Scope, endpoint contracts (`api_contract.json`), and approved dependencies |
| **3** | Verified workspace conventions (`codebase-notes.md`) | Existing module layout, package manager lockfile (`uv.lock` / `poetry.lock`), and tooling |
| **4** | **Pack Overrides (`O1`–`O8`)** ([02-clean-architecture-overrides.md](references/02-clean-architecture-overrides.md)) | SQLAlchemy 2 async ORM + repositories (no `SQLModel`), `mypy` (no `ty`), `async def` routes, domain error mapping |
| **5** | **Official Bundled FastAPI Skill** ([01-official-skill-and-adopted-idioms.md](references/01-official-skill-and-adopted-idioms.md)) | FastAPI API mechanics (`Annotated`, `Depends`, `APIRouter`, Pydantic v2, `lifespan`, SSE, `httpx.ASGITransport`) |

## 2. Adopted Official Rules vs. Mandatory Pack Overrides (`F1`–`F6` & `O1`–`O8`)

| ID | Rule | Category | Reference |
|---|---|---|---|
| **F1** | **Locate & verify the installed `fastapi/.agents/skills/fastapi/` first** (or fall back to pinned `0.161.1` when `ABSENT`) and record the version in `codebase-notes.md`. | Adopted | [01](references/01-official-skill-and-adopted-idioms.md) |
| **F2** | **Use `Annotated[..., Depends(...)]` aliases in `app/api/deps.py`** (`SessionDep`, `CurrentUserDep`, `*ServiceDep`) using function dependencies, never class dependencies. | Adopted | [01](references/01-official-skill-and-adopted-idioms.md) |
| **F3** | **Ensure `yield` dependencies clean up in `finally` / `async with`** and never swallow exceptions after `yield`. | Adopted | [01](references/01-official-skill-and-adopted-idioms.md) |
| **F4** | **Configure `prefix`, `tags`, and shared `dependencies` on `APIRouter`** with one HTTP method per function (`@router.get`, `@router.post`). | Adopted | [01](references/01-official-skill-and-adopted-idioms.md) |
| **F5** | **Use `lifespan=` context manager (never `@app.on_event`)** and cached `get_settings()` dependency. | Adopted | [01](references/01-official-skill-and-adopted-idioms.md) |
| **F6** | **Avoid deprecated `ORJSONResponse` / `UJSONResponse` and `RootModel`**; use native Pydantic v2 Rust serialization and `EventSourceResponse` for SSE. | Adopted | [01](references/01-official-skill-and-adopted-idioms.md) |
| **O1** | **SQLAlchemy 2 async ORM + Repositories + separate Pydantic v2 schemas** — **never `SQLModel`**. | Override | [02](references/02-clean-architecture-overrides.md) |
| **O2** | **Enforce `mypy` (with `pydantic.mypy`)** instead of `ty` (unless `ty` is an existing workspace `D-NN`). | Override | [02](references/02-clean-architecture-overrides.md) |
| **O3** | **Use `async def` on all DB/I/O routes and dependencies**; offload sync CPU/blocking calls via `anyio.to_thread.run_sync`. | Override | [02](references/02-clean-architecture-overrides.md) |
| **O4** | **No `Asyncer` or new dependencies without an approved `D-NN`**. | Override | [02](references/02-clean-architecture-overrides.md) |
| **O5** | **Respect the lockfile package manager (`uv.lock` vs `poetry.lock` vs `.venv`)**. | Override | [02](references/02-clean-architecture-overrides.md) |
| **O6** | **Strict layering (`Router → Service → Repository → AsyncSession`)** — never query `session` or call `commit()` inside a router. | Override | [02](references/02-clean-architecture-overrides.md) |
| **O7** | **Raise framework-free domain errors (`app/core/errors.py`)** in services/repositories and map once in `app/api/error_handlers.py`. | Override | [02](references/02-clean-architecture-overrides.md) |
| **O8** | **Return explicit Pydantic v2 schemas (`-> OrderRead`) from services/routers** — never return raw ORM models. | Override | [02](references/02-clean-architecture-overrides.md) |

## 3. CLI Verification Gates (`PASS` / `FAIL`) & Review Grading

| Gate | Command | Pass Criteria (`PASS` / `FAIL`) |
|---|---|---|
| **Override & Anti-Pattern Scan** | `rg -n "sqlmodel|ORJSONResponse|UJSONResponse|on_event\(" app/` | `PASS` when 0 matches exist in `app/` |
| **Layer Purity Scan** | `rg -n "^\s*(from|import) (fastapi|starlette)" app/services app/repositories app/models app/schemas app/core` | `PASS` when 0 matches exist outside `app/api/` and `app/main.py` |
| **Static Lint & Types** | `uv run ruff check . && uv run mypy app` | `PASS` on exit code `0` (`0` errors) |

Reviewer findings use **`BLOCKER` / `MAJOR` / `MINOR`** ([03-cli-gates-and-review-checklist.md](references/03-cli-gates-and-review-checklist.md)).

## 4. Reference Guides

| Topic | Reference File |
|---|---|
| Locating the bundled `fastapi/.agents/skills/fastapi/` skill, pinned `0.161.1` fallback, and adopted FastAPI idioms (`F1`–`F6`) | [01-official-skill-and-adopted-idioms.md](references/01-official-skill-and-adopted-idioms.md) |
| Mandatory Clean Architecture & async overrides (`O1`–`O8`) with Unsafe vs. Safe code examples | [02-clean-architecture-overrides.md](references/02-clean-architecture-overrides.md) |
| Pre-handoff CLI verification gates (`PASS` / `FAIL`) and `BLOCKER` / `MAJOR` / `MINOR` review rubric | [03-cli-gates-and-review-checklist.md](references/03-cli-gates-and-review-checklist.md) |
