---
name: requirements-elicitation
description: "Spec Writer's first stage of every work item (Stage 1A, 1A-0, 1A-G) in dev-team — reads every source once into a Source Inventory (READ / UNREACHABLE / NOT_PROVIDED, including L3 escalation-report.md from bug-squad without re-asking), settles job type and stack scope, sizes the work, drafts 1-3 outcome goals (G-NN) with observable success signals plus non-goals, anti-goals, and source conflicts, and asks the single Goal Question before any other Q-NN."
---

# Requirements Elicitation & Goal Framing

Answer one question before any other: **what outcome must this work item deliver, and how will we observe that it did?** Tickets and inputs vary widely — a one-line task, a parent issue with many children, an L3 `escalation-report.md` from `bug-squad`, a PO document that cannot be opened, or a comment that changes an earlier criterion. Never copy raw ticket text blindly into `requirements.md`. Settle the goals (`G-NN`) with the user first; every later `Q-NN`, workflow `W-NN`, `BR-NN`, `AC-NN`, design element, and `PHASE-NN` then serves a confirmed `G-NN`.

Used by `spec_writer` in **`dev-team`** (including when invoked from a `bug-squad` L3 escalation). When Gate 1 is already locked (`APPROVED`), `dev-team` skips `spec_writer` and `requirements-elicitation` completely.

## Reference Guides

| Guide | Topic |
|---|---|
| [01 — Source Intake, Job Type & Sizing](references/01-source-intake-and-job-type.md) | Stage 1A one-read source intake (Huly, downloads, L3 `escalation-report.md`, codebase), `## 0A. Source Inventory`, parent coverage check, Stage 1A-0 job-type classification, stack scope check, and work sizing |
| [02 — Goal Framing, Split Check & Goal Question](references/02-goal-framing-and-question.md) | Stage 1A-G read-back, hypothesis & confidence, drafting 1–3 `G-NN` goals, non-goals, anti-goals, split check, asking the single Goal Question, and locking `## 0. Goals` |

## Stage Sequence

| Stage | Step | Output | Asks the User? |
|---|---|---|---|
| **1A** | [Source intake](references/01-source-intake-and-job-type.md#1-what-to-read-once-stage-1a--no-questions-yet): read Huly, downloads, L3 escalation report, prompt, and codebase once | `codebase-notes.md` → `## 0A. Source Inventory` & `## 3. Verified Baseline Facts` | No |
| **1A-0** | [Job type, stack & size](references/01-source-intake-and-job-type.md#4-job-type-classification-stage-1a-0) | First `D-NN` (job type) when the ticket is not new; `BLOCKED` stack parts; artifact path (`brief.md` vs `requirements.md`) | Only when the ticket is not new |
| **1A-0** | [Parent coverage](references/01-source-intake-and-job-type.md#3-parent--child-tickets-coverage) (parent tickets only) | `Parent part | Covered by | Status` table + `D-NN` | Once, about `NO CHILD` parts |
| **1A-G** | [Goal candidates & split check](references/02-goal-framing-and-question.md#1-drafting-goal-candidates-stage-1a-g-prep) | Read-back, hypothesis + confidence, `G-01..G-03`, non-goals, anti-goals, conflicts, split table | No |
| **1A-G** | [The Goal Question](references/02-goal-framing-and-question.md#3-asking-the-goal-question-single-ask_question-call) | `D-NN` + `requirements.md` → `## 0. Goals` (`Status: CONFIRMED`) | Yes — 1 question via `ask_question`, asked alone |

In the same turn that `## 0. Goals` is confirmed, Stage 1B drafts `requirements.md` + `codebase-notes.md`, Stage 1A-UX runs [`figma-intake`](../figma-intake/SKILL.md) to extract `S-NN` screens and `W-NN` workflows when UI is in scope, and the remaining `Q-NN` follow [`grilling`](../grilling/SKILL.md).

## Golden Rules (`GF1`–`GF11`)

| # | Rule | Why |
|---|---|---|
| `GF1` | Read every available source before the first question; never ask what a readable source or the codebase already answers. | Avoidable questions waste the user's attention. |
| `GF2` | Never infer the content of an `UNREACHABLE` or `NOT_PROVIDED` source from its title or link text. Ask the user to attach/paste it or confirm proceeding without it (`D-NN`). | A guessed PO document produces a confident wrong spec. |
| `GF3` | Read Huly once through [`huly-task-intake`](../huly-task-intake/SKILL.md) and consolidate into `codebase-notes.md` so no downstream agent re-queries Huly. | Single source of truth across all roles and departments. |
| `GF4` | Job type maps onto the 8 canonical `work-item-contract` Types (`feature`, `bugfix`, `refactor`, `optimization`, `migration`, `maintenance`, `investigation`, `documentation`). | Unified vocabulary for sequences, validators, and reviews. |
| `GF5` | Any part whose stack has no installed pack in `.agents/stack.json` is `BLOCKED — out of plugin scope`: report it, list it under Non-goals with the reason, and write no spec/design/code for it. | Unsupported stacks cannot be validated or tested in this workspace. |
| `GF6` | A goal is a user/business outcome (`<actor> can <result> so that <business value>`) with an observable, technology-agnostic success signal — never a feature list, buzzword, or Gate 2 technical solution. | Outcomes survive architecture changes; technical solutions belong to Gate 2. |
| `GF7` | Draft at most 3 goals (`G-01..G-03`). When AC cluster into independently shippable groups, propose linked work items via the split check instead of adding more goals. | `validate_proposal_spec` (`REQ-005`) flags >3 goals; larger batches are multiple features. |
| `GF8` | An unclear topic that remains in scope is a `Q-NN`, never a non-goal. Non-goals are explicitly ruled out and carry a reason. | Parking unclear items under Non-goals silently drops required scope. |
| `GF9` | The Goal Question is asked alone via `ask_question`; only an explicit `Confirm goals`, `Edit goals`, or `Narrow to G-01 only` closes it. | Vague replies (*"sounds good"*, *"whatever you think"*) are delegation, not a recorded decision. |
| `GF10` | Present your own synthesis as a proposal to confirm, never as something the user stated. Never write an `Assumptions` section or unconfirmed guesses. | `grilling` Law 2: every inference is confirmed as a `D-NN`. |
| `GF11` | **Zero-Re-Ask Continuity:** When starting from a `bug-squad` L3 `escalation-report.md`, ingest its reproduction, root cause, and impact directly into `codebase-notes.md` without re-asking symptom or reproduction steps. When Gate 1 is already locked (`APPROVED`), `dev-team` skips `requirements-elicitation` completely. | Eliminates redundant questioning across handoffs. |

## Hand-Off Contract

- `codebase-notes.md`: `## 0A. Source Inventory` populated; job-type, parent-coverage, and goal confirmation recorded in `## 1. Decision Log (D-NN)`.
- `requirements.md` (or `brief.md` on the small path): `## 0. Goals` with each `G-NN` set to `CONFIRMED` and citing its `D-NN`, plus `- **Non-goals**:` and `- **Anti-goals**:`.
- Goal lock (`work-item-contract`) is now active: every subsequent `Q-NN`, `W-NN`, `BR-NN`, `AC-NN`, design element, and `PHASE-NN` must serve a confirmed `G-NN`.
