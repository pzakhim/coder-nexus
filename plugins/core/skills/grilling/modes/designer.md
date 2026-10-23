# Mode: designer — workflow, screens, states, viewports (`designer`)

Use with [SKILL.md](../SKILL.md). The detailed interview, proposal format and viewport command live in `ui-ux-design` → [workflow interview](../../ui-ux-design/references/01_workflow_interview.md); this file lists which rows the designer owns and how they enter the shared queue. Present alternative flows with `solution-options` (UI flow options) when more than one is viable.

## 1. Before asking

Read the confirmed goals, the requirements draft, the source inventory, `screen-catalog.md`, the screenshots of the screens involved, and `codebase-notes.md` → Question Queue and Decision Log. Ask only rows with `Owner: designer` plus what the sources leave open. A business-rule, permission or API question goes back to spec_writer's queue as `Owner: spec_writer`, not to the user.

## 2. Rows the designer owns

| Row | Settle | Queue group (SKILL §2.2) |
|---|---|---|
| Actor and device | Who does this, on which device(s). | 2 Scope and actors |
| Entry | Which existing screen, menu, button, notification or deep link starts it. | 3 Workflow |
| Steps | What the user does at each step and what the system shows back. | 3 Workflow |
| Branches | Invalid input, no data, no permission, network error, duplicate action. | 3 Workflow / 6 Edge cases |
| Exit | Where the user ends and what changed (saved, sent, status). | 3 Workflow |
| Screens | Which existing screens change and which stay as context only. | 3 Workflow |
| States | `Default/Content`, `Loading`, `Empty`, `Error` (plus disabled, input retention) per screen. | 5 States |
| Viewports | Platforms, size per platform, orientation — once per project, not per work item. | 5 States |

## 3. How to ask

- One workflow per user-visible scenario (`W-NN`), proposed as numbered steps and confirmed in one question: `Confirm (Recommended)` / `Change steps` / `Split into more workflows`. The proposal is one decision, so it stays within the one-question law.
- Viewports: one question settling platforms, sizes and orientations together, pre-filled from the sources; skip it when `coder-nexus ux viewports --project .` already reports them confirmed.
- Every `W-NN` serves a confirmed `G-NN`; a flow that serves none is a non-goal and is not drawn.
- If the interview changes a goal or the scope, stop and hand it back to spec_writer (Gate 1 again).
