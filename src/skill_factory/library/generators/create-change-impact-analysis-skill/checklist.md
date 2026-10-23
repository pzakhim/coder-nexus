# Checklist — change-impact-analysis

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule CX1–CX7 is adopted, adapted, or "not adopted" with a reason; CX1 and CX6 are adopted
- [ ] The impact map lists only categories the workspace has, with real folders and commands
- [ ] External consumers are named or asked about
- [ ] Each tracing recipe has runnable commands with cwd
- [ ] Regression suites map to modules with real commands
- [ ] The fixed `change-impact.md` sections are kept; the skill says how to fill them
- [ ] Behavior delta rows use ADDED / MODIFIED / REMOVED against the built code; AC delta rows use Add / Change / Remove / Keep and trace to them; each REMOVED row says what happens to existing data and users
- [ ] The trial re-analysis was compared with a real past change
