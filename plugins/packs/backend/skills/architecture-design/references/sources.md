# Sources

Ideas were rewritten in this repo's vocabulary (`AC-NN`, `D-NN`, `PHASE-NN`, gates). Links are pinned to a commit.

| Source | Stars | Idea taken | Where used |
|---|---|---|---|
| [bmad-code-org/BMAD-METHOD `skills/bmad-architecture/SKILL.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-architecture/SKILL.md) | 54k | Record a decision only when independently built parts could choose incompatibly and it is non-obvious; ratify existing conventions in brownfield code; lint, then rubric review before handoff | `SKILL.md` §1, §2 |
| [bmad-code-org/BMAD-METHOD `skills/bmad-architecture/assets/spine-template.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-architecture/assets/spine-template.md) | 54k | Deferred items each carry the reason they can wait | `SKILL.md` §2 Deferred decisions |
| [github/spec-kit `templates/plan-template.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/plan-template.md) | 142k | Complexity tracking: violation, why needed, simpler alternative rejected because | `SKILL.md` §2 Complexity justifications |
| [Fission-AI/OpenSpec `schemas/spec-driven/templates/design.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/schemas/spec-driven/templates/design.md) | 73k | Risks and trade-offs beside decisions; migration plan with rollback | `SKILL.md` §2 Risk → Mitigation, Migration plan and rollback |
| [addyosmani/agent-skills `skills/documentation-and-adrs/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/documentation-and-adrs/SKILL.md) | 109k | Schema and data-model choices are expensive to reverse, so the rejected alternatives are recorded | `SKILL.md` §2 Complexity justifications (on the `D-NN`) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Fast path drafting with assumption tags | BMAD architecture | Conflicts with "confirm every inference"; choices are `Q-NN` closed into `D-NN` |
| Open Questions section in the design | OpenSpec design template | `design.md` must have 0 open questions (`DESIGN-005`) |
| Separate memlog, spine and `AD-n` IDs | BMAD architecture | `codebase-notes.md` and `D-NN` already hold the decision log |
| Separate ADR files in this skill | agent-skills ADRs | The optional `decision-records` skill owns ADR promotion |
