# Changelog — create-domain-knowledge-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see [../../core/sync-protocol.md](../../core/sync-protocol.md)). Bump rules: [../../core/versioning.md](../../core/versioning.md).

## 1.1.0 — 2026-10-25

- Consolidated generated `references/` from 5 fragmented files into 3 cohesive topic files: `01-glossary-and-ubiquitous-language.md` (`DK1`, `DK9`), `02-entities-lifecycles-and-rules.md` (`DK2`, `DK4`), and `03-roles-scopes-and-upkeep.md` (`DK3`, `DK5`–`DK8`).
- Standardized all rules `DK1`–`DK9` as mandatory compliance (workspaces without RBAC roles or data scopes document a one-line `N/A for this workspace` entry).
- Added deterministic CLI tool gates (`PASS` / `FAIL`) for banned synonym (`"Avoid saying"`), unresolved `OPEN` fact, and secret/PII checks alongside the unified `BLOCKER` / `MAJOR` / `MINOR` review rubric (`shared_contracts/flags_and_statuses.md`).
- Added `<!-- {{profile_references}} -->` marker support for `profiles/{imespro,external-structured,external-standard}/` and removed `references/sources.md`.
- Made `references/detection.md` 100% stack-agnostic (`<src>`).

**Affects:** `SKILL.md`, `references/01-glossary-and-ubiquitous-language.md`, `references/02-entities-lifecycles-and-rules.md`, `references/03-roles-scopes-and-upkeep.md`.
**Migration:**
1. Merge `01-glossary.md` into `references/01-glossary-and-ubiquitous-language.md` (`DK1`, `DK9`), `02-entities-and-lifecycles.md` + `04-business-rules.md` into `references/02-entities-lifecycles-and-rules.md` (`DK2`, `DK4`), and `03-roles-and-scopes.md` + `05-sources-and-upkeep.md` into `references/03-roles-scopes-and-upkeep.md` (`DK3`, `DK5`–`DK8`).
2. Update `SKILL.md` with the deterministic `PASS` / `FAIL` CLI gate table, mandatory `DK1`–`DK9` principle index, `BLOCKER` / `MAJOR` / `MINOR` review note, and `<!-- {{profile_references}} -->` marker.

## 1.0.0 — 2026-10-22

First version.

- Base rules DK1–DK8 with reasons: one term one meaning, entity cards with lifecycles, roles × scopes × actions, business-rule catalog with locations, labelled facts, linked volatile facts, upkeep, no personal data.
- Domain-neutral detection of entities, statuses, transitions, roles, data scopes, user-facing labels and documents; tracker history optional.
- Mandatory: `SKILL.md`, glossary, entities and lifecycles, roles and scopes, business rules, sources and upkeep.
- Layout: flat; large domains split per module.
- Output path: `<workspace>/.agents/skills/domain-knowledge/`.

**Affects:** all generated files.
**Migration:** existing glossary or domain docs → run the generator to **adopt** (keeps terms, IDs and confirmed rules).
