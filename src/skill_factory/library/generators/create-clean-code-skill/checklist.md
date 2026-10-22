# Checklist — clean-code

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule C1–C14 is adopted, adapted to a workspace contract, cited as enforced by a gate, or "not adopted" with a reason; C1, C3, C4, C10, C11, C14 are adopted
- [ ] Naming tables per branch built from real names in the workspace; drift listed
- [ ] Thresholds match existing numbers or the confirmed defaults; clean-architecture's long-file reference (if it exists) links here instead of repeating them
- [ ] Error contract and logger are the workspace's real ones
- [ ] Self-check commands exist in the workspace (no uninstalled tools); greps scoped to changed files
- [ ] Severities and review outcome words match the workspace's review process
- [ ] Existing rule IDs (e.g. C1–C10) and gates kept (P5)
- [ ] 02b present per branch; it links clean-architecture placement (or the fallback) and 02 is the only place with thresholds
