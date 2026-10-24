---
name: work-item-contract
description: The shared contract for Client work items - folder and version rules, the 8 Types, which file each gate approves, templates, the goal-lock rule, ownership, the plan and task format, hand-offs and status words. Use whenever an agent creates, reads, writes or hands off anything under .superpowers/work-items/<slug>/vN/, writes or executes a plan task, or returns a status.
---

# Work-item contract

This skill defines **what** agents exchange, not **who runs when**: orchestration lives in `dev-team` and in each agent profile (`agents/*.md`). Plugin files are guidance, not a runtime orchestrator; the host coordinator assigns agents, asks the user, records real approvals and owns item status.

Detail: [work-item contract](references/work-item-contract.md), [type sequences](references/type-sequences.md) (read only the selected row), [Hub tool use](references/tool-usage.md), [sources](references/sources.md).

Single homes of every hand-off format (other skills point here, never restate):

| Reference | Defines |
|---|---|
| `shared_contracts/flags_and_statuses.md` | Canonical SSOT registry for all `coder-nexus` flags: tool gate results (`PASS`/`FAIL`), unified finding severities (`BLOCKER`/`MAJOR`/`MINOR`), agent statuses, verdicts, and integration modes |
| [plan-and-task-contract](references/plan-and-task-contract.md) | Plan-level sections, task fields with **Expected**, `MATCH` / `CODE_WRONG` / `PLAN_WRONG` triage, frozen vs amendable after Gate 3, `## Plan change log` |
| [handoff-and-status](references/handoff-and-status.md) | Hand-off per role pair, every status word, evidence row, review and test report shapes, where each record lives under `vN/` |
| [debug-item-contract](references/debug-item-contract.md) | The `.superpowers/debug/<bug-slug>/` folder of `defect-resolution`, severity S1–S4, fix level L1–L3 and routing rules, bug status words and hand-offs, the L1 no-review exception, investigation items (`diagnosis.md`, temporary instrumentation) of `debug-investigation` |
| [test-run-contract](references/test-run-contract.md) | The `.superpowers/test-runs/<slug>/` folder of `feature-testing`, scenario to cases, default checks (`expected inferred`), case and run status words, read-only rules |

Changing an approved plan: [`change-control`](../change-control/SKILL.md).

## Folder and versions

- New work lives in `${workspaceFolder}/.superpowers/work-items/<slug>/vN/` in Client Git.
- Never overwrite a closed version; later work opens `vN+1`. Reason: approvals and evidence are tied to exact revisions.
- Every `v2+` compares the previous approved documents with the **actual code** in `change-impact.md` (validator `IMPACT-001..003`). Reason: an old design is not proof that it shipped.
- Historical `docs/features/` and `.agents/plan` paths stay read-only sources; do not migrate or rewrite them.
- Reviews go to `vN/reviews/`, test and visual evidence to `vN/evidence/`; never write run output into `.agents/` (synced configuration only).

## Types

One primary `Type` per item, chosen by the independently accepted outcome: `feature`, `bugfix`, `refactor`, `optimization`, `migration`, `maintenance`, `investigation`, `documentation`. Two job words map onto them:

| Job word | Type | Means |
|---|---|---|
| change | `feature` or `refactor` | New `vN` against built code, with `change-impact.md` |
| verification | `investigation` | Spec Writer sets the AC to verify; Test Runner writes findings to `verification.md`; no code |

Job-type question for a ticket that is not new:

| Ticket state | Offer | Effect |
|---|---|---|
| In progress | continue | Resume the current `vN` at its last approved gate |
| In progress | restart | Open `vN+1` from Gate 1; keep the dropped draft readable; what happens to the unfinished code is a `Q-NN` |
| Built or later | change / bugfix / verification / documentation | New `vN` of the mapped Type |

## Files per gate

| Gate | Approves the exact revision of | Owner | Structural check |
|---|---|---|---|
| Gate 1 (spec) | `requirements.md` + `codebase-notes.md` (or `brief.md` for small phase-free items); `change-impact.md` for `v2+`; approved `design-uiux/uiux.md` revision for UI-impact items | Spec Writer (Designer for `design-uiux/`) | `validate_proposal_spec` (`REQ-001..006`, `NOTES-000..005`, `IMPACT-001..003`), `validate_ux_design` |
| Gate 2 (design) | `design.md` - required for `feature`, optional otherwise | Planning | `validate_proposal_spec` (`DESIGN-007`, `DESIGN-008`) |
| Gate 3 (plan) | `implementation-plan.md` and **all linked** `phases/*.md` - required for `feature` | Planning | `validate_plan_slices` (`PLAN-V-010`) |
| After build | `reviews/`, `evidence/`, `as-built.md` (code) or `verification.md` (findings/docs) | Reviewer, Test Runner, Docs Writer | none; the coordinator checks provenance |

Before any gate: 0 `OPEN` `Q-NN`, and no `Option A / Option B`, `Open Questions`, `Assumptions` or `TBD` in `requirements.md` or `design.md`. Validators prove structure only; only the user approves.

## Templates

Render only the files the Type needs; resolve every placeholder from real sources; skip optional files instead of leaving empty sections. Never rename or remove a template heading - validators read them.

| Template | Gate |
|---|---|
| [requirements](templates/requirements.md.tpl), [codebase-notes](templates/codebase-notes.md.tpl), [brief](templates/brief.md.tpl) | 1 |
| [change-impact](templates/change-impact.md.tpl) (`v2+`: ADDED / MODIFIED / REMOVED behavior) | 1 |
| design template of `{{slot:architecture-design}}` | 2 |
| [implementation-plan](templates/implementation-plan.md.tpl), [phase](templates/phase.md.tpl) | 3 |
| [bug-brief](templates/bug-brief.md.tpl), [fixing-plan](templates/fixing-plan.md.tpl) (L2), [escalation-report](templates/escalation-report.md.tpl) (L3), [diagnosis](templates/diagnosis.md.tpl) (investigation) | none: debug items ([debug-item-contract](references/debug-item-contract.md)) |
| [test-scenario](templates/test-scenario.md.tpl) (optional), [test-plan](templates/test-plan.md.tpl), [test-run-report](templates/test-run-report.md.tpl) | none: test runs ([test-run-contract](references/test-run-contract.md)) |

## Goal lock

Shared by every role. Reason: work that serves no confirmed goal is scope creep the user never approved.

1. Every `Q-NN`, `BR-NN`, `AC-NN`, design element and `PHASE-NN` serves a confirmed `G-NN` from `requirements.md` → `## 0. Goals`.
2. Anything else is a non-goal (record it as one) or needs a `D-NN` confirmed by the user.
3. Changing, adding or dropping a goal reopens Gate 1; later approvals tied to the old goals are invalid.
4. Validators enforce parts: `REQ-005` (every BR/AC serves a goal, every goal has an AC), `DESIGN-007` (`## Goal alignment` covers every goal), `PLAN-V-010` (every goal is delivered by a phase).

## Ownership and handoff

| Agent | Writes | Returns |
|---|---|---|
| Spec Writer | `requirements.md`, `codebase-notes.md`, `change-impact.md` (`brief.md` for phase-free items) | `READY_FOR_PLANNING`, findings-only `READY_FOR_VERIFICATION`, or `BLOCKED` |
| Designer | `design-uiux/` (`uiux.md`, screens, components, mock data, `CHANGELOG.md`) for UI-impact items | `READY_FOR_SPEC`, `SKIPPED`, or `BLOCKED` |
| Planning | `codebase-notes.md` (`D-NN`), `design.md` (Gate 2), `implementation-plan.md` + `phases/*.md` (Gate 3), `## Plan change log` and `PCR-NN` answers | `READY_FOR_BUILD`, `SKIPPED`, or `BLOCKED`; `AMENDED` or `ESCALATED` for a change request |
| Code Writer | Assigned Client runtime and test files; task ticks; `writer-handoff.md` | `READY_FOR_REVIEW` with full diff scope (optional Concerns), `BLOCKED`, or `NEEDS_CONTEXT` |
| Docs Writer | Assigned reader-facing docs; phase `as-built.md` after each `APPROVED` review and after final QA | `READY_FOR_REVIEW` for reader docs; `RECORDED` (or `BLOCKED`) for the as-built record |
| Code Reviewer | `vN/reviews/` report | `APPROVED`, `CHANGES_REQUESTED`, or `BLOCKED` |
| Test Runner | `vN/evidence/` report | Per-AC `PASS`, `FAIL`, `BLOCKED`, or `NOT_RUN`; feature `ACCEPTED`, `CHANGES_REQUESTED`, or `BLOCKED` |

Only Spec Writer and Planning write `codebase-notes.md`; everyone else reads it. The coordinator alone changes item status, checks that `as-built.md` matches the evidence and, after a UI item is verified, updates `.superpowers/ux/screen-catalog.md` (NEW → EXISTING, approved design revision, current screenshot).

**Hand-offs** carry the common header and the per-pair payload in [handoff-and-status](references/handoff-and-status.md); a hand-off is a set of claims the receiver re-checks.

`NOT_RUN`, `BLOCKED` and `UNVERIFIED` never become `PASS`; any fix invalidates the affected review and check evidence. Keep Huly read-only and credentials in the Client. No fake business data, APIs, package variants or results.
