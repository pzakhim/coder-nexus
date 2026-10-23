# Sources — grilling

Ideas were rewritten in this repo's vocabulary (`G-NN`, `Q-NN`, `D-NN`, `BR-NN`, `AC-NN`, gates). No text was copied. Star counts as of the research date.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| Internal: former `core/skills/grill-me/SKILL.md` | — | The 4 laws, sufficiency summary, queue order, progress `câu i/N`, batch rule, who-asks-what, reply classification, turn loop, role rules | [SKILL.md](../SKILL.md) §1–§3, §6; [modes/spec.md](../modes/spec.md) §4; [modes/planning.md](../modes/planning.md) §4 |
| Internal: `core/skills/delivery-workflow/references/02_interview_rubric_and_gates.md` (removed; content moved here) | — | 5-group clarify table, multi-screen axes, API count mismatch example, unknown external contracts stay `BLOCKED` | [modes/spec.md](../modes/spec.md) §2–§4 |
| Internal: `core/skills/ui-ux-design/references/01_workflow_interview.md` (read, not edited) | — | Designer topics, one `W-NN` per scenario, viewport question once per project | [modes/designer.md](../modes/designer.md) |
| [mattpocock/skills `grilling/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/grilling/SKILL.md) | 300k | Facts are the agent's job, decisions the user's; a pending lookup blocks only downstream questions; frontier batch where "yes" accepts the recommendations; only independent items in one batch | SKILL §4; [modes/batch-confirm.md](../modes/batch-confirm.md) §2 |
| [mattpocock/skills `grill-me/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/grill-me/SKILL.md) | 300k | Confirms the rename: `grill-me` is only an entry point to `grilling` | Skill name |
| [mattpocock/skills `to-questionnaire/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/to-questionnaire/SKILL.md) | 300k | Ask the user only about the send (recipient, what is needed back); document parts; most important first; one idea per question; "why it matters" only where needed | [modes/questionnaire.md](../modes/questionnaire.md) §2–§3 |
| [addyosmani/agent-skills `interview-me/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/interview-me/SKILL.md) | 109k | Weak replies are not a yes, re-ask as two concrete options; "want versus should want" probe for buzzword answers; stop test (predict the next answers); step back when answers keep surprising | SKILL §3, §5 |
| [github/spec-kit `templates/commands/clarify.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/commands/clarify.md) | 142k | Impact × uncertainty prioritization; a question must stand alone plus one "why it matters" line; "yes" accepts the stated recommendation; replace contradicted text instead of duplicating | SKILL §2.2, §1 Law 4, §3 |
| [anthropics/skills `doc-coauthoring/SKILL.md`](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/doc-coauthoring/SKILL.md) | 183k | Context is sufficient when edge cases can be asked without basics being explained (supports the stop test); fresh-reader testing | SKILL §5 (reader test belongs to `cold-reader-check`) |
| [BMAD-METHOD `bmad-advanced-elicitation/SKILL.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-advanced-elicitation/SKILL.md) | 54k | Never change the document unless the user accepts the proposal | SKILL §3 (close only on a clear pick) |
| [BMAD-METHOD `assets/methods.csv`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-advanced-elicitation/assets/methods.csv) | 54k | Boundary and edge-case sweep, assumption audit as checks a dimension walk must cover | [modes/spec.md](../modes/spec.md) §1 (dimension 4, "mark N/A with a reason") |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Ask the whole frontier in every round | mattpocock `grilling` | Conflicts with "one question at a time"; kept only as the single batch exception for low-risk items. |
| At most 5 questions per session; stop when the user says "done" | spec-kit `clarify` | Conflicts with 0 `OPEN` `Q-NN` before a gate; an early stop would leave unconfirmed inferences. |
| Write answers into a `## Clarifications` section of the spec | spec-kit `clarify` | Decisions live in `codebase-notes.md` → Decision Log; new headings in `requirements.md` are not in the template. |
| Free short answers (≤ 5 words) as a format | spec-kit `clarify` | Free text is accepted but classified (SKILL §3); not promoted as the default. |
| Hypothesis with a confidence percentage before each question | addyosmani `interview-me` | The goal question and the `(Recommended)` option already carry the agent's guess; a number adds noise without a checkable rule. |
| "Statement of intent" restate and save to `docs/intent/` | addyosmani `interview-me` | Covered by the goal question (`requirements-elicitation`) and `requirements.md` → Goals; a second document would compete with the template. |
| Brainstorm 5–20 options per section, numbered curation | anthropics `doc-coauthoring` | Requirements are confirmed, not curated; options belong to `solution-options` with 2–3 choices. |
| Info dump before questions, 5–10 numbered questions at once | anthropics `doc-coauthoring` | Conflicts with one question at a time; sources are read before asking instead. |
| Elicitation method menu (personas, debates, random reshuffles) | BMAD | Adds a menu step and invented personas to every round; the fixed dimension walk covers the same gaps. Pre-mortem style review belongs to `gate-review`. |
| Informed guesses / an Assumptions list to move faster | several | Conflicts with "confirm every inference"; REQ-003 / NOTES-005 reject Assumptions sections. |
