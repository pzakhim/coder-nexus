# Sources

Ideas rewritten in this repo's vocabulary (`PCR-NN`, `D-NN`, `Q-NN`, `PHASE-NN`, gates). Links are pinned to a commit. Internal base input: `src/skill_factory/library/generators/create-incremental-implementation-skill/references/base-rules.md` (rules I5 "a mapped component that does not fit is a planning blocker, never a local workaround" and I11 "a contract change goes back to its gate").

| Source (link pinned to sha) | Stars | Idea taken | Where used |
|---|---|---|---|
| [bmad-code-org/BMAD-METHOD `skills/bmad-build/plan-template.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-build/plan-template.md) | 54k | Human-owned intent is frozen after approval; an append-only plan change log records the trigger, the amendment and the known-bad state it avoids | SKILL §3 (frozen = escalate), §4 step 4; log format in `work-item-contract` plan-and-task-contract §5 |
| [bmad-code-org/BMAD-METHOD `skills/bmad-build/step-04-review.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-build/step-04-review.md) | 54k | Split review findings by root cause: gap in frozen intent goes back to the human, plan defect amends the non-frozen plan; read all earlier log entries before amending; loop cap then escalate | SKILL §3 (`SCOPE_CHANGE` / `DESIGN_CHANGE` vs `TASK_DETAIL`), §4 step 1, §7 |
| [bmad-code-org/BMAD-METHOD `skills/bmad-build/step-03-implement.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-build/step-03-implement.md) | 54k | Never edit a test expectation to match the code; ambiguous expectation stops and asks | SKILL §2 (no edited check or Expected) |
| [obra/superpowers `skills/executing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/executing-plans/SKILL.md) | 303k | Three outcomes after a step's Expected line: matches, code wrong, plan wrong; the plan-wrong cases (contradicts spec, interface mismatch, command cannot work) | SKILL §1 triggers; triage in plan-and-task-contract §3 |
| [obra/superpowers `skills/subagent-driven-development/references/handling-reports.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/references/handling-reports.md) | 303k | A blocked report needs something to change before re-dispatch; context gap vs task too large vs plan wrong | SKILL §1 "Not a plan change", §6 |
| [obra/superpowers `skills/subagent-driven-development/implementer-prompt.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/implementer-prompt.md) | 303k | Stop and escalate on decisions with several valid approaches or restructuring the plan did not foresee; say what was tried and what is needed | SKILL §1, §2 |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Executor rules on plan conflicts itself and keeps going, ledgering the ruling | superpowers executing-plans | Conflicts with no self-approval: the Code Writer stops; only Planning amends `TASK_DETAIL`, and the user decides anything frozen |
| "Continuous execution" without checking in between tasks | superpowers executing-plans | The fixed process asks the user before each next phase; a pending request pauses the phase |
| Revert all code and re-derive it from the amended plan on every plan defect | BMAD step-04 | Too broad for a `TASK_DETAIL`; only affected tasks are unticked and redone. A re-approved design still restarts the phase |
| Loop cap of 5 review iterations | BMAD step-04 | The process cap is 3 review rounds per phase |
| Auto-patching small findings without a plan entry | BMAD step-04 | Every fix is a new revision through review; a plan conflict is never patched around |
| Re-dispatch with a more capable model as the answer to a blocked task | superpowers handling-reports | Model choice belongs to the host coordinator; this skill only routes plan defects |
| Deferred-work file for pre-existing issues | BMAD step-04 | Out of scope for a plan change; pre-existing defects are reported by the reviewer, not planned here |
