# Sources

Ideas were rewritten in this repository's vocabulary (`G-NN`, `Q-NN`, `D-NN`, Gates); no text was copied.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/brainstorming/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/brainstorming/SKILL.md) | 303k | Generate several real approaches, drop the weak ones (including those that work against why the user wants it or that existing work rules out), present 2-3 grounded in the project with trade-offs, recommend one; when there is genuinely one way, say why the others do not fit; any choice the agent makes is never presented as something the user agreed to | [SKILL.md](../SKILL.md) §2-§3, §4 "no silent defaults" |
| [addyosmani/agent-skills `skills/idea-refine/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/idea-refine/SKILL.md) | 109k | Divergent then convergent thinking; lenses (inversion, constraint removal, audience shift, combination, 10x simpler); cluster into 2-3 meaningfully different directions; quality over quantity; honest, not a yes-machine | [divergent-pass.md](divergent-pass.md), [SKILL.md](../SKILL.md) §2 step 3 |
| [mattpocock/skills `codebase-design/DESIGN-IT-TWICE.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/codebase-design/DESIGN-IT-TWICE.md) | 300k | Parallel subagents each given a different design constraint produce radically different interfaces; each returns interface, usage, what it hides, dependencies, trade-offs; compare, recommend, allow a hybrid | [modes/planning.md](../modes/planning.md) "Draft the options" |
| [mattpocock/skills `codebase-design/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/codebase-design/SKILL.md) | 300k | Comparison criteria depth (leverage per unit of interface), locality, seam placement; one adapter means a hypothetical seam, two mean a real one | [modes/planning.md](../modes/planning.md) "Compare" |
| [anthropics/skills `skills/doc-coauthoring/SKILL.md`](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/doc-coauthoring/SKILL.md) | 183k | Start with the part that has the most unknowns (the core decision) before the rest of the document | [modes/spec.md](../modes/spec.md) "When" (scope choice settled before the questions it removes) |

## Not adopted

| Idea | Source | Why not |
|---|---|---|
| Show 5-8 variations (or 5-20 brainstorm items) to the user and let them curate by number | idea-refine, doc-coauthoring | Replaces one decision with many and breaks one question at a time; the wide list stays in working notes |
| "Key Assumptions to Validate" section in the output | idea-refine | Conflicts with "confirm every inference": no Assumptions section; each unconfirmed point is a `Q-NN` |
| One-pager in `docs/ideas/` or a design doc in `docs/superpowers/specs/` with an Approaches part | idea-refine, brainstorming | Work items have a fixed folder contract; options live only in the Decision Log, never in `requirements.md` or `design.md` |
| "10x version at massive scale" lens | idea-refine | Pushes past the confirmed goals (goal lock); only the 10x simpler lens is kept |
| Spike (throwaway build) to choose between approaches | brainstorming | Nothing is built before the gates approve; designer revisions already give the user something to react to |
| Visual companion for side-by-side options | brainstorming | `ui-ux-design` already owns visuals; designer mode describes variants in steps and draws only the chosen one |
| Settling "how it gets made" choices as the agent's own sensible defaults | brainstorming | Conflicts with "confirm every inference"; a default the user never chose becomes a `Q-NN` |
| Mandatory deep-module glossary (module, interface, adapter) | codebase-design | Core stays stack-neutral and uses the workspace's own vocabulary; only the comparison criteria are kept |
