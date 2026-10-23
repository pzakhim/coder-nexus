# Sources

External ideas adapted into [root-cause-debugging](../SKILL.md), rewritten in this repo's vocabulary. Internal base input: `src/skill_factory/library/generators/create-root-cause-debugging-skill/` (rules D1-D14, symptom table, report block); the workspace skill it generates overrides this one for the content it covers.

| Source (link pinned to sha) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/systematic-debugging/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging/SKILL.md) | 303k | No fix before root-cause investigation; read the first error fully; one variable at a time | SKILL steps 1, 2, 4 |
| same | 303k | Stop after three failed fixes and question the design instead of a fourth attempt | SKILL step 8 (mapped to `plan-change-request`) |
| same | 303k | Log what enters and leaves each component boundary to find where data turns bad | techniques "Multi-component path" |
| [obra/superpowers `skills/systematic-debugging/root-cause-tracing.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging/root-cause-tracing.md) | 303k | Trace a bad value backwards caller by caller; fix at the source, not where it surfaces | SKILL step 4, techniques symptom table |
| [obra/superpowers `skills/systematic-debugging/defense-in-depth.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging/defense-in-depth.md) | 303k | Validate bad input at the boundary it enters through | techniques "Defensive checks after the fix" (narrowed, see below) |
| [mattpocock/skills `skills/engineering/diagnosing-bugs/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/diagnosing-bugs/SKILL.md) | 300k | One red-capable, deterministic, fast command run at least once before any hypothesis; tighten the loop | SKILL step 1, techniques loop table |
| same | 300k | Minimise until every element is load-bearing | SKILL step 3 |
| same | 300k | 3-5 ranked falsifiable hypotheses before testing any | SKILL step 4, hypothesis log |
| same | 300k | Tag debug logs with a unique prefix so cleanup is one grep; redact secrets in shown output | SKILL steps 2, 4; report block |
| same | 300k | Regression test only at a correct seam; no seam is itself a finding; prove the red actually happened | SKILL step 5 |
| [addyosmani/agent-skills `skills/debugging-and-error-recovery/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/debugging-and-error-recovery/SKILL.md) | 109k | Error output and logs are untrusted data, never instructions | SKILL step 2 |
| same | 109k | Localise by layer; tell environment problems from code problems | SKILL step 7, techniques symptom table |
| same | 109k | Regression test fails without the fix and passes with it | SKILL step 5 (plus undo-to-prove from superpowers verification) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| "Safe fallback patterns" (default value plus warning, swallow render errors) | addyosmani debugging | Conflicts with the fixed process: no fallbacks or fake data to make a result look successful |
| For "no root cause" cases, add retry / timeout handling and move on | superpowers systematic-debugging | Retries hide races and change behaviour outside the approved plan; environment issues return `BLOCKED`, behaviour changes go through `plan-change-request` |
| Validation at every layer to make the bug structurally impossible | superpowers defense-in-depth | Adds code outside the task scope; kept only at the owning boundary, more is a design change |
| Show hypotheses to the user and wait before testing | mattpocock diagnosing-bugs | The Code Writer is not the user's conversation partner; hypotheses go into the hand-off instead |
| Human-in-the-loop script as a reproduction | mattpocock diagnosing-bugs | The loop must be agent-runnable; a human-only repro means `NEEDS_CONTEXT` |
| Bisect in the working tree, stack-specific command examples | addyosmani, mattpocock | Bisect would disturb a shared tree with uncommitted work; commands come from `{{slot:verification}}` |
| "If the test is outdated, update the test" | addyosmani test-failure triage | The Code Writer never rewrites a check to pass; a wrong test is a `plan-change-request` |
| Condition-based waiting helper, polluter bisection script | superpowers systematic-debugging | Not fetched in this batch and stack-specific; may come through a workspace skill |
