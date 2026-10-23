# Source intake (Stage 1A)

Collect every source once, before any question, and record it in `codebase-notes.md` → `## 0A. Source Inventory`. No question is asked in this stage.

## What to read

| Pillar | How | Notes |
|---|---|---|
| Huly ticket, parent, children, comments | [`huly-task-intake`](../../huly-task-intake/SKILL.md) (`huly_get_task_detail`), once | Comments often add or change AC; read them all. |
| Downloads | `.superpowers/sources/<ISSUE-ID>/` | Open images and diagrams; a diagram can show parts no child covers. |
| PO / BA documents, PDFs, designs | Open every mention and link you can | Unopenable means `UNREACHABLE`, never "probably says ...". |
| User prompt | The request itself | Counts as a source; cite it. |
| Codebase | `rg -n` / `rg --files`, read-only | Learn how the touched parts work today and what the change would touch. Verified facts go to `## 3. Verified Baseline Facts & Cross-Agent Notes`. |
| Stack-specific pillars | As the installed stack rules define (for example design exports, API sources) | Record a missing pillar; never invent it. |

Read until you can explain, in a few lines, how the relevant parts work today. That read feeds the read-back in the goal question.

## Source Inventory

Use the table already in the `codebase-notes.md` template; do not rename its heading or columns.

| Source | Kind | Read status | What it contributes / conflicts |
|---|---|---|---|
| IMES-1190 | Huly ticket (child of IMES-1167) | READ | 3 behaviors as prose, no AC |
| IMES-1167 | Huly parent | READ | Feature name, 10 children |
| REQ-MFG-ECN-03 (mentioned in description) | PO requirements doc | UNREACHABLE (no permission) | Ask the user |
| Screen spec PDF (comment link) | PDF | NOT_PROVIDED | Ask the user |
| Comment 9/19 "added warning beyond FR" | Huly comment | READ | AC differs from FR doc |

- **Kind**: Huly ticket / parent / child / comment / PO doc / PDF / design / user prompt / codebase.
- **Read status**: `READ`; `UNREACHABLE` (exists, cannot be opened); `NOT_PROVIDED` (referenced or expected, not supplied).
- Each `UNREACHABLE` / `NOT_PROVIDED` row goes into the sufficiency summary's "Missing" line. If it could change the goals, ask for it before the goals are confirmed.

## Parent and child tickets

Follow [`huly-task-intake` → parent and sub-issues](../../huly-task-intake/references/parent-and-sub-issues.md): a parent gives one work item built from the parent plus every open child's AC (each tagged with its Huly ID); a child scopes the item to that child with the parent as context; closed children are out of scope.

**Parent coverage.** Before drafting goals for a parent, list its parts from every readable source (text, diagrams, readable documents), map each to the child that covers it or to `NO CHILD`, and ask once about the `NO CHILD` parts. Never drop one silently and never invent a child for it. Record the answer as a `D-NN`.

## Conflicts between sources

Write each disagreement into the inventory's last column and carry it to the goal question: FR document versus ticket AC, comment versus description, parent versus child, sibling versus sibling. Never pick a side yourself. A conflict that changes a goal is settled in the goal question; one that changes only a rule becomes a `Q-NN`.
