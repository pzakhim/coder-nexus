# Architecture Discovery, Layer Taxonomy & Splitting Guide

Stack-neutral guide for discovering a workspace's folder structure, mapping responsibilities to layers, defining dependency direction, and decomposing oversized modules.

---

## 1. Universal Layer Taxonomy (For `01-layout-and-layer-roles.md`)

Inspect the workspace's existing directory tree (`layer-first` or `feature-first`) and map its directories onto these canonical responsibilities. Always preserve an existing workspace's verified directory layout (`clean-code` C11) unless the user explicitly approves a migration decision, and render all folder trees using standard box-drawing connectors (`├──`, `│   `, `└──`):

```text
# Feature-First (Modular) Layout          # Layer-First Layout
<source_root>/                            <source_root>/
├── core/                                 ├── core/
└── modules/                              ├── delivery/
    └── <feature>/                        ├── application/
        ├── domain/                       ├── domain/
        ├── data/                         └── data/
        └── delivery/
```

| Canonical Layer | Typical Responsibilities | Must Never Contain |
|---|---|---|
| **Entry / Presentation / Delivery** | Route/endpoint handlers, screens/views, UI widgets, request/input binding, view-state rendering, and error-to-response/UI translation. | Direct database/storage queries, business policy calculations, or unmapped raw DTO/ORM objects. |
| **Application / Use Case / State Holder** | Orchestrating one business action or screen flow, authorization/precondition checks, transaction/unit-of-work boundary, and state emission. | Transport-specific protocol objects, raw SQL/storage driver calls, or UI layout markup. |
| **Domain (Contracts & Entities)** | Pure business entities, value objects, domain error hierarchy, and abstract repository/service contracts (when multiple implementations exist). | Framework, UI, transport, or persistence library imports. |
| **Data / Persistence / Infrastructure** | Repository implementations, remote/local data sources, storage models/tables, DTO-to-domain mappers, and external provider adapters. | UI state, transport routing, or cross-aggregate transaction commit decisions. |
| **Core / Shared Foundation** | Application bootstrap, DI composition root, typed configuration/settings, logging, and cross-cutting primitives used by 2+ features. | Feature-specific business rules or generic `utils`/`helpers` dumping grounds (`clean-code` C16). |

---

## 2. Dependency Direction & Verification Gates (For `02-dependencies-di-and-contracts.md`)

Dependencies point strictly inward/downward toward stable contracts (`Entry → Application → Domain ← Data`, with `Core` depended on by outer layers and depending on nothing above it).

### Constructing the Dependency Matrix
For each directory in the confirmed layout, document:
1. **May import:** The exact sibling or inner layers it is permitted to import.
2. **Never imports:** The outer or sibling layers it is forbidden from importing.
3. **Why:** The concrete failure or coupling prevented by the boundary.

### Deterministic Boundary Verification
1. **Architecture Validator / Import Linter Gate (`PASS` / `FAIL`):** Use the workspace's configured architecture validator or import-boundary linter when present.
2. **Ripgrep (`rg`) Boundary Audit (`PASS` / `FAIL`):** Define exact `rg -n` commands that scan inner layers (`domain`, `application`, `data`, `core`) for forbidden imports of outer layers or external frameworks. Every boundary command must return zero hits (`exit != 0` on `rg` when no matches are found, or empty output) on changed files.

---

## 3. Adding Features & Splitting Oversized Modules (For `03-adding-splitting-and-review.md`)

### Step-by-Step Feature Addition Order
Order tasks inside an implementation phase from inner contracts to outer delivery so each step compiles and passes its own unit check (`incremental-implementation`):
1. **Domain / Contract:** Entities, domain errors, or schemas/contracts.
2. **Data / Persistence:** Storage models, migrations (if applicable), data sources, mappers, and repository implementations + unit/integration tests.
3. **Application / Use Case / State Holder:** Business orchestration, state transitions, and unit tests.
4. **Delivery / Entry + DI Wiring:** Route/screen/handler, composition-root registration, and boundary tests.

Skip any layer the approved behavior does not require (**A10**).

### Splitting Oversized Files (`clean-code` C6 Coordination)
Size thresholds are owned by `clean-code` (`01-structure-naming-and-types.md`). When a file exceeds the threshold or accumulates multiple reasons to change:
1. **Split by responsibility, not arbitrary line ranges:** Separate distinct sub-resources, use-case groups, query vs. command paths, or cohesive sub-components.
2. **Place each extracted file in its owning layer** per the role table in `01-layout-and-layer-roles.md`.
3. **Update all callers in the same task and delete the old symbol location**—never leave pass-through wrapper files or compatibility re-export shims (`clean-code` C1, C17).
