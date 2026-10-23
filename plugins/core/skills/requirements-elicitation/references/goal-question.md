# The goal question (Stage 1A-G, first Q-NN)

One `ask_question` call with exactly one question, before any other `Q-NN` (the job-type question, when needed, comes just before it). Keep the body short enough to read in a minute; link long tables instead of pasting them.

## Body, in this order

1. **Your request, in my words** - the read-back, plus any constraint, conflict or cheaper path ([goal candidates §1](goal-candidates.md#1-read-back)).
2. **Read** - one line with confidence and, below ~70%, what is missing.
3. **Sources** - counts per read status, and every `UNREACHABLE` / `NOT_PROVIDED` source by name.
4. **Job type and size** - the Type (and the job-type `D-NN` when one was asked) and the artifact path: `brief.md` or `requirements.md` + `codebase-notes.md`; a split proposal when the split check fired.
5. **Goals** - `G-01..G-03`, each with its success signal.
6. **Non-goals**, **Anti-goals**, **Conflicts** - one short list each, with reasons and cited sources.
7. **Sufficiency summary** (from `grilling`): *Enough for* (what the read sources settle), *Missing* (what only the user can supply; ask to attach or paste it), *Next* (how many questions are queued, by topic).

## Options

| Option | Meaning |
|---|---|
| **Confirm goals (Recommended)** | The goals, non-goals, anti-goals and size stand as shown. |
| **Edit goals** | The user rewrites in their own words; free text is welcome. |
| **Narrow to G-01 only** | Keep the first goal; the others become non-goals or linked work items. |

Recommend Edit instead of Confirm when a missing source could change the goals; say which source.

## Reading the answer

| Reply | Action |
|---|---|
| Confirm | Record `D-NN`; write `## 0. Goals`. |
| Narrow | Record `D-NN`; move the dropped goals to Non-goals with "narrowed by `D-NN`". |
| Edit, or free text | Fold the change in, check it against the sources and the stack, and re-ask the goal question with the revised goals. |
| A missing document is supplied | Read it, add it to the inventory as `READ`, re-check the goals and conflicts, and re-ask. |
| Counter-question | Answer with evidence and re-ask; the question stays open. |
| "Sounds good", "whatever you think", "just start" | Not a decision. Re-ask with the concrete choice between Confirm and Narrow. |

## Writing `## 0. Goals`

Fill the existing table of the `requirements.md` template exactly (`Goal ID | Goal | Success signal | Source | Status`); never rename its heading or columns. Each row has `Status: CONFIRMED` and cites the sources plus the confirming `D-NN`. Below the table, keep the `- **Non-goals**:` line and add `- **Anti-goals**:` when any were confirmed. On the small path, the same content goes in the goal line of `brief.md`.

In the same turn, Stage 1B writes the rest of the `DRAFT` and queues the remaining `Q-NN`, each naming the `G-NN` it serves. The goal-lock rule that governs the rest of the work item lives in `work-item-contract`.
