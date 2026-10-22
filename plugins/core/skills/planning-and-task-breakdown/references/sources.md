# Sources

Ideas were rewritten in this repo's vocabulary (`AC-NN`, `BR-NN`, `D-NN`, `Q-NN`, `PHASE-NN`, gates). Links are pinned to a commit.

| Source | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/writing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/writing-plans/SKILL.md) | 303k | Plan-level Global Constraints and Review Focus; task interface block (Consumes as the counterpart of Produces); task right-sizing; a step gives signature and pinned values, not bodies; proportion check; type-consistency self-review | `SKILL.md` §2.3–2.4, [04](04_plan_structure_and_task_rules.md) §1, §2, §4, §5, [01](01_phase_slicing_rules.md) §4 |
| [obra/superpowers `skills/executing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/executing-plans/SKILL.md) | 303k | The final reviewer checks the plan's Review Focus lines deliberately; executor checks each Consumes against the matching Produces | `SKILL.md` §3, [04](04_plan_structure_and_task_rules.md) §1, §5 |
| [github/spec-kit `templates/plan-template.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/plan-template.md) | 142k | A gate checked before the plan is accepted; the delivered plan carries no option labels | `SKILL.md` §2.10 |
| [github/spec-kit `templates/commands/plan.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/commands/plan.md) | 142k | Unknowns are resolved before tasks; validation guides do not contain full implementation code | [04](04_plan_structure_and_task_rules.md) §4 |
| [github/spec-kit `templates/commands/tasks.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/commands/tasks.md) | 142k | Field constraints from the data model are written exactly into the task, not left to the implementer | [04](04_plan_structure_and_task_rules.md) §1 (pinned values), §4 |
| [bmad-code-org/BMAD-METHOD `skills/bmad-build/plan-template.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-build/plan-template.md) | 54k | Always/Never boundaries shared by every task (as Global constraints); an input/edge-case matrix (as Review focus); keep the plan short, boundaries over "how" | [04](04_plan_structure_and_task_rules.md) §1, §4 |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Executor makes "rulings" on plan conflicts and keeps going | superpowers executing-plans | Conflicts with "confirm every inference": a plan defect the user must settle is a `Q-NN`, closed into `D-NN` |
| Choice between subagent-per-task and inline execution; per-task commits | superpowers writing-plans / executing-plans | Fixed process: one Code Writer, sequential tasks; commits belong to the coordinator flow |
| Full test code inside the plan's test steps | superpowers writing-plans | The plan names the test and its assertions; test code is the Code Writer's job under `{{slot:unit-test}}` |
| `[P]` parallel markers and Setup / Foundational / Polish phases | spec-kit tasks | Single Code Writer runs in order; a Foundational or Polish phase is a horizontal slice |
| Tests optional unless requested | spec-kit tasks | The Review DoD always requires developer tests ([03](03_review_dod_and_testing.md)) |
| research.md / data-model.md / quickstart.md artifacts and extension hooks | spec-kit plan | `design.md` (Gate 2) and `codebase-notes.md` already hold these facts; one home per fact |
| Append-only change and review-triage logs inside the plan | BMAD plan template | The plan freezes at Gate 3; progress and results go to `as-built.md` |
| Risk level field driving review depth | BMAD plan template | Review depth is fixed by the process; risk is expressed by phase order and each phase's `## Risks` |
