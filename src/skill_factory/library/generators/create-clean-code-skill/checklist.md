# Checklist — clean-code

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule C1–C17 is adopted, adapted to a workspace contract, cited as enforced by a CLI gate, or "not adopted" with a stated reason; C1, C3, C4, C10, C11, C14, C15, C16, C17 are adopted
- [ ] C15–C17 use the workspace's real private visibility convention and entry-file names; existing `utils`/`helpers` buckets and wildcard exports are listed as drift, not rewritten outside a task
- [ ] Naming table built from real names sampled in the workspace; drift listed
- [ ] Size thresholds match existing configured numbers or the confirmed defaults; `clean-architecture`'s long-file reference (if it exists) links to `01-structure-naming-and-types.md` instead of repeating them
- [ ] Error contract, lifecycle/disposal rules, and logger are the workspace's real ones
- [ ] Self-check CLI commands (`PASS`/`FAIL`) exist in the workspace (no uninstalled tools); `rg` checks are scoped to changed files
- [ ] Reviewer findings use the unified `BLOCKER` / `MAJOR` / `MINOR` scale (`shared_contracts/flags_and_statuses.md` §2)
- [ ] Existing rule IDs (e.g. C1–C10) and gates kept (P5)
- [ ] `01-structure-naming-and-types.md`, `02-errors-lifecycle-and-logging.md`, and `03-self-check-and-review.md` present in `references/`; `01` links `clean-architecture` placement (or the fallback) and is the single source of size thresholds
