# Sources

Built from the former `feature-planner` goal-framing reference and the Stage 1A / 1A-0 / 1A-G text of the `spec_writer` agent, then extended with the ideas below. Ideas were rewritten in this repository's vocabulary; nothing was copied.

| Source (pinned) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/brainstorming/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/brainstorming/SKILL.md) | 303k | Look before you ask; echo the request back and surface constraints, conflicts or a cheaper path; anti-goals (failure even if it works); size the work (small change gets a short document); say when the request is really several projects; anything you filled in is shown as your proposal | [goal-candidates §1, §5](goal-candidates.md), [job-type-and-stack → size](job-type-and-stack.md#size-the-work), SKILL rules GF1, GF10 |
| [addyosmani/agent-skills `skills/interview-me/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/interview-me/SKILL.md) | 109k | One-sentence hypothesis with a confidence number and what is missing below ~70%; "predict the next three answers" check; restate frame Outcome / User / Why now / Success / Out of scope; buzzword answers are probed; "sounds good" / "whatever you think" is not a yes | [goal-candidates §2, §3](goal-candidates.md), [goal-question → reading the answer](goal-question.md#reading-the-answer), GF9 |
| [addyosmani/agent-skills `skills/spec-driven-development/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/spec-driven-development/SKILL.md) | 109k | Scope check before specifying: AC that cluster into independently shippable groups get a capability map with one-way dependencies and a build order; reframe vague instructions as checkable success criteria | [goal-candidates → split check](goal-candidates.md#split-check), §3 buzzwords, GF7 |
| [github/spec-kit `templates/spec-template.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/spec-template.md) | 142k | Measurable, technology-agnostic success criteria; stories ordered by value, each independently testable | [goal-candidates §3](goal-candidates.md) (signals, `G-01` = most valuable), split check |
| [github/spec-kit `templates/commands/specify.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/commands/specify.md) | 142k | Success signals describe user-facing outcomes, not system internals (no endpoint or cache metrics); spec focuses on what and why, not how | [goal-candidates §3](goal-candidates.md), GF6 |
| [mattpocock/skills `skills/engineering/wayfinder/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/wayfinder/SKILL.md) | 300k | Name the destination first, because it fixes the scope; keep "out of scope" (ruled out, with a reason) separate from "not yet specified" (in scope, still unclear); if nothing is unclear, no heavy map is needed | SKILL opening, [goal-candidates §4](goal-candidates.md#4-non-goals), GF8, small path |

## Not adopted

| Idea | Source | Why not |
|---|---|---|
| Open with an open question and avoid option menus | brainstorming, interview-me | The fixed process asks through `ask_question` with `(Recommended)` first. Kept the spirit: Edit takes free text in the user's own words. |
| Offer to "just dive in" and skip the questions | brainstorming | Gates 1/2/3 and 0 OPEN `Q-NN` before a gate are fixed. |
| Lay out build approaches during goal framing | brainstorming | Approaches belong to `solution-options` (spec: behavior/scope; planning: technical). |
| Visual companion and throwaway spikes before the spec | brainstorming | UI flows are owned by `designer` after goal framing; no code before Gate 1 and the item branch. |
| Builder check by a fresh subagent | brainstorming | Covered by `cold-reader-check` before each gate, not at goal framing. |
| Long interview until ~95% confidence before restating | interview-me | Goal framing asks one goal question; the remaining questions go to the `Q-NN` queue under `grilling`. |
| Stop the turn right after the intent is confirmed | interview-me | `grilling` Law 1 writes the `DRAFT` in the turn the goals are confirmed, so nothing is lost. |
| "Assumptions I'm making - correct me or I proceed" list; Assumptions section; informed guesses for unclear points | spec-driven-development, spec-kit | Conflicts with "confirm every inference": every inference becomes a `Q-NN`. |
| `Open Questions` section and `[NEEDS CLARIFICATION]` markers, max 3, all asked together | spec-driven-development, spec-kit | Open items live only in `## 0. Question Queue`, unlimited, one question at a time; requirements read in one straight line. |
| Stable module ids and per-module `SPEC-<id>.md` files | spec-driven-development | Linked work items already have slugs and `vN` folders (`work-item-contract`). |
| Commands, project structure, code style in the spec | spec-driven-development | Planning and the workspace skills own them; `requirements.md` has no code or file names. |
| Short-name and branch generation; quality checklist file | spec-kit | Slug and folders belong to `work-item-contract`, branches to `git-preflight`, checks to `gate-review` and the validators. |
| Map of decision tickets on the issue tracker, one ticket per session | wayfinder | Huly is read-only; decisions live as `D-NN` in `codebase-notes.md`. |
