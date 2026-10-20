# 01 — Context Scan and Module Routing

Scan the actual Flutter Client at `${workspaceFolder}` before proposing a feature design. Read `pubspec.yaml` for package names and installed dependencies, inspect `lib/modules/` for the business owner, and inspect `lib/core/`, `lib/commons/widgets/`, routing and DI where relevant. Resolve imports from the Client; do not copy a package name or API from an example.

## Scope classification

| Scope | How to recognize it | Design and approval boundary |
|---|---|---|
| `INIT` | No existing module owns the behavior. | Confirm lower_snake_case module owner at Gate 2. Use the module blueprint for Domain, Data and Presentation ownership where needed; use Pattern A `BaseBlocState` for a new Cubit and register new DI through `modules_di.dart`. |
| `EXTEND` | An existing module already owns the behavior. | Preserve its file placement, state convention and consumers. An existing Pattern B `Equatable` module stays Pattern B unless migration is approved. Add only required files. |
| `CORE IMPACT` | The work changes shared core/auth/network/storage/boot behavior. | Identify all affected consumers and compatibility risks. Obtain explicit approval for the material shared change before implementation. |

Classify scope from evidence, not from the ticket title. A UI-only extension may use existing state/DI without creating new Domain/Data classes.

## State and integration scan

Inspect the module's state root: Pattern A extends `BaseBlocState` and concrete states override `equatableProps`; Pattern B extends `Equatable` and uses its existing `props` convention. Check the actual AutoRoute wrapper, router entry, Cubit provision and DI function before naming a new file or constructor. Do not invent routes, callbacks or API methods.
