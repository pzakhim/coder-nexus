# Sources

External ideas behind IP10–IP17. Ideas were rewritten in Coder Nexus vocabulary (`G-NN`, `BR-NN`, `AC-NN`, `Q-NN`, `D-NN`, `PHASE-NN`, gates); nothing is copied. Stars as of 2026-10.

| Source (pinned) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/writing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/writing-plans/SKILL.md) | 303k | Plan header with item-wide constraints copied verbatim and inherited by every task | IP10 → 01 "Plan header" |
| same | 303k | A short list of inputs the spec implies but no test covers, each pinned by a test in the owning task | IP11 → 01, 02 |
| same | 303k | Split only where a reviewer could reject one task and approve its neighbour; fold setup and docs into the task that needs them | IP12 → 02 "Size" |
| same | 303k | Steps carry signatures, pinned values and test assertions, not bodies; a plan longer than its code is a transcript | IP16 → 02 "Shape" |
| [addyosmani/agent-skills `skills/planning-and-task-breakdown/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/planning-and-task-breakdown/SKILL.md) | 109k | XS–XL size scale; split on XL, "and" in the title, two independent subsystems | IP12 → 02 "Size" |
| same | 109k | High-risk tasks early (fail fast) | IP13 → 01 |
| [mattpocock/skills `skills/engineering/to-tickets/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/to-tickets/SKILL.md) | 300k | Prefactor first ("make the change easy, then make the easy change") | IP14 → 01, 02 |
| same | 300k | Wide refactors as expand → migrate in batches sized by blast radius → contract, each batch its own unit | IP15 → 01 |
| [github/spec-kit `templates/tasks-template.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/tasks-template.md) | 142k | Phases grouped by independently testable behavior, each with its own checkpoint (confirms the fixed vertical slicing) | IP17 (counter-example: its final "Polish" phase) |
| [Fission-AI/OpenSpec `schemas/spec-driven/templates/tasks.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/schemas/spec-driven/templates/tasks.md) | 73k | Numbered checkbox tasks inside groups — already the phase-file task format; nothing new taken | — |

## Not adopted

| Idea | Source | Why not |
|---|---|---|
| `[P]` parallel markers and parallel tracks | spec-kit, agent-skills | One Code Writer runs the tasks of a phase in order; the fixed process forbids `[PARALLEL]` tracks and join points. |
| Final "Polish & cross-cutting" phase; tests optional unless requested | spec-kit | A final phase is a horizontal slice and tests are part of every phase's Definition of Done (IP6, IP17). |
| "Expected behavior a reasonable person would expect" and "the implementer makes a reasonable choice" where the plan is silent | superpowers | Conflicts with "confirm every inference": a missing expected result or value becomes a `Q-NN` before Gate 3. |
| Fixed "no task touches more than ~5 files" limit | agent-skills | IP2/IP12 take sizes from the repository's history; 8+ files is only a split trigger. |
| Checkpoint plus human review every 2–3 tasks | agent-skills | Phases are the checkpoints and Gate 3 is the human review; extra stops inside a phase are not part of the process. |
| TDD step list and a commit step per task | superpowers | Test-writing belongs to `unit-testing` / `incremental-implementation`; commits belong to `git-workflow`. |
| Choosing an execution mode (subagent per task or native) | superpowers | The fixed process has one Code Writer and a separate Code Reviewer. |
| Avoid file paths in tasks | to-tickets | IP3 requires real paths from `clean-architecture`. |
| Shared integration branch when migrate batches cannot stay green | to-tickets | Every task must keep its check green (IP4); branches belong to `git-workflow`. |
| Publishing tasks to a tracker; "never overwrite an unfinished plan" | to-tickets, agent-skills | Trackers and versions (`vN/`) are owned by `work-item-contract` and the ticket runner. |
