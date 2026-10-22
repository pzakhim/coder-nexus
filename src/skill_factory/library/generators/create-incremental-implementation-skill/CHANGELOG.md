# Changelog — create-incremental-implementation-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`).

## 1.0.0 — 2026-10-22

First version.

- Base rules I1–I14 extracted from Coder Nexus `plugins/core/skills/incremental-implementation` (generic parts only).
- Plan-format detection (work-items dossier, versioned feature docs, issue/PR checklists, plain plan file).
- Verification commands per stack; layer order of work per branch.
- Layouts: flat `references/01–07`; branched `references/shared/01–05`, `be/06–07`, `fe/06–07`.
- Output path: `<workspace>/.agents/skills/incremental-implementation/`.
- Step 0: never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name. Distributed with `skill-factory get`.
- Output table gains Kind + Why columns. **Mandatory:** `SKILL.md`, task loop (02), phase completion (03), verification (06), and rules I1, I4, I5, I10, I11, I14. Other files are suggested shapes and may merge (e.g. 04 + 05 into 03 for a light plan format).
- Base rules I1–I14 gain a Why column; generated rules carry their reason (`core/authoring-guide.md`).
- Every template starts with a `<!-- GEN: Why … -->` note.
- New Step 7 **Trial run** with topic tasks (implement a real task, mapped component that does not fit, a check that cannot run) — `core/trial-run.md`.
- New Step 8 **Description**; Step 9 records provenance and reports deviations.
- Generator description rewritten to trigger on more phrasings (incl. Vietnamese).
- Added: phase completion (03) links root-cause-debugging for failing checks; root-cause-debugging added to the sibling skills in Step 4.
- Changed: sibling skill name `unit-test` → `unit-testing` in the Step 4 gate list; generated sibling links should point to `.agents/skills/unit-testing/`.

**Affects:** all generated files.
**Migration:** existing, unregistered `incremental-implementation` skills in a workspace → run the generator there to **adopt** (keeps workspace rules and custom blocks, records provenance).
