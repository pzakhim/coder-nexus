# Skill Factory

Generators (`create-*-skill`) that turn one shared **base** into a skill tailored to each workspace, plus an agent-driven way to push base changes into every workspace that uses them.

- **Base** lives here, in Git, versioned per generator.
- **Workspace skill** is generated into `<workspace>/.agents/skills/<name>/` after the user confirms the key decisions, then grows with the workspace inside `custom` blocks and project-owned files.
- **Sync** is done by the agent reading the CHANGELOG and editing the workspace files — no scripts.
- **Provenance** (which workspace uses which version) is private: `~/.claude/skill-factory-registry/`, never in a workspace or this repo.
- **Scope: manual workspaces only.** Workspaces synced by the Coder Nexus extension (`.agents/plugins/coder-nexus/`, e.g. `AIFactory/examples/*`) are managed by Coder Nexus; the generators stop for them (`core/workflow.md` Step 0).

## Layout

```
skill-factory/
  core/                          # shared by every generator (not a skill)
    workflow.md                  # Step 0 + the 9 standard steps
    authoring-guide.md           # mandatory vs suggested, explain the why, description
    trial-run.md                 # with/without-skill check on real workspace tasks
    detect-stack.md              # stack, fullstack, monorepo detection
    existing-project.md          # P1–P5 lessons for existing workspaces
    research-guide.md
    layouts.md                   # flat vs shared/be/fe
    provenance.md                # private registry format
    versioning.md                # VERSION + CHANGELOG rules
    sync-protocol.md             # how an agent syncs a workspace
    checklist-common.md
    coder-skill-family.md        # ownership & vocabulary shared by all Code Writer skills
  generators/
    create-clean-architecture-skill/          # VERSION, CHANGELOG.md, SKILL.md, references/, stacks/, templates/
    create-incremental-implementation-skill/  # VERSION, CHANGELOG.md, SKILL.md, references/, templates/
    create-clean-code-skill/                  # VERSION, CHANGELOG.md, SKILL.md, references/, templates/
  sync-workspace-skills/         # skill: status table + sync, workspace by workspace
  ROADMAP.md                     # planned coder skills
```

## Install (per machine)

Claude Code loads skills from `~/.claude/skills/`. Link the factory once, then each skill:

```bash
ln -s "$PWD/skill-factory" ~/.claude/skill-factory
```

```bash
ln -s ~/.claude/skill-factory/generators/create-clean-architecture-skill ~/.claude/skills/create-clean-architecture-skill
```

```bash
ln -s ~/.claude/skill-factory/generators/create-incremental-implementation-skill ~/.claude/skills/create-incremental-implementation-skill
```

```bash
ln -s ~/.claude/skill-factory/generators/create-clean-code-skill ~/.claude/skills/create-clean-code-skill
```

```bash
ln -s ~/.claude/skill-factory/sync-workspace-skills ~/.claude/skills/sync-workspace-skills
```

Run the commands from the repository root. Generators refer to shared files as `~/.claude/skill-factory/core/...`, so the first link is required.

## Use

| Goal | Run in the workspace |
|---|---|
| Create a workspace skill | `/create-clean-architecture-skill`, `/create-incremental-implementation-skill`, `/create-clean-code-skill` |
| Adopt an existing, unregistered skill | Run its generator (it detects the skill and adopts it) |
| Sync this workspace after the base changed | `/sync-workspace-skills` |
| Check / sync every workspace | `/sync-workspace-skills all` |

## Change a generator

1. Edit the generator.
2. Bump `VERSION` and add a `CHANGELOG.md` entry with **Affects** and **Migration** ([core/versioning.md](core/versioning.md)).
3. Commit. Workspaces pick it up on their next sync.

## A new base rule found inside a workspace

You notice, while working in workspace A, a rule that every workspace should follow:

1. In workspace A, tell the agent to **promote it to the base** (or answer "yes" when `sync-workspace-skills` offers it — [sync-protocol](core/sync-protocol.md) step 9).
2. The agent writes the rule into the generator in general terms (no workspace paths), bumps **minor**, and adds a CHANGELOG entry with **Affects** and **Migration**.
3. In workspace A the rule moves out of its custom block into the generated section (the registry records the new version).
4. In workspaces B, C… run `/sync-workspace-skills` (or `all`): the agent reads the new entry and applies the rule with each workspace's own paths and names, after you confirm each one.

## Add a generator

Copy the structure of `generators/create-clean-architecture-skill/` (SKILL.md that follows `core/workflow.md`, topic references, stacks, templates, checklist, `VERSION` 1.0.0, `CHANGELOG.md`), then link it into `~/.claude/skills/`. See [ROADMAP.md](ROADMAP.md).

## Not shipped with the extension

This folder is for Claude Code on the maintainer's machine; it is excluded from the `.vsix` (`.vscodeignore`). The registry is never inside this repository.
