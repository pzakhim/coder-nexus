---
skills:
  - frappe-ui-catalog
---
## Frappe UI rules

### Frappe UI Checks
- Check compliance with `rules/frappe_specific_rules.md` and Frappe UI Catalog (`frappe-ui-catalog`).
- Verify clean separation of Resource/API layer (`createResource` / Mock resource), UI components, and Page/Desk routing (`pages/*.vue` or desk view).
- Reject any hardcoded inline CSS hacks, raw non-Frappe UI widget recreations, or unmanaged asynchronous resource calls.
