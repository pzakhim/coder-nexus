# Checklist — change-impact-analysis

Run this and [../../core/checklist-common.md](../../core/checklist-common.md).

- [ ] Every rule `CX1`–`CX7` is enforced as mandatory compliance with the workspace's real tools, paths, and reason
- [ ] The impact map (`references/01-impact-map-and-tracing-recipes.md`) lists all present categories with real folders and commands, and names or asks about external consumers
- [ ] Each tracing recipe (`references/01-impact-map-and-tracing-recipes.md`) has runnable `rg` or dependency-graph commands with working directory
- [ ] Hit classification, contract break flags, `Q-NN` unknown escalation, and regression suites (`references/02-classification-and-regression-selection.md`) map to real modules and commands
- [ ] The fixed `change-impact.md` sections (`references/03-writing-change-impact-and-gates.md`) use `ADDED` / `MODIFIED` / `REMOVED` behavior deltas against built code (with data/user migration for `REMOVED`) and `Add` / `Change` / `Remove` / `Keep` AC deltas
- [ ] Review findings use strictly `BLOCKER` / `MAJOR` / `MINOR` and deterministic CLI checks use `PASS` / `FAIL`
- [ ] `SKILL.md` links to the 3 cohesive reference files and retains `<!-- {{profile_references}} -->`
- [ ] The trial re-analysis was compared with a real past change
