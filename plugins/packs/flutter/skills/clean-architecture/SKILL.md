---
name: clean-architecture
description: Guide Flutter Clean Architecture module structure, layer boundaries, DI order, and screen contracts using verified Client conventions.
---

# Flutter Clean Architecture (`domain/` · `data/` · `presentation/`)

Use this skill when creating or extending a Flutter feature module (`lib/modules/<feature>/`), inspecting project structure, or choosing Domain, Data, Presentation, and DI ownership. Apply the active workspace profile (`architecture_profile` in `.superpowers/setup.json`).

---

## 1. Deterministic Tool & Boundary Gates (`PASS` / `FAIL`)

Run these checks before handoff or review. Each tool gate produces a binary **`PASS`** or **`FAIL`** status (`plugins/shared_contracts/flags_and_statuses.md` §1):

| Check | Command / Tool | Gate Status |
|---|---|---|
| **File-level architecture validator** | `validate_architecture_code` (per changed Dart file, with explicit `layer` and `architecture_profile`) | `PASS` / `FAIL` (`UNVERIFIED` requires analyzer run) |
| **Module-level architecture validator** | `validate_module_architecture` (when a full module is added or restructured) | `PASS` / `FAIL` |
| **Static analyzer (`very_good_analysis` / `flutter_lints`)** | `flutter analyze` | `PASS` / `FAIL` |
| **Structural metrics (`dart_code_linter`)** | `dart run dart_code_linter:metrics analyze lib` | `PASS` / `FAIL` |
| **Domain purity boundary check (`rg`)** | `rg -n "import 'package:flutter/|/data/|/presentation/" lib/modules/*/domain/` (expect 0 matches) | `PASS` / `FAIL` |
| **Presentation → Data isolation check (`rg`)** | `rg -n "/data/(data_sources|models|mappers|repo_impl)/" lib/modules/*/presentation/` (expect 0 matches) | `PASS` / `FAIL` |

---

## 2. Core Architecture & Layer Principles (`A1`–`A10` — Mandatory Compliance)

All 10 architectural principles are **mandatory compliance** when designing, writing, or modifying Flutter code. During Code Review, violations are graded on the unified 3-tier scale (`BLOCKER` / `MAJOR` / `MINOR` — see [03-screens-adding-and-splitting.md](references/03-screens-adding-and-splitting.md)):

| ID | Principle | Flutter / Dart Contract | Reference |
|---|---|---|---|
| **A1** | **Separation of Contracts & DTO Models** | Keep immutable Domain entities (`domain/entities/`) separate from Data DTO models (`data/models/`). Convert between DTOs and Entities via explicit mappers (`data/mappers/`) inside the Repository implementation; never pass raw JSON maps or DTOs into Presentation states or widgets | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md), [02 — Dependencies, DI & Contracts](references/02-dependencies-di-and-contracts.md) |
| **A2** | **Thin Presentation / Entry Boundary** | Screens (`presentation/screens/`) and widgets (`presentation/widgets/`) render state and dispatch user intents to a Cubit/Bloc (`presentation/bloc/`). Never perform HTTP calls, JSON parsing, storage writes, or multi-step business rules directly inside a Widget | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md), [03 — Screens, Adding & Splitting](references/03-screens-adding-and-splitting.md) |
| **A3** | **UseCase & State Ownership** | Each UseCase (`domain/usecases/`) represents one focused business action. Cubits (`presentation/bloc/`) own presentation state transitions (`BlocBuilder` for rendering, `BlocListener` for navigation/dialogs/snackbars) and invoke Domain UseCases | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md), [02 — Dependencies, DI & Contracts](references/02-dependencies-di-and-contracts.md) |
| **A4** | **Explicit Dependency Injection** | Wire dependencies at the module boundary (`lib/modules/<feature>/di.dart` registered via `lib/modules/modules_di.dart`) in strict dependency order: Mapper → DataSource → Repository (bound to abstract Domain interface) → UseCase → screen-scoped Cubit (`registerFactory`) | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md), [02 — Dependencies, DI & Contracts](references/02-dependencies-di-and-contracts.md) |
| **A5** | **Pure Domain & Grounded Core** | `domain/` is pure Dart — zero `package:flutter/*`, `dio`, storage, Data, or Presentation imports. `lib/core/` holds app-wide infrastructure (network, auth, storage, router, core DI); never dump single-feature business logic into `lib/core/` or `lib/commons/` | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md), [02 — Dependencies, DI & Contracts](references/02-dependencies-di-and-contracts.md) |
| **A6** | **Build / Import Lifecycle Purity** | Widget `build()` methods and layout hooks must be pure functions of state — never trigger network calls, Cubit mutations, navigation, or `TextEditingController` creation inside `build()` | [03 — Screens, Adding & Splitting](references/03-screens-adding-and-splitting.md) |
| **A7** | **Explicit Cross-Module Boundaries** | A feature module may consume another module's published Domain UseCase or Entity through the approved dependency contract. Never import another module's private Cubit, State, DataSource, DTO Model, or Repository implementation | [02 — Dependencies, DI & Contracts](references/02-dependencies-di-and-contracts.md) |
| **A8** | **Explicit Data Fetching & Parse Fail-Fast** | DataSources use verified endpoint constants and explicit query/pagination parameters. DTO parsing validates mandatory fields and fails explicitly — never mask missing required API fields with `0`, `""`, `[]`, or fabricated fallback records | [02 — Dependencies, DI & Contracts](references/02-dependencies-di-and-contracts.md) |
| **A9** | **Proportional Layers (Ponytail Minimalism)** | Distinguish `INIT` from `EXTEND`. Create only the layers and DI registrations required by the approved phase behavior; a scoped UI-only extension does not create empty Domain, Data, or DI classes | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md), [03 — Screens, Adding & Splitting](references/03-screens-adding-and-splitting.md) |
| **A10** | **Scope & Cohesive Splitting** | Split files when a single file mixes layers or exceeds structural limits (`{{slot:clean-code}}` C6: ~300 LOC / ~200 LOC per class). Extract cohesive sub-widgets to `presentation/widgets/` rather than stacking helper methods (`_build*`) inside a screen | [03 — Screens, Adding & Splitting](references/03-screens-adding-and-splitting.md) |

---

## 3. Reference Guides

Load only the reference file needed for the current task:

| Reference | Topics Covered |
|---|---|
| [01 — Layout, Boot & Layer Roles](references/01-layout-and-layer-roles.md) | Root directory layout (`lib/main*.dart`, `lib/core/`, `lib/modules/`, `lib/commons/`), boot sequence, feature module structure (`domain/` · `data/` · `presentation/`), layer responsibilities, and 5-step Module DI registration order |
| [02 — Dependencies, DI & Data Contracts](references/02-dependencies-di-and-contracts.md) | Pure Dart Domain rules, layer dependency matrix, `rg` boundary verification, cross-module boundaries, network/DataSource/DTO/Repository error contracts, and Cubit state patterns |
| [03 — Screens, Adding, Splitting & Review](references/03-screens-adding-and-splitting.md) | Screen destination (`*_screen.dart`, `*Screen`) vs. dialog/child widget classification, step-by-step adding/extending a module (`INIT` vs `EXTEND`), splitting oversized files, and `BLOCKER` / `MAJOR` / `MINOR` review rubric |
| [Source Provenance (`manifest.json`)](references/manifest.json) | Reference provenance and starter template inventory (`templates/*.dart.tpl`) |
<!-- {{profile_references}} -->
