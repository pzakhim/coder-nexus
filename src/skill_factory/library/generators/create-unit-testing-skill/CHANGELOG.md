# Changelog — create-unit-testing-skill

## 1.1.0 — 2026-10-24

- **Affects:** `SKILL.md`, `references/base-rules.md`, `references/deriving-the-model.md`, `templates/`, `checklist.md`.
- **Changed:**
  - Standardized all rules `U1`–`U14` as Mandatory Compliance (removed `P1`/`P2`/`P3` per-rule severity column).
  - Enforced binary CLI test gates (`PASS` / `FAIL`) and unified Reviewer grading (`BLOCKER` / `MAJOR` / `MINOR`).
  - Consolidated 6 fragmented templates (`branch/01..05` + `shared/06`) into 3 cohesive reference templates (`01-test-matrix-and-structure.md.tmpl`, `02-doubles-fixtures-and-quality.md.tmpl`, `03-execution-boundaries-and-review.md.tmpl`).
  - Made the generator 100% stack-agnostic and added `profiles/<profile>/testing-contracts.md` support.
- **Migration:** Regenerate or sync workspace/pack `unit-testing` skills into the 3-file `references/` layout and move profile-specific rules into `profiles/<profile>/testing-contracts.md`.

## 1.0.0 — 2026-04-06

- Initial generator release.
