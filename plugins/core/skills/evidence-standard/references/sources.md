# Sources

External ideas adapted into [evidence-standard](../SKILL.md), rewritten in this repo's vocabulary. Internal base inputs: the evidence and status rules of [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) and the reporting rules of `src/skill_factory/library/generators/create-quality-reporting-skill/` (NOT_RUN and BLOCKED never count as passed).

| Source (link pinned to sha) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/verification-before-completion/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion/SKILL.md) | 303k | No completion claim without fresh verification; identify, run, read, verify, then claim | SKILL section 1 |
| same | 303k | Claim-to-evidence table: build, lint and tests do not prove each other; agent reports are not evidence | SKILL section 2 |
| same | 303k | Regression test proven by red-green with the fix reverted | SKILL section 2 row "Regression test" |
| same | 303k | Requirements met only after re-reading the plan into a line-by-line checklist | SKILL section 4 |
| same | 303k | Hedging words and early satisfaction are stop signals | SKILL section 5 |
| [mattpocock/skills `skills/engineering/diagnosing-bugs/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/diagnosing-bugs/SKILL.md) | 300k | Redact secrets in shown output; quote only the lines that carry the signal | SKILL section 3 "Key output" |
| [addyosmani/agent-skills `skills/debugging-and-error-recovery/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/debugging-and-error-recovery/SKILL.md) | 109k | Verify end to end: targeted test, full suite, build, then the real scenario | SKILL section 2 (separate rows per kind of check) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| "Run the verification in this message" as the freshness rule | superpowers verification | Hand-offs cross agents and sessions; freshness is bound to the named revision instead |
| Committing or opening a PR as the trigger point | superpowers verification | Commits and PRs are gated by `git-preflight` and the coordinator; the trigger here is any status claim or tick |
| Stack-specific example commands | superpowers, addyosmani | Commands come from the task's Acceptance Criteria and `{{slot:verification}}` |
