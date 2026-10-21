# Framework-agnostic principles

## 1. Four layers

| Layer | Responsibility | Examples |
|---|---|---|
| **Domain** | Pure business concepts & rules | Entities, value objects, domain errors, repository interfaces |
| **Application** | Orchestrates one use case | Use case / service: load data → apply rules → persist → return result |
| **Infrastructure** | Talks to the outside world | DB, HTTP clients, files, queues, third-party SDKs, repository implementations |
| **Presentation** | Takes input, returns output | Controllers, route handlers, pages, widgets, components, CLI commands |

Plus a **composition root**: the single place where things are assembled (DI, config loading, client creation).

## 2. Dependency rule (hard rule)

- Dependencies point inward only: `presentation → application → domain`, `infrastructure → domain`.
- Domain imports no framework, ORM, HTTP, or UI code.
- Application depends on **interfaces** (declared in domain/application), not on infrastructure implementations.
- Feature A never imports the internals of feature B — only its public API (`index`/`__init__`/barrel) or via events/shared services.
- No circular imports.

## 3. Where logic lives

| Kind of logic | Lives in |
|---|---|
| Business rule ("orders over $200 ship free") | Domain (entity / value object / domain service) |
| Sequence of a business operation, transactions | Application (use case) |
| Input format checks (required, email, length) | Presentation (schema / DTO) |
| Mapping DB/API data ↔ entities | Infrastructure (mapper / model) |
| Mapping entities ↔ responses / view models | Presentation |
| Display formatting (money, dates) | Presentation or a shared UI helper |

## 4. Organization: feature-first

Default to **feature-first**: group by feature/domain, split into layers inside each feature. Why: changes usually happen per feature; features are easy to remove or extract; no giant `services/` folder.

Layer-first (the whole project grouped by layer) only fits very small projects or frameworks that force it.

## 5. Shared code

- Only move code into `shared/`/`common/`/`core/` when it is used by ≥ 3 features, or is purely technical (HTTP client, logger, config).
- Keep technical shared code apart from business shared code; shared business logic usually deserves its own feature.
- No `utils/`, `helpers/`, `misc/` dumping grounds. Every file name says what it does.

## 6. Adoption levels

| Level | When | Structure |
|---|---|---|
| `lite` | Scripts, small tools, prototypes, < ~20 files | Separate I/O from logic; group by feature; no interfaces yet |
| `standard` | Most real apps | Feature-first; per feature: presentation / application / data (infra); interfaces only where swapping/mocking is needed |
| `full` | Complex domains, multiple teams, long-lived | All 4 layers per feature, ports/adapters, pure domain, lint-enforced rules |

Never recommend `full` for a small project just because it is "proper". The level can be raised later.

## 7. Framework first

Conventions the framework enforces are the outer shell. Clean architecture applies to your own code inside. Examples: Next.js file-based routing lives in `app/` and only calls down into `features/`; a NestJS module acts as the composition root of its feature.

## 8. Naming

- Folder/file names state **what it does** or **the business concept**, never something vague (`order-pricing.ts`, not `helpers.ts`).
- Role suffixes are consistent project-wide (`.use-case`, `.repository`, `.controller`, `_service.py`...), following the stack's conventions.
- Follow the stack's casing: kebab-case (TS), snake_case (Python, Dart), PascalCase for React components.
