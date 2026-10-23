# Sources

External ideas behind C15–C17 and the wrapper/alias wording of C1. Ideas were rewritten in this generator's vocabulary (C-rules, P1/P2/P3); nothing is copied. Stars as of 2026-10. C15–C17 themselves are the Coder Nexus user's mandatory structure rules (fixed skill `plugins/core/skills/clean-code`, CC3–CC5); the sources below confirm and sharpen them.

| Source (pinned) | Stars | Idea taken | Where used |
|---|---|---|---|
| [addyosmani/agent-skills `skills/code-review-and-quality/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/code-review-and-quality/SKILL.md) | 109k | Reuse the canonical helper instead of a bespoke near-duplicate; keep feature logic out of shared modules | C16 → 02 "Helper locality" |
| same | 109k | Delete a pass-through wrapper; backwards-compat shims and no-op variables are dead code | C1, C2 (unchanged rules; wording confirmed) |
| same | 109k | Every finding carries a severity so the author knows what blocks | Default severities of C15–C17 (P1 only for exposed internals or mutable global state) |
| [mattpocock/skills `skills/engineering/code-review/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md) | 300k | A documented workspace standard overrides the generic baseline; skip what tooling already enforces | Step 2 mapping: C15–C17 cite a gate (linter rule, export check) when one exists |
| same | 300k | Middle Man: a unit that only delegates is cut | C1 (unchanged) |

## Not adopted

| Idea | Source | Why not |
|---|---|---|
| Fowler smells as judgement-call labels for every rule | mattpocock code-review | C15–C17 are mandatory rules with checks, not heuristics; smells stay in `create-code-simplification-skill` |
| Feature Envy, Shotgun Surgery, Divergent Change | mattpocock code-review | Responsibility and module boundaries belong to `create-clean-architecture-skill` |
| Ask before deleting unused exports or helpers | addyosmani code-review-and-quality | Unused exports added by the task are removed in the task (C2, C17); existing ones outside the task are listed as drift |
| File-size inspection signal (~1000 lines) | addyosmani code-review-and-quality | Thresholds are already owned by 02 with confirmed workspace numbers |
