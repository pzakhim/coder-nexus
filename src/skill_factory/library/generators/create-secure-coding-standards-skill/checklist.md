# Checklist — secure-coding-standards

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule SC1–SC14 is adopted, adapted, cited as enforced by a gate, or "not adopted" with a reason; SC1, SC2, SC3, SC4, SC6, SC13 are adopted
- [ ] Trust boundaries listed with real paths and their validators
- [ ] Authorization uses the workspace's real guards; the RBAC contract and scope matrix are copied verbatim when they exist
- [ ] Every data scope has carrier, enforcement point and "leak looks like"
- [ ] Safe patterns name the workspace's own helpers (validation, network guard, sanitiser, crypto) where they exist
- [ ] No real secret, token or personal data appears in any example
- [ ] Security gates cited, or "none — reviewer checks by hand"
- [ ] Review triggers match the workspace's handoff notation and roles
