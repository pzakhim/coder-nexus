---
name: incremental-implementation
description: Execute one approved phase of a work item task by task — verifying preconditions, running a Consumes/Produces interface pre-flight, executing the A–E task loop with Expected-result triage, running phase-end checks, and writing a revision-bound hand-off.
---

# Incremental Implementation (Core Code Writer Workflow)

One Code Writer executes one approved phase, tasks strictly in order, and proves each task before moving to the next. Formats for task fields and amendment classes live in [plan-and-task-contract.md](../work-item-contract/references/plan-and-task-contract.md); statuses and evidence rows live in [handoff-and-status.md](../work-item-contract/references/handoff-and-status.md).

---

## 1. Execution Flow & Canonical Statuses

1. **Before coding ([01 — Preconditions & Pre-flight](references/01-preconditions-and-preflight.md)):** Verify Gate 1–3 approvals, `PHASE-00` readiness, and the active Git branch; build the **Consumes / Produces Pre-flight Table** against real code signatures before Task 1.
2. **Per-task loop ([02 — Task Loop & Checks](references/02-task-loop-and-checks.md)):** Execute tasks top to bottom (**A. Read & Ground → B. Code in Scope → C. Run Check → D. Triage → E. Tick & Re-read**). Never code two tasks in one pass.
3. **Phase end ([03 — Phase End & Hand-off](references/03-phase-end-and-handoff.md)):** Run full phase verification (`{{slot:verification}}`), UI checks (`{{slot:visual-quality}}`), self bug-hunt (`{{slot:bug-hunt}}`), and named-smell simplification (`{{slot:code-simplification}}`).
4. **Hand-off ([03 — Phase End & Hand-off](references/03-phase-end-and-handoff.md)):** Commit the phase, re-run phase checks on the committed `REVIEW_REVISION`, and write `evidence/<phase-id>/<REVIEW_REVISION>/writer-handoff.md`.

| Category | Canonical Flags ([`handoff-and-status.md`](../work-item-contract/references/handoff-and-status.md)) |
|---|---|
| **Deterministic Tool / Evidence Gate** | `PASS` · `FAIL` · `NOT_RUN` · `BLOCKED` · `UNVERIFIED` (`NOT_RUN`, `BLOCKED`, `UNVERIFIED` are never `PASS`) |
| **Per-Task Check Triage** | `MATCH` (tick & continue) · `CODE_WRONG` (debug & fix in scope) · `PLAN_WRONG` (leave unticked, raise `PCR-NN`, return `BLOCKED`) |
| **Phase Hand-off Status** | `READY_FOR_REVIEW` · `BLOCKED` · `NEEDS_CONTEXT` |

---

## 2. Core Implementation Rules (`I1`–`I17` — Mandatory Compliance)

All 17 rules are **mandatory compliance** across every stack pack:

| ID | Rule | Contract | Reference |
|---|---|---|---|
| **I1** | **Approved Scope Only** | Implement only what an approved `implementation-plan.md` + phase file (or approved phase-free `brief.md`) covers; never widen scope or start before Gate 1–3 approvals | [01 — Preconditions & Pre-flight](references/01-preconditions-and-preflight.md) |
| **I2** | **One Phase at a Time** | Execute only the assigned phase after `PHASE-00` is ticked ready and all phases in `Depends on` have passed | [01 — Preconditions & Pre-flight](references/01-preconditions-and-preflight.md) |
| **I3** | **Concrete Task Contract** | Every task must specify `Scope / Files`, `Acceptance Criteria` (command + cwd), and `Expected`; missing fields require a `PCR-NN` (`change-control`), never a guess | [01 — Preconditions & Pre-flight](references/01-preconditions-and-preflight.md) |
| **I4** | **Strict A–E Task Loop** | Run **Read → Code → Check → Triage → Tick & Re-read** per task; never batch-code multiple tasks | [02 — Task Loop & Checks](references/02-task-loop-and-checks.md) |
| **I5** | **Edit Only Task Scope** | Modify only files listed in the active task's `Scope / Files` and use the mapped components from `design.md` | [02 — Task Loop & Checks](references/02-task-loop-and-checks.md) |
| **I6** | **Immediate Task Check** | Execute the task's Acceptance Criteria command in its cwd immediately after coding and read the full output before ticking | [02 — Task Loop & Checks](references/02-task-loop-and-checks.md) |
| **I7** | **Full Phase Verification** | After all tasks are ticked, run the full phase suite (analyzer, type check, tests, build, architecture validator) via `{{slot:verification}}` | [03 — Phase End & Hand-off](references/03-phase-end-and-handoff.md) |
| **I8** | **Visual Verification (UI)** | For UI-impacting phases, verify approved targets and states via `{{slot:visual-quality}}` | [03 — Phase End & Hand-off](references/03-phase-end-and-handoff.md) |
| **I9** | **Self Bug-Hunt Pass** | Run `{{slot:bug-hunt}}` (`quick` effort) on the phase diff; fix `CONFIRMED` defects with reproducing tests (`{{slot:unit-testing}}`) and carry `PLAUSIBLE` ones as Concerns | [03 — Phase End & Hand-off](references/03-phase-end-and-handoff.md) |
| **I10** | **Honest Evidence Ledger** | Record `claim \| command (+cwd) \| revision \| exit code \| key output \| result` per `evidence-standard` | [03 — Phase End & Hand-off](references/03-phase-end-and-handoff.md) |
| **I11** | **Contract Changes Go to Gate** | Any fix requiring a behavior, API, architecture, dependency, or mapped-component change stops and routes through `change-control` (`PCR-NN`) | [01 — Preconditions & Pre-flight](references/01-preconditions-and-preflight.md), [03 — Phase End & Hand-off](references/03-phase-end-and-handoff.md) |
| **I12** | **Targeted Simplicity Pass** | Run `{{slot:code-simplification}}` on changed code only when a named smell from its 4-lens catalog or `{{slot:clean-code}}` is present; re-run checks after | [03 — Phase End & Hand-off](references/03-phase-end-and-handoff.md) |
| **I13** | **Revision-Bound Hand-off** | Commit the phase before final phase checks so `REVIEW_REVISION` is a clean commit SHA (never `+dirty`), and write `writer-handoff.md` | [03 — Phase End & Hand-off](references/03-phase-end-and-handoff.md) |
| **I14** | **Zero Fabrication or Test Weakening** | Never invent business records, mock fallbacks in production code, or placeholder successes; never delete, skip, or loosen test assertions | [01 — Preconditions & Pre-flight](references/01-preconditions-and-preflight.md), [02 — Task Loop & Checks](references/02-task-loop-and-checks.md) |
| **I15** | **Pre-Flight Before Task 1** | Build the Consumes / Produces table against real code signatures before writing code; raise a `PCR-NN` on any mismatch | [01 — Preconditions & Pre-flight](references/01-preconditions-and-preflight.md) |
| **I16** | **Triage Against Expected** | Compare check output against `Expected` (`MATCH` / `CODE_WRONG` / `PLAN_WRONG`); never patch output to mimic `Expected` | [02 — Task Loop & Checks](references/02-task-loop-and-checks.md) |
| **I17** | **Resume from the Record** | When resuming a session, use phase-file ticks (`- [x]`) and `git log` as the source of truth; re-run the last ticked task's check if the working tree changed | [02 — Task Loop & Checks](references/02-task-loop-and-checks.md) |

---

## 3. Reference Guides

Load only the reference file needed for your current step:

| Reference | Topics Covered |
|---|---|
| [01 — Preconditions & Pre-flight](references/01-preconditions-and-preflight.md) | Gate 1–3 & `PHASE-00` readiness checks, `PHASE-00 [EXECUTE]` handling, authoritative sources of truth, and the **Consumes / Produces Pre-flight Table** (`I1`–`I3`, `I14`, `I15`) |
| [02 — Task Loop, Triage & Tick Format](references/02-task-loop-and-checks.md) | Step-by-step A–E task loop, `MATCH` / `CODE_WRONG` / `PLAN_WRONG` triage matrix, exact `- [x]` tick line format, 7 hard rules during coding, and session resume protocol (`I4`–`I6`, `I14`, `I16`, `I17`) |
| [03 — Phase-End Checks, Hand-off & Review Rounds](references/03-phase-end-and-handoff.md) | 5 phase-end verification gates, `evidence/<phase-id>/<REVIEW_REVISION>/writer-handoff.md` template, status rules, and round-N review replies (`I7`–`I13`) |

---

## 4. Stack Slots & Core Handshake Skills Called

| Need | Target Skill / Slot |
|---|---|
| Layer placement, module structure & profile architecture contracts | `{{slot:clean-architecture}}` |
| Code structure, naming, foundation/UI kit reuse & self-check | `{{slot:clean-code}}` |
| Input, auth, scope & secret safety | `{{slot:secure-coding-standards}}` |
| Writing & running unit tests | `{{slot:unit-testing}}` |
| Diagnosing a `CODE_WRONG` failure | `{{slot:root-cause-debugging}}` |
| Phase-end self bug-hunt & simplification | `{{slot:bug-hunt}}`, `{{slot:code-simplification}}` |
| Phase-end suite & UI visual verification | `{{slot:verification}}`, `{{slot:visual-quality}}` |
| Plan defects (`PLAN_WRONG`), review replies & evidence | [`change-control`](../change-control/SKILL.md), [`review-resolution`](../review-resolution/SKILL.md), [`evidence-standard`](../evidence-standard/SKILL.md) |
