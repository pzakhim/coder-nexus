# 01 — Layout, Boot Sequence & Layer Roles

> Scope: Root layout (`lib/`), boot order, feature module layout (`lib/modules/<feature>/`), layer responsibilities, and Module DI registration order (`A1`–`A5`, `A9`).

---

## 1. Project Root Structure

Inspect the actual Flutter Client workspace before applying this blueprint (`get_project_structure` with `scope: "root"` or `scope: "module"`):

```text
lib/
├── main_dev.dart, main_stage.dart, main_prod.dart  # Flavor entrypoints (when present)
├── main.dart                                       # Shared bootstrap entrypoint
├── app.dart                                        # Root MaterialApp / Router configuration
├── core/                                           # App-wide infrastructure (network, auth, storage, router, core DI)
│   └── constants/                                  # Shared constants and verified API endpoint routes
├── commons/                                        # Cross-feature UI widgets and shared helpers (2+ modules)
└── modules/
    ├── modules_di.dart                             # Feature composition root
    └── <feature>/                                  # Self-contained feature module (lower_snake_case)
```

### Boot Sequence
1. Initialize flavor configuration (`AppConfig` / environment config) in the active entrypoint.
2. Initialize Core DI (`lib/core/`), storage, and network/auth interceptors.
3. Register feature modules via `lib/modules/modules_di.dart` in the verified Client boot order.
4. Launch the root `App` widget (`app.dart`).
- **Rule:** Never introduce a second bootstrap path or place feature business logic in `main.dart` or `app.dart`.

---

## 2. Feature Module Structure (`lib/modules/<feature>/`)

Each feature lives under `lib/modules/<feature>/` and owns its Domain, Data, Presentation, and DI wiring:

```text
lib/modules/<feature>/
├── di.dart                         # Module dependency injection registration
├── domain/                         # Pure Dart business rules & contracts (zero Flutter/Data imports)
│   ├── entities/                   # Immutable business entities (*_entity.dart)
│   ├── repo/                       # Abstract repository interfaces (*_repository.dart)
│   └── usecases/                   # Focused single-action use cases (*_usecase.dart)
├── data/                           # Data transport, DTO parsing & contract implementation
│   ├── data_sources/               # Remote/local data sources (*_data_source.dart)
│   ├── models/                     # Raw DTO models with fail-fast parsing (*_model.dart)
│   ├── mappers/                    # Bidirectional or Model -> Entity mappers (*_mapper.dart)
│   └── repo_impl/                  # Repository implementations (*_repository_impl.dart)
└── presentation/                   # UI delivery & state management
    ├── bloc/                       # Cubit/Bloc and immutable State classes (*_cubit.dart, *_state.dart)
    ├── screens/                    # Navigable screen destinations (*_screen.dart, class *Screen)
    └── widgets/                    # Feature-private child widgets and dialogs
```

> **Proportionality (`A9`):** Create only the folders and files required by the approved phase. Do not create a top-level `views/` folder beside `presentation/`, and do not scaffold empty `domain/` or `data/` files for a UI-only change.

---

## 3. Layer Responsibilities (`A1`–`A5`)

| Layer | Owns | Must Never Contain |
|---|---|---|
| **Domain (`domain/`)** | Immutable business `Entity` classes (`Equatable`), abstract `Repository` contracts, and focused `UseCase` classes | `package:flutter/*` imports, HTTP/Dio clients, JSON serialization annotations/logic, DTO models, or Presentation/Cubit references |
| **Data (`data/`)** | `DataSource` (API/local calls using verified endpoint constants), `Model` (DTO parsing with explicit mandatory-field checks), `Mapper` (`Model ↔ Entity`), and `RepositoryImpl` (error wrapping + mapping) | UI widgets, `BuildContext`, navigation calls, presentation state, or silent fallback data (`0`, `""`, `[]`) on parse/network failures |
| **Presentation (`presentation/`)** | `Cubit`/`Bloc` state holders, immutable `State` classes, navigable `*Screen` classes (`presentation/screens/`), and feature-private child widgets (`presentation/widgets/`) | Direct `DataSource` or `DTO Model` imports, raw `Dio`/HTTP calls, SQL queries, or multi-step domain orchestration inside widget `build()` methods |
| **Core & Commons (`lib/core/`, `lib/commons/`)** | App-wide transport, auth, router, theme, and widgets shared by **2 or more** feature modules | Single-feature business logic, feature-specific DTOs/use cases moved into `core/` to bypass module boundaries |

---

## 4. Module DI Registration Order (`A4`)

When a feature phase introduces the full vertical slice, register dependencies in `lib/modules/<feature>/di.dart` in strict bottom-up dependency order:

1. **Mapper** — `registerLazySingleton`
2. **DataSource** — `registerLazySingleton` (injecting the verified Core API/storage service)
3. **Repository** — `registerLazySingleton<FeatureRepository>` (bound to the abstract Domain interface, injecting `DataSource` and `Mapper`)
4. **UseCase** — `registerLazySingleton` (injecting the abstract `FeatureRepository`)
5. **Cubit / Bloc** — `registerFactory` for screen-scoped state holders (injecting the required `UseCase`s) so each screen instance receives a fresh lifecycle; use singleton scope only when the approved design explicitly specifies app-wide shared state.

Finally, register the module's DI setup function in `lib/modules/modules_di.dart`. Only register components that the current phase actually introduces.
