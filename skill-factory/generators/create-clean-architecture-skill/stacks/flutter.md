# Preset: Dart / Flutter

> A starting point, not a final answer. Always tailor to the project and confirm with the user.

## Detect

`pubspec.yaml` with the `flutter` SDK. State management decides a lot: `flutter_bloc`, `flutter_riverpod`/`hooks_riverpod`, `provider`, `get`. Also check `get_it`, `injectable`, `go_router`, `dio`, `freezed`, `json_serializable`.

## Framework-enforced conventions

App code in `lib/`, entry `lib/main.dart`, tests in `test/`, platform folders (`android/`, `ios/`, `web/`...) untouched. Files are `snake_case.dart`.

## Concept mapping

| Concept | In this stack |
|---|---|
| Presentation | Pages/screens + widgets + state holder (Bloc/Cubit, Notifier, controller) |
| Use case | Class with a `call()` method in `domain/usecases/` (`full`) or service in `application/` |
| Domain entity | Immutable class (`freezed` optional) without JSON code |
| Repository interface | `abstract interface class` in `domain/repositories/` |
| Repository implementation | `data/repositories/*_impl.dart` |
| Data source | `data/datasources/` (remote via `dio`, local via storage) |
| DTO / model | `data/models/` with `fromJson`/`toJson` |
| DI / composition root | `get_it`/`injectable` setup in `app/di.dart`, or Riverpod providers |
| Routing | `go_router` config in `app/router.dart` |

## Standard tree (feature-first)

```
lib/
  main.dart
  app/                         # App widget, router, DI setup, theme
  core/                        # network client, errors, constants (technical shared)
  features/
    orders/
      data/
        datasources/order_remote_datasource.dart
        models/order_model.dart
        repositories/order_repository_impl.dart
      domain/
        entities/order.dart
        repositories/order_repository.dart
        usecases/get_orders.dart
      presentation/
        pages/orders_page.dart
        widgets/order_tile.dart
        bloc/                  # or providers/ / controllers/ per state management
test/                          # mirrors lib/
```

## Lite / full variations

- **lite:** per feature `data/` + `presentation/` only; no use cases, repository without interface.
- **full:** as above with use cases for every operation, `Either`/result types for errors, `freezed` entities.

## Naming

| Kind | Pattern |
|---|---|
| File | `snake_case.dart` |
| Class | `PascalCase` (`OrderRepositoryImpl`, `GetOrders`) |
| Bloc | `orders_bloc.dart`, `orders_event.dart`, `orders_state.dart` |

## Enforcing import rules

No standard tool as established as in TS/Python. Options: a `custom_lint` rule, an import-check script in CI (e.g. grep for `features/*/data` imports inside `domain/`), and review checklists. Check pub.dev for a maintained import-lint package during research before recommending one.

## Stack-specific pitfalls

- Business logic and API calls inside `build()` or widget callbacks.
- One giant `widgets/` folder at the root holding feature UI.
- Domain entities with `fromJson` (JSON belongs in `data/models`).
- Mixing several state-management approaches in one project.

## Reference sources

Candidates to verify: Flutter official "App architecture" guide, Andrea Bizzotto's Riverpod architecture articles (codewithandrea.com), Reso Coder's Flutter TDD clean architecture series.
