---
skills:
  - frappe-ui-catalog
---
## Frappe UI rules

### Frappe UI Architecture Rules
1. Follow `{{slot:clean-architecture}}`, `frappe-ui-catalog`, and `rules/frappe_specific_rules.md`.
2. Structure implementation into Resources (`createResource` / `createDocumentResource` / Mock Resource) -> UI Components (Frappe UI buttons, controls, dialogs) -> Page/Desk routing (`pages/*.vue` or desk view).
3. Use only catalogued Frappe UI components. Prohibit inline custom CSS or unapproved low-level HTML tags when standard Frappe UI controls exist.
