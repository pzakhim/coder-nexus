# 01 — Huly Workspace Setup & Authentication (`coder-nexus setup huly`)

Configure or re-verify the Huly connection in the Client workspace's **development** `.env` by driving the `coder-nexus setup huly` CLI. The CLI performs all network checks and `.env` writes; the agent only collects inputs from the user and reports results. Finish by showing **one open task** from the user's Huly list.

## 1. When to Run This Guide

- When the user explicitly asks to set up, connect, log in to, fix, or check Huly (e.g., *"setup huly giúp tôi"*, *"connect Huly"*, *"Huly không lấy được task"*).
- Automatically as **Step 1 (Connection & Auth Preflight)** of [`huly-task-intake`](../SKILL.md) whenever `${workspaceFolder}/.env` lacks Huly configuration or a Huly MCP call fails authentication.

## 2. Non-Negotiable Security & Read-Only Rules

- Always pass `--json --project "${workspaceFolder}"`. Read the single JSON object on stdout; progress text goes to stderr.
- `.env` holds **development-only** credentials. Never echo the password or session token in chat, reports, `codebase-notes.md`, work items, or the Hub repository. Never write `.env` directly and never commit it.
- Never invent a URL, email, password, workspace ID, or task. Report only what the CLI returned.
- Huly is strictly **read-only**: setup never creates, updates, or deletes Huly tasks.
- If `coder-nexus` is not found on PATH, instruct the user to run **Coder Nexus: Install / Update CLI** in the IDE and return `BLOCKED`.

## 3. Step-by-Step Setup Workflow

1. **Check current `.env` state:**
   ```bash
   coder-nexus setup huly --json --project "${workspaceFolder}"
   ```
   - `status: already_configured` → skip to **Step 5**.
   - `status: needs_input`, `step: url` → proceed to **Step 2** (or run `coder-nexus init --project "${workspaceFolder}"` if the user only wants `.env` initialized with empty keys to edit manually).
   - `status: needs_input`, `step: account` → show the saved `workspace_url` in `.env` and ask the user to confirm that URL (or provide a new Huly URL to run Step 2 with `--url "<NEW_URL>"`) alongside **Step 3**.
   - `status: verify_failed` → the saved session is expired; inform the user and run **Step 2** with `--reset`.
   - If `warning` is present (`.env` missing from `.gitignore`), show the warning and offer to add `.env` to `.gitignore`.

2. **Configure Huly URL:**
   Ask the user for the Huly URL (suggest `https://huly.app` for Huly Cloud), then run:
   ```bash
   coder-nexus setup huly --json --project "${workspaceFolder}" --url "<URL>"
   ```
   - `url_unreachable` → show `message`, report setup `BLOCKED`, and ask the user to check the URL, VPN, or network. Do not continue.
   - `needs_input`, `step: account` → the URL is saved; continue to **Step 3**.

3. **Authenticate Account:**
   Offer the user two options via `ask_question`:
   - **(Recommended) Run in your own terminal (keep password out of chat):** The user runs `coder-nexus setup huly` in their terminal (it reuses the saved URL and prompts for email and password). Once they confirm completion, re-run **Step 1** to verify.
   - **Provide credentials in chat (passed via stdin):** Ask for email and password, then pipe the password on stdin (never as a CLI argument):
     ```bash
     printf '%s\n' '<PASSWORD>' | coder-nexus setup huly --json --project "${workspaceFolder}" --email "<EMAIL>" --password-stdin
     ```

4. **Check Login Result:**
   - `login_failed` → show `message` and ask for email and password again (repeat **Step 3**). Never guess credentials.
   - `configured` → continue to **Step 5**.

5. **Report Verified Connection & Sample Task:**
   From the JSON output, report:
   - `workspace_url`, `email`, and `workspace_id` (never password or token)
   - `open_task_count`
   - **One open task**: `first_task.id`, `first_task.title`, `first_task.status`, `first_task.priority`
   - If `first_task` is `null`, state that the connection succeeded (`PASS`) and the user currently has 0 open tasks, then return to [`huly-task-intake`](../SKILL.md).

## 4. CLI Exit Codes

| Exit Code | Meaning | Gate Result |
|---|---|---|
| `0` | Configured & verified | `PASS` |
| `1` | Login failed | `FAIL` |
| `2` | URL unreachable | `FAIL` (`BLOCKED`) |
| `3` | Needs user input (`url` or `account`) | `BLOCKED` |
| `4` | Session verification failed (`--reset` needed) | `FAIL` |
| `130` | Aborted by user | `BLOCKED` |
