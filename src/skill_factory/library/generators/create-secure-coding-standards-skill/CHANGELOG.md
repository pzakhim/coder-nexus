# Changelog — create-secure-coding-standards-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.2.0 — 2026-10-24

- Standardized generator to 100% stack-agnostic structure: consolidated `references/` into `base-rules.md` and `deriving-the-model.md` (removed stack-specific `risks-by-stack.md`).
- Consolidated generated skill references from 6 fragmented files (`shared/01..06`, `branch/04`) into 3 cohesive reference templates (`01-input-auth-and-data-scope.md.tmpl`, `02-secrets-data-and-crypto.md.tmpl`, `03-runtime-risks-deps-and-review.md.tmpl`) plus `SKILL.md.tmpl` with `<!-- {{profile_references}} -->`.
- Enforced unified `PASS` / `FAIL` deterministic gates and `BLOCKER` / `MAJOR` / `MINOR` review severities (removed all `P1` / `P2` / `P3` severities).

**Affects:** `SKILL.md`, `references/`, `templates/`.
**Migration:** re-sync generated skills to consolidate `references/01..06` into `references/01..03` and adopt unified flags.

## 1.1.0 — 2026-10-23

- Unified slot generator versioning for Coder Nexus v3.2.0 core-pack decoupling.

**Affects:** generator metadata.
**Migration:** none required for existing workspace skills.

## 1.0.0 — 2026-10-22

First version.

- Base rules SC1–SC14 with reasons (input validation at trust boundaries, object-level authorization, data-scope isolation, injection, output encoding, secrets, authentication/sessions, sensitive data in logs and errors, outbound calls/SSRF, file handling, dependencies, cryptography, fail closed, review triggers).
- Safe vs unsafe patterns per stack; method to derive the workspace's security model.
- Mandatory: `SKILL.md`, trust boundaries & input, authorization & data scope, secrets & sensitive data, stack risks. Suggested: dependencies, review triggers.
- Layouts: flat `references/01–06`; branched `shared/01–03, 05, 06`, `be/04`, `fe/04`.
- Shared by the Engineering and Application Security packs.
- Output path: `<workspace>/.agents/skills/secure-coding-standards/`.

**Affects:** all generated files.
**Migration:** existing security guidance → run the generator to **adopt** (keeps RBAC contract and scope matrix verbatim).
