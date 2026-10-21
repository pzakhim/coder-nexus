# Detecting the stack & context

## 1. From the user's input

Look in `$ARGUMENTS` and the latest messages for: framework, language, project type, feature/domain names. What the user states explicitly always wins over what you infer from code.

## 2. From the project

| File | Stack | What to read for the framework |
|---|---|---|
| `package.json` | JS/TS | `dependencies`: `next`, `react`, `@nestjs/core`, `express`, `fastify`, `vue`, `nuxt`, `@angular/core`, `react-native`, `expo` |
| `tsconfig.json` | TypeScript | `paths` (import aliases), `strict` |
| `pyproject.toml`, `requirements*.txt`, `Pipfile` | Python | `fastapi`, `django`, `flask`, `litestar`; ORM: `sqlalchemy`, `sqlmodel`; `pydantic` |
| `pubspec.yaml` | Dart/Flutter | `flutter_bloc`, `riverpod`/`flutter_riverpod`, `provider`, `get_it`, `go_router`, `dio` |
| `go.mod` | Go | `gin`, `echo`, `fiber`, `chi`; `gorm`, `sqlc`, `ent` |
| `pom.xml`, `build.gradle(.kts)` | Java/Kotlin | `spring-boot`, `ktor`; Android if `com.android.application` |
| `*.csproj`, `*.sln` | .NET | ASP.NET Core, EF Core |
| `composer.json` | PHP | `laravel/framework`, `symfony/*` |

Framework version matters when conventions change between versions (e.g. Next.js Pages Router vs App Router — check for `app/` vs `pages/`).

## 3. Fullstack & monorepos

**Fullstack signals:** a backend manifest and a frontend manifest in different folders of one repo (e.g. `backend/pyproject.toml` + `frontend/package.json`, `api/` + `web/`), a `docker-compose.yml` running both, root docs describing both.

For a fullstack repo:
- Record both stacks and their folders (`be_dir`, `fe_dir`) in the Context Card.
- Default: **one skill with the branched layout** (`references/shared/`, `be/`, `fe/`) at the repo root `.agents/skills/clean-architecture/`.
- Look for existing BE/FE-specific agents (`.agents/agents/be-*`, `fe-*`) and skills: they should point at `be/` and `fe/` afterwards.

**Monorepo signals:** `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`, `melos.yaml`, `go.work`, `workspaces` in `package.json`, multiple `pyproject.toml`.

For a monorepo:
- List the apps/packages and the stack of each; ask which to cover.
- One BE app + one FE app → treat as fullstack (branched layout at the root).
- Several apps of the same kind → ask: one branched skill at the root, or one flat skill per app at `<app>/.agents/skills/clean-architecture/`.
- Shared packages (`packages/shared`, `packages/ui`) need their own rule: no business logic owned by a single app.

## 4. Current state (existing code)

- Look at the tree 3 levels deep, skipping `node_modules`, `.venv`, `build`, `dist`, `.dart_tool`, `.git`.
- Count files per folder; find the 10 longest files.
- Identify the current style: feature-first, layer-first, or mixed.
- Note deviations (logic in controllers/components, circular imports...) for the migration path.

## 5. Questions when information is missing

Only ask what you cannot infer. Bundle into one AskUserQuestion round:

| Missing | Question | Sample options |
|---|---|---|
| Framework | "Which framework does this project use?" | The 2–3 most likely for the known language |
| Project type | "What kind of project is this?" | FE / BE API / Fullstack / Mobile |
| State/DI (FE, mobile) | "How is state managed?" | Per stack, e.g. Flutter: Riverpod / BLoC |
| Level | "How much clean architecture?" | standard (Recommended) / lite / full |
| Domains | "What are the core features?" | Suggest from routes, models, DB tables you saw |

Real domain/feature names are mandatory so the tree is not generic. For a brand-new project, ask the user for 3–5 planned features.
