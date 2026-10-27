# 02 — Parent Issues, Sub-Issues & Git / Plan Traceability

`huly_get_task_detail` returns `parent` (when the issue is a child) and `sub_issues` (direct children, one level, sorted by number, each with its own `acceptance_criteria`, `acceptance_criteria_source`, `is_closed`, and `sub_issue_count`).

## 1. Core Rule: Parent Goes to Spec, Children Feed Planning & Commits

| User Links | Spec (`spec_writer`, Gate 1 in `dev-team`) | Branch & Commit (`git-preflight`) | Planning (`planning`, Gate 3 in `dev-team`) |
|---|---|---|---|
| **Parent issue** (has `sub_issues`) | **One** work item for the whole feature. Build requirements from the parent description **plus** every open child's AC. Every requirement / `AC-NN` records its source issue ID (e.g., `Huly MOB-11`). | Branch is named after the **Parent-Ticket**: `<type>/<PARENT-TICKET>-<short-description>`. Phase commits cite the **Sub-Ticket**: `<type>(<SUB-TICKET>): <summary> [parent: <PARENT-TICKET>, PHASE-NN]`. | Children are **input**, not the phase list. Re-cut them into vertical behavior phases by dependency. Children are often split by role (BE / FE / design), so never map one child blindly to one phase. Every open child ID must appear in at least one phase or be marked out of scope. |
| **Child issue** (has `parent`) | Work item scoped to **that child only**. Read the parent for context (feature name, shared terms, constraints) and record it in `codebase-notes.md` as context. Parent AC and sibling scope are **not** in scope unless the user confirms (`D-NN`). | Branch is named after the **Parent-Ticket** (`<type>/<PARENT-TICKET>-<short-description>`) when working on a sub-issue of a parent feature, or `<type>/<CHILD-TICKET>-<short-description>` if standalone; commits cite `<SUB-TICKET>` and `[parent: <PARENT-TICKET>, PHASE-NN]`. | Standard vertical phase breakdown for the scoped child. |
| **Standalone issue** | Standard single-ticket intake. | Branch: `<type>/<TICKET>-<short-description>`; commit: `<type>(<TICKET>): [PHASE-NN] <summary>`. | Standard vertical phase breakdown. |

## 2. Parent Coverage Check (Mandatory Before Drafting Requirements)

Children often cover only part of the parent issue. Before drafting `requirements.md`:

1. List the parent's functional parts from every readable source: description text, downloaded images/diagrams, and readable PO documents in `.superpowers/sources/<ISSUE-ID>/`.
2. Map each part to the child issue that covers it, or to `NO CHILD`.
3. Show the user one table (`| Parent part | Covered by | Status |`) and ask once with `ask_question`: which `NO CHILD` parts belong to this work item, and which are out of scope or tracked elsewhere. Record the confirmed answer as `D-NN` in `codebase-notes.md`.

Never silently drop a `NO CHILD` part, and never invent a child ticket for it.

## 3. Scope Checks (One Question at a Time via `ask_question` → `D-NN`)

- **Closed children** (`is_closed: true`, `DONE` or `CANCELLED`): list them as `Out of scope — already closed in Huly`. Do not write `AC-NN` for them and do not reopen them.
- **Many or unrelated children** (more than 8 open, or children that belong to different features): ask the user whether the current `vN` batch covers all open children or a named subset before drafting. Record the rest as out of scope for this `vN`.
- **Child without explicit AC** (`acceptance_criteria_source: none`): queue a `Q-NN` for that child. Never turn description prose into acceptance criteria without user confirmation.
- **Conflicting AC** between parent and child, or between siblings: queue a `Q-NN` (`grilling` + `solution-options`). Never pick one silently.
- **Deeper levels** (`sub_issue_count > 0`): only one level is expanded automatically. List the nested count and ask whether those grandchildren are in scope; if yes, fetch each with `huly_get_task_detail(..., download: true)`.
- **Child assigned to someone else**: keep it in the spec when it is in scope and note `assignee_name`. Ownership is a planning concern, not a reason to drop requirements.

## 4. One-Time Recording in `codebase-notes.md` (Zero Re-Query Across Departments)

- **`requirements.md` / `brief.md` header**: list the source Parent-Ticket ID and all in-scope Sub-Ticket IDs.
- **`codebase-notes.md` (`## 3. Verified Baseline Facts & Cross-Agent Notes`)**: consolidate parent and child details **once** in a permanent table:

| Huly ID | Role (`Parent` / `Sub-issue` / `Standalone`) | Title | Status | Assignee | In Scope (`YES`/`NO`) | Explicit AC Count |
|---|---|---|---|---|---|---|
| `IMES-1200` | `Parent` | `<title>` | `In Progress` | `<name>` | `YES` | 4 |
| `IMES-1201` | `Sub-issue` | `<title>` | `Todo` | `<name>` | `YES` | 3 |

- **`implementation-plan.md`**: include the traceability table `| Huly ID | AC-NN | Phase |` so `code_writer` knows which `<SUB-TICKET>` to cite in each phase commit.
- Downstream agents (`planning`, `code_writer`, `code_reviewer`, `test_runner`, `docs_writer` in `dev-team`) read `codebase-notes.md` and `.superpowers/sources/<ISSUE-ID>/` directly and **never re-query Huly**.
