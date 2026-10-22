# Changelog — create-security-review-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules SR1–SR14 with reasons: triggered scope on a fixed revision, per-change threat model, authorization matrix, data-scope isolation, injection and deserialization, client-side risks, secrets and personal data, outbound calls and files, dependencies, crypto and auth flows, exploit-scenario findings, security sign-off, safe-testing boundaries, hand-over from bug-hunt and contribute-back to secure-coding-standards.
- Threat-model prompts (STRIDE-lite) and checks with read-only tools per stack.
- Two modes: separate Security role, or the Code Reviewer runs it for triggered changes.
- Mandatory: `SKILL.md`, scope & triggers, threat model, authorization & scope, checks, findings & verdict. Suggested: report.
- Layouts: flat `references/01–06`; branched `shared/01, 02, 03, 05, 06`, `be/04`, `fe/04`.
- First review generator of the Application Security Pack (`core/security-skill-family.md`).
- Output path: `<workspace>/.agents/skills/security-review/`.

**Affects:** all generated files.
**Migration:** existing security review guidance → run the generator to **adopt** (keeps RBAC matrix, triggers, severity scale and disclosure channel).
