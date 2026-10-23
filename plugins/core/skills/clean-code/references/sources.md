# Sources

External ideas adapted into this skill, rewritten in Coder Nexus vocabulary (rules CC1–CC15, P1/P2/P3, `D-NN`, READY_FOR_REVIEW, `CHANGES_REQUESTED`). Nothing is copied. Stars as of 2026-10.

Internal base input (read-only): `src/skill_factory/library/generators/create-clean-code-skill/references/base-rules.md` (C1–C17). CC1–CC5 are the user's mandatory structure rules; CC6–CC15 generalise C2–C14.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [mattpocock/skills `skills/engineering/code-review/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md) | 300k | Documented repository standards override a generic smell baseline | [SKILL](../SKILL.md) "Where the rules come from" |
| same | 300k | Smells are labelled heuristics, never hard violations; skip what tooling already enforces | [SKILL](../SKILL.md) note under Rules; self-check step 1 runs the tools first |
| same | 300k | "Middle Man" (a unit that mostly delegates) is cut and the target called directly | CC1 |
| same | 300k | "Mysterious Name": if no honest name comes, the design is unclear | CC6 |
| [addyosmani/agent-skills `skills/code-review-and-quality/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/code-review-and-quality/SKILL.md) | 109k | Backwards-compat shims and no-op variables count as dead code | CC2, CC8 |
| same | 109k | Delete a pass-through wrapper that adds indirection without clarifying anything | CC1, [structure-rules](structure-rules.md) CC1 table |
| same | 109k | Reuse the canonical helper instead of a near-duplicate; keep feature logic out of shared modules | CC4, [structure-rules](structure-rules.md) CC4 step 3 |
| same | 109k | Label every finding with a severity; lead with what matters, few high-conviction findings | "Review severity" |
| same | 109k | Deferred cleanup rarely happens | CC14 + self-check step 3: in-scope hits fixed in the same revision |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Two parallel review sub-agents (standards vs spec) and their report layout | mattpocock code-review | The review process belongs to `review-process`; this skill only supplies the code-quality rules |
| Fowler smells Feature Envy, Shotgun Surgery, Divergent Change, Refused Bequest, Repeated Switches | mattpocock code-review | Module structure and responsibilities belong to `{{slot:clean-architecture}}`; repeating them here would give two owners |
| Primitive Obsession (a small type for every domain primitive) | mattpocock code-review | Pushes speculative types into small tasks; a `D-NN` or the stack's architecture decides domain types |
| Ask before deleting dead code | addyosmani code-review-and-quality | Dead code the task created is removed without asking (CC8); dead code outside the scope is not touched but reported in Concerns (CC14) |
| Approve when the change improves overall code health even if imperfect | addyosmani code-review-and-quality | Verdicts follow the fixed P1/P2/P3 and bug-hunt rules, not a reviewer's overall impression |
| Defer to the author when they disagree | addyosmani code-review-and-quality | No self-approval; disagreements after three rounds escalate through the coordinator |
| Change-size targets (~100 / ~300 / ~1000 lines) and commit-message rules | addyosmani code-review-and-quality | Phase and task size belong to `planning-and-task-breakdown`; commits to the workspace's git rules |
| Reviewer inverts a condition and reruns the suite | addyosmani code-review-and-quality | The reviewer never edits code; missing tests are found by reading and by the test skills |
