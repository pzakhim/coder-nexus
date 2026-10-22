# Changelog — create-quality-reporting-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules RP1–RP12 with reasons: revision-bound report with environment record, per-case results with evidence, AC coverage derived from cases, feature verdict criteria, defect list and lifecycle, limitations, honest counting, evidence hygiene, destination and authorisation, re-test history, verdict-first summary, no edited expectations.
- Full report template.
- Mandatory: `SKILL.md`, report structure, coverage & verdict, defects, evidence & distribution.
- Layout: always flat (FE and BE results in separate tables for fullstack).
- Output path: `<workspace>/.agents/skills/quality-reporting/`.

**Affects:** all generated files.
**Migration:** existing reporting conventions → run the generator to **adopt** (keeps locations, words and IDs).
