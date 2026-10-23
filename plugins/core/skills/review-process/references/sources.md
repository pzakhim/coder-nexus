# Sources

External ideas adapted into `review-process`, rewritten in this repo's vocabulary (`AC-NN`, `D-NN`, `PHASE-NN`, Gates, `REVIEW_REVISION`). Internal base: `src/skill_factory/library/generators/create-code-review-skill/` (rules R1–R14 in `references/base-rules.md`) and the existing `plugins/core/agents/code_reviewer.md`.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `task-reviewer-prompt.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/task-reviewer-prompt.md) | 303k | Treat the implementer's report as unverified claims; a stated rationale never lowers severity | [SKILL](../SKILL.md) pass 1 |
| same | 303k | Missing / Extra / Misunderstood triad; a listed file without a hunk is Missing | [claims-check](claims-check.md) |
| same | 303k | Requirements not decidable from the diff are reported separately, not assumed met | [claims-check](claims-check.md) `UNVERIFIED` rule |
| same | 303k | Plan-mandated defects are still findings, labelled as such | [SKILL](../SKILL.md) "Findings" (`plan-mandated`) |
| same | 303k | The reviewer does not spawn other reviewers; one review seat per phase | [SKILL](../SKILL.md) end of "Order of passes" |
| same | 303k | Global constraints passed to the reviewer as binding input | [SKILL](../SKILL.md) Inputs, [claims-check](claims-check.md) |
| [obra/superpowers `code-reviewer.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/requesting-code-review/code-reviewer.md) | 303k | "Declined to judge" list so nothing set aside is dropped silently | [SKILL](../SKILL.md) "Report" |
| same | 303k | Strictly read-only on the checkout | [SKILL](../SKILL.md) "Read-only" |
| same | 303k | Issues with the plan itself are reported as plan issues | [SKILL](../SKILL.md) "When a finding conflicts with the plan" |
| [obra/superpowers `requesting-code-review/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/requesting-code-review/SKILL.md) | 303k | Review receives crafted inputs (base/head revision, plan, hand-off), not the writer's session history | [SKILL](../SKILL.md) Inputs |
| [bmad-code-org/BMAD-METHOD `verification-gap.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-build/review-prompts/verification-gap.md) | 54k | Four gap shapes, screen → behaviour → consumers → named regression → read the test, list of things that do not count as a test | [verification-gap](verification-gap.md) |
| [bmad-code-org/BMAD-METHOD `claims-check.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-build/references/claims-check.md) | 54k | Read the plan's claims only after the cold trace; plan is testimony, not evidence; verified claims produce nothing | [claims-check](claims-check.md) intro and last rule |
| [mattpocock/skills `code-review/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md) | 300k | Pin the fixed point and fail early on a bad ref; keep spec conformance and standards as separate passes so one cannot mask the other | [SKILL](../SKILL.md) Inputs (`BLOCKED` on unresolvable revision), passes 3 and 6 kept separate |
| [addyosmani/agent-skills `agents/code-reviewer.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/agents/code-reviewer.md) | 109k | Every blocking finding carries a fix direction; say so when uncertain instead of guessing | [SKILL](../SKILL.md) finding row (`PLAUSIBLE` names deciding evidence) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Do not re-run the tests; trust the implementer's TDD evidence | superpowers task reviewer | Conflicts with the fixed process: hand-off evidence is a claim; the reviewer re-runs the checks on `REVIEW_REVISION` (`evidence-before-claims`) |
| Two separate verdicts (spec compliance, quality) and "Ready to merge: With fixes" | superpowers reviewers | One verdict set only: `APPROVED` / `CHANGES_REQUESTED` / `BLOCKED`; "with fixes" would approve code nobody reviewed |
| Critical / Important / Minor (or Critical / Required / Optional / Nit) severities | superpowers, addyosmani | One scale across roles: bug-hunt `BLOCKER` / `MAJOR` / `MINOR` with `CONFIRMED` / `PLAUSIBLE` |
| Mandatory "Strengths" / praise section | superpowers, addyosmani | Not part of the shared report shape; adds length without changing the verdict |
| A spec's silence means "reasonable user expectation is a requirement" | superpowers code-reviewer | Requirements come only from approved docs and `D-NN`; unconfirmed expectations go to the user as a question, not into a review finding. The "declined to judge" list surfaces them instead |
| Pushing back on the reviewer and acting on feedback | superpowers requesting-code-review | Writer-side behaviour; belongs to `receiving-review` |
| Parallel sub-agents per axis, aggregated without reranking | mattpocock | One reviewer, one seat per phase; passes run in a fixed order instead |
| Fowler smell baseline inside the review | mattpocock | Smells belong to `clean-code` / `code-simplification` and `{{slot:clean-code}}`; the review applies those skills rather than a second list |
| Five dimensions incl. performance as a fixed checklist | addyosmani | Correctness and security are covered by bug-hunt and `secure-coding`; performance blocks only as a concrete bug-hunt failure scenario or a stack rule in `{{slot:code-review}}` |
| JSON output with `kind` / `confidence` high-medium-low | BMAD claims check | Findings use the shared markdown row and `CONFIRMED` / `PLAUSIBLE` |
| No severity on gap findings | BMAD verification gap | Every finding needs a severity for the verdict rules; gaps get `MAJOR` / `MINOR` by what they leave unprotected |
| Reviewer decides deviations are "justified improvements" | superpowers code-reviewer | No reviewer waivers; a deviation is a finding or a `plan-change-request` |
