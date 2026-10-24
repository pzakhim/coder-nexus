---
name: huly-setup
description: Set up (or re-check) the Huly connection for this Client workspace by running `coder-nexus setup huly`, then prove it works by showing one of the user's open Huly tasks.
---

# Huly Setup

Configure the Huly connection in the Client workspace's **development** `.env` by driving the `coder-nexus setup huly` CLI. The CLI does all checks and writes; you only collect answers from the user and report results. Finish by showing **one open task** from the user's Huly list.

## When to use

Activate when the user asks to set up, connect, log in to, fix or check Huly (for example "setup huly giúp tôi", "connect Huly", "Huly không lấy được task").

## Rules

- Always pass `--json --project "${workspaceFolder}"`. Read the single JSON object on stdout; progress text goes to stderr.
- `.env` holds **development-only** credentials. Never echo the password or session token in chat, reports, work items or the Hub repository. Never write `.env` yourself and never commit it.
- Never invent a URL, email, password, workspace ID or task. Show only what the CLI returned.
- Huly is read-only: setup never creates or edits Huly tasks.
- If `coder-nexus` is not found, tell the user to run **Coder Nexus: Install / Update CLI** in the IDE and stop.

## Workflow

1. **Check what is already in `.env`:**
   `coder-nexus setup huly --json --project "${workspaceFolder}"`
   - `status: already_configured` → go to step 5.
   - `status: needs_input`, `step: url` → step 2. (You can also run `coder-nexus init --project "${workspaceFolder}"` if the user only wants `.env` initialized with empty keys to edit manually.)
   - `status: needs_input`, `step: account` → tell the user which `workspace_url` is currently saved in `.env` and ask them to confirm that URL (or give a different Huly URL, in which case run step 2 with `--url "<NEW_URL>"`) alongside step 3.
   - `status: verify_failed` → the saved session is likely expired; tell the user and run step 2 with `--reset`.
   - If `warning` is present (`.env` missing from `.gitignore`), show it and offer to add `.env` to `.gitignore`.

2. **Step 1: URL.** Ask the user for the Huly URL (suggest `https://huly.app` for Huly Cloud). Then run:
   `coder-nexus setup huly --json --project "${workspaceFolder}" --url "<URL>"`
   - `url_unreachable` → show `message`, say setup stopped, and ask the user to check the URL, VPN or network. Do not continue.
   - `needs_input`, `step: account` → the URL is saved. Continue to step 3.

3. **Step 2: account.** Offer the user two options:
   - **(a) Keep the password out of chat:** the user runs `coder-nexus setup huly` in their own terminal. It reuses the saved URL, asks for email and password, and retries until login succeeds. When they say it is done, go to step 1 to read the result.
   - **(b) Give it to you:** ask for email and password, then pass the password on stdin (never as an argument):
     `printf '%s\n' '<PASSWORD>' | coder-nexus setup huly --json --project "${workspaceFolder}" --email "<EMAIL>" --password-stdin`

4. **Login result.**
   - `login_failed` → show `message` and ask for email and password again (repeat step 3). Do not guess credentials.
   - `configured` → continue to step 5.

5. **Show the result.** From the JSON, report:
   - URL, email and workspace ID (never the password or token)
   - `open_task_count`
   - **one open task**: `first_task.id`, `first_task.title`, `first_task.status`, `first_task.priority`

   If `first_task` is `null`, say the connection works but the user has no open tasks. Offer to continue with `huly-task-intake` (task detail and acceptance criteria).

## Exit codes

`0` ok · `1` login failed · `2` URL unreachable · `3` needs input · `4` verify failed · `130` aborted
