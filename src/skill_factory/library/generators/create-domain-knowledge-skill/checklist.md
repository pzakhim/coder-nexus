# Checklist — domain-knowledge

Run this alongside [../../core/checklist-common.md](../../core/checklist-common.md).

- [ ] All rules `DK1`–`DK9` are enforced as mandatory compliance (workspaces without RBAC roles or data scopes document a one-line `N/A for this workspace` entry in `03-roles-scopes-and-upkeep.md`)
- [ ] Every fact carries `VERIFIED` (with `file:symbol` or path), `CONFIRMED`, or `OPEN`; zero inferred facts are written as verified or confirmed (`DK5`)
- [ ] Glossary terms come from the workspace (labels, entities, documents); banned synonyms (`"Avoid saying"`) are listed and checked by `gate-review` spec mode and CLI `rg` gates (`DK1`)
- [ ] Challenging overloaded/fuzzy words (`DK9`) uses a real overloaded word from the workspace, maps questions to `Q-NN` and decisions to `D-NN`, and states where to verify behavior claims against code
- [ ] Entity cards (`DK2`) and the business-rule catalog (`DK4`) in `02-entities-lifecycles-and-rules.md` list status values, allowed/forbidden transitions, triggers, and `file:symbol` enforcement locations
- [ ] The `Role × Scope × Action` matrix (`DK3`) in `03-roles-scopes-and-upkeep.md` was shown to and confirmed by the user (or states `N/A for this workspace` in one line)
- [ ] Volatile facts are linked rather than copied (`DK6`), same-work-item upkeep owner/trigger is stated (`DK7`), and zero personal data (PII) or secrets appear anywhere (`DK8`)
- [ ] Deterministic CLI checks use strictly `PASS` / `FAIL` and review criteria use strictly `BLOCKER` / `MAJOR` / `MINOR`
