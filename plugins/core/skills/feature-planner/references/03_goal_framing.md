# 03 — Goal Framing (Gate 1, before any other question)

Huly tickets are not uniform. A ticket can be a one-line task, or a feature parent with many children. The real requirements are often elsewhere: a PO document mentioned in the description (which may not open for the developer's account), a PDF linked in a comment, or an AC added in a comment that differs from the FR document. So `spec_writer` does not copy the ticket. It **settles the goals with the user first** and keeps every later artifact on those goals.

## Step 0 — Job type and stack (before anything else)

**Job type.** Read `status` and `status_category` from `huly_get_task_detail` (and from each in-scope child). If the ticket is not new work, ask first, in one `ask_question`, what the job is:

| Ticket state | Example statuses | Ask |
|---|---|---|
| Not started | Backlog, Todo | No question: new implementation is assumed. State it in the goal question. |
| In progress | DEV IN PROGRESS | Continue the existing implementation, or start over? |
| Built or later | Dev Done, QA/QC …, Prod …, RESOLVED, Done | Is this a **change** (new or changed behavior), a **bug fix**, **verification** (test what was built against the ticket), or **documentation**? |
| Closed | Canceled / LOST category | Confirm the user really wants to work on a canceled ticket. |

The answer is the first `D-NN`. It changes the flow. A change gets a new `vN` with `change-impact.md` against the built code. A bug fix follows the fix sequence. Verification produces findings, not new code. Documentation goes to Docs Writer.

**Stack.** Compare the stack the ticket needs with the packs in `.agents/stack.json`. Clues are ticket text, title, sources and comments: for example ".NET", "C#", "Windows service", "Java", "iOS native". Any part whose stack has **no installed pack** is `BLOCKED — out of plugin scope`:
- Tell the user which part is blocked and why ("IMES-1249 is a .NET Windows service; this workspace has no .NET pack").
- Do not write requirements, design or plan for that part, and do not guess its code. List it under Non-goals with the reason.
- Parts in a supported stack continue normally. If only the blocked part remains, stop with `BLOCKED`.

## Step 1 — Source inventory (`codebase-notes.md` → `## 0A. Source Inventory`)

Collect every source once and record it:

| Source | Kind | Read status | What it contributes |
|---|---|---|---|
| IMES-1190 | Huly ticket (child of IMES-1167) | READ | 3 behaviors as prose, no AC |
| IMES-1167 | Huly parent | READ | Feature name, 10 children |
| REQ-MFG-ECN-03 (doc mention) | PO requirements doc | UNREACHABLE (no permission) | — ask user |
| 02_SCREEN_SPEC_WMS_IS_NO_PO.pdf (comment link) | Screen spec PDF | NOT_PROVIDED | — ask user |
| Comment 9/19 "added warning beyond FR" | Huly comment | READ | AC differs from FR doc |

- Kinds: Huly ticket / parent / child / comment / PO doc / PDF / design / user prompt / codebase.
- Read status: `READ`, `UNREACHABLE` (exists but cannot be opened), or `NOT_PROVIDED`.
- Never infer the content of an `UNREACHABLE` or `NOT_PROVIDED` source from its title. Ask the user to attach or paste it, or to confirm that the work goes ahead without it.

## Step 2 — Goal candidates

Draft **1–3 goals**. A goal is an **outcome**, not a feature list:

> `<Actor>` can `<achieve something>` so that `<business result>` — **success signal:** `<observable / measurable check>`

Derive them from the ticket and parent titles, the purpose of the PO document, the AC, and the comments. Also draft:

- **Non-goals**: things mentioned but not in this batch. Examples: closed children, other stacks (for example a .NET agent), "later" items, and siblings of a child ticket.
- **Conflicts**: places where sources disagree (FR document versus ticket AC versus comment).
- **Parent coverage** (for a parent ticket): the parts of the parent that no child covers (see `huly-task-runner` → `references/parent-and-sub-issues.md`).

## Step 3 — The goal question (first `Q-NN`, asked alone)

Before any other question, ask one `ask_question` that shows:

1. the source inventory, including what is missing;
2. the goal candidates with their success signals;
3. the non-goals and the conflicts.

Options: **Confirm goals (Recommended)** / **Edit goals** / **Narrow to G-01 only**. Record the answer as `D-NN` and write `## 0. Goals` with each goal set to `Status: CONFIRMED`, citing that `D-NN`. If the user supplies a missing document, read it and re-check the goals before you lock them.

## Step 4 — Goal lock (rest of the work item)

- **Questions**: each later `Q-NN` names the `G-NN` it serves. A question that serves no goal is not asked; record the topic under Non-goals.
- **Requirements**: every `BR-NN` and `AC-NN` cites a `G-NN`, and every goal has at least one AC. The validator enforces `REQ-005`.
- **Design**: `## Goal alignment` maps each goal to the design elements that deliver it. Remove elements that serve no goal, or record them as a decision with a reason. The validator enforces `DESIGN-007`.
- **Plan**: phases list their `Goals`, and every goal is delivered by at least one phase. The validator enforces `PLAN-V-010`.
- **Gate presentations** (Gate 1, 2 and 3) open with a one-line recap of the goals and anything dropped as a non-goal.
- **Review**: `code_reviewer` flags any change that cannot be traced to a goal (scope creep).
- **Goal change**: if the user changes a goal later, record a new `D-NN`, update `requirements.md`, ask for Gate 1 approval again, and re-check the design and plan.
