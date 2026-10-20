# 04 — Cross-Module Boundaries and Composition

Apply the approved profile through [core-usage](../../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

> **Sources:** Senior AGENTS, DI and routing rules.
> **Scope:** Dependencies between feature modules and their shared composition root.

## Boundary rules

A feature may consume another module's published Domain use case, entity or parameters through the approved dependency contract. Do not import another module's private Cubit, state, DataSource, DTO or repository implementation. Do not move feature-specific business rules into `lib/core/` or `lib/commons/` to bypass ownership.

## Composition root

`lib/modules/modules_di.dart` registers feature DI functions in the Client's verified boot order. Do not add a second composition root. A new registration requires the approved phase and an inspection of existing consumers.

## UI ownership

Keep widgets used only by one feature under `lib/modules/<feature>/presentation/widgets/`. Move a widget to `lib/commons/widgets/` only when actual multiple-module reuse warrants it and the change is approved. Check the `app_ui_kit` GUIDE (via `core-usage`) and shared widgets before introducing a private widget.
