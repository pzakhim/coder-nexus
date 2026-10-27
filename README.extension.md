# Coder Nexus

**Turn your AI coding agent into a delivery team: requirements → design → plan → code → review → verification, with you approving each key step.**

Coder Nexus installs agent roles, skills and rules into your project. Your host agent (for example Antigravity) uses them when you ask it to build something. Nothing runs on its own.

## What you get

- **7 Agent roles across 2 Departments**:
  - **`dev-team`**: Spec Writer (with Huly + Figma screen/workflow intake at Gate 1), Planning (with Figma token/tree → UI Kit & Clean Architecture audit at Gate 2), Code Writer, Code Reviewer, Test Runner, Docs Writer.
  - **`bug-squad`**: Bug Fixer, Code Reviewer (L2), Test Runner (4-Gate bug reproduction, root-cause forensics, S1–S4 / L1–L3 triage, and verification), plus read-only `debug-investigation` and `feature-testing`.
- **Approval gates**: you approve requirements, screens (`S-NN`) & workflows (`W-NN`) (`Gate 1`), technical design & UI Kit mapping (`Gate 2`), and the implementation plan (`Gate 3`) — or bug triage level (`L1/L2/L3`) — before production code is written.
- **Always-On constitutional rules & stack packs**: Flutter (maintained) and Backend (preview), with profile-aware skill injection (`external-standard`, `external-structured`, `imespro`). One pack per workspace.
- **Skill Factory** *(new in 3.0)*: 22 generators that write skills tailored to *your* project — domain knowledge, requirements, planning, API contracts, change impact, architecture, clean code, unit tests, debugging, migrations, Git workflow and versioning, code review, security, QA and visual checks. Your generated skills take priority over pack skills on the same topic.
- **MCP tools** via the `coder-nexus` CLI: Huly task intake, two-layer Figma extraction (`tokens.json` + `<node>.spec.json` + per-screen `.png`), architecture & spec validators.
- **Architecture dashboard** to see how the pieces fit.

## Getting started

**1. Install the CLI.** Click **Coder Nexus** in the status bar → **Install / Update CLI**. A terminal opens and installs everything it needs.

**2. Sync agents into your project.** Open your project. Click **Sync Now** when prompted, or run **Coder Nexus: Sync Stack to Workspace (Auto-Detect)** from the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`) and pick your stack.

**3. Check your setup.** Run **Coder Nexus: Doctor / Check Environment & CLI**.

**4. Start working.** Talk to your agent using any of the built-in workflows:

| Workflow | Example prompt | What happens |
|---|---|---|
| **`dev-team`** | *"Implement task ABC-12"* | Extracts Huly specs + Figma screens/workflows (`Gate 1`), maps Figma tokens/tree to the UI Kit & Clean Architecture (`Gate 2`), plans phases (`Gate 3`), codes & reviews phase by phase, runs `Test Runner` QA, and records a visual `as-built.md` |
| **`bug-squad`** | *"Fix bug: order list crashes when empty"* | Reproduces first, proves root cause & impact, asks you to confirm `S1–S4` & `L1/L2/L3`, then fixes and verifies |
| **`debug-investigation`** | *"Debug why screen B shows stale data"* | Reproduces/traces with temporary `[DBG-<slug>]` logs, cleans up 100% of temporary edits, and writes `diagnosis.md` |
| **`feature-testing`** | *"Test flow from page A to B to C"* | `Test Runner` executes your scenario on the real app/API (read-only) and writes `test-run-report.md` |

> After updating the extension, run **Install / Update CLI** and the sync again.

## Skill Factory (new in 3.0)

Pack skills are the same for every project. Skill Factory generators study *your* workspace, ask you to confirm the key decisions, and write a skill that matches your code and conventions into `.agents/skills/`. It is yours to edit.

1. In the project terminal, list the generators: `skill-factory list`
2. Copy the ones you need, one by one (`skill-factory get clean-code unit-testing`) or by package (`skill-factory get -p coder`).
3. Ask your agent to run a generator, e.g. `/create-clean-code-skill`. It writes `.agents/skills/clean-code/` and trial-runs it on your code.

| Package | For | Generators |
|---|---|---|
| `coder` | Code Writer | clean architecture, incremental implementation, clean code, unit testing, simplification, bug hunt, root-cause debugging, secure coding, database migrations, Git workflow, API contracts |
| `reviewer` | Code Reviewer | code review, bug hunt, security review and the coding standards it grades against |
| `security` | Security | secure coding standards, security review |
| `quality` | Quality Engineer | test planning, test environment, acceptance tests, QA reporting, visual quality, domain knowledge |
| `planning` | Spec Writer, Planning | domain knowledge, requirements specification, change impact analysis, implementation planning, API contract design |

The `skill-factory` command is installed together with the `coder-nexus` CLI.

## Commands

Open the Command Palette and type **Coder Nexus**, or click **Coder Nexus** in the status bar.

| Command | What it does |
|---|---|
| Quick Actions Menu | All actions in one menu |
| Install / Update CLI | Install or update the `coder-nexus` CLI |
| Doctor / Check Environment & CLI | Check that the CLI and project setup are ready |
| Sync Stack to Workspace (Auto-Detect) | Detect stacks and install the picked pack into the project |
| Install Flutter / Backend Pack in Workspace | Install that pack (asks before replacing a different installed pack) |
| Sync Plugin to Antigravity Global Config | Install the Flutter pack globally |
| Show Architecture Dashboard | Open the architecture overview |

The sync writes to `.agents/` in your project: roles in `agents/`, Always-On constitutional rules in `rules/`, skills in `plugins/coder-nexus/`, and `stack.json` mapping the pack to its folders (edit it if detection guessed wrong).

## Useful CLI commands

Run these in the project's terminal.

| Command | What it does |
|---|---|
| `coder-nexus doctor` | Check the environment |
| `coder-nexus setup huly` | Connect the Huly task tracker (guided) |
| `coder-nexus my-tasks` | List your open tasks |
| `coder-nexus task-detail <ID> --download` | Show a task and save its attachments and Figma frames (`tokens.json`, `<node>.spec.json`, `<node>-SNN.png`) |
| `coder-nexus figma fetch "<url>"` | Fetch a Figma frame into `tokens.json`, `<node>.spec.json`, and per-screen `.png`/`.jpg` |
| `coder-nexus setup flutter --check` | Check Flutter project setup |
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
