# Checklist — domain-knowledge

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule DK1–DK8 is adopted, adapted, or "not adopted" with a reason; DK5 and DK8 are adopted
- [ ] Every fact carries `VERIFIED` (with path), `CONFIRMED` or `OPEN`; nothing inferred is labelled as fact
- [ ] Glossary terms come from the workspace (labels, entities, documents); synonyms to avoid are listed where they exist
- [ ] Entity cards list status values and transitions with trigger and enforcement location
- [ ] The roles × scopes matrix was shown to and confirmed by the user; a workspace without roles or scopes says so in one line
- [ ] Business rules have `file:symbol` locations and sources; IDs do not collide with work-item `BR-NN`
- [ ] No category is invented for a workspace that does not have it; no domain words are carried over from the generator's examples
- [ ] No personal data, secrets or volatile values copied
- [ ] Upkeep owner and trigger are stated
