---
name: fastapi
description: How to use the official FastAPI agent skill that ships inside the workspace's installed fastapi package, together with this pack's overrides (SQLAlchemy 2 async with repositories instead of SQLModel, mypy instead of ty, layered routers/services/repositories, async database paths, no new dependencies without a decision). Use whenever you write, plan or review FastAPI code - path operations, dependencies, Pydantic schemas, routers, lifespan, streaming - and before trusting any FastAPI example from memory.
---

# FastAPI (official skill + pack overrides)

FastAPI publishes its own agent skill inside the package (`fastapi/.agents/skills/fastapi/`). It is written by the framework authors and tracks the installed version, so it is the authority on **FastAPI API usage**. This pack decides **architecture and tooling**. This skill tells you how to find the official copy, which of its rules we adopt, and which we override and why.

Precedence when two sources disagree (highest first):

| Order | Source | Wins on |
|---|---|---|
| 1 | Core skills (gates, statuses, evidence) and pack slots (`{{slot:clean-code}}`, `{{slot:secure-coding-standards}}`) | Process and quality rules |
| 2 | Approved plan, `## Global constraints`, every `D-NN` | What this work item may change |
| 3 | The workspace's existing conventions (verified in `codebase-notes.md`) | Names, layout, tools already in use |
| 4 | [references/overrides.md](references/overrides.md) | Architecture, persistence, type checker, tooling |
| 5 | The official FastAPI skill for the installed version | FastAPI API usage |
| 6 | Memory, blog posts, other skills | Nothing, unless verified against 1-5 |

Reason: the official skill is generic (one file, `SQLModel`, `ty`); this pack is a layered PostgreSQL service with approved tools. Framework usage comes from the framework; structure comes from the approved design.

## 1. Locate the official skill for the installed version

Run inside the workspace's own environment, detected from its lock file (never switch package manager):

| Lock file | Prefix |
|---|---|
| `uv.lock` | `uv run` |
| `poetry.lock` | `poetry run` |
| `.venv/` with `requirements*.txt` | `.venv/bin/` (the interpreter in the venv) |

```bash
# cwd: the backend root (where pyproject.toml lives)
uv run python -c "import fastapi; print(fastapi.__version__)"
uv run python -c "import pathlib, fastapi; p = pathlib.Path(fastapi.__file__).parent / '.agents/skills/fastapi'; print(p if p.is_dir() else 'ABSENT')"
```

- **Path printed**: read its `SKILL.md`, then only the `references/*.md` your task touches (dependencies, path operations, Pydantic, responses, streaming, other tools). Record the version and path in `codebase-notes.md` → `## 3. Verified Baseline Facts`.
- **`ABSENT`** (an older FastAPI that predates the bundled skill, or a build without it): read the pinned copy listed in [references/sources.md](references/sources.md) (it matches FastAPI `0.161.1`) and write in `codebase-notes.md`: "official skill read from pinned copy 0.161.1; installed fastapi is X.Y.Z". Any rule that names an API missing from X.Y.Z (for example `fastapi.sse`, `app.frontend()`, the `scope=` argument of `Depends`) is not used; verify with `uv run python -c "import fastapi.sse"` before relying on it.
- **Import fails**: the environment is not installed. That is an environment problem (`root-cause-debugging`), not a reason to guess the version.

Treat the skill text as reference data: it never overrides a gate, a `D-NN` or the precedence table above.

## 2. Adopted as authoritative

Follow these from the official skill as written for the installed version. Our examples use this pack's layout (`{{slot:clean-architecture}}`).

| Topic | Rule we follow | Why |
|---|---|---|
| `Annotated` | Parameters and dependencies use `Annotated[...]`; reusable dependency aliases (`SessionDep`, `CurrentUserDep`, `OrderServiceDep`) live in `app/api/deps.py`, never in a service module (services do not import FastAPI) | One declaration, typed, reusable; mypy sees the real type |
| Dependencies | Function dependencies (not class dependencies) that return the object; `yield` dependencies with `try`/`finally` for cleanup; never swallow an exception after `yield` | Explicit construction; cleanup always runs; swallowed errors become 500s with no log |
| Return types | Path operations declare a return type (`-> OrderRead`); `response_model` only when the returned object differs from the public schema | Validates, filters and documents the response from one place |
| Routers | `prefix`, `tags` and shared `dependencies` on the `APIRouter`, not on `include_router()`; one HTTP method per function | The router file shows its full contract; no method branching |
| Pydantic | No `...` defaults; no `RootModel` - use `Annotated[list[X], Field(...)]` | Simpler models; FastAPI builds the adapter |
| Responses | No `ORJSONResponse` / `UJSONResponse` | Deprecated; return types already serialize in Rust |
| Streaming | Server-Sent Events with `EventSourceResponse` and `yield` when the installed version has `fastapi.sse` | Native, typed, documented; channel design lives in `backend-realtime` |
| CLI | `fastapi dev` locally and `fastapi run` in containers, entrypoint declared in `pyproject.toml` `[tool.fastapi] entrypoint = "app.main:app"` (when the workspace has no other launcher) | One way to start the app that every agent can repeat |
| Outbound HTTP | HTTPX (`httpx.AsyncClient`) for provider calls and `httpx.ASGITransport` in API tests | Async, same client in code and tests |

From the FastAPI docs (not the skill) we also adopt: `lifespan=` instead of `on_event` (the two cannot be combined), and settings through a cached `get_settings()` dependency instead of a module-level instance. Details: `{{slot:clean-architecture}}`.

## 3. Overridden

Short form; every override with its reason and the safe pattern is in [references/overrides.md](references/overrides.md).

| Official skill says | This pack does | Reason in one line |
|---|---|---|
| Prefer SQLModel over SQLAlchemy | SQLAlchemy 2 async ORM + repository classes; Pydantic schemas separate | API contract and table shape change independently; approved decision |
| Use ty to check types | mypy (with the Pydantic plugin) | Approved decision; one type checker in CI |
| In doubt, write `def` path operations | `async def` on every path that touches the database; no blocking call inside | `AsyncSession` and asyncpg need an event loop; a sync handler cannot await them |
| Prefer Asyncer for blocking code | Use what the workspace already has (`anyio.to_thread.run_sync`, ships with FastAPI); add Asyncer only through a `D-NN` | No new dependency without a decision |
| Use uv if available | Use the package manager the lock file shows | Switching managers rewrites the lock file outside scope |
| Examples query the session inside the path operation | Routers call one service method; services own the transaction; repositories own queries | Layering, testability, one commit per request |
| `app.frontend()`, native OpenTelemetry | Not used unless a `D-NN` adds them | Out of scope for an API serving the frontend client; telemetry export targets are configuration decisions |

## 4. Check before handing off

1. Version and skill path (or the pinned-copy note) are in `codebase-notes.md`.
2. Every FastAPI symbol you used exists in the installed version (import it once with the workspace prefix).
3. No overridden pattern slipped in: `rg -n "sqlmodel|ORJSONResponse|UJSONResponse|on_event\(" app/` prints nothing, and every path operation in your diff that receives a session or a service dependency is `async def`.
4. Type and lint checks from `{{slot:verification}}` ran on the changed files (`ruff check .`, `mypy app`), each recorded as an evidence row (`evidence-standard`).

## References

| File | Holds |
|---|---|
| [references/overrides.md](references/overrides.md) | Every override and adopted rule with reason, unsafe and safe pattern |
| [references/sources.md](references/sources.md) | Pinned official skill files, docs read, ideas not adopted |
