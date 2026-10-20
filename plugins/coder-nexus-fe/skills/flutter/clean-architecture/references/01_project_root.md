# 01 — Project Root and Boot Sequence

Apply the approved profile through [core-usage](../../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

> **Sources:** Clean Architecture and Flutter modular blueprint.
> **Scope:** Root structure of the Flutter Client. Inspect the actual workspace before applying this blueprint.

```text
lib/
├── main_dev.dart, main_stage.dart, main_prod.dart  # Flavor entrypoints when present
├── main.dart                                       # Shared bootstrap
├── app.dart                                        # MaterialApp and router
├── core/                                          # Network, auth, providers, storage, routes, core DI
├── modules/
│   ├── modules_di.dart                            # Feature composition root
│   └── <feature>/                                  # Feature-owned modules
├── commons/                                       # Shared UI and helpers
├── core/constants/                                # Shared constants and API endpoints
```

## Boot order

Initialize `AppConfig` for the selected flavor, then Core DI, background services and feature module DI in the order verified in the Client. Do not introduce a second bootstrap path or put feature business logic in `main.dart` or `app.dart`.

## Tooling and formatting

Read `.fvmrc` and project commands before using FVM; do not assume it is installed. Run only approved generation, analyzer, test and build commands for the affected phase. Format changed Dart files when needed, not the whole repository.
