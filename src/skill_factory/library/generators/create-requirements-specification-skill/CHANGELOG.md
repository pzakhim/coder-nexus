# Changelog — create-requirements-specification-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see [../../core/sync-protocol.md](../../core/sync-protocol.md)). Bump rules: [../../core/versioning.md](../../core/versioning.md).

## 1.1.0 — 2026-10-25

- Consolidated generated `references/` from 5 fragmented files into 3 cohesive topic files under `templates/references/`: `01-sources-and-grilling-questions.md` (`RS1`, `RS2`, `RS8`, `RS9`), `02-edge-cases-and-writing-rules.md` (`RS3`–`RS5`, `RS7`, `RS10`), and `03-gate-review-and-verification.md` (`RS6`).
- Made all base rules `RS1`–`RS10` mandatory compliance in `references/base-rules.md`, `SKILL.md`, and `checklist.md`.
- Standardized Gate 1 spec review findings on the unified `BLOCKER` / `MAJOR` / `MINOR` severity scale alongside `[Gap]` / `[Ambiguity]` / `[Conflict]` tags (`shared_contracts/flags_and_statuses.md`).
- Standardized automated CLI verification gates on binary `PASS` / `FAIL` (`validate_proposal_spec` and `rg` checks for vague words, banned synonyms from `domain-knowledge`, open `Q-NN`, and AC traceability).
- Added `<!-- {{profile_references}} -->` marker support in `templates/SKILL.md.tmpl` for workspace profile injection (`profiles/{imespro,external-structured,external-standard}/`) and removed `references/sources.md`.

**Affects:** `SKILL.md`, `references/01-sources-and-grilling-questions.md`, `references/02-edge-cases-and-writing-rules.md`, `references/03-gate-review-and-verification.md`.
**Migration:**
1. Merge `01-sources-intake.md` and `02-question-bank.md` (plus language and fixed-process rules `RS8`–`RS9`) into `references/01-sources-and-grilling-questions.md`.
2. Merge `03-mandatory-edge-cases.md` and `04-writing-rules-and-ac.md` (`RS3`–`RS5`, `RS7`, `RS10`) into `references/02-edge-cases-and-writing-rules.md`.
3. Rename `05-gate-review-questions.md` to `references/03-gate-review-and-verification.md`, grade Gate 1 findings strictly with `BLOCKER` / `MAJOR` / `MINOR` alongside `[Gap]` / `[Ambiguity]` / `[Conflict]`, and add deterministic `PASS` / `FAIL` CLI checks (`rg` audits for vague words, banned synonyms, open `Q-NN`, and AC traceability).
4. Update `SKILL.md` to link the 3 cohesive reference guides, include `<!-- {{profile_references}} -->`, and enforce all `RS1`–`RS10` rules as mandatory compliance.

## 1.0.0 — 2026-10-22

First version.

- Base rules `RS1`–`RS9` with reasons: source map, question bank per grilling dimension, mandatory edge cases, observable AC, domain terms only, Gate 1 review checklist per job type, bug specs, language, fixed process unchanged.
- Generic edge-case catalog (keep only what the workspace has); detection of past specs, ticket, and AC style.
- Output path: `<workspace>/.agents/skills/requirements-specification/`.

**Affects:** all generated files.
**Migration:** existing spec guides → run the generator to adopt (keeps AC style, IDs, and checklists).
