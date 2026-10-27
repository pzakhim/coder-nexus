# Clean Architecture & Delivery Rules for Flutter Workspaces

Apply the active workspace profile from `.superpowers/setup.json` (`profile` / `architecture_profile`) and the profile-activated references in [clean-architecture](../skills/clean-architecture/SKILL.md).

> **Source:** Senior Flutter Standards · AIFactory-Coder
> **Applies to:** Flutter Client code generated or changed under an approved feature version and behavior phase.

Read the current Client module and the approved `.superpowers/work-items/<slug>/vN/` (or legacy `docs/features/<module>/<feature>/vN/`) requirements, design, and phase before changing code. Existing verified conventions and the approved scope determine which files and layers need work; do not create empty classes or registrations solely to satisfy a checklist.

## 1. Department Routing & Approval Gates

- **Route requests to the matching entry skill**:
  - Full feature delivery (`v1` / `v2+`, including Huly + Figma intake at Gate 1) → `dev-team`
  - L1 / L2 / L3 defect triage & fixing → `bug-squad`
  - Read-only bug or trace diagnosis → `debug-investigation`
  - Read-only scenario testing → `feature-testing`
- **Explicit user approval gates**:
  - Never self-approve Gate 1 (Requirements, Screens `S-NN` & Workflows `W-NN`), Gate 2 (Architecture Design & `## UI/UX mapping`), or Gate 3 (Implementation Plan / `PCR-NN`).
- **Interactive clarification (`ask_question`)**:
  - Ask one focused question at a time (or the 4-item setup batch) and place `(Recommended)` first.

## 2. Unified Statuses, Severities & Evidence Gate

- **Canonical tokens**:
  - Enforce [flags_and_statuses.md](../../../shared_contracts/flags_and_statuses.md) and [api_handshake_protocol.md](../../../shared_contracts/api_handshake_protocol.md).
  - Deterministic CLI tool gates report binary `PASS` or `FAIL`; all code findings and test-case severities use `BLOCKER` / `MAJOR` / `MINOR` (never `P1` / `P2` / `P3`).
- **Fresh revision-bound evidence**:
  - Require fresh command or runtime evidence on the exact reviewed revision before claiming `PASS`, `FIXED`, `APPROVED`, `ACCEPTED`, or `RECORDED`.
  - `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` are never `PASS`; changing code invalidates affected earlier evidence.
- **Data provenance & fail-fast**:
  - Never fabricate business records, source availability, or silent production fallback defaults (`0`, `""`, `[]`) to hide missing data or broken contracts.
  - Approved contract-derived fixtures (`FE_MOCKOON`) support UI/contract checks only; live acceptance (`BE_LIVE`) requires real services.

## 3. Three-Layer Clean Architecture & DI Boundaries

- **Feature home**:
  - `lib/modules/<feature>/{domain,data,presentation}` owns the feature's layers.
  - Add code to `lib/core/` only when two or more modules share a capability approved at Gate 2 with an option comparison; never move feature-specific business rules into `lib/core/` or `lib/commons/`.
- **Domain (`domain/entities/`, `domain/repositories/`, `domain/usecases/`)**:
  - Keep business entities, repository contracts, and use cases 100% independent of Flutter UI, DTOs, Data, and Presentation implementations.
  - Put immutable value entities in `domain/entities/` (using `Equatable` where the module's entity contract calls for value equality).
  - Put required repository contracts and single-action use cases in their approved Domain locations following the active profile's result/error contract.
- **Data (`data/datasources/`, `data/models/`, `data/mappers/`, `data/repositories/`)**:
  - Parse DTOs in `data/models/` with explicit mandatory-field validation.
  - Map `Model → Entity` in `data/mappers/` (add `Entity → Model` only when an approved write contract requires it).
  - Preserve real failures through DataSources and repository implementations according to the active profile's error contract.
- **Presentation (`presentation/bloc/`, `presentation/screens/`, `presentation/widgets/`)**:
  - Do not create a top-level `views/` folder beside the architecture layers.
  - Keep state immutable (`Equatable` or sealed classes matching the module's verified convention); render with `BlocBuilder` and handle side effects (navigation, dialogs, notifications) with `BlocListener`.
  - Follow the active profile's screen base and component reuse rules via [UI kit mapping guide](../skills/ui-kit-mapping/SKILL.md) and [feature module reference](../skills/clean-architecture/references/01-layout-and-layer-roles.md). Missing a base required by the selected profile is `BLOCKED`.
- **Module DI (`di.dart`) & Cross-Module Isolation**:
  - When a behavior requires all five dependency kinds, register them in `di.dart` in dependency order (`Mapper` → `DataSource` → `Repository` bound to its abstract Domain type → `UseCase` → screen-scoped `Cubit` via `registerFactory`) and wire new modules through `lib/modules/modules_di.dart`.
  - Cross-module calls go only through published Domain contracts (entities and use cases); never import another module's `Cubit`, `State`, `DataSource`, `Model`, or repository implementation directly.

## 4. Verification & Test Integrity

- **Keep diffs focused**: Reuse existing platform and module capabilities; format only changed files and avoid unrelated refactors.
- **Multi-screen flow discipline**: For flows spanning multiple screens, document the state owner, navigation/back behavior, failure paths, validation timing, step-up security, and post-flow effects (or mark inapplicable axes `N/A` with a reason).
- **Test & gate integrity**: Never delete, disable, or weaken an assertion merely to make a failing check pass. Verify static analyzer, structural metrics, unit/widget tests, and required runtime visual checks on the reviewed revision per the [Client check contract](../skills/verification/references/01-gates-and-check-contract.md).
