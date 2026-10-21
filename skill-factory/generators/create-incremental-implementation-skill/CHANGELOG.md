# Changelog — create-incremental-implementation-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`).

## 1.1.0 — 2026-10-22

- Output table gains Kind + Why columns. **Mandatory:** `SKILL.md`, task loop (02), phase completion (03), verification (06), and rules I1, I4, I5, I10, I11, I14. Other files are suggested shapes and may merge (e.g. 04 + 05 into 03 for a light plan format).
- Base rules I1–I14 gain a Why column; generated rules carry their reason (`core/authoring-guide.md`).
- Every template starts with a `<!-- GEN: Why … -->` note.
- New Step 7 **Trial run** with topic tasks (implement a real task, mapped component that does not fit, a check that cannot run) — `core/trial-run.md`.
- New Step 8 **Description**; Step 9 records provenance and reports deviations.
- Generator description rewritten to trigger on more phrasings (incl. Vietnamese).

**Affects:** `SKILL.md` (description), all rule-bearing files (reasons added); file layout may differ per workspace.
**Migration:** add a one-clause reason to each I-rule in the workspace skill, rewrite its description per the authoring guide, offer a trial run. Do not restructure files that already work. Non-breaking.

## 1.0.0 — 2026-10-21

First version.

- Base rules I1–I14 extracted from Coder Nexus `plugins/core/skills/incremental-implementation` (generic parts only).
- Plan-format detection (work-items dossier, versioned feature docs, issue/PR checklists, plain plan file).
- Verification commands per stack; layer order of work per branch.
- Layouts: flat `references/01–07`; branched `references/shared/01–05`, `be/06–07`, `fe/06–07`.
- Output path: `<workspace>/.agents/skills/incremental-implementation/`.
- Scope: manual workspaces only; Step 0 stops for workspaces synced by Coder Nexus.

**Affects:** all generated files.
**Migration:** existing, unregistered `incremental-implementation` skills in a workspace → run the generator there to **adopt** (keeps workspace rules and custom blocks, records provenance).
