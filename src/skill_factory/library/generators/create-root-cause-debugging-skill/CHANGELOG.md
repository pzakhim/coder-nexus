# Changelog — create-root-cause-debugging-skill

## 1.1.0 — 2026-10-24

- **Affects:** `SKILL.md`, `references/base-rules.md`, `references/deriving-the-model.md`, `templates/`, `checklist.md`.
- **Changed:**
  - Standardized all rules `D1`–`D14` as Mandatory Compliance with binary CLI gates (`PASS` / `FAIL`) and unified Reviewer grading (`BLOCKER` / `MAJOR` / `MINOR`).
  - Consolidated 6 fragmented templates (`shared/01..04, 06` + `branch/05`) into 3 cohesive chronological reference templates (`01-reproduce-read-and-tools.md.tmpl`, `02-isolate-and-hypothesize.md.tmpl`, `03-fix-escalate-and-report.md.tmpl`).
  - Made the generator 100% stack-agnostic and added `profiles/<profile>/debugging-contracts.md` support.
- **Migration:** Regenerate or sync workspace/pack `root-cause-debugging` skills into the 3-file `references/` layout and move profile-specific rules into `profiles/<profile>/debugging-contracts.md`.

## 1.0.0 — 2026-04-06

- Initial generator release.
