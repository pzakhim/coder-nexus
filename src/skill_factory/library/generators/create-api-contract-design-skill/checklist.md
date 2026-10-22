# Checklist — api-contract-design

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule AP1–AP9 is adopted, adapted, or "not adopted" with a reason; AP1, AP6 and AP9 are adopted
- [ ] The source of truth for the contract is named and real
- [ ] Naming, response and error shapes come from real endpoints; drift is listed
- [ ] Every endpoint example states roles, scope and the denied response
- [ ] The compatibility table gives a compatible path for every breaking change and links the version rules
- [ ] Prefer adding over modifying, Hyrum's Law and the One-Version Rule are stated in 04
- [ ] The error envelope is defined once; endpoints reference it
- [ ] Retried mutations: key source, atomic claim, payload-mismatch error, in-flight answer, timeout as unknown outcome and retention are stated, or "no retried mutations" in one line
- [ ] Clients and mocks are named with real paths, or stated as absent
- [ ] No real tokens, keys or personal data in examples
- [ ] Branched layout: shared conventions in `shared/`, enforcement in `be/`, consumption in `fe/`
