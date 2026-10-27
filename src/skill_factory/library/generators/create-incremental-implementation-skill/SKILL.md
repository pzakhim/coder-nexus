---
name: create-incremental-implementation-skill
description: Write a workspace's own incremental-implementation skill from the skill-factory knowledge base - the Code Writer's process for executing one approved plan phase task by task (preconditions and a Consumes/Produces pre-flight, ground each task, edit only its scope, check immediately, triage against the expected result, tick and re-read the plan, verify the phase, self bug-hunt, simplicity pass, hand off with evidence) - for any stack. Use whenever the user wants to set up, standardize or update how the coder agent implements approved plans in a workspace, or says things like "quy trình code theo plan", "coder làm từng phase", "chuẩn hoá cách code writer làm việc", even if they do not say "skill". Detects the plan format, gates and commands, gets them confirmed, writes .agents/skills/incremental-implementation/, then trial-runs it on real tasks.
argument-hint: "[stack/framework] [where plans live]"
---

# Create Incremental Implementation Skill

Goal: produce `<workspace>/.agents/skills/incremental-implementation/` — the workspace's own version of the Code Writer process, built from the generic base rules in this generator plus the workspace's real plan format, gates, commands and sibling skills.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). The skill family and ownership: `~/.claude/skill-factory/core/coder-skill-family.md`.

## Step 1 — Context Card (+ process inputs)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and, for existing workspaces, P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing process skills | `.agents/skills/` and `.claude/skills/`: `incremental-implementation`, `work-item-contract`, `implementation-planning`, `dev-team*` |
| Coder role files | `.agents/agents/*coder*`, `*writer*`, `coordinator*`; `AGENTS.md` sections on delivery flow |
| Plan artifacts | Found with `references/discovery-and-checks.md` §1 |
| Check commands | Task, phase, architecture and visual commands found with `references/discovery-and-checks.md` §2 |
| Base inputs (read-only) | `references/base-rules.md` and `references/discovery-and-checks.md` |

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule I1–I17, decide: adopted with the workspace's real facts, adapted to its plan format, or "not adopted" with a stated reason. I1, I4, I5, I10, I11, I14 and I16 are never "not adopted".

## Step 3 — Propose

- Existing process skill or established plan format → document it as-is (P4); propose only the missing pieces (e.g. no pre-flight, no expected result per task, no evidence vocabulary).
- No plan format yet → propose the **lightest** format that supports the mandatory rules (a plain plan file with phases and task checkboxes), never a heavy dossier the workspace does not need.
- Commands per level from real scripts, the plan-change process and words, the tick line, the hand-off fields and who records results.

## Step 4 — Gate (user confirms)

One confirmation round where possible:

1. Plan location, phase/task format and the plan-change process
2. Approval gates that must pass before coding
3. Task check, phase suite, architecture gate and visual check commands (`PASS` / `FAIL`)
4. Hand-off format, statuses and who records results
5. Sibling skills to call (clean-architecture, clean-code, unit-testing, root-cause-debugging, code-simplification, bug-hunt): existing ones linked, missing ones noted

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The loop on one screen, the rules and where to look |
| `references/01-preconditions-and-preflight.md` | `templates/references/01-preconditions-and-preflight.md.tmpl` | **Mandatory** | Readiness and interface pre-flight — what stops work on an unready or outdated plan |
| `references/02-task-loop-and-checks.md` | `templates/references/02-task-loop-and-checks.md.tmpl` | **Mandatory** | Task loop, triage and real commands — what prevents bulk coding, scope creep and silent deviation |
| `references/03-phase-end-and-handoff.md` | `templates/references/03-phase-end-and-handoff.md.tmpl` | **Mandatory** | Phase suite, self-checks, evidence and hand-off on one revision |

Writing rules: keep each template's purpose, give every rule its reason, real paths/commands only, every I-rule expressed or marked "not adopted", sibling links per `coder-skill-family.md`, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Implementing approved plans
   The Code Writer follows `.agents/skills/incremental-implementation/SKILL.md` for every approved phase.
   ```
2. Offer to add the same link to the coder role files (P3: list inbound/outbound links, ask, edit only link lines).

## Step 7 — Trial run

Follow `~/.claude/skill-factory/core/trial-run.md` (read-only subagents, with vs without the skill). Task ideas:

- "Implement task 1 of phase N" from a real or recent plan (or a small realistic plan drafted with the user).
- A task whose consumed signature differs from the real code — does the pre-flight catch it and stop with a plan change?
- A task whose check output differs from the expected result because the plan is wrong — does the agent leave it unticked instead of patching?
- Finishing a phase where one check cannot run — does the agent report `BLOCKED` / `NOT_RUN` instead of `PASS`?

Compare: tasks done one by one with re-reads, edits limited to the task's files, checks named with real commands, triage outcomes, evidence lines, correct stop-and-ask behavior. The user may skip this step; record it.

## Step 8 — Description

Tune the generated description (`~/.claude/skill-factory/core/authoring-guide.md` "Description"): workspace name; situations such as "implement phase", "start coding the approved plan", "next task", "hand off"; the team's own words. It must not trigger on brainstorming or planning requests.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report files written, deviations from the suggested shape, rules not adopted, missing siblings, trial-run results.

## Update mode

Existing `.agents/skills/incremental-implementation/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep workspace rules such as dossier gates, validator commands, vocabulary).

## Changing this generator

Bump `VERSION` and add a `CHANGELOG.md` entry with **Affects** and **Migration** (`~/.claude/skill-factory/core/versioning.md`).

## Resources

- [Base Rules](references/base-rules.md) — I1–I17 with reasons, target files and the default order of work
- [Discovery & Checks](references/discovery-and-checks.md) — plan formats to detect and how to find task/phase/visual commands
- `templates/` — `SKILL.md.tmpl` and `references/01–03.md.tmpl`
- [Checklist](checklist.md) — topic verification checks
