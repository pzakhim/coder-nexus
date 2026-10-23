# Clean Architecture Rules for Flutter Projects

Apply the approved profile through [core-package-usage](../skills/core-package-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

> **Source:** Senior Flutter Standards · AIFactory-Coder
> **Applies to:** Flutter Client code generated or changed under an approved feature version and behavior phase.

Read the current Client module and the approved `docs/features/<module>/<feature>/vN/` requirements, design, and phase before changing code. The Hub's module blueprint is a reference; existing verified conventions and the approved scope determine which files and layers need work. Do not create empty classes or registrations solely to satisfy a checklist.

## 0. Where the layers live

- **`lib/modules/<feature>/` is the home of Clean Architecture.** Domain, Data, and Presentation for a feature live here.
- **Foundation reuse follows the profile.** iMESPro reads `app_core`, `app_util`, and `app_ui_kit` GUIDEs and reuses fitting APIs or records a Core gap. External-structured follows Client foundations; external-standard needs no company packages.
- **`lib/core/` in the Client is not a default layer.** Add code there only when two or more modules need something the packages lack (helper, widget, constant, wiring). A full `lib/core/<capability>/{domain,data,presentation}` exists only for a new cross-cutting business capability, approved at Gate 2 with an option comparison.

## 1. Three-layer boundaries

### Domain Layer

- Keep business entities, repository contracts, and use cases independent of Flutter UI, Data, and Presentation implementations.
- Put immutable value entities in `domain/entities/`. Use `Equatable` where the module's entity contract calls for value equality.
- Put required repository contracts in the approved Domain location. Follow the Client error/result contract; `DataState<T>` is an iMESPro convention where applicable.
- Put one focused business action in each required use case under `domain/usecases/`. Follow the real module's callable signature; do not invent parameters or response types.

### Data Layer

- Put API-backed sources in the approved Data location. Reuse a verified base where one exists; external-standard requires none. Use real network/configuration APIs and preserve failures.
- Put DTOs in `data/models/`. Parse with safe validation helpers and validate mandatory fields explicitly. Never hide missing required data behind `0`, an empty string, an empty collection, or another fake fallback.
- Put Model → Entity conversion in `data/mappers/`. Add Entity → Model conversion only when an approved write contract requires it.
- Put repository implementations in the approved Data location. Follow the Domain contract and preserve real failures; iMESPro uses `tryCatch`/`tryCatchAsync` where its package contract applies.

### Presentation Layer

- Put Cubits and states in `presentation/bloc/`, screens in `presentation/screens/`, and feature-specific widgets in `presentation/widgets/`. Do not create a top-level `views/` folder beside the architecture layers.
- Classify routed screens separately from dialogs and child widgets. iMESPro uses verified `BaseScreen`/`BaseScreenState` and `*_screen.dart`; external-structured uses its Client screen policy; external-standard may use standard Flutter widgets. Missing a base required by the selected profile is `BLOCKED`. See the screen contract in `{{slot:clean-architecture}}`.
- Cubit state follows the Client's existing convention (copy a sibling module: a project state base if one exists, sealed classes, or `Equatable`). Preserve an extended module's convention unless a migration was approved. Do not invent a state base class.
- Use `BlocBuilder` to render from state and `BlocListener` for side effects such as navigation and notifications. Keep state immutable.
- A scoped UI change may reuse existing Domain, Data, state, and DI code without creating new classes.

## 2. Module DI Order

When a behavior needs all five kinds of dependency, register them in `di.dart` in dependency order:

1. Mapper — `registerLazySingleton`
2. DataSource — `registerLazySingleton`
3. Repository under its abstract Domain type — `registerLazySingleton<FeatureRepository>`
4. Use case — `registerLazySingleton`
5. Screen-scoped Cubit — `registerFactory`

Register a new module through `lib/modules/modules_di.dart`. Keep an existing app-wide singleton lifetime when the real Client architecture requires it. A phase that does not introduce one of these dependencies does not need an empty registration or an invented class.

## 3. Cross-module boundaries

- A module may consume another module's published use case and entity through the approved dependency boundary.
- Do not import another module's Cubit, state, DataSource, model, or repository implementation directly.
- Do not move feature-specific business rules into `lib/core/` or `lib/commons/` to bypass module ownership.

## 4. Evidence, UI reuse, and code quality

1. **Keep the diff focused.** Reuse existing platform and module capabilities. Format changed Dart files as needed; avoid repository-wide formatting and unrelated refactors.
2. **Preserve data provenance.** Follow plugin-root `shared_contracts/api_handshake_protocol.md`. Approved contract-derived fixtures support UI/contract checks only; live acceptance requires real services. Never fabricate business records, source availability or production success fallbacks. Missing required evidence is `BLOCKED`.
3. **Read before building UI.** Inspect the visual and selected foundation via `{{slot:core-package-usage}}`. iMESPro reads the Kit GUIDE: one fitting row → reuse; several → user choice; no fit → compose or record a Core gap. External-structured uses Client components/tokens; external-standard uses standard Flutter. Confirm real signatures and approved Visual AC.
4. **Resolve multi-screen behavior.** For a flow with multiple screens, document the applicable state owner, navigation/back behavior, failure paths, input dependencies and validation timing, step-up security, and post-flow effects. Mark inapplicable axes N/A with a reason. Do not invent security or cache behavior.
5. **Protect test integrity.** Never delete, disable, or weaken an assertion merely to make a failing implementation pass. Diagnose whether the production code or the test contradicts the approved AC. A legitimate test change requires the same scope and review as a code change; return to the affected approval gate if the AC itself changes.
6. **Verify the reviewed revision.** Analyzer, tests, and required runtime visual checks must run against the relevant code revision. `NOT_RUN` and `BLOCKED` are not `PASS`; changing code invalidates affected earlier evidence.

See the bundled [feature module reference](../skills/clean-architecture/references/03_feature_module.md), [UI discovery matrix](../../../core/skills/delivery-workflow/references/03_ui_ux_intake_and_discovery_matrix.md), and [Client check contract](../skills/verification/references/01_client_check_contract.md) for detailed procedures.
