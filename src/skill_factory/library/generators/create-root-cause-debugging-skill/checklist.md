# Checklist — root-cause-debugging

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule D1–D14 is adopted, adapted, or "not adopted" with a reason; D1, D7, D8, D9, D12 are adopted
- [ ] Reproduce / rerun-failed / verbose / analyzer / bisect commands are real per branch
- [ ] The workspace's tracing tool and its mandatory rules (e.g. impact before edit) are included, or `rg` as fallback
- [ ] Environment checks name real signs (service down, env var, cache) and the BLOCKED rule; "never touch a stack you did not start" kept
- [ ] Time-box number and escalation role confirmed; back-to-gate rule present
- [ ] Never-list present in `SKILL.md`
- [ ] incremental-implementation (if present) links here from its "when a check fails" step
