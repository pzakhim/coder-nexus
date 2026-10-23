---
name: cold-reader-check
description: Before presenting Gate 1, 2 or 3, spawns one fresh read-only subagent that gets only the gate documents (no conversation), cannot ask the author, and lists the questions it would need answered to do the next role's job. The author sorts each question into answered already (point to or improve the text), minor (agent decides, recorded as the agent's call in codebase-notes.md) or user's call (new OPEN Q-NN, so the gate waits). Use in Spec Writer before Gate 1 and in Planning before Gates 2 and 3. It never approves anything.
---

# Cold reader check

The author of a document knows things the document does not say. A reader with no conversation finds those gaps before the next agent has to guess. This check tests the document, not the work: it adds questions, never approval.

## 1. When

Run once per gate, when the document is otherwise ready to present: 0 `OPEN` `Q-NN`, validators pass, and the gate's `gate-review` (when it runs for this gate) is done. Running it last means the reader sees what the user will see.

| Gate | Author | Gate documents | Reader plays | Prompt |
|---|---|---|---|---|
| Gate 1 | `spec_writer` | `requirements.md`, `codebase-notes.md` (and the approved `design-uiux/uiux.md` revision when Gate 1 includes it) | `planning` | [modes/gate-1.md](modes/gate-1.md) |
| Gate 2 | `planning` | `design.md` | `code_writer` | [modes/gate-2.md](modes/gate-2.md) |
| Gate 3 | `planning` | `implementation-plan.md`, `phases/*.md` | `code_writer` | [modes/gate-3.md](modes/gate-3.md) |

Small phase-free items whose Gate 1 approves `brief.md` use the Gate 1 prompt with `brief.md` as the gate document.

## 2. Spawn the reader

- **One fresh subagent, read-only.** It writes no files, runs no state-changing command and talks to no one.
- **Gate documents only.** Pass their paths and, for Gates 2 and 3, the already approved documents as context (named as approved). It may open files those documents cite by path, to check that a cited fact exists, but not to fill a gap the document leaves. Never pass the conversation, your notes or your summary. Reason: whatever you add is context the real next agent will not have.
- **Tell it it cannot ask the author.** It reports only questions where it would otherwise have to guess and a wrong guess would change its work. It skips what the document explicitly leaves to its role, what it can decide itself, and wording nits.
- Use the prompt shape in the gate's mode file; fill in the placeholders and nothing else.
- **No subagent tool?** Read the gate documents yourself as that role, from the top, with the same prompt, and say in the gate presentation that the cold read was done by the author. Reason: a self-read is weaker and the user should know.

## 3. Sort every question

Sort each reported question yourself; the reader does not decide where it goes.

| Pile | Test | Action |
|---|---|---|
| Answered already | The answer is in a gate document, a `D-NN` or a cited source | Point to it. If the reader missed it because the text is unclear, rewrite that text so it says the same thing more plainly. Never change behavior here |
| Minor | The next role could settle it without changing what the user sees, approved, or can measure, and no `D-NN` covers it | Decide it yourself and record it in `codebase-notes.md` → `## 3. Verified Baseline Facts & Cross-Agent Notes` as `Agent's call (cold-reader-check, Gate N): <question> → <decision> — <reason>`. Update the gate document if it should state the decision |
| User's call | Only the user can answer it, or the answer changes behavior, scope, a goal, or an approved revision | Queue a new `OPEN` `Q-NN` (owner by `grilling` ownership) and ask it through `grilling`, one at a time. The gate waits for 0 `OPEN` rows |

Never minor, whatever the reader thinks: business rules, permissions and data scope, money, data loss, external or API contracts, observable states, acceptance criteria, scope and goals. Reason: these are the decisions "confirm every inference" exists for. When unsure between minor and user's call, it is the user's call.

## 4. Close the loop

1. Apply the answers and text fixes, then rerun the gate's validators (and the sections `gate-review` checks, if the text moved).
2. One round per gate revision. Run the check again only when the user's answers changed a goal, a workflow, the design's architecture or the phase list; otherwise present.
3. In the gate presentation, say the check ran and give the counts per pile, list every agent's call so the user can review them while reading, and name the new `D-NN` that came from it.

## 5. Limits

- The check never approves, never marks a document `APPROVED`, and never replaces the user's gate answer. "Nothing important left" means the reader found no gap, not that the document is right.
- It does not judge quality or compliance; that is `gate-review`. It does not hunt code defects; that is `{{slot:bug-hunt}}`.
- It adds no new section or heading to any gate document or template.

## References

- [modes/gate-1.md](modes/gate-1.md), [modes/gate-2.md](modes/gate-2.md), [modes/gate-3.md](modes/gate-3.md)
- [references/sources.md](references/sources.md)
