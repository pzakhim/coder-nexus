# Sources

External ideas adapted into this skill, rewritten in Coder Nexus vocabulary (SC1–SC11, bug-hunt `BLOCKER` / `MAJOR` / `MINOR`, `CONFIRMED` / `PLAUSIBLE`, READY_FOR_REVIEW). Nothing is copied. Stars as of 2026-10.

Internal base input (read-only): `src/skill_factory/library/generators/create-secure-coding-standards-skill/references/base-rules.md` (SC1–SC14, aligned with OWASP Top 10 / ASVS) and `risks-by-stack.md`, which seeds the `{{slot:secure-coding}}` content of each pack. SC1–SC11 here merge SC4+SC5, SC7+SC12 and SC9+SC10 of the base.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [addyosmani/agent-skills `skills/code-review-and-quality/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/code-review-and-quality/SKILL.md) | 109k | Data from external sources (APIs, stored user content, config) is untrusted and validated at the boundary before logic or rendering | SC1, checklist "Input" rows |
| same | 109k | Secrets stay out of code, logs and version control; queries parameterised; output encoded | SC4, SC5 |
| same | 109k | Dependency discipline: reason for every new package, read the changelog on upgrade, one package per change, review the lockfile diff | SC10, checklist "Dependencies" |
| same | 109k | A silent fallback that papers over an unclear invariant is a defect | SC8 (no default or fake data on failure) |
| [mattpocock/skills `skills/engineering/code-review/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md) | 300k | Repository-documented standards override the generic baseline | Opening paragraph: workspace and slot supply specifics, but may not relax a rule |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| A separate `security-and-hardening` skill holding the checklist | addyosmani code-review-and-quality | One skill keeps rules and checklist together; a workspace `security-review` skill can still go deeper |
| "Critical / Required / Optional / Nit" labels | addyosmani code-review-and-quality | Findings use the shared bug-hunt scale so verdict rules stay in one place |
| Performance axis (N+1, unbounded fetches) | addyosmani code-review-and-quality | Not a security topic; unbounded fetches that enable abuse are covered by SC1 size limits |
| Dependency audit with a specific package-manager command | addyosmani code-review-and-quality | Commands are stack-specific and belong to `{{slot:secure-coding}}` / `{{slot:verification}}` |
| Base rule SC14 as a separate security sign-off role | create-secure-coding-standards-skill | Release 3.2.0 has no security agent; SC11 hands the flags to the Code Reviewer |
