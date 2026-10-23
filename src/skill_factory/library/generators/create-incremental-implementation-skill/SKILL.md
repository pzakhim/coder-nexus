---
name: create-incremental-implementation-skill
description: Write a workspace's own incremental-implementation skill from the skill-factory knowledge base - the Code Writer's process for executing one approved plan phase task by task (ground each task, edit only its scope, check immediately, re-read the plan, verify the phase, self bug-hunt, hand off with evidence). Use whenever the user wants to set up, standardize or update how the coder agent implements approved plans in a workspace, for any stack and for fullstack repos, or says things like "quy trình code theo plan", "coder làm từng phase", "chuẩn hoá cách code writer làm việc", even if they do not say "skill". Detects the plan format, gates and commands, gets them confirmed, writes .agents/skills/incremental-implementation/, then trial-runs it on real tasks.
argument-hint: "[stack/framework] [where plans live]"
---

# Create Incremental Implementation Skill

Goal: produce `<workspace>/.agents/skills/incremental-implementation/` — the workspace's own version of the Code Writer process, built from the generic base rules in this generator plus the workspace's real plan format, gates, commands and sibling skills.

User input: $ARGUMENTS

Follow the standard steps and shared rules in `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). This file only adds what is specific to incremental implementation. The skill family and ownership: `~/.claude/skill-factory/core/coder-skill-family.md`.

## Step 1 — Context Card (+ process inputs)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and, for existing workspaces, P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing process skills | `.agents/skills/` and `.claude/skills/`: `incremental-implementation`, `work-item(s)`, `implementation-planning`, `dev-team*`, `delivery-workflow`... |
| Coder role files | `.agents/agents/*coder*`, `*writer*`, `coordinator*`; `AGENTS.md` sections on delivery flow |
| Validators / gates scripts | e.g. `validate_dossier.py`, CI checks on plan files |
| Base input (read-only) | `<coder repo>/plugins/core/skills/incremental-implementation/SKILL.md` (Coder Nexus source, read from the repo, not from a workspace) |

## Step 2 — Detect the plan artifacts

Read `references/plan-formats.md`. Identify: where approved plans live, how a phase and a task are written (checkbox format, IDs), the approval gates, optional preparation phase, where results are recorded (as-built, handoff), and the workspace's status vocabulary. Record each item as **found** (with path) or **missing**.

## Step 3 — Propose

- Existing process skill or established dossier format → document it as-is (P4); propose only the missing pieces (e.g. no immediate local check per task, no evidence vocabulary).
- No plan format yet → propose the **lightest** format that supports I1–I14 (plain `plans/<slug>/plan.md` with phases and task checkboxes), never a heavy dossier the workspace does not need.
- Map every base rule in `references/base-rules.md` to the workspace (adopted with real facts, or "not adopted" with a reason).

## Step 4 — Gate (user confirms)

Confirm in one AskUserQuestion round where possible:

1. Plan location and phase/task format
2. Approval gates that must be passed before coding
3. Verification commands per branch (task-level check, phase suite, visual check) — from `references/verification-by-stack.md` + the workspace's real scripts
4. Handoff format and who records results
5. Sibling skills to call (clean-architecture, clean-code, unit-testing, code-simplification, bug-hunt, root-cause-debugging): existing ones linked, missing ones noted

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are **suggested shapes**; only **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md`.

**Mandatory content** (wherever it lands): rules I1, I4, I5, I10, I11, I14 with their reasons; the task loop A–D; task-level and phase-level commands per branch.

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The loop on one screen + where to look |
| `references/02-task-loop.md` | `references/shared/02-…` | `templates/shared/02-task-loop.md.tmpl` | **Mandatory** | Prevents bulk coding and scope creep — the core of the process |
| `references/03-phase-completion.md` | `references/shared/03-…` | `templates/shared/03-phase-completion.md.tmpl` | **Mandatory** | Evidence and "back to the gate" — what stops a red or out-of-scope phase from being handed off |
| `references/06-verification.md` | `references/be/06-…`, `references/fe/06-…` | `templates/branch/06-verification.md.tmpl` | **Mandatory** | Real commands — without them "check immediately" is a wish |
| `references/01-inputs-and-preconditions.md` | `references/shared/01-…` | `templates/shared/01-inputs-and-preconditions.md.tmpl` | Suggested | Readiness checklist; may merge into `SKILL.md` for a light plan format |
| `references/04-simplicity-pass.md` | `references/shared/04-…` | `templates/shared/04-simplicity-pass.md.tmpl` | Suggested | Short; may merge into 03 |
| `references/05-handoff.md` | `references/shared/05-…` | `templates/shared/05-handoff.md.tmpl` | Suggested | Handoff template; may merge into 03 when there is no separate reviewer |
| `references/07-order-of-work.md` | `references/be/07-…`, `references/fe/07-…` | `templates/branch/07-order-of-work.md.tmpl` | Suggested | Layer order when the plan leaves it open; may merge into 06 |

Writing rules: keep each template's purpose (`<!-- GEN: Why … -->`), give every rule its reason, replace every `{{…}}`, delete every `<!-- GEN … -->`, real paths/commands only, every I-rule expressed or marked "not adopted", sibling links per `coder-skill-family.md`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Implementing approved plans
   The Code Writer follows `.agents/skills/incremental-implementation/SKILL.md` for every approved phase.
   ```
2. Offer to add the same link to the coder role files (P3: list inbound/outbound links, ask, edit only link lines).

## Step 7 — Trial run

Follow `~/.claude/skill-factory/core/trial-run.md` (read-only subagents, with vs without the skill). Task ideas for this topic:

- "Implement task 1 of phase N" from a real or recent plan in the workspace (or a small realistic plan you draft with the user).
- A phase where one task's mapped component does not fit — does the agent stop and report a planning blocker instead of working around it?
- Finishing a phase where one check cannot run — does the agent report `BLOCKED`/`NOT_RUN` instead of `PASS`?

Compare: tasks done one by one with re-reads, edits limited to the task's files, checks named with real commands, evidence lines, correct stop-and-ask behavior. The user may skip this step; record it.

## Step 8 — Description

Tune the generated description (`~/.claude/skill-factory/core/authoring-guide.md` "Description"): workspace name; situations such as "implement phase", "start coding the approved plan", "next task", "hand off"; the team's own words (e.g. their phase/task names). It must not trigger on brainstorming or planning requests — that belongs to other skills.

## Step 9 — Verify, record & report

1. Run `checklist.md` and `~/.claude/skill-factory/core/checklist-common.md`.
2. Record provenance in the private registry (`~/.claude/skill-factory/core/provenance.md`).
3. Report files written, deviations from the suggested shape with reasons, decisions, rules not adopted, missing siblings, trial-run results.

## Update mode

Existing `.agents/skills/incremental-implementation/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep workspace rules such as dossier gates, validator commands, vocabulary).

## Changing this generator

Bump `VERSION` and add a `CHANGELOG.md` entry with **Affects** and **Migration** (`~/.claude/skill-factory/core/versioning.md`).

## Resources

- `references/base-rules.md` — I1–I14 generic rules, their reasons, and where each goes
- `references/plan-formats.md` — detecting plan artifacts, gates, vocabulary
- `references/verification-by-stack.md` — typical task/phase/visual commands per stack
- `templates/` — `SKILL.md.tmpl`, `shared/01–05`, `branch/06–07` (suggested shapes)
- `checklist.md` — topic checks
- `~/.claude/skill-factory/core/authoring-guide.md`, `~/.claude/skill-factory/core/trial-run.md`
