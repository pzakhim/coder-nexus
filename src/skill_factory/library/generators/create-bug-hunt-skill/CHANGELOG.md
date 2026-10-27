# Changelog — create-bug-hunt-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.1.0 — 2026-10-24

- Decoupled base inputs from core `plugins/core/skills/bug-hunt`, relying directly on self-contained `references/base-rules.md` and stack-agnostic `references/deriving-the-model.md`.
- Consolidated output template structure from 5 branched files (`01`–`05`) into 3 cohesive reference files (`01-scope-dimensions-and-patterns.md`, `02-verify-and-disprove.md`, `03-severity-verdict-and-report.md`).
- Standardized on mandatory `H1`–`H14` compliance, binary `PASS`/`FAIL` read-only CLI checks, and unified `BLOCKER`/`MAJOR`/`MINOR` severities.

**Affects:** generator templates and reference guides.
**Migration:** existing workspace skills can consolidate `01`+`05` → `01-scope-dimensions-and-patterns.md`, `02` → `02-verify-and-disprove.md`, and `03`+`04` → `03-severity-verdict-and-report.md`.

## 1.0.0 — 2026-10-22

First version.
