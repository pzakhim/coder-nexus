# 01 — Source Intake, Job Type, Stack Scope & Sizing (Stage 1A & 1A-0)

## 1. What to Read Once (Stage 1A — No Questions Yet)

Collect every available source once, before asking any question, and record it in `codebase-notes.md` → `## 0A. Source Inventory`. No question is asked during Stage 1A.

| Pillar | How to Read | Notes |
|---|---|---|
| Huly ticket, parent, children, comments | [`huly-task-intake`](../../huly-task-intake/SKILL.md) (`huly_get_task_detail`, `download: true`), once | Comments often add or modify AC; read all of them. Downstream agents never re-query Huly. |
| Downloaded attachments | `.superpowers/sources/<ISSUE-ID>/` | Open downloaded PDFs, images, and diagrams directly; a diagram can show parts no child ticket covers. |
| PO / BA documents, PDFs, designs | Open every reachable mention and link | Unopenable means `UNREACHABLE`, never *"probably says …"*. |
| `bug-squad` L3 escalation report | `.superpowers/debug/<bug-slug>/escalation-report.md` (+ `brief.md`, `evidence/`) | **Zero-Re-Ask Rule**: Ingest symptom, reproduction steps, environment, root cause (`file:line`), affected layers/contracts, and quoted triage test directly into `## 0A. Source Inventory` (`READ`) and `## 3. Verified Baseline Facts`. Never re-ask the user for bug symptoms or reproduction steps. |
| User prompt | The user request itself | Counts as a primary source; cite it in the inventory. |
| Codebase | Read-only search (`rg -n` / `git grep`) | Inspect how the touched modules work today and what the change affects. Verified facts go to `## 3. Verified Baseline Facts & Cross-Agent Notes`. |
| Stack-specific pillars | As defined by the active pack rules (e.g., UI design inputs, API contracts) | Record a missing pillar in the inventory; never invent it. |

Read until you can explain, in 2–3 lines, how the relevant parts work today. That baseline feeds the read-back in the goal question ([02 — Goal Framing & Question](02-goal-framing-and-question.md)).

## 2. Source Inventory Table (`codebase-notes.md` → `## 0A. Source Inventory`)

Use the exact table heading and columns in the `codebase-notes.md` template:

| Source | Kind | Read status | What it contributes / conflicts |
|---|---|---|---|
| `IMES-1190` | Huly ticket (child of `IMES-1167`) | `READ` | 3 behaviors as prose, no explicit AC |
| `IMES-1167` | Huly parent | `READ` | Feature name, 10 children |
| `REQ-MFG-ECN-03` (mentioned in description) | PO requirements doc | `UNREACHABLE` (no permission) | Ask the user |
| Screen spec PDF (comment link) | PDF | `NOT_PROVIDED` | Ask the user |
| Comment 9/19 "added warning beyond FR" | Huly comment | `READ` | AC differs from FR doc |

- **Kind**: Huly ticket / parent / child / comment / PO doc / PDF / design / `escalation-report.md` / user prompt / codebase.
- **Read status**:
  - `READ`: Opened and read directly.
  - `UNREACHABLE`: Exists or linked, but cannot be opened (permissions, broken link, network).
  - `NOT_PROVIDED`: Referenced or expected, but not supplied.
- Each `UNREACHABLE` or `NOT_PROVIDED` row goes into the sufficiency summary's **Missing** line. If a missing source could change the goals, ask the user for it before confirming goals.
- **Conflicts between sources**: Record every disagreement in the last column (FR doc vs ticket AC, comment vs description, parent vs child, sibling vs sibling). Never pick a side silently. A conflict that changes a goal is settled in the goal question; one that changes only a detailed rule becomes a `Q-NN`.

## 3. Parent & Child Tickets Coverage

Follow [`huly-task-intake` → 02 — Parent & Sub-Issues Traceability](../../huly-task-intake/references/02-parent-and-sub-issues.md):
- A **parent ticket** yields one work item built from the parent description plus every open child's AC (each tagged with its Huly ID).
- A **child ticket** scopes the work item to that child only, with the parent recorded in `codebase-notes.md` as context.
- **Closed children** (`is_closed: true`) are listed as `Out of scope — already closed in Huly`.
- **Parent coverage check**: Before drafting goals for a parent ticket, list its functional parts from every readable source (text, diagrams, PO documents), map each to the covering child or `NO CHILD`, and ask the user once via `ask_question` which `NO CHILD` parts belong to this work item (`D-NN`).

## 4. Job Type Classification (Stage 1A-0)

The 8 work-item `Type` values from [`work-item-contract`](../../work-item-contract/SKILL.md) are canonical: `feature`, `bugfix`, `refactor`, `optimization`, `migration`, `maintenance`, `investigation`, `documentation`. Read `status` and `status_category` of the ticket (and of each in-scope child):

| Ticket State | Example Statuses | Ask? | Answer → `Type` and Path |
|---|---|---|---|
| **Not started** | `Backlog`, `Todo` | No separate question. Classify the `Type` from sources and state it in the goal question so the user can correct it. | Classified `Type`, new work item (`v1`) |
| **In progress** | `DEV IN PROGRESS` | Ask: **Continue the existing work, or restart?** | **continue** → same `Type`, resume current `vN` at its last approved gate. **restart** → same `Type`, open `vN+1` from Gate 1; what happens to unfinished code is a `Q-NN`. |
| **Built or later** | `Dev Done`, `QA/QC`, `Prod`, `RESOLVED`, `Done` | Ask: **Is this a change, a bug fix, a verification, or documentation?** | **change** → `feature` (observable behavior changes) or `refactor` (behavior unchanged), opening `vN+1` with `change-impact.md` against built code. **bug fix** → `bugfix`. **verification** → `investigation` writing findings to `verification.md` (no code). **documentation** → `documentation` handed to `docs_writer`. |
| **Closed** | `Canceled` / `LOST` | Confirm the user intends to work on a canceled ticket. | Then classify as above. |

When asked, the job-type answer is recorded as the first `D-NN` in `codebase-notes.md` before the goal question.

## 5. Stack Scope Check & Work Sizing

### Stack Scope Check
Compare the stack each part requires against `.agents/stack.json`. Any part whose stack has no installed pack in this workspace is `BLOCKED — out of plugin scope`:
- Inform the user which part is blocked and why (ticket ID, required stack, no pack installed).
- Write no requirements, design, or plan for the blocked part, and never guess its code. List it under **Non-goals** with the reason.
- Continue with supported parts; if only blocked parts remain, return `BLOCKED`.

### Work Sizing
State the work size in plain words inside the goal question (the user can override it via `Edit goals`):

| Size | Signal | Artifacts |
|---|---|---|
| **Small** | Not a `feature`; one checked result, no phase depends on another, no new behavior contract to approve | `brief.md` (phase-free path of `work-item-contract`), with its goal line confirmed by `D-NN` |
| **Work item** | Any `feature`, or multiple dependent results | `requirements.md` + `codebase-notes.md`, Gates 1 / 2 / 3 as the `Type` requires |
| **Several work items** | AC split into groups that can ship and be verified independently | Propose linked work items ([02 — Split Check](02-goal-framing-and-question.md#2-split-check-when-scope-is-multiple-work-items)) |

If a small item later grows a second dependent result or a new behavior contract, record a `D-NN` and upgrade to `requirements.md` + `codebase-notes.md`; never stretch `brief.md` past its purpose.
