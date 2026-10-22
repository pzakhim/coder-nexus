# Sources

Ideas were rewritten in this repository's vocabulary (`Q-NN`, `D-NN`, Gates, roles); no text was copied.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/brainstorming/builder-check-prompt.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/brainstorming/builder-check-prompt.md) | 303k | A fresh subagent plays the next builder, cannot talk to the author, and reports only the questions where a wrong guess would matter, ranked, skipping what is left to the builder and wording nits, with an explicit "nothing left" answer | [modes/gate-1.md](../modes/gate-1.md), [gate-2.md](../modes/gate-2.md), [gate-3.md](../modes/gate-3.md) prompt shapes; [SKILL.md](../SKILL.md) §2 |
| [obra/superpowers `skills/brainstorming/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/brainstorming/SKILL.md) | 303k | Sort the builder's questions into answered already / minor (the agent settles it and marks it as its own call) / the user's; bring the user's pile back; hand over with the list of the agent's calls; one round of questions per check; read it yourself when no subagent exists | [SKILL.md](../SKILL.md) §3-§4, §2 "No subagent tool" |
| [anthropics/skills `skills/doc-coauthoring/SKILL.md`](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/doc-coauthoring/SKILL.md) | 183k | Reader testing with a fresh instance and no context bleed catches what makes sense only to the authors; checks for ambiguity and context the document assumes; loop back and fix the text | [SKILL.md](../SKILL.md) intro, §2 "Gate documents only", §3 "Answered already" text fixes |

## Not adopted

| Idea | Source | Why not |
|---|---|---|
| The agent settles minor questions freely, including product choices, as long as it marks them | brainstorming | Conflicts with "confirm every inference": business rules, permissions, contracts, states, AC, scope and goals are never minor here and always become `Q-NN` |
| Bring all of the user's questions back in one message | brainstorming | One question at a time through `grilling`; each user's-call question is its own `Q-NN` |
| Predict reader questions and test each with a separate subagent, iterating until the reader answers everything correctly | doc-coauthoring | Too costly per gate and would loop; one reader per gate revision, rerun only after a material change |
| Manual testing in a separate chat when no subagents exist | doc-coauthoring | The author does the cold read and discloses it; no extra user work before a gate |
| Writing the design doc to its own path and committing it | brainstorming | The work-item folder contract fixes the gate documents; nothing is committed before the item branch exists |
| Recording minor calls inside the main document as "the agent's call" sections | brainstorming | Gate documents keep their validated sections; calls go to `codebase-notes.md` → `## 3. Verified Baseline Facts & Cross-Agent Notes` and are listed in the gate presentation |
