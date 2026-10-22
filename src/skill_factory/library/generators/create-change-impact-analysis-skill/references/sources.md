# Sources

External material read when shaping this generator. Ideas are rewritten in this repository's vocabulary (`AC-NN`, `BR-NN`, `Q-NN`, `vN`, Gate 1); nothing is copied.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [Fission-AI/OpenSpec `docs/writing-specs.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/docs/writing-specs.md) | 73k | Three delta kinds — ADDED (new behavior), MODIFIED (existing behavior that changes, given in full), REMOVED (behavior that goes away, with why); look at the current behavior before choosing, because a wrong kind leaves nothing to replace or duplicates a rule | CX7, `04` "Behavior delta" |
| [Fission-AI/OpenSpec `schemas/spec-driven/templates/spec.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/schemas/spec-driven/templates/spec.md) | 73k | A change document lists only the requirements it touches, grouped by delta kind | CX7 (only affected AC are classified; unaffected = Keep) |
| [github/spec-kit `templates/commands/checklist.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/commands/checklist.md) | 142k | When state is changed, ask whether rollback and migration behavior is written down | CX7 (migration note for REMOVED) |

## Not adopted

| Idea | Source | Why not |
|---|---|---|
| Writing ADDED / MODIFIED / REMOVED in the AC delta column | OpenSpec | `validate_proposal_spec` IMPACT-002 accepts Keep / Add / Change / Remove there; the words live in "Behavior delta" and AC rows trace to them. |
| Archiving the delta into a living main spec, and capability retirement | OpenSpec | Coder Nexus keeps each version in its own `vN/` folder; the baseline is the built code at a commit SHA, not a merged spec. |
| Comparing against the previous spec text only | OpenSpec | CX7 compares with the actual code at the baseline revision, because the old design may differ from what was built. |
