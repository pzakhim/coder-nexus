# 08 — Flutter Context Scan and Module Routing

Stack details for the core `feature-planner` context scan (scope classification `INIT` / `EXTEND` / `CORE IMPACT` stays in the core skill) and for the `dev-team` coordinator's Step 0 and Step 2A.

## Detection (Step 0)

- `pubspec.yaml` and `lib/*.dart` identify a Flutter Client (Target Platform: `mobile`). Foundation/UI authority is resolved through [core-usage](../../core-usage/SKILL.md) from Client evidence.

## Workspace scan

Scan the actual Flutter Client at `${workspaceFolder}` before proposing a feature design. Read `pubspec.yaml` for package names and installed dependencies, inspect `lib/modules/` for the business owner, and inspect `lib/core/`, `lib/commons/widgets/`, routing and DI where relevant. Resolve imports from the Client; do not copy a package name or API from an example.

Planning (Step 2A): resolve and record the profile via [core-usage](../../core-usage/SKILL.md), start from `requirements.md` and `codebase-notes.md`, and inspect the target module, router and DI. Only iMESPro runs company setup and reads `../app-*/guidance/GUIDE.md`; external profiles inspect Client foundations or standard Flutter. Planning owns the Data Pipeline architecture (`DataSource`/`Model`/`Repo`/`Cubit`/DI).

## Scope classification — Flutter specifics

| Scope | Flutter design and approval boundary |
|---|---|
| `INIT` | Confirm a lower_snake_case module owner at Gate 2. Use the module blueprint for Domain, Data and Presentation ownership where needed; use Pattern A `BaseBlocState` for a new Cubit and register new DI through `modules_di.dart`. |
| `EXTEND` | An existing Pattern B `Equatable` module stays Pattern B unless migration is approved. |
| `CORE IMPACT` | Shared core/auth/network/storage/boot behavior under `lib/core/`. |

## State and integration scan

Inspect the module's state root: Pattern A extends `BaseBlocState` and concrete states override `equatableProps`; Pattern B extends `Equatable` and uses its existing `props` convention. Check the actual AutoRoute wrapper, router entry, Cubit provision and DI function before naming a new file or constructor. Do not invent routes, callbacks or API methods.

When updating an existing feature's UI design, classify screen destinations with [the screen contract](../../clean-architecture/references/05_screen_contract.md) and record verified base, metadata and layout ownership; do not migrate unrelated historical files.
