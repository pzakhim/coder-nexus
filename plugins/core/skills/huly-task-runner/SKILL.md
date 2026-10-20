---
name: huly-task-runner
description: Connect to Huly, list unfinished tasks, and extract real descriptions and acceptance criteria for development.
---

# Huly Task Runner

Use the Coder Nexus MCP Hub to read the developer's Huly workspace. Huly is read-only. A feature request can also originate from the user without a Huly ticket.

## When to use

Activate when the user asks to list Huly work, inspect a task, extract its acceptance criteria, or begin a feature linked to Huly.

## Workflow

1. Check whether the Client workspace has a usable Huly session or credentials in `${workspaceFolder}/.env`. Never print or copy secret values into reports or the Hub repository. If configuration is missing, explain that the developer must configure the Client workspace or run `uv run coder-nexus login`.
2. Call `huly_get_my_tasks` with `workspace_path: "${workspaceFolder}"` when a task must be selected. Show only the tasks actually returned, including their real IDs, titles, status, priority and assignee. If the tool returns `status: error`, show that error and its actionable hint.
3. When the user selects an actual task ID, call `huly_get_task_detail` with that ID and the Client workspace path. Present its description, acceptance criteria, source links and Figma references if present. Distinguish a criterion in the ticket from a proposed interpretation or open question.
4. Pass verified task facts to `spec_writer`. If the ticket omits an actor, contract, exception, scope boundary or AC, ask the user; record the answer as `USER_CONFIRMED` or mark the dependent item `BLOCKED`. Do not manufacture a task or claim an approval.

## Golden rules

- **Read-Only:** Never create, update, close or delete Huly tasks.
- **Zero Mock Data:** Never fabricate credentials, task rows, business values or a fallback response when authentication or network access fails.
- **Credential boundary:** Personal Huly credentials belong only in the developer's Client environment, never in the Hub repository.
