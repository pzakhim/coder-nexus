# Changelog — create-requirements-specification-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## Unreleased

- Changed: renamed every reference to the fixed `grill-me` skill to `grilling` (D2, no alias) in `SKILL.md`, `references/02-question-bank.md` and the `CLAUDE.md` pointer. (minor — the old name no longer exists)
- Added: RS10 delta for change jobs — each affected BR/AC classified ADDED / MODIFIED / REMOVED against the built code with a reason, a migration note for REMOVED, written in `change-impact.md` "Behavior delta" (BR) and "AC delta" (Add / Change / Remove / Keep) → `references/04-writing-rules-and-ac.md` "Change jobs: delta". RS10 is never "not adopted". (minor)
- Changed: RS4 extended with a team vague-word list (each word with what replaces it; an unresolved word becomes a `Q-NN`) and measurable `G-NN` success signals → 04 "Words we never write", "Goals and success signals". (minor)
- Changed: RS5 tightened — glossary terms verbatim in goals, BR, AC and scenarios; a synonym is a defect reported by `gate-review` → 04 "Terms", `SKILL.md` "Always". (minor)
- Changed: RS6 is now the workspace part of `gate-review` spec mode — questions about the spec text per job type, tagged `[Gap]` / `[Ambiguity]` / `[Conflict]`, run after the validators and the fixed checklist, findings become `Q-NN` — instead of a separate ready checklist. Output file renamed `references/05-ready-checklist.md` → `references/05-gate-review-questions.md`. (major)
- Changed: job types follow the work-item Types (D1); "change" and "verification" mapped onto them → `references/base-rules.md` "Job types". (patch)
- Added: detection of past review findings and past deltas; `references/sources.md` with the external sources and ideas not adopted. (patch)

**Affects (when released):** `SKILL.md`, `references/01-sources-intake.md` (GEN note only), `references/02-question-bank.md`, `references/04-writing-rules-and-ac.md`, `references/05-ready-checklist.md` → `references/05-gate-review-questions.md`, the `CLAUDE.md` / `AGENTS.md` pointer.
**Migration (when released):**
1. Replace `grill-me` with `grilling` in the workspace skill and in the `## Requirements` pointer of `CLAUDE.md` / `AGENTS.md`.
2. Rename `references/05-ready-checklist.md` to `references/05-gate-review-questions.md`; rewrite each checkbox as a question about the spec text with a `[Gap]` / `[Ambiguity]` / `[Conflict]` tag; drop items the validators or the fixed `gate-review` spec checklist already cover; update the link in `SKILL.md` and inbound links (P3).
3. In `references/04-writing-rules-and-ac.md` add "Terms", "Goals and success signals", "Words we never write" (look up vague words in past specs and review comments first) and "Change jobs: delta"; confirm the vague-word list with the user.
4. Add the ADDED / MODIFIED / REMOVED bullet and the verbatim-terms bullet to `SKILL.md` "Always".

## 1.0.0 — 2026-10-22

First version.

- Base rules RS1–RS9 with reasons: source map, question bank per grill-me dimension, mandatory edge cases, observable AC, domain terms only, ready checklist per job type, bug specs, language, fixed process unchanged.
- Generic edge-case catalog (keep only what the workspace has); detection of past specs, ticket and AC style.
- Mandatory: `SKILL.md`, sources and intake, question bank, mandatory edge cases, writing BR/AC/bugs, ready checklist.
- Layout: flat.
- Output path: `<workspace>/.agents/skills/requirements-specification/`.

**Affects:** all generated files.
**Migration:** existing spec guides → run the generator to **adopt** (keeps AC style, IDs and checklists).
