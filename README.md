# Coder Nexus

**Agent and skill bundles for software delivery in VS Code / Antigravity.**

This extension copies Coder Nexus agent profiles, skills, and rules into the workspace you choose. A host agent uses them to turn a real request into approved requirements, design, implementation, review, and verification. The extension also includes an architecture dashboard. Roles run when the host invokes them; installing the extension does not start an autonomous agent team.

## How the pieces fit

| Part | Responsibility |
|---|---|
| Agent roles | Spec Writer, Designer (UI/UX), Planning, Code Writer, Code Reviewer, Test Runner, and Docs Writer divide delivery responsibilities. |
| Skills and rules | Guide discovery, design, implementation, review, and evidence collection for the target project. |
| Stack packs | Flutter, Frappe UI and Backend packs add stack rules and skills on top of shared, stack-neutral roles. A workspace can hold several packs (e.g. a monorepo with an app and a service). |
| Python MCP Hub | Provides read-only Huly intake, architecture guidance, UX patterns, UI/UX design tooling (`coder-nexus ux …`), and static validators. Install its runtime separately if you need these tools. |
| Extension | Explicitly synchronizes plugins into workspace or global configuration and displays the architecture dashboard. |

Feature work uses three actual user approvals: **requirements → design → implementation plan**. When the work changes what the user sees, the requirements approval also covers an approved UI/UX design revision. Delivery then implements bounded phases, reviews the code revision, records evidence, and performs independent acceptance verification. Work items live under `.superpowers/work-items/<slug>/vN/`; smaller work types have their own sequences.

All stacks share one set of role agents and process skills; each pack adds its own rules and `<stack>-<slot>` skills, and `.agents/stack.json` records which pack owns which paths. The Frontend–Backend API handshake is a documented contract workflow; in separate workspaces agents exchange contract artifacts, in a monorepo each side edits only the paths its pack owns.

## Architecture profiles

The three profiles describe where a Flutter project's reusable foundations come from. They are alternatives, not maturity levels or separate agent teams.

| Profile | Project context | Intended behavior |
|---|---|---|
| `imespro` | Uses company foundations | Verify `app_core`, `app_util`, and `app_ui_kit`, read their guidance, and reuse fitting APIs. |
| `external-structured` | Has its own foundations or design system | Reuse the project's existing patterns and shared components. |
| `external-standard` | Has no established shared foundation | Use the smallest clear implementation and standard framework components. |

All three guides ship in the same Flutter bundle. There is currently no separate installer or `--profile` option for external projects. Profile selection is recorded in the approved design. Company package details live in the separate packages' `guidance/GUIDE.md` files; they are not included in this extension.

Validators accept the selected profile and reserve company-specific checks for iMESPro. External Client conventions still require source inspection, analysis and runtime evidence. A complete external delivery replay is not yet verified.

## Current support

- **Flutter:** the primary maintained delivery workflow, with the deepest guidance for iMESPro packages.
- **Backend:** a preview pack on the shared roles (clean architecture, API contracts, unit tests, review and verification skills); equivalent delivery acceptance has not been demonstrated.
- **Frappe UI:** a preview pack (clean architecture and the Frappe UI catalog). Steps without Frappe guidance install as placeholders that make agents stop with `BLOCKED` instead of borrowing Flutter rules.
- **General Web:** not a pack yet.

The source manifest lists **30 public skills** across shared and pack folders and **9 MCP tools**. Installation selects shared skills plus the chosen packs; it does not install all 30 into every workspace.

## Quickstart

No repository clone is needed. You install the extension, then let it install the CLI.

### 1. Install the extension
In VS Code / Antigravity open **Extensions** (`Cmd+Shift+X` / `Ctrl+Shift+X`), search **Coder Nexus** (`IMP-AIFactory.coder-nexus`, published on Open VSX) and click **Install**. A `.vsix` from [GitHub Releases](https://github.com/pzakhim/coder-nexus/releases) also works (**Install from VSIX...**).

### 2. Install the `coder-nexus` CLI (one click)
The CLI is the MCP server runtime (`coder-nexus serve`) plus the Huly and Flutter setup commands. The extension does not bundle it.

Click **Coder Nexus** in the status bar → **Install / Update CLI** (or run **Coder Nexus: Install / Update CLI**). The terminal installs [`uv`](https://docs.astral.sh/uv/) if missing, then the CLI pinned to the extension version. Manual equivalent:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh        # Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
uv tool install --force git+https://github.com/pzakhim/coder-nexus.git@vX.Y.Z   # X.Y.Z = extension version
coder-nexus --help
```

After updating the extension, run **Install / Update CLI** again so the CLI matches. Run **Coder Nexus: Doctor** to check the CLI.

### 3. Sync agents into your project
Open the project. When the extension recognizes Flutter, Frappe or Backend folders (also in subfolders of a monorepo) it offers **Sync Now**; otherwise run **Coder Nexus: Sync Stacks to Workspace (Auto-Detect)** and tick the stacks the workspace contains. This writes:

- `.agents/plugins/coder-nexus/`: the shared skills plus the `<stack>-*` skills of each selected pack,
- `.agents/agents/`: the seven roles, each followed by the rules of every selected pack,
- `.agents/stack.json`: the selected packs and the paths each one owns (edit the paths if detection guessed wrong).

**Add … Pack to Workspace** commands add one pack to the ones already installed. Re-syncing replaces only these generated files and removes the pre-2.8 `coder-nexus-fe` / `coder-nexus-be` folders. Sync again after the CLI is installed so `mcp_config.json` points at the absolute CLI path (IDEs launched from the Dock/Finder may not see `~/.local/bin`). **Sync Plugin to Antigravity Global Config** is an explicit, separate command (Flutter).

### 4. Connect Huly (optional)
Huly settings live in the project's **development-only** `.env` (`HULY_WORKSPACE_URL`, `HULY_EMAIL`, `HULY_PASSWORD`, `HULY_SESSION_TOKEN`, `HULY_WORKSPACE_ID`).

**Terminal.** From the project folder:

```sh
coder-nexus setup huly           # guided: check .env → Step 1 URL (ping, saved) → Step 2 email/password (retries until login works) → shows 1 open task
coder-nexus setup huly --check   # read-only; exit 0 only when all five values are in .env
coder-nexus setup huly --reset   # ignore saved values and start again (e.g. expired session, new server)
coder-nexus my-tasks             # list open tasks assigned to you
coder-nexus my-tasks --all       # open tasks of the whole workspace
coder-nexus task-detail AUTH-101
```

If the URL cannot be reached, setup stops and nothing is saved. Once it is reachable, the URL is saved before the login step.

**Agent (Antigravity).** Ask the agent to "set up Huly". The `huly-setup` skill drives the same command with `--json`, asks you for the URL and then the account (or lets you type the password in your own terminal), and ends by showing one of your open tasks. Non-interactive flags: `--url`, `--email`, `--password-stdin`, `--json`. Exit codes: `0` ok, `1` login failed, `2` URL unreachable, `3` needs input, `4` verify failed.

> **Make sure `.env` is in your project's `.gitignore`.** `setup huly` warns when it is not. It stores the password and session token in plain text.

To exercise the MCP tools without an agent: `npx @modelcontextprotocol/inspector coder-nexus serve`.

### 5. Flutter setup

```sh
coder-nexus doctor                                              # read-only: Huly status + Flutter gate
coder-nexus setup flutter --check                               # read-only gate
coder-nexus setup flutter --profile external-standard           # any Flutter project
coder-nexus setup flutter --profile imespro                     # company projects
```

`imespro` clones `app-core`, `app-util` and `app-ui-kit` next to the project from the company Git group set in `CODER_NEXUS_CORE_GIT` (for example `export CODER_NEXUS_CORE_GIT=ssh://git@git.example.com/group`); it needs company Git access. Without `--profile`, setup asks; with `--yes` it defaults to `imespro`. Use the extension (step 3) to install plugins: `coder-nexus install-plugin` only works from a source checkout.

## UI/UX design

Every change the user can see gets a UI/UX design that the user approves before technical design. The designer role confirms the workflows (`W-NN`) with the user, then draws static HTML screens (`S-NN`, with their states) and new components (`C-NN`) using only an HTML kit generated from the project's real look. Each work item keeps its design in `.superpowers/work-items/<slug>/vN/design-uiux/`; `uiux.md` is the source of truth and `index.html` shows the workflows in a device frame.

```sh
coder-nexus ux extract --project .                 # design source + .superpowers/ux/kit/
coder-nexus ux viewports --project .               # mobile / tablet / web sizes, asked once per project
coder-nexus ux new --work-item .superpowers/work-items/<slug>/v1 --title "Feature"
coder-nexus ux screen --work-item … --id S01 --slug list --title "…" --steps W-01#1
coder-nexus ux component --work-item … --id C01 --slug warning --title "…" --used-in S01
coder-nexus ux sync --work-item …                  # uiux.md -> data/flows.js for index.html
coder-nexus ux validate --work-item … [--write-hash]
```

`ux validate` (MCP `validate_ux_design`) checks rules UX-001 … UX-010: header and sections, no `TODO` left for review, workflows cite confirmed goals, workflows ↔ screens ↔ files, required states, kit classes only, new components documented, mock data paths, confirmed viewports and design source, and a content hash so an approved design cannot change silently. Requirements then map every workflow (`REQ-006`), the technical design maps every screen and new component (`DESIGN-008`), and review and visual verification compare the running app with the approved revision. Only the Flutter pack has a design source today; Frappe UI gets a `BLOCKED` placeholder and Backend has no UI. Screenshots of designs (`ux shoot`) and a real ticket pilot are not done yet.

## Verification and boundaries

The Hub suite (`uv run --offline python -m pytest -q`) covers validators, Huly adapter, setup, profile regression and CLI/extension installation. These are Hub and packaging checks. A real approved feature replay through host invocation, implementation, review, runtime visuals, and acceptance testing remains **NOT_RUN**.

Huly operations are read-only. Credentials belong in the Client's untracked `.env`. Agents cannot self-approve gates, invent package APIs, or turn `BLOCKED`, `NOT_RUN`, or `UNVERIFIED` into `PASS`. Lexical validators do not replace Client analysis and runtime tests.

More documentation (not included in the VSIX):

- [Installation and CLI setup](https://github.com/pzakhim/coder-nexus/blob/main/docs/guides/installation.md)
- [Flutter profiles and iMESPro packages](https://github.com/pzakhim/coder-nexus/blob/main/docs/guides/flutter.md)
- Release notes: [GitHub Releases](https://github.com/pzakhim/coder-nexus/releases)

Maintained by IMP-AIFactory.
