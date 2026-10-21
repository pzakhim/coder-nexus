# Provenance (private registry)

Every workspace skill produced by a factory generator is recorded in a **private registry on this machine**, never inside the workspace and never in this repository.

## Location

```
~/.claude/skill-factory-registry/<workspace-slug>.json
```

- `<workspace-slug>`: the workspace folder name, lowercased (`erp-knowledge-platform`). Add a short suffix if two workspaces share a name.
- `~/.claude/skill-factory` is a symlink into the Coder Nexus repo (public). The registry is a **separate** folder so workspace paths and decisions never get committed or published.
- Workspaces carry no provenance file. Their skills contain only content plus `<!-- custom:start --> … <!-- custom:end -->` blocks.

## Entry format

```json
{
  "workspace": "/Users/<you>/Space/CodeSpace/erp-knowledge-platform",
  "skills": {
    "clean-architecture": {
      "generator": "create-clean-architecture-skill",
      "version": "1.0.0",
      "factory_commit": "<git rev of the coder repo when generated/synced>",
      "updated_at": "2026-10-21",
      "path": ".agents/skills/clean-architecture",
      "layout": "branched",
      "stacks": { "be": "python-fastapi", "fe": "ts-nextjs" },
      "levels": { "be": "full", "fe": "standard" },
      "decisions": ["A3: split repositories per aggregate", "A4: non-whitelisted FE folders are debt"],
      "files": {
        "SKILL.md": "generator",
        "references/be/01-folder-structure.md": "generator",
        "references/shared/no-wrapper-rule.md": "project",
        "scripts/check-fe-boundaries.sh": "project"
      }
    }
  }
}
```

| Field | Meaning |
|---|---|
| `version` | Generator `VERSION` the workspace skill currently matches |
| `factory_commit` | `git -C <coder repo> rev-parse HEAD` at generation/sync time; lets the agent read the old base with `git show <commit>:skill-factory/...` |
| `files` | `generator` = refreshed on sync (outside custom blocks); `project` = never touched by sync |
| `decisions` | Confirmed choices the sync must respect |

## Who writes it

- A generator, at the end of a generate / adopt / update run.
- `sync-workspace-skills`, after a workspace was synced and the user confirmed.

The agent edits the JSON by hand (Read/Write); no script is involved. Create the folder if it does not exist.
