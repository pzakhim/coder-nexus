# Changelog — create-visual-quality-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules V1–V12 with reasons (from the erp-knowledge-platform visual-fidelity check and the Coder Nexus approved-design comparison, generalised): approved reference or labelled baseline, like-for-like matrix, capture with the workspace's browser tool into the evidence path, dimension checklist, blocking vs minor deviations, decisions allow deviations, optional diff tools, baseline updates need approval, no judging by taste, per-screen report, missing reference/state handling, no secrets in screenshots, read-only.
- Comparison checklist with blocking examples.
- Mandatory: `SKILL.md`, references & matrix, capture, compare checklist, deviations & verdict.
- Layout: always flat, frontend only.
- Output path: `<workspace>/.agents/skills/visual-quality/`.

**Affects:** all generated files.
**Migration:** existing visual checks → run the generator to **adopt** (keeps checklist items, evidence paths and references).
