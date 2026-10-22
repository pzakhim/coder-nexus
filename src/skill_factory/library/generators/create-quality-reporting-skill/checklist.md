# Checklist — quality-reporting

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule RP1–RP12 is adopted, adapted, or "not adopted" with a reason; RP1, RP3, RP4, RP7, RP8 are adopted
- [ ] Report location, naming, results record and owner are the workspace's own
- [ ] AC coverage rule and verdict criteria use the workspace's words; NOT_RUN/BLOCKED never count as passed
- [ ] Defect IDs, severity scale and status lifecycle defined; "won't fix" requires the user's decision
- [ ] Limitations section required at the top (stubs, not-run cases, uncovered roles/environments, flaky cases)
- [ ] Evidence path and redaction rules stated; external posting needs authorisation
- [ ] Fullstack reports keep separate BE and FE result tables
