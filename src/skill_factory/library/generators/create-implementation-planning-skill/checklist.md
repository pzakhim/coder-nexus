# Checklist — implementation-planning

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule IP1–IP9 is adopted, adapted, or "not adopted" with a reason; IP3, IP4 and IP8 are adopted
- [ ] The fixed process is unchanged: vertical phases, PHASE-00 first, one Code Writer in order, `validate_plan_slices`
- [ ] The order inside a behavior was confirmed and shown on a delivered feature
- [ ] Every kind of task has a check command that runs, with cwd
- [ ] Task-size guidance comes from the repository's history
- [ ] PHASE-00 items are the ones this workspace needs, labelled `[EXECUTE]` / `[INFO_NOTE]`
- [ ] Production merges and tags appear only as commands for the user
- [ ] Branched layout keeps `be/` and `fe/` parallel; shared rules live in `shared/`
