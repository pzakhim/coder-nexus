# 03 — Feature Module Structure and Layer Contracts

Apply the approved profile through [core-usage](../../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

> **Sources:** Senior Clean Architecture guide, state-management and DI rules.
> **Scope:** `lib/modules/<feature>/`; compare this blueprint with the actual Client and approved design.

```text
lib/modules/<feature>/
├── di.dart
├── domain/
│   ├── entities/       # Immutable business entities
│   ├── repo/           # Abstract repository contracts
│   └── usecases/       # Focused business actions
├── data/
│   ├── data_sources/   # Verified API and local sources
│   ├── models/         # Parsed DTOs
│   ├── mappers/        # Model to Entity conversion
│   └── repo_impl/      # Repository implementations
└── presentation/
    ├── bloc/           # Cubit and state
    ├── screens/        # Screen destinations: *_screen.dart, *Screen extends BaseScreen
    └── widgets/        # Feature-private UI
```

## Dependency direction

Domain is pure Dart and does not import Flutter, Data or Presentation. Data implements Domain contracts. Presentation consumes Domain actions and entities, rather than DataSource or DTO internals. DI composes dependencies at the module boundary. Do not create unused layers or classes for a scoped UI-only change.

Classify destinations before creating files. All screens in the approved scope use the verified Client `BaseScreen`/`BaseScreenState` and screen metadata/layout hooks; dialog and child widgets do not. See [the screen contract](05_screen_contract.md). A missing active base API blocks generation.

## State patterns

Cubit state follows the Client's existing convention (a project state base such as `BaseBlocState` only if the Client already has one; otherwise sealed classes or `Equatable`). Existing modules keep their convention unless migration is approved. Use `BlocBuilder` for rendering and `BlocListener` for navigation, notifications and other side effects.

## Module DI Order

When all components are required, register Mapper → DataSource → Repository under its abstract Domain type → UseCase → screen-scoped Cubit. A screen-scoped Cubit uses `registerFactory`; app-wide lifetimes follow the actual Client design. Add a new module's DI entry to `lib/modules/modules_di.dart`. A phase need only register dependencies it actually introduces.
