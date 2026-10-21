# Sync protocol (agent-driven)

How an agent brings a workspace skill up to date with its generator. **No script does this.** The agent reads the generator, the registry and the workspace, then edits the workspace's `.agents/skills/` files itself, with the user's confirmation.

## Inputs

- The private registry entry: `~/.claude/skill-factory-registry/<workspace-slug>.json` ([provenance.md](provenance.md)).
- The generator: `VERSION`, `CHANGELOG.md`, templates and references (current).
- The old base, when needed: `git -C <coder repo> show <factory_commit>:skill-factory/generators/<generator>/<file>`.
- The workspace skill (working copy) at the recorded `path`.

## Steps

1. **Status.** Compare the recorded `version` with the generator `VERSION`. Equal → report "up to date" and stop.
2. **Read changes.** Read every `CHANGELOG.md` entry newer than the recorded version, oldest first. Collect their **Affects** and **Migration** lines.
3. **Check the workspace.** `git status` in the workspace; note uncommitted changes in the affected files (P3). Read each affected file.
4. **Classify each affected spot:**

   | Situation | Action |
   |---|---|
   | File owned by `project` | Do not touch; only mention it if the migration concerns it |
   | Inside `<!-- custom:start --> … <!-- custom:end -->` | Do not touch |
   | Generated section equal (in meaning) to the old base | Apply the migration |
   | Generated section edited by hand since the old base | **Conflict** → show old base / workspace / new base and ask: keep workspace, take new, or merge |

5. **Prepare edits.** Apply the migrations with the workspace's real paths and names (same rules as generation: English, no `{{…}}`, no `<!-- GEN -->`, real examples). Renames follow P3: list inbound links and ask before changing them.
6. **Show the user** a summary per file (added / changed / conflicts) and the planned link updates. Wait for confirmation.
7. **Write** the confirmed edits. Do not commit in the workspace unless the user asks.
8. **Record.** Update the registry entry: `version`, `factory_commit`, `updated_at`, `files` (new files owned by `generator`, anything the user chose to keep as `project`).
9. **Contribute back (optional).** If a custom block or project file looks general (useful to other workspaces), ask whether to promote it into the generator. If yes: edit the generator, bump **minor**, add a CHANGELOG entry. Do not apply it to other workspaces in the same run unless asked.

## Many workspaces

`sync-workspace-skills` runs these steps for each registered workspace that is behind, **one workspace at a time, one confirmation each**. It starts with a status table:

| Workspace | Skill | Recorded | Latest | Status |
|---|---|---|---|---|

Status values: `up to date`, `behind N`, `behind N (conflicts)`, `missing` (path no longer exists → ask whether to drop the entry).

## Never

- Overwrite custom blocks or project-owned files.
- Edit a workspace that the user did not confirm.
- Store provenance inside a workspace or inside this repository.
- Skip versions: migrations are applied in order.
