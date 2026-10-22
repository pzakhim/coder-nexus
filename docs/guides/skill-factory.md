# Skill Factory

Coder Nexus ships two kinds of skills. A workspace can use both.

| Kind | What it is | How you get it | Lives in | Owned by |
|---|---|---|---|---|
| **Fixed packs** | Ready-made roles and skills per stack | Extension: `Coder Nexus: Sync …` (or `coder-nexus install-plugin`) | `.agents/plugins/coder-nexus/`, `.agents/agents/` | Coder Nexus — regenerated on every sync |
| **Skill Factory** | Generators (`create-*-skill`) that write a skill tailored to *your* workspace | `skill-factory get …`, then run the generator | `.agents/skills/` | Your workspace — edit or delete freely |

When both provide the same skill (same name, or the same topic as a stack skill), the Code Writer and Code Reviewer roles follow the **workspace skill**.

## Install

The `skill-factory` command comes with the Coder Nexus CLI (same Python package). From a source checkout:

```bash
uv run skill-factory list
```

## Commands

```bash
skill-factory list                        # every generator: name · version · package · what it covers
skill-factory list -p coder               # only the coder package
skill-factory list --json
```

```bash
skill-factory get clean-code              # one generator (default mode is -s / --skills)
skill-factory get -s clean-code unit-testing
skill-factory get -p coder                # a whole package
skill-factory get .                       # everything
```

`get` options: `--workspace PATH` (default: current directory), `--force` (replace copies that already exist, and refresh the copied core), `--no-claude-link`.

Names can be full (`create-clean-code-skill`) or short (`clean-code`). `.` cannot be combined with names or `-p`, and names cannot be combined with `-p`. Exit codes: `0` done, `1` something was skipped (already exists), `2` bad arguments or unknown name (with suggestions).

## What `get` writes

```
<workspace>/
  .agents/
    skills/create-clean-code-skill/     # the generator — yours to edit
    skill-factory-core/                 # shared core, copied once (refresh with --force)
  .claude/skills/create-clean-code-skill → ../../.agents/skills/create-clean-code-skill
```

Inside the copy, references to `~/.claude/skill-factory/core/` point to `.agents/skill-factory-core/`, so the workspace needs nothing else. The `.claude/skills/` link lets Claude Code run `/create-clean-code-skill`.

Then run the generator in the workspace. It asks you to confirm the key decisions and writes the real skill, e.g. `.agents/skills/clean-code/`.

## Packages

Defined in [`src/skill_factory/library/packages.json`](../../src/skill_factory/library/packages.json).

| Package | Generators |
|---|---|
| `coder` | create-clean-architecture-skill · create-incremental-implementation-skill · create-clean-code-skill · create-unit-testing-skill · create-code-simplification-skill · create-bug-hunt-skill · create-root-cause-debugging-skill · create-secure-coding-standards-skill · create-database-migrations-skill |
| `reviewer` | create-code-review-skill · create-bug-hunt-skill · create-clean-architecture-skill · create-clean-code-skill · create-unit-testing-skill · create-secure-coding-standards-skill · create-database-migrations-skill · create-security-review-skill |
| `security` | create-secure-coding-standards-skill · create-security-review-skill |
| `quality` | create-quality-planning-skill · create-quality-environment-skill (acceptance, reporting, visual planned) |

Planned packages and generators: [skill-factory-roadmap.md](skill-factory-roadmap.md).

## Source layout

```
src/skill_factory/
  cli.py · catalog.py · installer.py     # skill-factory list / get (no dependency on coder_nexus)
  library/                               # shipped inside the wheel
    packages.json
    core/                                # workflow (Step 0 + 9 steps), authoring guide, trial run,
                                         # stack detection, P1–P5, layouts, versioning, sync protocol…
    generators/create-*-skill/           # SKILL.md, VERSION, CHANGELOG.md, references/, templates/, checklist.md
    sync-workspace-skills/               # agent-driven update (to be replaced by `skill-factory diff`)
```

## Change a generator

1. Edit it under `src/skill_factory/library/generators/`.
2. Add a bullet under `## Unreleased` in its `CHANGELOG.md`, tagged patch / minor / major ([versioning](../../src/skill_factory/library/core/versioning.md)).
3. When the batch is done, bump `VERSION` once and turn `Unreleased` into the dated entry with **Affects** and **Migration**.

Workspaces that already copied a generator keep their copy; they compare it with the new base and take what they want.

## A new base rule found inside a workspace

1. In that workspace, ask the agent to **promote the rule to the base**.
2. The agent writes it into the generator in general terms (no workspace paths) and adds an `Unreleased` minor bullet.
3. Other workspaces pick it up when they compare their copy with the new base.

## Maintainer shortcut

For working on generators directly from the checkout, Claude Code can load them machine-wide:

```bash
ln -s "$PWD/src/skill_factory/library" ~/.claude/skill-factory
```
