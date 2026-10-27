# Checklist — incremental-implementation

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Plan root, phase pattern, task format, gates, dependency notation, plan-change process and results file are real paths/notation from the workspace (or a confirmed new plain format)
- [ ] Every rule I1–I17 is expressed with workspace facts or listed under "Not adopted" with a reason; I1, I4, I5, I10, I11, I14, I16 are adopted
- [ ] The pre-flight (Consumes / Produces table) and the triage outcomes are in the workspace's words
- [ ] Task check, phase suite and architecture gate commands exist in the workspace and were confirmed; results are `PASS` / `FAIL` / `NOT_RUN` / `BLOCKED` / `UNVERIFIED`
- [ ] Visual check present only when the workspace has UI
- [ ] The phase-end bug-hunt and simplify lines use the workspace's hand-off notation
- [ ] Sibling skills linked when they exist; missing ones say "not set up in this workspace"
- [ ] `references/01-preconditions-and-preflight.md`, `02-task-loop-and-checks.md` and `03-phase-end-and-handoff.md` are present
- [ ] Coder role files point at the skill (if the user agreed)
