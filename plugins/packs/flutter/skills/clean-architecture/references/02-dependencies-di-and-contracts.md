# 02 — Dependencies, Cross-Module Boundaries & Data/State Contracts

> Scope: Layer import matrix, `rg` boundary verification, cross-module boundaries, network/DataSource/DTO/Repository contracts, and Cubit state conventions (`A1`–`A8`).

---

## 1. Layer Dependency Matrix (`A5`, `A7`)

Dependencies flow strictly inward toward `domain/`:

| Source Layer | May Import From | Forbidden Imports (`BLOCKER` / `MAJOR`) |
|---|---|---|
| `domain/` | Dart SDK (`dart:core`, `dart:async`), `equatable`, pure-Dart foundation domain contracts (`Entity`, `UseCase`, result types), or another module's published `domain/` contract | `package:flutter/*`, `data/`, `presentation/`, `dio`, local storage plugins, router packages, or another module's `data/` / `presentation/` |
| `data/` | Own `domain/`, Core network/storage/error contracts, DTO/parsing helpers | `package:flutter/material.dart`, `presentation/` (`bloc/`, `screens/`, `widgets/`), or another module's `data/` / `presentation/` |
| `presentation/` | Own `domain/` (`entities/`, `usecases/`), `flutter/*`, `flutter_bloc`, Core router/theme, `lib/commons/widgets/`, and the active UI kit | Own or another module's `data/` (`data_sources/`, `models/`, `mappers/`, `repo_impl/`), raw HTTP clients (`Dio`), or another module's private `bloc/` / `screens/` / `widgets/` |
| `di.dart` | Own `domain/`, `data/`, `presentation/bloc/`, and Core DI container (`GetIt`) | Unrelated feature modules' private implementations |

### Fast Boundary Verification (`rg`)

Run these deterministic checks on any touched module before handoff:

```bash
# 1. Domain purity (must return 0 matches)
rg -n "import 'package:flutter/|/data/|/presentation/" lib/modules/<feature>/domain/

# 2. Data layer UI isolation (must return 0 matches)
rg -n "import 'package:flutter/|/presentation/" lib/modules/<feature>/data/

# 3. Presentation -> Data isolation (must return 0 matches)
rg -n "/data/(data_sources|models|mappers|repo_impl)/" lib/modules/<feature>/presentation/

# 4. Cross-module private import check (must only match approved domain/ contracts)
rg -n "modules/(?!<feature>)[a-z0-9_]+/(data|presentation)/" lib/modules/<feature>/
```

---

## 2. Cross-Module Boundaries & Shared Code Ownership (`A5`, `A7`)

1. **Cross-module communication:** A feature module may consume another module's published Domain `UseCase`, `Entity`, or parameter object through DI when approved in `design.md`. Never import another module's `Cubit`, `State`, `DataSource`, `Model`, `Mapper`, or `RepositoryImpl`.
2. **Single composition root:** `lib/modules/modules_di.dart` registers all feature DI functions in the Client's verified boot order. Do not introduce secondary composition roots.
3. **Widget ownership (`presentation/widgets/` vs `lib/commons/widgets/`):**
   - Keep widgets used by a single feature inside `lib/modules/<feature>/presentation/widgets/`.
   - Promote a widget to `lib/commons/widgets/` only when **2 or more** feature modules share it and the promotion is part of the approved design.
   - Never move feature-specific business rules into `lib/core/` or `lib/commons/` to bypass module boundaries.

---

## 3. Network, DataSource, DTO & Repository Contracts (`A1`, `A8`)

1. **Single HTTP stack:** Reuse the Client's configured network client (`ApiClient` / `ApiService` over `Dio` or `HttpClient`) with its core auth and logging interceptors. Never instantiate an ad-hoc `Dio()` client inside a feature module.
2. **DataSources & Endpoints:** Inject the Core API service into `DataSource` via constructor DI. Reference verified endpoint constants from the Client's route/config table — never hardcode raw URL paths inline.
3. **DTO Parsing & Fail-Fast Integrity (`A8`):**
   - Parse raw JSON into typed `Model` classes (`data/models/`) using safe parsing helpers.
   - Validate mandatory fields explicitly (e.g., primary IDs, required timestamps, status enums).
   - **Zero fake fallback rule:** Never hide missing mandatory fields or failed API responses behind `0`, `""`, `[]`, or fabricated placeholder objects. If a required field is missing or malformed, fail explicitly so the Repository surfaces a typed error state.
4. **Repository Error Wrapping:**
   - Convert `Model` to `Entity` through the injected `Mapper` inside `RepositoryImpl`.
   - Catch and wrap transport/parsing failures into the Client's typed result contract (preserving error codes and messages) instead of letting raw exceptions leak into `Presentation`.

---

## 4. State Management (`Cubit` / `Bloc`) Patterns (`A2`, `A3`)

1. **Follow the module's state convention:**
   - Inspect a sibling module (for `INIT`) or the target module (for `EXTEND`).
   - Preserve the existing state hierarchy (e.g., project base state class with `equatableProps`, or `sealed class` / `Equatable` with `props`) unless a migration is explicitly approved.
2. **Cubit responsibilities:**
   - Receive `UseCase`s via constructor injection.
   - Emit immutable state transitions (`loading`, `loaded`/`success`, `failure`/`error`).
   - Never hold `BuildContext`, `TextEditingController`, or widget references inside a `Cubit`.
3. **Widget consumption:**
   - Use `BlocBuilder` (or `BlocSelector`) for pure UI rendering from state.
   - Use `BlocListener` (or `BlocConsumer`'s listener) for one-shot side effects: route navigation, dialogs, bottom sheets, and snackbars/toasts.
