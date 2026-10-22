# Checklist — implementation-planning

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule IP1–IP17 is adopted, adapted, or "not adopted" with a reason; IP3, IP4, IP8 and IP17 are adopted
- [ ] The fixed process is unchanged: vertical phases, PHASE-00 first, one Code Writer in order, `validate_plan_slices`
- [ ] The order inside a behavior was confirmed and shown on a delivered feature
- [ ] Every kind of task has a check command that runs, with cwd
- [ ] Task sizes XS–XL come from the repository's history; split triggers stated (XL, 8+ files, "and" in the title, two subsystems)
- [ ] Global constraints and Review focus are added as new sections; no template or validated section is renamed or removed
- [ ] Missing spec values or expected results become `Q-NN`, never defaults
- [ ] No final testing, docs or polish phase; no `[P]` parallel markers
- [ ] Tasks carry signatures and pinned values, not function bodies
- [ ] PHASE-00 items are the ones this workspace needs, labelled `[EXECUTE]` / `[INFO_NOTE]`
- [ ] Production merges and tags appear only as commands for the user
- [ ] Branched layout keeps `be/` and `fe/` parallel; shared rules live in `shared/`
