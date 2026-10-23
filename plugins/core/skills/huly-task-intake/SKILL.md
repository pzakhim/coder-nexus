---
name: huly-task-intake
description: Connect to Huly, list unfinished tasks, and extract real descriptions and acceptance criteria for development.
---

# Huly Task Runner

Use the Coder Nexus MCP Hub to read the developer's Huly workspace. Huly is read-only. A feature request can also originate from the user without a Huly ticket.

## When to use

Activate when the user asks to list Huly work, inspect a task, extract its acceptance criteria, or begin a feature linked to Huly.

## Workflow

1. Check whether the Client workspace has a usable Huly session or credentials in `${workspaceFolder}/.env`. Never print or copy secret values into reports or the Hub repository. If configuration is missing or authentication fails, switch to the `huly-setup` skill (or ask the developer to run `coder-nexus setup huly` in the Client workspace).
2. Call `huly_get_my_tasks` with `workspace_path: "${workspaceFolder}"` when a task must be selected. It returns only the open tasks assigned to the logged-in user. Pass `include_all: true` only when the user asks for the whole workspace. Show only the tasks actually returned, including their real IDs, titles, status, priority and assignee. If the tool returns `status: error`, show that error and its actionable hint.
3. When the user names a task (an ID like `APP-123`, or a Huly issue link pasted from the browser — pass it as-is), call `huly_get_task_detail` with it and the Client workspace path. The issue does not have to be assigned to the user. If the tool says a bare number matches several issues, ask which full ID they mean. Present its description, acceptance criteria, source links and design references if present. Distinguish a criterion in the ticket from a proposed interpretation or open question. Show the assignee by `assignee_name` when present. If `acceptance_criteria_source` is `none`, the ticket has no explicit criteria: say so and ask the user; do not turn description prose into criteria.
4. **Ticket state and stack:** report `status` / `status_category`. For built, QA, released or canceled tickets, say that the job type must be confirmed (change / bug fix / verification / docs). Flag any part whose stack has no installed pack (e.g. .NET) as `BLOCKED — out of plugin scope`.
5. **Parent / sub-issues:** if the result has `sub_issues`, show them as a short list (ID, title, status, AC count, closed flag). If it has `parent`, show the parent as context. Then apply [parent and sub-issues](references/parent-and-sub-issues.md), starting with its parent coverage check: a parent goes to one spec with the children as requirement sources and planning input; a child is scoped to itself with the parent as context.
6. **Sources beyond the ticket**: the ticket is rarely the full requirement. Call `huly_get_task_detail` with `download: true` before drafting requirements. Then:
   - read `comments` (author, time, text) for decisions and AC changes;
   - open every `sources` item: `READ` documents carry their text; `DOWNLOADED` files (PDF screen specs, images, attachments) are saved under `.superpowers/sources/<ISSUE-ID>/` (Git-ignored, local only, never commit or copy them into work-item docs), so open them and read them (view PDFs and images directly). In requirements cite them by title and Huly origin, not by local path;
   - `UNREACHABLE` (for example a PO document this account cannot open) and `EXTERNAL` links: tell the user exactly which ones, and ask them to attach or paste the content or confirm going ahead without it. Never summarize a source you could not open.
   Hand the result to `spec_writer` for the source inventory (`READ` / `UNREACHABLE` / `NOT_PROVIDED`) and goal framing.
7. Pass verified task facts to `spec_writer`. If the ticket omits an actor, contract, exception, scope boundary or AC, ask the user; record the answer as `USER_CONFIRMED` or mark the dependent item `BLOCKED`. Do not manufacture a task or claim an approval.

## Golden rules

- **Read-Only:** Never create, update, close or delete Huly tasks.
- **Zero Mock Data:** Never fabricate credentials, task rows, business values or a fallback response when authentication or network access fails.
- **Credential boundary:** Personal Huly credentials belong only in the developer's Client environment, never in the Hub repository.
