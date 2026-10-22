# Checklist — unit-testing

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule U1–U14 is adopted, adapted, cited as enforced by a gate, or "not adopted" with a reason; U2, U4, U5, U6, U12 are adopted
- [ ] The per-layer matrix uses the workspace's real layers and paths, with happy + each handled failure + edges
- [ ] Location and naming come from the real test tree; drift listed
- [ ] Doubles policy names real ports/fakes/fixtures; the subject, authorization and DB are never mocked away
- [ ] Only installed frameworks/libraries are used; no second framework
- [ ] Focused and full commands exist; "confirm the new test ran" is concrete
- [ ] The task-level check in incremental-implementation (if present) matches the focused command
- [ ] What unit tests cannot prove is stated, with who covers it (or "not set up")
