# Flutter guide

The Flutter pack is the most complete stack pack. Install it first ([installation guide](installation.md)), then pick an **architecture profile** for your project.

## Architecture profiles

A profile tells the agents where the project's reusable building blocks (base screens, networking, design system…) come from. Profiles are alternatives, not levels.

| Profile | Choose it when the project… | Agents will… |
|---|---|---|
| `external-standard` | has no shared foundation or design system | use standard Flutter widgets and add only the structure the feature needs |
| `external-structured` | already has its own core layer or design system | inspect and reuse the existing patterns and components |

All profiles ship in the same Flutter pack; no extra install is needed.

## Set up a project

Read-only check:

```sh
coder-nexus setup flutter --check
```

Set up with a profile:

```sh
coder-nexus setup flutter --profile external-standard
```

Run against another folder with `--project /absolute/path/to/project`. Without `--profile`, setup asks you.

`READY` means setup is done, not that the app builds or features pass.

## How the profile is used

During planning the agent records the chosen profile in the approved `design.md`:

```yaml
architecture_profile:
  mode: external-structured
  core_source: lib/core/
```

Later roles keep this choice and pass it to the architecture validators. To change the profile, change it in the design and approve it again.

## Where the guidance lives

| Location | Content |
|---|---|
| `skills/flutter-core-package-usage/` (installed) | How each role discovers and reuses foundations |
| `skills/flutter-core-package-usage/references/` | One reference per profile |
| Each shared package's `guidance/GUIDE.md` | When to use (and not use) each API, with examples |

## Good to know

- Agents confirm imports and signatures in the actual package source before using an API.
- Feature work never edits or copies shared package source; missing capabilities are recorded as a gap in `design.md`.
- Validators check common boundaries; project-specific conventions still need code review and runtime tests.
