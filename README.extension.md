# Coder Nexus

**Turn your AI coding agent into a delivery team: requirements → design → plan → code → review → verification, with you approving each key step.**

Coder Nexus installs agent roles, skills and rules into your project. Your host agent (for example Antigravity) uses them when you ask it to build something. Nothing runs on its own.

## What you get

- **Agent roles**: Spec Writer, Designer (UI/UX), Planning, Code Writer, Code Reviewer, Test Runner, Docs Writer.
- **Approval gates**: you approve requirements, design and the plan before any code is written.
- **Stack packs**: Flutter, Backend (preview), Frappe UI (preview). Several packs can live in one workspace.
- **Skill Factory** *(new in 3.0)*: 16 generators that write skills tailored to *your* project — architecture, clean code, unit tests, debugging, migrations, code review, security, QA and visual checks. Your generated skills take priority over pack skills on the same topic.
- **MCP tools** via the `coder-nexus` CLI: task intake, UI/UX design tooling, validators.
- **Architecture dashboard** to see how the pieces fit.

## Getting started

**1. Install the CLI.** Click **Coder Nexus** in the status bar → **Install / Update CLI**. A terminal opens and installs everything it needs.

**2. Sync agents into your project.** Open your project. Click **Sync Now** when prompted, or run **Coder Nexus: Sync Stacks to Workspace (Auto-Detect)** from the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`) and tick your stacks.

**3. Check your setup.** Run **Coder Nexus: Doctor / Check Environment & CLI**.

**4. Start working.** Ask your agent, e.g. *"Implement task ABC-12"* or *"Add a settings screen"*. It will stop at each gate for your approval.

> After updating the extension, run **Install / Update CLI** and the sync again.

## Skill Factory (new in 3.0)

Pack skills are the same for every project. Skill Factory generators study *your* workspace, ask you to confirm the key decisions, and write a skill that matches your code and conventions into `.agents/skills/`. It is yours to edit.

1. In the project terminal, list the generators: `skill-factory list`
2. Copy the ones you need, one by one (`skill-factory get clean-code unit-testing`) or by package (`skill-factory get -p coder`).
3. Ask your agent to run a generator, e.g. `/create-clean-code-skill`. It writes `.agents/skills/clean-code/` and trial-runs it on your code.

| Package | For | Generators |
|---|---|---|
| `coder` | Code Writer | clean architecture, incremental implementation, clean code, unit testing, simplification, bug hunt, root-cause debugging, secure coding, database migrations |
| `reviewer` | Code Reviewer | code review, bug hunt, security review and the coding standards it grades against |
| `security` | Security | secure coding standards, security review |
| `quality` | Quality Engineer | test planning, test environment, acceptance tests, QA reporting, visual quality |

The `skill-factory` command is installed together with the `coder-nexus` CLI.

## Commands

Open the Command Palette and type **Coder Nexus**, or click **Coder Nexus** in the status bar.

| Command | What it does |
|---|---|
| Quick Actions Menu | All actions in one menu |
| Install / Update CLI | Install or update the `coder-nexus` CLI |
| Doctor / Check Environment & CLI | Check that the CLI and project setup are ready |
| Sync Stacks to Workspace (Auto-Detect) | Detect stacks and install agents into the project |
| Add Flutter / Backend / Frappe UI Pack to Workspace | Add one more pack to the project |
| Sync Plugin to Antigravity Global Config | Install the Flutter pack globally |
| Show Architecture Dashboard | Open the architecture overview |

The sync writes to `.agents/` in your project: roles in `agents/`, skills in `plugins/coder-nexus/`, and `stack.json` mapping each pack to its folders (edit it if detection guessed wrong).

## Useful CLI commands

Run these in the project's terminal.

| Command | What it does |
|---|---|
| `coder-nexus doctor` | Check the environment |
| `coder-nexus setup huly` | Connect the Huly task tracker (guided) |
| `coder-nexus my-tasks` | List your open tasks |
| `coder-nexus task-detail <ID> --download` | Show a task and save its attachments and designs |
| `coder-nexus setup flutter --check` | Check Flutter project setup |
| `coder-nexus ux extract --project .` | Prepare the UI/UX design kit from your project |
| `coder-nexus ux validate --work-item <dir>` | Check a design before approval |
| `skill-factory list` | List the Skill Factory generators |
| `skill-factory get -p <package>` | Copy a package of generators into the project |

Credentials for Huly and Figma (`FIGMA_TOKEN`) go into the project's local `.env`. **Keep `.env` in `.gitignore`.**

## Requirements

- VS Code 1.75+ or Antigravity
- Internet access for the first CLI install

## Learn more

- [Documentation & source](https://github.com/pzakhim/coder-nexus)
- [Skill Factory guide](https://github.com/pzakhim/coder-nexus/blob/main/docs/guides/skill-factory.md)
- [Release notes](https://github.com/pzakhim/coder-nexus/releases)
