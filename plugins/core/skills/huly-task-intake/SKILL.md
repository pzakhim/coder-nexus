---
name: huly-task-intake
description: "Set up or verify the Huly workspace connection (coder-nexus setup huly), list open tasks, and ingest Huly issue details, parent/sub-issues, comments, and downloaded attachments (.superpowers/sources/<ISSUE-ID>/) once into codebase-notes.md so no downstream agent or department re-queries Huly or re-asks the user."
---

# Huly Task Intake & Setup

Use the Coder Nexus CLI and MCP Hub to connect to and read the developer's Huly workspace. Huly is strictly **read-only**. A work item can also start from a direct user request without a Huly ticket.

## Reference Guides

| Guide | Topic |
|---|---|
| [01 — Huly Workspace Setup & Auth](references/01-huly-setup.md) | Driving `coder-nexus setup huly --json --project "${workspaceFolder}"`, `.env` credential safety, login options, and exit codes |
| [02 — Parent & Sub-Issues Traceability](references/02-parent-and-sub-issues.md) | Parent coverage check (`NO CHILD`), scoping open/closed children, Parent-Ticket branch vs Sub-Ticket phase commits, and one-time recording in `codebase-notes.md` |

## When to Use

Activate when:
1. The user asks to set up, connect, log in to, or troubleshoot Huly (follow [01 — Huly Workspace Setup & Auth](references/01-huly-setup.md)).
2. `spec_writer` (in **`dev-team`**) needs to list open Huly tasks, inspect a ticket, download its attachments, or extract its acceptance criteria for Gate 1.

## Workflow (One-Read Huly Protocol)

1. **Step 1 — Connection & Auth Preflight ([01 — Huly Setup](references/01-huly-setup.md))**:
   - Check whether `${workspaceFolder}/.env` has a working Huly session. Never print or copy secret values into chat, reports, or `codebase-notes.md`.
   - If configuration is missing or authentication fails (`needs_input` or `verify_failed`), run [01 — Huly Workspace Setup & Auth](references/01-huly-setup.md) (`coder-nexus setup huly --json --project "${workspaceFolder}"`).

2. **Step 2 — Listing Open Tasks (`huly_get_my_tasks`)**:
   - When the user wants to pick a task from their queue, call `huly_get_my_tasks(workspace_path="${workspaceFolder}")`. Pass `include_all: true` only when the user explicitly asks for the entire workspace.
   - Present only the tasks actually returned (ID, title, status, priority, `assignee_name`). If the tool returns `status: error`, surface the exact message and hint.

3. **Step 3 — Single-Read Task Detail & Attachment Download (`huly_get_task_detail` with `download: true`)**:
   - When the user provides a task ID (e.g., `APP-123`) or a pasted Huly browser URL (pass it as-is), call `huly_get_task_detail` with `download: true` and `workspace_path: "${workspaceFolder}"`.
   - If a bare number matches multiple issues, ask the user which full ID they mean via `ask_question`.
   - Distinguish explicit ticket criteria from proposed interpretations. If `acceptance_criteria_source` is `none`, state that the ticket has no explicit criteria and queue `Q-NN` for the user — never convert description prose silently into `AC-NN`.

4. **Step 4 — Ticket State, Job Type & Stack Scope Check**:
   - Report `status` and `status_category`. For built, QA, released, or canceled tickets, confirm the job type (`change` / `bugfix` / `verification` / `documentation`) per [`work-item-contract`](../work-item-contract/SKILL.md).
   - Flag any part whose stack has no installed pack in this workspace as `BLOCKED — out of plugin scope`.

5. **Step 5 — Parent & Sub-Issues Coverage ([02 — Parent & Sub-Issues](references/02-parent-and-sub-issues.md))**:
   - If the response includes `sub_issues` or `parent`, apply [02 — Parent & Sub-Issues Traceability](references/02-parent-and-sub-issues.md): run the **Parent coverage check** (`| Parent part | Covered by | Status |`), ask once about any `NO CHILD` parts (`D-NN`), and record both the **Parent-Ticket ID** (used by `git-preflight` for branch naming) and **Sub-Ticket IDs** (used for phase commit checkpoints).

6. **Step 6 — Deep Source Inspection (`comments` & `.superpowers/sources/<ISSUE-ID>/`)**:
   - Read all `comments` (author, timestamp, text) for requirement refinements or scope decisions.
   - Inspect every entry in `sources`:
     - `READ` documents include their text directly.
     - `DOWNLOADED` files (PDF screen specs, images, attachments, visual assets) are saved under `.superpowers/sources/<ISSUE-ID>/` (Git-ignored, local only; never commit or copy raw files into `vN/`). Open and read/view every downloaded PDF and image directly; cite them in `requirements.md` by title and Huly origin, not local path.
     - `UNREACHABLE` or `EXTERNAL` links: report the exact titles/URLs to the user and ask via `ask_question` whether they will attach/paste the content or confirm proceeding without it (`D-NN`). Never guess or summarize an unread source.

7. **Step 7 — Consolidate Once in `codebase-notes.md` (Zero Re-Query / Zero Re-Ask Across Departments)**:
   - Record the **Source Inventory** (`READ` / `DOWNLOADED` / `UNREACHABLE` / `EXTERNAL`) and the **Huly Parent / Sub-Issues Table** in `codebase-notes.md` (`## 3. Verified Baseline Facts & Cross-Agent Notes`).
   - Once recorded by `spec_writer`, neither `planning`, `code_writer`, `code_reviewer`, nor `test_runner` (in `dev-team`) ever re-queries Huly or re-asks the user for ticket facts.

## Golden Rules

- **Strictly Read-Only:** Never create, update, close, or delete Huly tasks.
- **Zero Fabrication:** Never invent credentials, task rows, acceptance criteria, or fallback data when authentication or network access fails (`BLOCKED`).
- **Credential Isolation:** Huly credentials live only in `${workspaceFolder}/.env` (untracked), never in work-item docs or the Hub repository.
