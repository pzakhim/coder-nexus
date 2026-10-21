# Naming by stack

Starting points for `01-naming.md`. The workspace's real names (sampled in Step 1) win; use these only to fill gaps or settle inconsistency.

## Python (FastAPI / Django)

| Kind | Convention | Example |
|---|---|---|
| Module / file | `snake_case.py`, named by role, no `_utils`/`_helper`/`_manager` | `manage_users.py`, `sqlalchemy_repository.py` |
| Class | `PascalCase`; use case `<Verb><Noun>UseCase`, port `<Noun>Port`, DTO `<Noun><Purpose>DTO`, error `<Condition>Error`, adapter `<Tech><Noun>` | `CreateOrderUseCase`, `OrderRepositoryPort` |
| Function / method | `snake_case` verb: `get_` (one), `list_` (many), `is_/has_/can_` (bool), `<a>_to_<b>` (convert) | `list_orders`, `order_to_dto` |
| Variable | Noun with unit/content: `timeout_seconds`, `tenant_id` | |
| Constant | `UPPER_SNAKE` at module top | `MAX_PAGE_SIZE` |
| Private | `_leading_underscore` | |
| Test | `test_<behavior>_<condition>` in `test_<topic>.py` | `test_create_order_rejects_closed_cart` |

## TypeScript / React / Next.js

| Kind | Convention | Example |
|---|---|---|
| File | `kebab-case`; role suffix where the workspace uses one | `docs-list-view.tsx`, `use-doc-detail.ts` |
| Component | `PascalCase` noun, same as file | `DocsListView` |
| Hook | `useXxx` | `useDocDetail` |
| Handler | prop `onXxx`, internal `handleXxx` by intent | `onSave` / `handleSave` |
| Variable / function | `camelCase`; booleans `isXxx/hasXxx/canXxx/shouldXxx` | `isDeleting` |
| Type / interface | `PascalCase`, no `I` prefix | `DocSummary` |
| Constant | `UPPER_SNAKE_CASE` | `DEFAULT_PAGE_SIZE` |
| CSS class | `kebab-case` with domain prefix, named by role | `docs-toolbar`, `status-badge--danger` |

## TypeScript / NestJS

Files `kebab-case.<role>.ts` (`.controller`, `.service`, `.use-case`, `.entity`, `.dto`, `.module`); classes `PascalCase` + role (`CreateOrderUseCase`, `OrdersController`); DTOs `CreateOrderDto`.

## Dart / Flutter

Files `snake_case.dart`; classes `PascalCase` (`OrderRepositoryImpl`, `GetOrders`); members `lowerCamelCase`; private `_leading`; Bloc files `orders_bloc.dart`, `orders_event.dart`, `orders_state.dart`; widgets named by what they show (`OrderTile`).

## Go

Packages short lowercase nouns (`orders`); exported `PascalCase`, unexported `camelCase`; interfaces by behavior (`OrderStore`, `-er` for single methods); no stutter (`orders.Service`, not `orders.OrdersService`); errors `ErrNotFound`.

## Everywhere

- Use the domain glossary's words exactly (e.g. `tenant`, `environment`, `change_set`); never two names for one concept.
- No position-based names (`new_`, `legacy_`, `v2_`).
- Abbreviations only when universal (`id`, `url`, `dto`, `uow`, `sql`).
