# 01 — Context Scan and Module Routing

Scan the actual Client at `${workspaceFolder}` before proposing a feature design. Read the dependency manifest for package names and installed dependencies, inspect the feature/module folders for the business owner, and inspect the core, shared-component, routing and DI locations where relevant. The stack's exact scan paths, state patterns and DI anchors are defined by `{{slot:architecture-design}}`. Resolve imports from the Client; do not copy a package name or API from an example.

## Scope classification

| Scope | How to recognize it | Design and approval boundary |
|---|---|---|
| `INIT` | No existing module owns the behavior. | Confirm the module owner (Client naming convention) at Gate 2. Use the module blueprint for Domain, Data and Presentation ownership where needed; use the stack's default state pattern for new state and register new DI through the Client's DI anchor (`{{slot:architecture-design}}`). |
| `EXTEND` | An existing module already owns the behavior. | Preserve its file placement, state convention and consumers. An existing module keeps its state convention unless migration is approved. Add only required files. |
| `CORE IMPACT` | The work changes shared core/auth/network/storage/boot behavior. | Identify all affected consumers and compatibility risks. Obtain explicit approval for the material shared change before implementation. |

Classify scope from evidence, not from the ticket title. A UI-only extension may use existing state/DI without creating new Domain/Data classes.

## State and integration scan

Inspect the module's state root and its existing state convention. Check the actual route wrapper, router entry, state provision and DI function before naming a new file or constructor (stack patterns: `{{slot:architecture-design}}`). Do not invent routes, callbacks or API methods.
