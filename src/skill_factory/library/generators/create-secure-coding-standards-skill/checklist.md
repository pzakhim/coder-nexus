# Checklist — secure-coding-standards

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] `SKILL.md` (< 150 lines) has Section 1 Deterministic Security Gates (`PASS` / `FAIL`), Section 2 Core Security Rules (`SC1`–`SC14` — Mandatory Compliance), and Section 3 Reference Guides (`01`..`03` + `<!-- {{profile_references}} -->` when profiles apply)
- [ ] `references/` is consolidated into 3 cohesive files (`01-input-auth-and-data-scope.md`, `02-secrets-data-and-crypto.md`, `03-runtime-risks-deps-and-review.md`) with zero micro-file fragmentation
- [ ] All 14 rules (`SC1`–`SC14`) are mapped to the workspace's real guards, helpers, and error contracts (`SC1`, `SC2`, `SC3`, `SC4`, `SC6`, `SC13` are never omitted)
- [ ] Trust boundaries, authentication/session lifecycle, object-level authorization, and data scopes are documented with concrete unsafe-vs-safe examples
- [ ] Review grading uses strictly `BLOCKER` / `MAJOR` / `MINOR` (zero `P1` / `P2` / `P3` remnants) and CLI gates use `PASS` / `FAIL`
- [ ] No real secrets, tokens, or personal data appear in any example
