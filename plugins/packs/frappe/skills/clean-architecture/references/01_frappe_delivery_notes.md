# 01 — Frappe UI Delivery Notes (preview, not yet maintained)

Frappe values for the stack placeholders used by the core `dev-team` and `feature-planner` skills.

- **Detection (Step 0):** `package.json` with `"frappe-ui"` or `hooks.py` identifies a Frappe UI Client (Target Platform: `web` Desk). UI Kit Authority: `frappe_ui_kit`.
- **Planning scan (Step 2A):** scan `pages/*.vue`, router, and session/resource hooks.
- **Implementation:** follow this skill's layer rules and `frappe-ui-catalog`; resources via `createResource` / `createDocumentResource`.
- **UI provenance:** match components against the `frappe_ui_kit` catalog.
