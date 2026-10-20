---
name: clean-architecture
description: Guide Flutter Clean Architecture module structure, contracts and DI using verified Client conventions.
---

# Flutter Clean Architecture

Apply the approved profile through [core-usage](../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Use this skill when creating or extending a Flutter feature module, inspecting project structure, or choosing Domain, Data, Presentation and DI ownership. The Hub blueprint is guidance; the actual Client and approved phase define the implementation scope.

## Before writing code

1. Confirm the same feature version's `requirements.md`, `design.md`, `implementation-plan.md` and linked phase have actual user approvals for their current revisions.
2. Read the approved profile via `core-usage`. Only iMESPro runs company setup and reads company guides. Inspect Client dependencies, target module, router and DI; resolve real imports and APIs.
3. Distinguish `INIT` from `EXTEND`. For a new module, copy the Client's existing Cubit state and DI conventions from a sibling module; for an existing module, preserve its convention unless migration is approved. A UI-only extension does not need empty Domain, Data or DI classes.
4. Call `get_project_structure` with `scope: "module"` and the real lower_snake_case feature name, or `scope: "root"` when root/boot structure is relevant. Compare the returned blueprint with the Client rather than copying it mechanically.
5. Follow the approved UI mapping: fitting iMESPro Kit APIs, existing external Client components, or standard Flutter. Missing an API actually required by the mapping blocks its use; never copy package source.
6. Classify each destination using [the screen contract](references/05_screen_contract.md). Only iMESPro mandates `BaseScreen`/`BaseScreenState`; external profiles follow their approved base/naming policy.

## References

| Topic | Source |
|---|---|
| Root and boot | [01_project_root.md](references/01_project_root.md) |
| Core and network | [02_core_subsystem.md](references/02_core_subsystem.md) |
| Feature module and DI order | [03_feature_module.md](references/03_feature_module.md) |
| Cross-module boundaries | [04_cross_boundaries.md](references/04_cross_boundaries.md) |
| Screen classification and base contract | [05_screen_contract.md](references/05_screen_contract.md) |
| Source provenance | [manifest.json](references/manifest.json) |

## Starter templates

These are iMESPro starter examples. External-structured uses real Client examples; external-standard writes the smallest needed implementation. Use only files required by the approved behavior:

- Domain: `templates/domain/entity.dart.tpl`, `repository.dart.tpl`, `usecase.dart.tpl`.
- Data: `templates/data/data_source.dart.tpl`, `model.dart.tpl`, `mapper.dart.tpl`, `repo_impl.dart.tpl`.
- Presentation: `templates/presentation/state.dart.tpl`, `cubit.dart.tpl`, `screen.dart.tpl`.
- DI: `templates/di/module_di.dart.tpl`.

Resolve every API path, constructor, package import and DataState contract from real Client source. Do not invent endpoints, test data, credentials or fallback values.

## Golden rules

1. Domain is pure Dart and does not import Flutter, Data or Presentation implementations.
2. Use the Client's base data source, endpoint constants, safe parsing helpers, and error wrappers where the real module contract calls for them. Missing mandatory data fails explicitly.
3. For a full new flow, register Mapper → DataSource → Repository under its abstract type → UseCase → screen-scoped Cubit in dependency order. Do not create registrations for components the phase does not need.
4. Resolve the real router, Cubit lifecycle and base-screen hooks when adding a screen. Use `AutoRouteWrapper`/`BlocProvider` only where the Client pattern requires them.
5. Keep the change small and verify the affected architecture, analyzer and tests on the actual code revision.
