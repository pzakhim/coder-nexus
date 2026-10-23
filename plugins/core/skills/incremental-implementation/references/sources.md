# Sources

External ideas adapted into [incremental-implementation](../SKILL.md), rewritten in this repo's vocabulary (gates, `PHASE-NN`, `D-NN`, task fields, Expected triage). Internal base input: `src/skill_factory/library/generators/create-incremental-implementation-skill/` (rules I1-I14 and the handoff template), read-only.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/executing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/executing-plans/SKILL.md) | 303k | Every command has an Expected line; compare real output and branch three ways: matches / code wrong / plan wrong | SKILL §3 triage `MATCH` / `CODE_WRONG` / `PLAN_WRONG` |
| same | 303k | Read the task text again each time; memory is a summary | SKILL §3 step A |
| same | 303k | A progress record that survives lost context; trust it and git history over recollection | SKILL §1 "Resuming", tick line in [pre-flight and hand-off](preflight-and-handoff.md#tick-line) |
| same | 303k | Read the plan's global constraints and review focus before task 1 | SKILL §2 step 1 |
| same | 303k | Completion only with evidence from this session, not from the diff looking right | SKILL §3 step C, §4 step 5 (`evidence-before-claims`) |
| [obra/superpowers `skills/subagent-driven-development/references/preflight.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/references/preflight.md) | 303k | Pre-flight output is a table of produce/consume pairs plus self-consistency rows, not a verdict; "clean" without rows is not a scan | SKILL §2, [pre-flight table](preflight-and-handoff.md#pre-flight-table) |
| [addyosmani/agent-skills `skills/incremental-implementation/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/incremental-implementation/SKILL.md) | 109k | Scope discipline with a "noticed but not touching" list | SKILL §3 hard rules, §5 hand-off |
| same | 109k | Keep the project buildable after every increment | SKILL §3 hard rules |
| same | 109k | Re-running a check on unchanged code adds no information | SKILL §1 "Resuming" (re-run only if the tree changed) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Executor rules on plan conflicts itself and continues, logging a "ruling" | superpowers executing-plans, preflight | Conflicts with no self-approval: a plan defect goes to Planning via `plan-change-request` (`AMENDED` / `ESCALATED`) |
| Continuous execution with no pauses for the whole plan | superpowers executing-plans | One Code Writer runs one approved phase; the phase checkpoint and review are fixed stops. No check-ins between tasks inside a phase is kept |
| Implementer fixes final-review findings in one pass with no re-review | superpowers executing-plans | Every fix is a new revision that invalidates review and test evidence; the Reviewer re-reviews |
| Deferring minor findings at the implementer's discretion; implementer re-grading reviewer severity | superpowers executing-plans | The Reviewer owns verdicts and severity; Code Writer answers findings via `receiving-review` |
| Workspace scripts (`sdd-workspace`, `task-start`, `task-done`) and a separate ledger file | superpowers executing-plans | No runtime scripts in the plugin; the phase file ticks plus git history are the ledger |
| Worktree creation by the executor | superpowers executing-plans | Branch is decided once by `git-preflight` and recorded as a `D-NN` |
| Slicing strategies (vertical, contract-first, risk-first) | addyosmani incremental-implementation | Slicing is Planning's job at Gate 3 (`planning-and-task-breakdown`); the Code Writer executes the approved slices |
| Feature flags for incomplete work | addyosmani incremental-implementation | Only when a `D-NN` in design says so; otherwise it adds unapproved behavior |
| Commit after every slice as a fixed rule | addyosmani incremental-implementation | Commit cadence follows the workspace convention in `git-preflight`; ticks record the revision either way |
| API fixture-server preparation steps inside this skill | previous version of this skill | Stack-specific; moved to the stack part of the Code Writer profile and `{{slot:verification}}` |
