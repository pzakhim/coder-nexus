# Checklist — quality-acceptance

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule A1–A14 is adopted, adapted, or "not adopted" with a reason; A1, A2, A4, A7, A9, A13 are adopted
- [ ] Browser and API tools were detected in the workspace and confirmed at the gate; no absent tool is named; fallback order recorded
- [ ] Operations map filled for the chosen frontend tool; role sessions and token handling described without values
- [ ] Frontend checks: real states, permissions per role, environment switch, reload persistence, console/network with baseline noise
- [ ] Backend checks: auth per role, status/shape, read-back persistence, side effects, direct 403 calls
- [ ] Evidence path and naming follow the workspace's rules (e.g. inside the workspace)
- [ ] Result words, defect format, flakiness and re-test scope present
- [ ] Safety: test accounts only, no production mutation, no secrets in evidence
