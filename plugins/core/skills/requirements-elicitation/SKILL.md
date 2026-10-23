---
name: requirements-elicitation
description: Spec Writer's first stage of every work item (Stage 1A, 1A-0, 1A-G) - reads every source once into a Source Inventory (READ / UNREACHABLE / NOT_PROVIDED), settles the job type and stack, sizes the work, drafts 1-3 outcome goals with observable success signals plus non-goals, anti-goals and source conflicts, and asks the goal question (Confirm / Edit / Narrow) before any other Q-NN. Use at the start of a work item, when a ticket is no longer new, or when the user changes a goal.
---

# Goal Framing

Answer one question before any other: **what outcome must this work item deliver, and how will we see that it did?** Tickets are uneven: a one-line task, a parent with many children, the real requirements in a PO document that does not open, a PDF linked in a comment, or an AC added in a comment that contradicts the FR document. Never copy the ticket into requirements. Settle the goals with the user first; every later `Q-NN`, `BR-NN`, `AC-NN`, design element and `PHASE-NN` then serves a `G-NN`.

Spec Writer only. A workspace `.agents/skills/requirements-specification/` adds the team's own sources and question bank; it never replaces the steps or sections below.

## Steps

| Stage | Step | Output | Asks the user? |
|---|---|---|---|
| 1A | [Source intake](references/source-intake.md): read Huly, downloads, the prompt and the codebase once | `codebase-notes.md` → `## 0A. Source Inventory` | No |
| 1A-0 | [Job type, stack and size](references/job-type-and-stack.md) | First `D-NN` (job type) when the ticket is no longer new; `BLOCKED` parts; artifact path | Only when the ticket is no longer new |
| 1A-0 | Parent coverage (parent tickets) | `Parent part / Covered by / Status` table | Once, about `NO CHILD` parts |
| 1A-G | [Goal candidates](references/goal-candidates.md): read-back, hypothesis, 1-3 goals, non-goals, anti-goals, conflicts, split check | Draft for the goal question | No |
| 1A-G | [Goal question](references/goal-question.md) | `D-NN` + `requirements.md` → `## 0. Goals` with `Status: CONFIRMED` | Yes, one question, asked alone |

Then Stage 1B drafts `requirements.md` + `codebase-notes.md` in the same turn, and the remaining `Q-NN` follow `grilling`.

## Rules

| # | Rule | Why |
|---|---|---|
| GF1 | Read every source before the first question, and never ask what a source or the codebase already answers. | Each avoidable question spends the user's attention on nothing. |
| GF2 | Never infer the content of an `UNREACHABLE` or `NOT_PROVIDED` source from its title or link text. Ask the user to attach or paste it, or to confirm the work goes ahead without it. | A guessed PO document becomes a confident wrong spec. |
| GF3 | Huly is read through `huly-task-intake` only, once; consolidate what it returns so later agents never re-query Huly. | One read, one source of truth in `codebase-notes.md`. |
| GF4 | Job type uses the 8 work-item Types; "change", "verification", "continue" and "restart" are only the words of the question. | One vocabulary for sequences, validators and reviews. |
| GF5 | A part whose stack has no installed pack is `BLOCKED — out of plugin scope`: say so, list it under Non-goals with the reason, write nothing for it. | Guessed code in an unsupported stack cannot be reviewed or tested here. |
| GF6 | A goal is an outcome (actor + result + business value) with an observable, technology-agnostic success signal. A feature list, a buzzword ("faster", "scalable") or a solution is not a goal. | Outcomes survive design changes; solutions lock the design before Gate 2. |
| GF7 | Draft at most 3 goals. When the AC cluster into groups that could ship and be checked on their own, propose linked work items instead of more goals. | `validate_proposal_spec` warns above 3 (`REQ-005`); a batch with more goals is usually several features. |
| GF8 | A topic still in scope but unclear is a `Q-NN`, not a non-goal. Non-goals are ruled out on purpose and carry a reason. | Fog parked under Non-goals silently drops scope. |
| GF9 | The goal question is the first `Q-NN` after the job-type question (when that is asked) and is asked alone; only an explicit Confirm, Edit or Narrow answer closes it. | "Sounds good" or "whatever you think" is delegation, not a decision. |
| GF10 | Your own read of the request appears as your proposal, never as something the user said. No Assumptions section, no informed guesses. | `grilling` Law 2: every inference is confirmed. |

## Goal lock (pointer)

After confirmation the goals are locked for the rest of the work item: every later question names its `G-NN`, every `BR-NN` / `AC-NN` cites one (`REQ-005`), design maps them in `## Goal alignment` (`DESIGN-007`), phases deliver them (`PLAN-V-010`), and gate presentations open with a one-line goal recap. The rule itself, including how a goal change re-opens Gate 1, lives in [`work-item-contract`](../work-item-contract/SKILL.md). This skill only produces the confirmed goals.

## Hand-off

- `codebase-notes.md`: `## 0A. Source Inventory` filled; the job-type, goal and parent-coverage answers in `## 1. Decision Log (D-NN)`.
- `requirements.md` (or `brief.md` on the small path): `## 0. Goals` with each `G-NN` `CONFIRMED` and citing its `D-NN`, plus Non-goals and Anti-goals.
- The sufficiency summary's "Next" line seeds the `Q-NN` queue that `grilling` orders.

Sources and ideas not adopted: [references/sources.md](references/sources.md).
