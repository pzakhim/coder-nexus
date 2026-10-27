# Checklist — implementation-planning

Run this checklist alongside [../../core/checklist-common.md](../../core/checklist-common.md).

- [ ] All rules `IP1`–`IP17` are enforced as mandatory compliance and instantiated with concrete workspace paths, tools, and rationale
- [ ] Fixed planning invariants remain intact: vertical behavior phases, `PHASE-00` first, single `code_writer` executing tasks in order, and `validate_plan_slices` passing (`PASS`)
- [ ] Generated skill uses the 3 cohesive reference files (`references/01-phase-order-and-slicing-strategy.md`, `references/02-task-shape-sizing-and-checks.md`, `references/03-phase-00-readiness-and-dod.md`) and preserves `<!-- {{profile_references}} -->` in `SKILL.md`
- [ ] Layer order inside one vertical behavior (`IP1`) is confirmed and illustrated with a real feature from this repository
- [ ] Every task kind has an executable check command with `cwd` that reports binary `PASS` / `FAIL` (`IP4`)
- [ ] Task sizes `XS`–`XL` are calibrated from repository history with explicit split triggers (`XL`, 8+ files, `"and"` in title, two subsystems) (`IP12`)
- [ ] `## Global constraints` and `## Review focus` sit above `## AC coverage` in `implementation-plan.md` without renaming or removing standard sections (`IP10`, `IP11`)
- [ ] Unpinned spec values or expected results become `Q-NN` before Gate 3, never agent defaults (`IP10`, `IP11`)
- [ ] Tasks specify exact signatures and pinned constants rather than transcribed function bodies (`IP16`), and tests/docs live inside each behavior phase with no final testing/polish phase (`IP17`)
- [ ] `PHASE-00` readiness items are tagged `[EXECUTE]` or `[INFO_NOTE]`, and out-of-workspace changes are recorded as handoffs or `BLOCKED` (`IP5`, `IP8`)
- [ ] `IP7` aligns with `git-workflow` (`G2`, `G3`, `M3`, `M10`): parent-ticket branch naming (`<type>/<PARENT-TICKET>-<short-description>`), verified sub-ticket or accepted-phase commit checkpoints (`<type>(<SUB-TICKET>): <summary> [parent: <PARENT-TICKET>, PHASE-NN]` / `<type>(<PARENT-TICKET>): [PHASE-NN] <summary>` / `<type>(phase-NN): <summary>`), and production merges/tags listed strictly as user-executed commands (`M6`)
- [ ] Plan review findings use strictly `BLOCKER` / `MAJOR` / `MINOR` and CLI verification gates use strictly `PASS` / `FAIL`
