# Flutter profiles and iMESPro knowledge

Flutter is the primary maintained delivery workflow. The same six roles serve three foundation profiles. Start with [installation](installation.md); installing the bundle and resolving application packages are separate steps.

## Where detailed guidance lives

| Source | Purpose |
|---|---|
| [core-usage](../../plugins/packs/flutter/skills/core-usage/SKILL.md) | Profile discovery and per-role reuse instructions. |
| [iMESPro profile](../../plugins/packs/flutter/skills/core-usage/references/01_profile_imespro.md) | Company package setup, imports, and reuse rules. |
| [External structured profile](../../plugins/packs/flutter/skills/core-usage/references/02_profile_external_structured.md) | Existing Client foundations and design system reuse. |
| [External standard profile](../../plugins/packs/flutter/skills/core-usage/references/03_profile_external_standard.md) | Minimal Flutter implementation without a pre-existing core. |
| Each resolved package's `guidance/GUIDE.md` | API selection, “Use when” / “Do not use when”, and linked examples. |
| Each resolved package's `lib/` source | Actual signatures and implementation evidence. |

The profile references ship under `skills/core-usage/references/` in the installed Flutter plugin. Company packages and guides remain separate repositories; the extension does not bundle those libraries into an external Client.

## iMESPro foundations

| Package | Responsibility | Examples to verify against resolved source |
|---|---|---|
| `app_core` | Architecture contracts, screen lifecycle, reusable screen/list foundations | `BaseScreen`, use-case contracts, mappers, paging. |
| `app_util` | Result/error handling, networking, parsing, storage and system helpers | `DataState`, `ApiService`, parsing and network extensions. |
| `app_ui_kit` | Design system and reusable UI | Buttons, form fields, dialogs, navigation and tokens. |

Read the relevant GUIDE before choosing an API. Reuse when its “Use when” fits; when several choices fit, obtain the required choice. Otherwise use the smallest Client implementation and record a Core gap in `design.md`. Confirm imports and signatures in the resolved package, and keep Domain independent of Flutter. Client feature work does not authorize editing or copying company package source.

The usual layout is:

```text
workspace-parent/
├── client/
├── app-core/
├── app-util/
└── app-ui-kit/
```

From the Hub checkout, check the actual Client without writing to it:

```sh
uv run coder-nexus setup flutter --check --project /absolute/path/to/client
```

For an iMESPro project that needs setup, the mutating command is:

```sh
uv run coder-nexus setup flutter --project /absolute/path/to/client
```

Package cloning needs the company Git group in `CODER_NEXUS_CORE_GIT` (for example `export CODER_NEXUS_CORE_GIT=ssh://git@git.example.com/group`); without it setup reports the missing variable instead of cloning. Setup can offer project creation and package cloning, update dependencies, and resolve packages. Git authentication uses existing SSH or credential-helper configuration; company repository access is required. Inspect setup output and repeat the read-only check. `READY` is a setup result, not proof that every package API, analyzer, runtime screen, or feature acceptance check passed.

## External projects

`external-structured` means the Client already has useful shared foundations. Inspect real consumers before choosing bases, state, routing, DI, and design tokens. An empty `core/` directory is not enough architectural evidence.

`external-standard` means no established foundation is available. Use standard Flutter widgets and add only the structure needed by the approved behavior. Do not add company packages solely to satisfy an unrelated rule.

Planning records the selected profile in the approved `design.md`, for example:

```yaml
architecture_profile:
  mode: external-structured
  core_source: lib/core/
```

Planning records dependency/base/consumer evidence alongside this block. Neighboring company folders alone never select iMESPro; empty shared folders never prove an external foundation. Downstream roles preserve the approved selection and pass `mode` as `architecture_profile` to `validate_architecture_code` and `validate_module_architecture`. Omitted arguments retain legacy iMESPro behavior, so new agent calls must include the profile.

External validation checks common boundaries without requiring company classes or layout. Client-specific base classes, state, network, DI and paths still require inspection against the approved mapping; `UNVERIFIED` is not a runtime pass.
