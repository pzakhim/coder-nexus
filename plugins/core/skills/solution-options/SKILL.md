---
name: solution-options
description: Lays out 2-3 real, materially different ways to meet the confirmed goals, each with its trade-offs and a recommendation, asks the user to pick one as a single Q-NN, and records the choice as D-NN with the rejected options in the Decision Log "Options Considered" column. Use in Spec Writer (behavior and scope options, after the goals are confirmed and before the draft is final), Planning (technical options at Gate 2) and Designer (UI flow variants), only when more than one sensible way exists.
---

# Solution options

Your first idea is rarely the only good one, and the user cannot reject an approach they never saw. This skill makes the choice between real alternatives explicit, one decision at a time, without ever leaving options inside `requirements.md` or `design.md`.

Run the mode for your role: [Spec Writer](modes/spec.md) · [Planning](modes/planning.md) · [Designer](modes/designer.md).

## 1. When to run

| Role | Moment | Kind of option |
|---|---|---|
| `spec_writer` | After the goal `D-NN` is recorded, while `requirements.md` is still `DRAFT` | Behavior and scope only |
| `planning` | Gate 2, after the codebase scan, before `design.md` is written | Technical (architecture, contract, component) |
| `designer` | Workflow interview, before anything is drawn | UI flow variants |

Run it only when **more than one materially different way** meets the confirmed `G-NN` goals. Materially different means the options change something the goal owner cares about: what the actor sees or can do, scope, cost, risk, reversibility, or where future change lands. Different names, wording or file layout for the same idea are not options.

Do not run it when:

- **One way is forced by a verified fact** (an existing contract, a foundation class, an approved `D-NN`). Record the fact and its evidence in `codebase-notes.md` → `## 3. Verified Baseline Facts & Cross-Agent Notes`; no question. Reason: asking about a settled fact wastes a question.
- **One way is obvious but not stated by the user.** It is an inference, not an option: queue a normal `Q-NN` through `grilling` (confirm every inference).
- **The topic serves no goal.** Record it under Non-goals (goal lock).

## 2. Build the options

1. **Ground first.** Read the sources, `## 1. Decision Log (D-NN)` and the code the change touches. Never offer an option an existing `D-NN` or verified fact already rules out.
2. **Optional divergent pass.** When the first options you see are variants of one idea, widen first with the lenses in [divergent pass](references/divergent-pass.md), then converge. The wide list stays in your working notes; only the converged options reach the user.
3. **Keep 2-3 real options.** Each one must meet every confirmed goal and constraint. Drop strawmen, options that break a `D-NN`, and options that work against the reason for the goal. Reason: a weak option placed next to the favorite steers the user instead of informing them.
4. **Describe each option the same way** (rows of the comparison table):

| Field | Content |
|---|---|
| What it is | One or two sentences in the asker's vocabulary (user terms for spec and designer) |
| Goals | Which `G-NN` it meets fully or partly |
| Gains | What it makes easy or cheap |
| Costs | What it makes harder, slower, riskier or irreversible |
| Evidence | The source, `D-NN` or file that supports the claims |

5. **Recommend one** and say why, tied to a goal or evidence. A hybrid may be one of the options when parts of two combine cleanly; name it as its own option.
6. **Only one sensible way after all?** Say so in one line with why the others do not fit, and treat it as an inference to confirm (step 1 bullets above).

## 3. Ask and record

- The choice is **one `Q-NN`** in `codebase-notes.md` → `## 0. Question Queue (Q-NN)`, owned by the asker (`grilling` ownership), with the recommended option in `Recommended Option`. Ask it alone through `grilling`: one question, `(Recommended)` first, each option with its trade-off in one line.
- Counter-questions, custom answers and changes to an earlier `D-NN` follow the `grilling` reply classification. Never close the `Q-NN` on a counter-question.
- On a clear choice: `Q-NN` → `CLOSED -> D-NN`. In `## 1. Decision Log (D-NN)`, `Options Considered` lists **every** option presented, recommended first, each with its main trade-off and, for rejected ones, why it lost. `User Confirmed Decision` holds only the chosen option.
- Write the chosen option into the gate document in one straight line citing `D-NN`: `requirements.md` (`BR-NN`, scope, `AC-NN`), `design.md` (`## Architectural decision`), or the `W-NN` steps in `uiux.md`.

## 4. Rules that never bend

- Never write `Option A / Option B`, an options table, `TBD` or a recommendation without a decision into `requirements.md` or `design.md`. Rejected options live only in the `Options Considered` column. Reason: the gate documents must read as one locked line (validators and `grilling` Law 3).
- No `Assumptions` section and no silent defaults. Any part of an option the user did not choose explicitly is a new `Q-NN`.
- A scope option that narrows or changes a goal is a goal change: ask the goal question again, never pick it quietly.
- An option never crosses ownership: spec options carry no technical choice, planning options never change business behavior, designer options never change rules or permissions. Route such a question to its owner's queue.
- The skill proposes; only the user's answer decides, and only Gate 1, 2 or 3 approval approves the document.

## References

- [modes/spec.md](modes/spec.md), [modes/planning.md](modes/planning.md), [modes/designer.md](modes/designer.md)
- [references/divergent-pass.md](references/divergent-pass.md)
- [references/sources.md](references/sources.md)
