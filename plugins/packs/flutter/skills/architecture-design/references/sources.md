# Sources

Ideas were rewritten in this repo's vocabulary (`G-NN`, `AC-NN`, `D-NN`, `PHASE-NN`, gates). Links are pinned to a commit.

| Source | Stars | Idea taken | Where used |
|---|---|---|---|
| [bmad-code-org/BMAD-METHOD `skills/bmad-architecture/SKILL.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-architecture/SKILL.md) | 54k | Record a decision only when independently built parts could choose incompatibly, it is non-obvious and a real trade-off; brownfield ratifies existing conventions; lint first, then a rubric review before handoff | `SKILL.md` §2, §4, [10](10_optional_design_subsections.md) §1 |
| [bmad-code-org/BMAD-METHOD `skills/bmad-architecture/assets/spine-template.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-architecture/assets/spine-template.md) | 54k | A Deferred list where each item carries the reason it can wait; optional sections cut when not needed | [design.md.tpl](../templates/design.md.tpl) `### Deferred decisions`, [10](10_optional_design_subsections.md) §2 |
| [github/spec-kit `templates/plan-template.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/plan-template.md) | 142k | Complexity tracking: violation, why needed, simpler alternative rejected because | [design.md.tpl](../templates/design.md.tpl) `### Complexity justifications`, [10](10_optional_design_subsections.md) §3 |
| [Fission-AI/OpenSpec `schemas/spec-driven/templates/design.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/schemas/spec-driven/templates/design.md) | 73k | Risks and trade-offs next to the decisions; migration plan with rollback | [design.md.tpl](../templates/design.md.tpl) `### Risk → Mitigation`, `### Migration plan and rollback`, [10](10_optional_design_subsections.md) §4–5 |
| [addyosmani/agent-skills `skills/documentation-and-adrs/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/documentation-and-adrs/SKILL.md) | 109k | A decision records the alternatives rejected and why; decisions expensive to reverse deserve the record | [10](10_optional_design_subsections.md) §3 |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Fast path that drafts with assumption tags for the user to correct | BMAD architecture | Conflicts with "confirm every inference" and the ban on Assumptions sections; every choice is a `Q-NN` closed into `D-NN` |
| Open Questions section in the design | OpenSpec design template | `design.md` must have 0 open questions (`DESIGN-005`); questions live in `codebase-notes.md` |
| Separate memlog, spine document and `AD-n` IDs | BMAD architecture | `codebase-notes.md` and `D-NN` already hold the decision log; one home per fact |
| Verify library versions on the web before binding | BMAD architecture | The approved foundation profile and `pubspec.yaml` decide versions in this pack |
| Separate ADR files | agent-skills ADRs | Optional `decision-records` skill owns ADR promotion; this skill keeps `D-NN` |
| New Goals / Non-Goals section in `design.md` | OpenSpec design template | Goals live in `requirements.md`; `## Goal alignment` already maps them |
