# Hand-off and status contract

The single home of what roles and departments hand each other, every status word they may return, the evidence row, the review and test report shapes, and where each record lives under `vN/`. Process and department skills (`dev-team`, `bug-squad`, `incremental-implementation`, `review-workflow`, `quality-acceptance`, `change-control`) use these formats; they do not redefine them.

All hand-offs go through the host coordinator: an agent returns a status, and the coordinator assigns the next role. No agent starts another, approves for the user, or changes item status.

## 1. Common header (every hand-off)

Item / version / Type; approved document revisions and the user response references behind them; goal IDs (`G-NN`) and AC IDs (`AC-NN`) in scope; task or phase; `BASE_REVISION` and `REVIEW_REVISION` where code exists; staged / unstaged / untracked scope; affected files; planned checks; UI target and states; for UI items the foundation profile recorded in design (`architecture_profile.mode` where the stack defines one, see `{{slot:architecture-design}}`; destinations per `{{slot:clean-architecture}}`); open `PCR-NN` and unresolved blockers.

A hand-off is a set of claims. The receiver re-checks what it relies on (`evidence-standard`).

## 2. Hand-off per role & department pair

| From → To | Status that triggers it | Carries, beyond the header | Lives at |
|---|---|---|---|
| Spec Writer → Planning (`dev-team` — **Zero-Re-Ask Handoff**) | `READY_FOR_PLANNING` + `BRANCH_READY` | Gate 1 user approval reference; `requirements.md` (including `## Screens & Visual Sources` `S-NN` and `## Workflows` `W-NN` when UI is in scope), `codebase-notes.md` (`0 OPEN Q-NN`), `change-impact.md` (`v2+`), and extracted Figma outputs (`.superpowers/sources/<ISSUE-ID>/figma/` `tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png`) or verified existing UI source; active item branch. **`planning` inherits every confirmed `G-NN`, `AC-NN`, `D-NN`, `S-NN`, and `W-NN` without re-asking the user** | `requirements.md`, `codebase-notes.md` |
| Planning → Code Writer | `READY_FOR_BUILD` naming the first phase (or `AMENDED` after a change request); the coordinator assigns one Code Writer | Gate 3 approval reference; plan and phase revisions; the one phase to build; last `## Plan change log` row | `implementation-plan.md`, `phases/` |
| Code Writer → Code Reviewer | `READY_FOR_REVIEW` | `BASE_REVISION..REVIEW_REVISION` (committed per `git-preflight` phase commit format, never `+dirty`); tasks ticked (for `PHASE-00`, its accepted tick, [plan-and-task-contract](plan-and-task-contract.md) §1); the pre-flight table; one evidence row per task check and per phase check; self `{{slot:bug-hunt}}` and `{{slot:code-simplification}}` results; Concerns; `PCR-NN` raised and their answers; from round 2 `## Review reply (round N)` | `evidence/<phase-id>/<REVIEW_REVISION>/writer-handoff.md` |
| Code Writer → Planning | `BLOCKED` naming a `PCR-NN` | The request shape of `change-control` (the Code Writer writes it) | `plan-changes/PCR-NN.md` |
| Code Reviewer or Test Runner → Planning | Its verdict, with a `PLAN_CONFLICT` row in its own report | Plan line, finding, evidence, options. The raiser stays read-only; the coordinator writes `PCR-NN.md` from that row | the report, then `plan-changes/PCR-NN.md` |
| Code Reviewer → Code Writer | `CHANGES_REQUESTED` | Report path, finding IDs to address, round number | `reviews/review_<phase-id>_<REVIEW_REVISION>.md` |
| Code Reviewer → coordinator | `APPROVED` | Report path; the exact approved `REVIEW_REVISION`. Coordinator runs the **User Checkpoint** before assigning the next phase (or assigns `test_runner` `final_qa` after the last phase) | `reviews/review_<phase-id>_<REVIEW_REVISION>.md` |
| coordinator → Test Runner | Last phase `APPROVED` (`final_qa`), or a phase the plan marks for its own acceptance run | The approved `REVIEW_REVISION`; scope from `requirements.md` → `## 1.` **Scope in** / **Scope out** (`brief.md` → `## Scope and contracts` for a phase-free item) | — |
| Test Runner → Code Writer | `CHANGES_REQUESTED` (feature verdict) | Each `FAIL` case: steps, expected vs actual, evidence path, `AC-NN` and its owning phase; defect severity | `evidence/final_qa/<revision>/` (or `evidence/<phase-id>/<revision>/` for a phase run) |
| Test Runner → Docs Writer (via coordinator) | `ACCEPTED` | Report path; per-AC results; limitations. Coordinator assigns `docs_writer` **once** for final closure | `evidence/final_qa/<revision>/` |
| Docs Writer → coordinator | `RECORDED` (or `BLOCKED`) | Final concise visual `as-built.md` ([template](../templates/as-built.md.tpl)) with Mermaid Flow Diagram, Delivered Code Map, and Phase/Review/QA Evidence Ledger | `as-built.md` |
| Docs Writer → Code Reviewer | `READY_FOR_REVIEW` (reader docs) | The changed reader-facing documents and the claims they make | the documents themselves |

A fix on any arrow creates a new revision. Review and test evidence for the touched code no longer counts; the chain restarts from the Code Reviewer.

**Order after `APPROVED`.** Per phase: Code Reviewer `APPROVED` → coordinator User Checkpoint → next phase (no `Docs Writer` run between phases). The Test Runner runs `final_qa` once after the last phase is `APPROVED` (plus any phase the plan explicitly marks for its own acceptance run). Once Test Runner returns `ACCEPTED`, the coordinator assigns `Docs Writer` **once** to write the final visual `as-built.md` (`RECORDED`).

**Writer hand-off revision & commit checkpoint.** `<REVIEW_REVISION>` in the hand-off path is the committed revision handed to review. The pre-flight table is drafted in working notes before Task 1 and copied into the hand-off at the end. A commit is required before `READY_FOR_REVIEW` following `git-preflight` (`<type>(<SUB-TICKET>): <summary> [parent: <PARENT-TICKET>, PHASE-NN]` when a sub-ticket exists, or `<type>(<PARENT-TICKET>): [PHASE-NN] <summary>`); `+dirty` appears only on intermediate task ticks.

**Review round N.** The per-finding reply table (reply words in §3) goes into the new `writer-handoff.md` under `## Review reply (round N)`. The delta review covers previous `REVIEW_REVISION`..new `REVIEW_REVISION`; the header keeps the phase's `BASE_REVISION`.

**Test Runner defect** (from `final_qa` or a phase run). The fix belongs to the phase that owns the failing `AC-NN` in `implementation-plan.md` → `## AC coverage`, inside that phase's **Scope / Files**, found and fixed through `{{slot:root-cause-debugging}}`. The Code Writer replies with the `review-resolution` per-finding table (`DEF-NN` rows), hands off to `evidence/<owning-phase-id>/<REVIEW_REVISION>/writer-handoff.md`, and the chain restarts at the Code Reviewer. The fix counts toward that phase's 3-review-round cap. A fix that needs a file outside that Scope / Files is a plan change request (`change-control`).

## 3. Status words

| Word | Returned by | Means |
|---|---|---|
| `READY_FOR_PLANNING` / `READY_FOR_VERIFICATION` / `READY_FOR_BUILD` | Spec Writer / Spec Writer (findings-only) / Planning | The next role may start on the approved revisions named. When `READY_FOR_PLANNING` is already approved, `dev-team` starts directly at `planning` |
| `BRANCH_READY` | `git-preflight` (Spec Writer, step 1E) | The item branch is decided and recorded as a `D-NN`; work may continue on it |
| `APPROVED_FOR_BUILD` | coordinator, recording the user's Gate 3 approval | Plan state, not a hand-off: specs and plan are frozen; Planning then returns `READY_FOR_BUILD` |
| `SKIPPED` | Planning | The step does not apply to this item; the reason is recorded |
| `READY_FOR_REVIEW` | Code Writer, Docs Writer (reader docs), Bug Fixer (L2) | Every task ticked on `MATCH`, phase checks run on a committed revision, evidence rows written. Optional **Concerns**: doubts about correctness or scope the reviewer reads after its cold passes (`review-workflow`); plain observations are listed as notes |
| `RECORDED` | Docs Writer | Final `as-built.md` (§8, [template](../templates/as-built.md.tpl)) is written after `ACCEPTED` QA (or for a `documentation` item), with every row citing a real report or evidence path |
| `NEEDS_CONTEXT` | Code Writer | Information missing from the hand-off. States what was tried (files read, commands run) and exactly what is needed |
| `BLOCKED` | any role | Cannot continue without something outside its authority: an approval, an environment, an external dependency, an answer to a `PCR-NN`. Names the blocker |
| `AMENDED` / `ESCALATED` | Planning, for a `PCR-NN` (never used as a reply to a finding) | `TASK_DETAIL` amended and logged / sent to Gate 2 (`DESIGN_CHANGE`) or Gate 1 (`SCOPE_CHANGE`) |
| `APPROVED` / `CHANGES_REQUESTED` / `BLOCKED` | Code Reviewer | Review verdict on one revision |
| `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` | Test Runner, every evidence row | Result per check or AC. Older files write `FAILED`; it means `FAIL` |
| `ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED` | Test Runner | Feature verdict on one revision |
| `MATCH` / `CODE_WRONG` / `PLAN_WRONG` | Code Writer | Triage of one task check ([plan-and-task-contract](plan-and-task-contract.md) §3) |
| `TASK_DETAIL` / `DESIGN_CHANGE` / `SCOPE_CHANGE` | Planning | Class of a plan change |
| `BLOCKER` / `MAJOR` / `MINOR` + `CONFIRMED` / `PLAUSIBLE` | Reviewer, `{{slot:bug-hunt}}` | Finding severity and confidence |
| `PLAN_CONFLICT` | Reviewer, Test Runner | A finding whose right fix touches the plan; recorded in the raiser's report, written up as `PCR-NN` by the coordinator (`change-control`) |
| `FIXED` / `DISPUTED` / `RAISED` | Code Writer, per finding (`review-resolution`) | Fixed on the new revision with evidence / disputed with technical evidence / sent on as a plan change request (`change-control`) or `NEEDS_CONTEXT` |
| `UNVERIFIED` | validators, any role | A claim with no executed check behind it |

- `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never become `PASS`, `APPROVED`, or `ACCEPTED`. Reason: a check that did not run proves nothing.
- No softened statuses ("done with small issues", "mostly passing"). Doubts go in Concerns; the status stays one of the words above.
- On `NEEDS_CONTEXT` or `BLOCKED` the coordinator changes something before re-assigning: adds the context, resolves the blocker, or routes the plan defect to Planning. Re-assigning unchanged repeats the failure.

## 4. Evidence row

| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
|---|---|---|---|---|---|
| Task 2.1 Expected met | `<check>` (cwd: `<dir>`) | `abc1234` | 0 | `12 passed` | `PASS` |

One row per executed check, on the exact revision. Key output is the short excerpt that decides the result (counts, the error line, status code), never secrets or personal data. A row from another revision does not count for this one.

## 5. Review report (`reviews/review_<phase-id>_<REVIEW_REVISION>.md`)

1. Header: item, `vN`, phase, round `N` of 3, `BASE_REVISION` (the phase's, kept on every round), `REVIEW_REVISION` (and the previous one for a delta round), approved input revisions.
2. Evidence: re-run checks as evidence rows.
3. Findings: `| ID | Pass | Severity | Confidence | File:line | Problem | Failure scenario / evidence | Fix direction |`, IDs `RV-NN`; a finding the plan itself mandates carries the label `plan-mandated` in Problem.
4. Plan conflicts: `PLAN_CONFLICT` rows (plan line, finding, evidence, options); the coordinator adds the `PCR-NN` it writes from them.
5. Verdict with a one-line reason.

Section order and pass content are defined in `review-workflow`.

## 6. Test report (`evidence/final_qa/<revision>/`, or `evidence/<phase-id>/<revision>/` for a phase run)

1. Verdict first: feature verdict with a one-line reason, counts, open defects.
2. Header: item, `vN`, phase or `final_qa`, tested revision (the `APPROVED` `REVIEW_REVISION`), environment record, test plan reference.
3. Per-AC table: the one table defined in `quality-acceptance` → "Per-AC results".
4. Case rows as evidence rows; artifacts beside the report.
5. Defects with severity; re-test history.
6. Limitations (stubbed providers, `NOT_RUN` reasons).

The stack may name the report file through `{{slot:verification}}`; the content above is required either way. Execution detail and the exact report layout are in `quality-acceptance` (`modes/reporting.md`).

## 7. Where things live under `vN/`

| Path | Owner | Holds |
|---|---|---|
| `requirements.md`, `codebase-notes.md`, `change-impact.md` (`v2+`) | Spec Writer (`codebase-notes.md` also written by Planning) | Gate 1 specification, permanent `Q-NN` / `D-NN` log, and `v2+` delta contract |
| `design.md`, `implementation-plan.md`, `phases/phase-NN-*.md` | Planning (Code Writer ticks tasks only) | Gate 2 architecture design, Gate 3 approved plan, `## Plan change log` |
| `plan-changes/PCR-NN.md` | Code Writer writes its request, or the coordinator writes it from a Reviewer / Test Runner `PLAN_CONFLICT` row; Planning writes the answer | One file per plan change request |
| `evidence/<phase-id>/<REVIEW_REVISION>/writer-handoff.md` | Code Writer | Hand-off claims, evidence rows, review replies |
| `reviews/review_<phase-id>_<REVIEW_REVISION>.md` | Code Reviewer | Review report |
| `evidence/test-plan.md`, `evidence/final_qa/<revision>/`, `evidence/<phase-id>/<revision>/` | Test Runner | Test plan, test report, artifacts |
| `as-built.md` / `verification.md` | Docs Writer (for `as-built.md`) / Test Runner (for `verification.md`) | Final concise visual as-built summary ([template](../templates/as-built.md.tpl)) written once after `ACCEPTED` QA / investigation findings |

Never write run output into `.agents/` (synced configuration only).

## 8. Final As-Built Record (`as-built.md`)

Written **once** by `Docs Writer` from [`templates/as-built.md.tpl`](../templates/as-built.md.tpl) after `Test Runner` returns `ACCEPTED` in `final_qa` (or directly for a `documentation` item). It must remain concise, scannable, and visual:

1. **Executive Summary**: Goals delivered (`G-NN`) and user-facing/system outcome.
2. **Visual Flow & Architecture Overview**: A single Mermaid diagram (`flowchart LR` or `sequenceDiagram`) depicting the actual built user/system flow across screens, state/domain controllers, and data/API boundaries.
3. **Delivered Code & Component Map**: Layer/area, file path, and role/reused foundation or Kit components.
4. **Phase, Review & QA Evidence Ledger**:

| Stage / Phase | Scope & `AC-NN` Covered | Approved Revision | Report / Evidence Path | Verdict |
|---|---|---|---|---|
| `PHASE-01` | `AC-01`, `AC-02` | `abc1234` | `reviews/review_PHASE-01_abc1234.md` | `APPROVED` |
| `final_qa` | `AC-01`..`AC-04` | `def5678` | `evidence/final_qa/def5678/test-report.md` | `ACCEPTED` |

5. **Deviations, Plan Changes & Known Limitations**: Approved `PCR-NN` items, runtime/fixture limits, and reader docs updated.

One ledger row per recorded stage, copied from a real report or evidence row, never from a status message. The Docs Writer returns `RECORDED` when `as-built.md` is complete, or `BLOCKED` naming the missing report.

## 9. Finding severity and verdict impact

The single unified scale every code finding uses, whoever raises it (Code Writer self-check, Code Reviewer, Test Runner defect), defined canonically in `shared_contracts/flags_and_statuses.md` §2. The stack skills (`{{slot:bug-hunt}}`, `{{slot:clean-code}}`, `{{slot:code-simplification}}`, `{{slot:secure-coding-standards}}`, `{{slot:code-review}}`) decide **what** is a finding and give rule IDs; this section decides how it is graded and what it does to the verdict.

### Unified Severity Scale (`BLOCKER` / `MAJOR` / `MINOR`)

Both behavioral defects and stack rule violations use the same three-level scale (never use `P1`/`P2`/`P3` for findings):

| Severity | Means |
|---|---|
| `BLOCKER` | 1. **Behavioral / Security defect**: Data loss or corruption, security hole, crash or hang on a normal path, approved AC behavior broken.<br>2. **Failed tool gate**: Any required CLI check defined in `{{slot:verification}}` or `{{slot:clean-code}}` (linter, formatter, static analyzer/type checker, architecture import linter, or test runner) exiting non-zero (`FAIL`).<br>3. **Mandatory design / craft rule violation**: Violation of a core rule in `{{slot:clean-code}}`, `{{slot:clean-architecture}}`, or `{{slot:secure-coding-standards}}` (pass-through wrapper, kept alias, exposed internal helper, mutable module global, swallowed error, layer boundary breach). |
| `MAJOR` | 1. **Edge-case defect**: Wrong result, crash, or resource leak on a realistic edge path (empty, failure, retry, last page, slow network).<br>2. **Maintainability risk**: Structural smell or localized complexity not already blocked by CLI linters that degrades readability or testability. |
| `MINOR` | Wrong result only in a rare self-correcting case, or optional style/readability polish. |

Confidence: `CONFIRMED` (traced end to end or shown by a command) or `PLAUSIBLE` (names the evidence that would decide it). Every behavioral defect names a failure scenario (`given … → when … → then …`); every rule violation puts its rule ID first in Problem. Only code changed in the phase is graded; debt outside the diff is a note, never a finding.

### Verdict impact

| Finding | Effect |
|---|---|
| `CONFIRMED` `BLOCKER` or `MAJOR` | `CHANGES_REQUESTED` |
| `PLAUSIBLE` `BLOCKER` | `BLOCKED` until the named evidence is supplied |
| Other `PLAUSIBLE`, `MINOR` (or localized `MAJOR` maintainability note outside touched scope) | Listed; fixed in the same revision when inside the phase's Scope / Files and cheap; never block alone |

No role lowers a severity to end a round; the 3-round cap and escalation are in `review-workflow`.

### Rows

- Review report: the findings table of §5. A rule violation puts its rule ID first in Problem (for example `<rule ID>: module-level mutable list`, the ID as the stack's clean-code skill numbers it); a defect from bug-hunt keeps its failure scenario.
- Code Writer hand-off, after its self-check: `bug-hunt: <n> CONFIRMED, <m> PLAUSIBLE (effort <level>)` or `bug-hunt: no defect found (effort <level>)`, and `simplify: <smell> -> <technique> at <path:line>[; ...]; net <+/-n> lines; checks: <command> exit <code>` or `simplify: nothing worth changing (looked at: <files>)`.

### Bug-hunt effort

| Effort | When | Cap |
|---|---|---|
| `quick` | Code Writer self-check, small non-feature item, docs-only | 5 findings |
| `standard` | Every feature phase review (`PHASE-01+`) | 10 findings |
| `deep` | Final phase before close, auth / payment / data-migration code, or a phase already returned twice | No cap |
