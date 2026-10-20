# Installation and workspace setup

Coder Nexus has two installation concerns: the host's agent/skill bundle and the Python Hub used by MCP tools. Architecture profiles are instructions within the Flutter bundle, not separately installed packages.

## Extension route

With the extension installed, open the target workspace and run a Command Palette command:

| Command title | Result |
|---|---|
| Coder Nexus: Sync Plugin to Workspace (Auto-Detect) | Suggests a framework and asks you to choose. |
| Coder Nexus: Force Sync Flutter to Workspace | Installs the Flutter FE projection. |
| Coder Nexus: Force Sync Backend (BE) to Workspace | Installs the BE projection. |
| Coder Nexus: Force Sync Frappe UI to Workspace | Selects the preliminary Frappe projection; this workflow is not yet maintained. |
| Coder Nexus: Force Sync Frontend (FE) to Workspace | Currently selects Flutter. |
| Coder Nexus: Sync Plugin to Antigravity Global Config | Explicitly syncs the Flutter FE bundle globally. |
| Coder Nexus: Show Architecture Dashboard | Opens the bundled architecture viewer. |

Workspace installation writes `.agents/plugins/coder-nexus-fe/` or `.agents/plugins/coder-nexus-be/` and copies role files into `.agents/agents/`. The extension replaces the selected plugin projection and removes the alternative FE/BE plugin from that workspace. Keep FE and BE in separate workspaces with the current installer; role filenames overlap. Keep local customizations outside generated projections.

Global extension sync targets `~/.gemini/config/plugins/coder-nexus-fe/`. Extension activation alone does not perform global sync. The extension also provisions bundled Ponytail when it cannot find it in the workspace or global plugin location.

The extension copies an MCP configuration that runs `coder-nexus serve`; that executable must be available to the host. The VSIX does not include the Python Hub runtime. The source route below creates an explicit configuration for a local Hub checkout.

## Source-based CLI route

Use a checkout of this repository, Python 3.12 or later, and `uv`.

To make the `coder-nexus` CLI available globally on your system (e.g. for IDE MCP runtime and terminal commands):

```sh
uv tool install .
```

Alternatively, from the Hub checkout, prepare its local environment:

```sh
uv sync
```

Then choose one target, replacing the example path with the real workspace:

```sh
uv run coder-nexus install-plugin --plugin fe --framework flutter --workspace /absolute/path/to/flutter-client
```

For a separate Backend workspace:

```sh
uv run coder-nexus install-plugin --plugin be --workspace /absolute/path/to/backend
```

Always supply `--workspace` for workspace-only installation. Omitting it defaults to global installation; `--global` explicitly requests global installation.

The CLI projection records source/version metadata in `installed_version.json` and writes `mcp_config.json` with `uv run --offline coder-nexus serve` and the Hub checkout as `cwd`. Keep that checkout and its prepared environment available. The CLI installer does not perform the extension's Ponytail provisioning.

Inspect the generated manifest, role files, skills, and MCP configuration. Confirm host discovery and tool invocation in the target IDE; copied files alone do not prove activation.

### How a projection is built

Plugin sources are split by responsibility and composed by `python -m coder_nexus.plugin_build` (the extension ships the built `plugins/dist/`; the CLI builds from the checkout):

| Source | Holds | Installed as |
|---|---|---|
| `plugins/core/agents/` | Stack-neutral role process (gates, handoffs, task loop) | `.agents/agents/<role>.md`, followed by overlays |
| `plugins/layers/frontend/agents/` | Frontend-shared rules (visual input, 4 visual states, Mockoon, API handshake) | appended to each role for Flutter and Frappe |
| `plugins/packs/<stack>/agents/` | Stack rules (Flutter profiles, BaseScreen, analyzer commands; Frappe resources) | appended last |
| `plugins/core/skills/` | Stack-neutral process skills | `skills/<name>/` |
| `plugins/packs/<stack>/skills/<slot>/` | Stack knowledge for a slot (`core-usage`, `clean-architecture`, `unit-test`, …) | `skills/<stack>-<slot>/` |

Core files refer to stack knowledge as `{{slot:<name>}}`, rendered to `<stack>-<name>`. The build fails a maintained pack when an agent declares a skill that is not installed, a link is broken, or a file mentions another stack's markers (listed in each `pack.json`); preview packs list these gaps in `projection.json`.

Every slot registered in `plugins/core/slots.json` resolves to an installed skill. A pack either implements it, lists it under `not_applicable` (the build installs a skill that tells agents to record `N/A` and continue), or, for a `preview` pack only, gets a generated placeholder that tells agents to stop with `BLOCKED` instead of borrowing another stack's rules. Frappe UI is currently a preview pack: it implements `clean-architecture` (plus `frappe-ui-catalog`) and receives placeholders for the other slots; the extension shows a warning listing them when you sync it. A maintained pack (Flutter) cannot ship with a missing slot.

## External versus iMESPro projects

- **External Flutter:** install the Flutter FE bundle above. Both external profile references are included. There is no separate external distribution or `--profile` installer flag. Planning records the foundation profile and evidence in the approved design (brief for phase-free work); downstream agents pass it explicitly to both validators. External profiles require no company package setup. A real external feature replay remains unverified.
- **iMESPro Flutter:** install the same bundle, then follow the [package setup and knowledge guide](flutter.md).
- **Backend:** install the BE bundle in its own workspace. Both installers project the canonical handshake guide into each selected plugin at `shared_contracts/api_handshake_protocol.md`. Share actual project API contract artifacts and their revisions explicitly between workspaces.

Huly is optional. If used, keep authentication in the target Client's untracked `.env`, not in the Hub checkout or plugin files. A user-supplied request can provide requirements without Huly.

See [README](../../README.md) for current support and verification limits.
