# Base rules (generic, every workspace)

Each rule goes into the generated skill with the workspace's real layout, commands and tools **and its reason**, or is marked "not adopted" with a reason. The fixed `planning-and-task-breakdown` rules (vertical behavior phases, mandatory PHASE-00, AC coverage, one Code Writer running tasks in order, `validate_plan_slices`) always apply.

| # | Rule | Why | Goes into |
|---|---|---|---|
| IP1 | **Order inside a behavior.** The repository's order for the layers one behavior crosses (for example contract → migration → backend → frontend → wiring); phases stay vertical. | The frontend never waits mid-phase for a backend that is not there. | 01 |
| IP2 | **Task shape.** One task = one file scope + what it produces + one check; size guidance from the repository's history, not an invented number. | The Code Writer knows when a task is done. | 02 |
| IP3 | **Paths from clean-architecture.** File paths in tasks follow the workspace's architecture skill; a plan never invents a new structure. | Plans and architecture stay consistent. | 02 |
| IP4 | **A real check per task.** The exact analyzer, linter or targeted test command, with cwd. | A check that cannot run proves nothing. | 02 |
| IP5 | **PHASE-00 items for this workspace.** Environments, test accounts per role, seed data, mock servers, migrations, feature flags — each `[EXECUTE]` or `[INFO_NOTE]`. | Missing readiness stalls the phase halfway. | 03 |
| IP6 | **Definition of Done per phase.** Checks green, tests for the agreed pass/fail data, migration verified on a disposable database when the phase has one, docs updated where required. | Writer and Reviewer share one finish line. | 04 |
| IP7 | **Branch and hotfix tasks.** Branch, base and merge targets come from the `git-preflight` `D-NN`; a production hotfix has explicit tasks for every line that must receive it; merges into production and tags are commands for the user, not tasks. | The plan matches how code reaches each environment. | 01, 04 |
| IP8 | **Out-of-workspace work is a handoff.** Changes in another repository, infrastructure or another team's system are a handoff or `BLOCKED`, never a Code Writer task. | Agents do not change what they may not change. | 03 |
| IP9 | **Unknowns early.** A technical uncertainty is settled in PHASE-00 or the first phase (a probe, a spike), not discovered in the last one. | Risks surface while change is cheap. | 01, 03 |

**Never "not adopted":** IP3, IP4, IP8.
