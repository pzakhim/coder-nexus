# Checklist — visual-quality

Run this checklist alongside `~/.claude/skill-factory/core/checklist-common.md`:

- [ ] All 12 mandatory rules (`V1`–`V12`) from `references/base-rules.md` are enforced in `SKILL.md` and `references/01..03-*.md` (zero `"not adopted"` sections)
- [ ] `SKILL.md` is concise (< 120 lines) with valid YAML frontmatter and routes cleanly to `references/01..03-*.md`
- [ ] Reference hierarchy and approval rules use the workspace's real design paths (extracted Figma per-screen `.png` renders & `<stem>.spec.json`, `design.md`, or labeled baseline when allowed)
- [ ] Screen × State × Viewport × Orientation matrix covers all 4 mandatory visual states (`Loading`, `Content`, `Empty`, `Error`) and separates fixture-backed UI checks (`FE_MOCKOON`) from live integration (`BE_LIVE`)
- [ ] Runtime capture and headless golden workflows enforce strict role separation (baseline updates require explicit review approval; verification never runs baseline-overwrite flags)
- [ ] 10-dimension comparison checklist uses the unified `BLOCKER` / `MAJOR` / `MINOR` severity scale and `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` / `UNVERIFIED` / `N/A` gate flags (`shared_contracts/flags_and_statuses.md`)
- [ ] Base `SKILL.md` and `references/01..03-*.md` are 100% stack-generic when `profiles/<profile>/` is used
