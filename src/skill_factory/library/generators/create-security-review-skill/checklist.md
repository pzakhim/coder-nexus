# Checklist — security-review

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule SR1–SR14 is adopted, adapted, or "not adopted" with a reason; SR1, SR3, SR4, SR11, SR12, SR13 are adopted
- [ ] Mode (separate Security role or reviewer-run) and triggers confirmed; deep areas named
- [ ] Roles, environments and scopes copied from the workspace's RBAC contract / secure-coding-standards
- [ ] Checks per branch link the safe patterns instead of repeating them; tools listed only if installed
- [ ] Severity and sign-off mapped to the workspace's levels and verdict words
- [ ] Safe-testing boundary and disclosure channel stated; no real secret or personal data in any example
- [ ] bug-hunt dimension 5 hand-over noted when a Security role exists
