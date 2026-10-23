# Installation guide

Coder Nexus has two things to install:

1. **Agent bundle**: roles, skills and rules copied into your project (or globally). Done by the extension or the CLI.
2. **`coder-nexus` CLI**: the MCP server (`coder-nexus serve`) and terminal commands. The extension does not bundle it.

## Option A: Using the extension (recommended)

### Install the CLI
Click **Coder Nexus** in the status bar → **Install / Update CLI**, or run that command from the Command Palette. Then check it:

```sh
coder-nexus doctor
```

### Sync the agent bundle
Open your project and run one of these commands from the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`):

| Command | Result |
|---|---|
| Coder Nexus: Sync Stack to Workspace (Auto-Detect) | Detects supported stacks (root and two folder levels down) and lets you pick one |
| Coder Nexus: Install Flutter Pack in Workspace | Installs the Flutter pack |
| Coder Nexus: Install Backend Pack in Workspace (preview) | Installs the Backend pack |
| Coder Nexus: Sync Plugin to Antigravity Global Config | Installs the Flutter pack globally (`~/.gemini/config/plugins/coder-nexus/`) |
| Coder Nexus: Show Architecture Dashboard | Opens the architecture viewer |

A workspace holds **one pack**. Installing the same pack again refreshes it. Installing a different pack asks you to confirm, then replaces the installed one; packs are never merged.

### What gets written

| Path | Content |
|---|---|
| `.agents/agents/<role>.md` | Each agent role, followed by the rules of the installed pack |
| `.agents/plugins/coder-nexus/skills/` | Shared skills plus the pack's `<stack>-*` skills |
| `.agents/plugins/coder-nexus/mcp_config.json` | How the host starts the MCP server |
| `.agents/stack.json` | The installed pack and the folders it owns |

Example `stack.json` for a Flutter app in a subfolder:

```json
{
  "packs": [
    { "stack": "flutter", "status": "maintained", "paths": ["apps/mobile"] }
  ]
}
```

Edit `paths` if auto-detection guessed wrong; re-syncing the same pack keeps your paths.

### Tips
- Re-syncing replaces only generated files. Keep your own customizations outside `.agents/plugins/coder-nexus/` and `.agents/agents/`.
- Sync again **after** installing or updating the CLI, so `mcp_config.json` uses the CLI's absolute path. IDEs started from the Dock or Finder may not see `~/.local/bin`.
- After updating the extension, run **Install / Update CLI** again so versions match.

## Option B: From source (CLI only)

Requirements: Python 3.12+ and [`uv`](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/pzakhim/coder-nexus.git
```

```sh
cd coder-nexus
```

```sh
uv sync
```

Make the CLI available everywhere (optional):

```sh
uv tool install .
```

Install the bundle into a project. Always pass `--workspace`; without it the bundle is installed globally.

```sh
uv run coder-nexus install-plugin --pack flutter --workspace /absolute/path/to/project
```

A workspace holds one pack. To switch a workspace to another pack, replace the installed one:

```sh
uv run coder-nexus install-plugin --pack backend --replace --workspace /absolute/path/to/project
```

With this route `mcp_config.json` runs the server from your checkout, so keep the checkout and its environment in place.

## Verify the installation

1. Open the project in your IDE and check that the agent roles and skills are listed.
2. Ask the agent to call a Coder Nexus MCP tool.
3. Or inspect the tools directly:

```sh
npx @modelcontextprotocol/inspector coder-nexus serve
```

Copied files alone do not prove the host picked them up. Always confirm in the IDE.

## Optional: task tracker

```sh
coder-nexus setup huly
```

Credentials are saved in the project's local `.env`. Keep `.env` in `.gitignore`. You can also skip the tracker and give requirements directly in chat.

## How a projection is built

For contributors. Plugin sources are split by responsibility and combined by `python -m coder_nexus.plugin_build`. The extension ships the prebuilt result in `plugins/dist/`; the CLI builds from the checkout.

| Source | Holds | Installed as |
|---|---|---|
| `plugins/core/agents/` | Stack-neutral role process (gates, handoffs, task loop) | `.agents/agents/<role>.md` |
| `plugins/layers/<layer>/agents/` | Rules shared by a group of stacks (e.g. frontend) | Appended to each role |
| `plugins/packs/<stack>/agents/` | Stack-specific rules | Appended for the installed pack |
| `plugins/core/skills/` | Stack-neutral process skills | `skills/<name>/` |
| `plugins/packs/<stack>/skills/<slot>/` | Stack knowledge for one slot (`clean-architecture`, `unit-testing`, …) | `skills/<stack>-<slot>/` |

Core files refer to stack knowledge as `{{slot:<name>}}`, rendered to `<stack>-<name>`. Every slot listed in `plugins/core/slots.json` must resolve to a skill. A pack either implements it, marks it `not_applicable` (agents record `N/A`), or, for a preview pack only, gets a placeholder that makes agents stop with `BLOCKED` instead of borrowing another stack's rules.

The build produces one projection per pack and layout (`workspace-backend`, `workspace-flutter`, `global-backend`, `global-flutter`); packs are not combined. It fails a maintained pack when a declared skill is missing, a link is broken, or a file mentions another stack's markers.
