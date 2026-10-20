# Parent issues and sub-issues

`huly_get_task_detail` returns `parent` (when the issue is a child) and `sub_issues` (direct children, one level, sorted by number, each with its own `acceptance_criteria`, `acceptance_criteria_source`, `is_closed` and `sub_issue_count`).

## Rule: the parent goes to the spec, the children go to planning

| User links | Spec (`spec_writer`, Gate 1) | Planning (`planning`, Gate 3) |
|---|---|---|
| **Parent issue** (has `sub_issues`) | **One** work item for the whole feature. Build requirements from the parent description **plus** every open child's AC. Every requirement / AC records its source issue ID (e.g. `Huly MOB-11`). | Children are **input**, not the phase list. Re-cut them into vertical behavior phases by dependency. Children are often split by role (BE / FE / design), so do not map one child to one phase. Every open child ID must appear in at least one phase or be marked out of scope. |
| **Child issue** (has `parent`) | Work item scoped to **that child only**. Read the parent for context (feature name, shared terms, constraints) and record it in `codebase-notes.md` as context. Parent AC and sibling scope are **not** in scope unless the user confirms. | As usual. |
| **Standalone issue** | As usual. | As usual. |

## Scope checks (ask with `ask_question`, one at a time; record answers as `D-NN`)

- **Closed children** (`is_closed: true`, DONE or CANCELLED): list them as `Out of scope — already closed in Huly`. Do not write AC for them. Do not reopen them.
- **Many or unrelated children** (more than 8 open, or children that clearly belong to different features): ask the user whether the batch covers all children or a named subset before drafting. The rest are recorded as out of scope for this `vN`.
- **Child without explicit AC** (`acceptance_criteria_source: none`): queue a `Q-NN` for that child. Never turn its prose into criteria.
- **Conflicting AC** between parent and child, or between siblings: queue a `Q-NN`. Never pick one silently.
- **Deeper levels** (`sub_issue_count > 0`): only one level is expanded. List the nested count and ask whether those grandchildren are in scope. If they are, fetch each with `huly_get_task_detail`.
- **Child assigned to someone else**: keep it in the spec when it is in scope, and note the assignee. Ownership is a planning concern, not a reason to drop requirements.

## Recording

- `brief.md` / requirements header: list the source parent and the in-scope child IDs.
- `codebase-notes.md`: consolidate parent and child details once, including a table `| Huly ID | Title | Status | In scope | AC count |`. Downstream agents never re-query Huly.
- `implement-plan.md`: add a traceability table `| Huly ID | AC-NN | Phase |`.
