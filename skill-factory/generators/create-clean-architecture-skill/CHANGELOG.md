# Changelog — create-clean-architecture-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace. Sync agents apply entries newer than the version recorded for a workspace (see `~/.claude/skill-factory/core/sync-protocol.md`).

## 1.1.0 — 2026-10-22

- Templates are **suggested shapes**; only the four slices 01–04 (per branch) and `SKILL.md` are **Mandatory**. Output table gains Kind + Why columns.
- Every template starts with a `<!-- GEN: Why … -->` note; rules are written with their reason, hard "never/always" only for absolute rules (`core/authoring-guide.md`).
- New Step 7 **Trial run**: 2–3 real workspace tasks planned with vs without the skill by read-only subagents; improve until the skill helps (`core/trial-run.md`).
- New Step 8 **Description**: workspace name, concrete situations, team trigger words; checked against the trial prompts.
- Step 9 now records provenance and reports deviations from the suggested shape.
- Generator description rewritten to trigger on more phrasings (incl. Vietnamese).

**Affects:** `SKILL.md` (description, explanations), every reference file (rules gain a short "why"); file layout may differ per workspace.
**Migration:** in a synced workspace, (1) add a one-clause reason to rules that have none, keeping their meaning; (2) rewrite the `SKILL.md` description per the authoring guide; (3) offer the user a trial run. Do not restructure files that already work. Non-breaking.

## 1.0.0 — 2026-10-21

First version inside the skill factory.

- Layouts: flat (single stack) and branched `shared/ + be/ + fe/` (fullstack).
- Knowledge: principles, backend rules B1–B13, frontend rules F1–F14, splitting protocol, presets for FastAPI, NestJS, Next.js, Flutter.
- Existing-project lessons P1–P5 (now in `core/existing-project.md`).
- Output path: `<workspace>/.agents/skills/clean-architecture/`.
- Scope: manual workspaces only; Step 0 stops for workspaces synced by Coder Nexus.

**Affects:** all generated files.
**Migration:** workspaces generated before the factory existed are not registered → run the generator in the workspace to **adopt** (records provenance, refreshes to this frame, keeps project rules and custom blocks).
