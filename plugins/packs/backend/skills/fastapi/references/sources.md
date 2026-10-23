# Sources

Ideas rewritten in this repo's vocabulary (`D-NN`, gates, evidence rows). The official skill text is not copied; read the installed copy or the pinned files below. Stars as of 2026-10.

## Pinned copy of the official skill (FastAPI `0.161.1`, commit `69ddc2b`)

Use these when the installed package has no `.agents/skills/fastapi/` directory ([../SKILL.md](../SKILL.md) §1). The pinned tree also has `references/streaming.md` (SSE, JSON Lines, byte streams), read by `backend-realtime`.

| Source (read 2026-10-23) | Stars | Idea taken | Where used |
|---|---|---|---|
| [fastapi/fastapi `fastapi/.agents/skills/fastapi/SKILL.md`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/.agents/skills/fastapi/SKILL.md) | 104k | `Annotated`, return types, router-level config, CLI entrypoint, no deprecated JSON responses, native SSE; the SQLModel / ty / `def`-by-default / Asyncer / frontend / telemetry advice we override | [../SKILL.md](../SKILL.md) §2-3, [overrides.md](overrides.md) |
| [same `references/dependencies.md`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/.agents/skills/fastapi/references/dependencies.md) | 104k | `yield` dependencies with `scope`; function dependencies over class dependencies | [overrides.md](overrides.md) "Adopted", O6 (legacy `query()` example) |
| [same `references/path-operations.md`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/.agents/skills/fastapi/references/path-operations.md) | 104k | Prefix/tags/dependencies on the router; one HTTP method per function | [../SKILL.md](../SKILL.md) §2 |
| [same `references/pydantic.md`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/.agents/skills/fastapi/references/pydantic.md) | 104k | No `...` defaults, no `RootModel` | [../SKILL.md](../SKILL.md) §2 |
| [same `references/responses.md`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/.agents/skills/fastapi/references/responses.md) | 104k | Return type first, `response_model` only for a different public schema | [overrides.md](overrides.md) O8 |
| [same `references/other-tools.md`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/.agents/skills/fastapi/references/other-tools.md) | 104k | HTTPX for outbound calls; Ruff; the uv / ty / Asyncer / SQLModel preferences we override | [overrides.md](overrides.md) O1-O5 |

## Official docs read (2026-10-23)

| Doc | Idea taken | Where used |
|---|---|---|
| https://fastapi.tiangolo.com/tutorial/bigger-applications/ | Routers per resource, `include_router`, `[tool.fastapi] entrypoint` | [../SKILL.md](../SKILL.md) §2 CLI |
| https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/ | Exit code runs after the response by default; re-raise after `except`; `scope="function"` | [overrides.md](overrides.md) "Adopted" (session scope, commit before response) |
| https://fastapi.tiangolo.com/advanced/events/ | `lifespan` replaces `on_event`; the two cannot be combined | [../SKILL.md](../SKILL.md) §2, [overrides.md](overrides.md) "Adopted" |
| https://fastapi.tiangolo.com/advanced/settings/ | Cached `get_settings()` dependency, no global instance | [../SKILL.md](../SKILL.md) §2 |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| SQLModel as the one model for table and API | official skill `other-tools.md` | O1: contract and storage change independently; approved SQLAlchemy 2 async + repositories |
| ty as type checker | official skill `other-tools.md` | O2: approved mypy |
| Plain `def` handlers by default | official skill `SKILL.md` | O3: async database stack |
| Asyncer for sync/async mixing | official skill `other-tools.md` | O4: no new dependency without `D-NN`; anyio is already installed |
| uv whenever available | official skill `other-tools.md` | O5: the lock file decides |
| `HTTPException` raised from path operations as the main error path | FastAPI tutorial | O7: services stay framework-free; one handler maps errors to the contract |
| `app.frontend()`, OpenTelemetry auto-setup, Ruff `FAST` rules by default | official skill `SKILL.md`, `other-tools.md` | O9: deployment / configuration decisions, need a `D-NN` |
| Copying the official skill into this pack (vendoring) | - | It tracks the installed FastAPI version; a copy goes stale. We point to the installed copy and keep only overrides |
