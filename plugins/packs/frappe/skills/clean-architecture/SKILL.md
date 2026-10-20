---
name: clean-architecture
description: Layered architecture, resource management, and Vue 3 conventions for Frappe UI applications.
---

# Frappe Clean Architecture

Provides architectural boundaries and conventions for Frappe UI (Vue 3 + Tailwind) frontend applications.

## 1. Directory Structure

A standardized Frappe UI frontend resides within `frontend/src/`:
```
frontend/src/
├── components/          # Reusable Vue 3 presentational widgets
├── pages/               # Top-level Desk pages and views
├── dialogs/             # Modal dialogs and action sheets
├── resources/           # Frappe createResource API bindings
├── stores/              # Pinia global stores (auth, user session)
└── router/              # Vue Router configuration
```

## 2. Layer Separation

- **Data Layer (`resources/`)**:
  - Encapsulates Frappe REST calls (`frappe.client.get`, custom whitelisted methods).
  - Uses `createResource` or `createListResource`.
- **Presentation Layer (`components/` & `pages/`)**:
  - Pure Vue 3 `<script setup lang="ts">`.
  - Consumes resources and renders UI states using Tailwind CSS and `frappe-ui` widgets.
- **State Flow**:
  - Local state in `ref` / `reactive`.
  - Shared domain state in Pinia stores.
  - Server state managed reactively by Frappe resources.

## 3. Delivery Notes for Core Skills

Stack values used by the core coordinator and planner (detection, scan targets, UI provenance): [01_frappe_delivery_notes.md](references/01_frappe_delivery_notes.md).

## Planning Codebase Scan

Planning's stack-specific readiness checklist (desk routes, resource auth, Frappe UI dependencies, screen checks in the plan): [planning_codebase_scan.md](references/planning_codebase_scan.md).
