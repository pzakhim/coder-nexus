# Changelog — create-git-workflow-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules: M1–M9 (from the fixed `git-preflight` skill), G1–G6 (Git Flow for DEV/STG/PROD, generalised from a team policy), V1–V7 (SemVer 2.0.0 for applications), R1–R2 (release integrity with artifact promotion).
- Presets: `gitflow-dev-stg-prod`, `github-flow`, `trunk-based`; read-only detection of branches, tags, merge history, CI, commit and release tools.
- Agents never merge into the production branch, tag or deploy production; they prepare the commands and checklist.
- Mandatory: `SKILL.md`, branch model, preflight table, naming and commits, merge and propagation, versioning and release.
- Layout: always flat.
- Output path: `<workspace>/.agents/skills/git-workflow/`.

**Affects:** all generated files.
**Migration:** existing Git or release skills → run the generator to **adopt** (keeps branch names, prefixes, merge rules and release steps).
