# Frappe UI codebase scan for Planning

Planning runs this checklist during readiness and gap analysis (core `planning-and-task-breakdown`, reference 01) before writing tasks for a Frappe UI Client.

1. **Desk Page & Router**: Check `src/router.js` or `pages/*.vue`.
2. **Resource Auth & Session**: Check existence of authentication/session resource hooks.
3. **Frappe UI Kit Dependencies**: Verify `frappe-ui` dependency in `package.json` and catalog components (`{{slot:ui-catalog}}`).
4. **Screen work in the plan**: include page/desk route, Frappe UI catalog components, and resource lifecycle checks.
