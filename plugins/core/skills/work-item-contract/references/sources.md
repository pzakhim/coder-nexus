# Sources

External ideas adapted into this contract, rewritten in this repo's vocabulary (`G-NN`, `BR-NN`, `AC-NN`, `Q-NN`, `D-NN`, `PHASE-NN`, gates).

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [Fission-AI/OpenSpec `docs/concepts.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/docs/concepts.md) | 73k | A change to built behavior is written as a delta (added / modified / removed), not a restated spec; a removal states why | [change-impact template](../templates/change-impact.md.tpl) `## Behavior delta` |
| [Fission-AI/OpenSpec `docs/concepts.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/docs/concepts.md) | 73k | A spec is a behavior contract: observable behavior only, implementation detail belongs in design and tasks | `## Behavior delta` guidance ("observable behavior, not implementation steps") |
| [Fission-AI/OpenSpec `docs/concepts.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/docs/concepts.md) | 73k | Each change is one self-contained folder kept for history | Already true: `.superpowers/work-items/<slug>/vN/`, closed versions never overwritten ([SKILL](../SKILL.md) "Folder and versions") |
| [Fission-AI/OpenSpec `schemas/spec-driven/templates/proposal.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/schemas/spec-driven/templates/proposal.md) | 73k | Separate new capabilities from existing ones whose requirements change; list affected code in an impact section | `## Behavior delta` (`ADDED` vs `MODIFIED`) next to the existing `## Code impact` |
| [Fission-AI/OpenSpec `schemas/spec-driven/templates/spec.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/schemas/spec-driven/templates/spec.md) | 73k | Delta sections named by kind of change, each requirement backed by a scenario | `ADDED` / `MODIFIED` / `REMOVED` values; `AC delta` rows trace to them |
| [github/spec-kit `templates/constitution-template.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/constitution-template.md) | 142k | A short set of non-negotiable principles shared by every role, which reviews check against | [SKILL](../SKILL.md) "Goal lock": one shared rule for all roles, enforced in part by `REQ-005`, `DESIGN-007`, `PLAN-V-010` |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| "Fluid not rigid", no phase gates, artifacts in any order | OpenSpec concepts | Conflicts with the fixed process: Gates 1/2/3 and their order are mandatory |
| Merging deltas into a living `specs/` source of truth on archive | OpenSpec concepts | This repo keeps each `vN` as the approved record and compares against actual code in `change-impact.md`; a second spec tree would duplicate `requirements.md` |
| Renaming sections to `## ADDED Requirements` / `### Requirement:` / `#### Scenario:` | OpenSpec spec template | Validators read the existing headings (`AC delta`, `Code impact`, Given/When/Then scenarios); headings stay unchanged |
| RFC 2119 keywords (SHALL / MUST / SHOULD / MAY) | OpenSpec concepts | `requirements.md` is plain business language; strength lives in `BR-NN` + `AC-NN`, and "SHOULD" invites unconfirmed exceptions |
| `skip_specs` marker for zero-delta changes | OpenSpec proposal template | Phase-free items already use `brief.md`; no new metadata file |
| Lite vs full spec rigor levels | OpenSpec concepts | The Type and its sequence row already decide which files are needed |
| Project constitution file with versioned amendments | spec-kit constitution | Stack rules live in stack packs and workspace skills; a second rule file would compete with them. Only the "shared non-negotiable rule" idea was kept |
