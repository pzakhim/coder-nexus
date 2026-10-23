---
name: create-root-cause-debugging-skill
description: Write a workspace's own root-cause-debugging skill from the skill-factory knowledge base - how the Code Writer fixes a failing check or a reported defect - reproduce, read the real error, isolate, test one hypothesis at a time, fix the root cause at the right layer with a regression test, never turn a check green by editing tests or adding fake fallbacks, tell environment problems from code problems, stop and escalate on time - with the workspace's real commands and tracing tools, for any stack and fullstack repos. Use whenever the user wants to set up, standardize or update how the coder agent debugs in a workspace, or says things like "tạo skill debug", "quy trình sửa lỗi", "test đỏ thì làm gì", "tìm nguyên nhân gốc", even if they do not say "skill". Writes .agents/skills/root-cause-debugging/, then trial-runs it on real failures.
argument-hint: "[stack/framework]"
---

# Create Root Cause Debugging Skill

Goal: produce `<workspace>/.agents/skills/root-cause-debugging/` — how the Code Writer turns a red check or a confirmed defect into a root-cause fix with a regression test, using this workspace's commands and tracing tools, and when it must stop instead.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — bug-hunt *finds* defects; root-cause-debugging *fixes* a failure that is already known; incremental-implementation decides when a fix is out of scope and goes back to the gate.

## Step 1 — Context Card (+ debugging inputs)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing debugging guidance | `.agents/skills/*debug*`, `.claude/skills/*debug*`, `AGENTS.md`/`CLAUDE.md` sections on fixing failures |
| Code-intelligence tools | GitNexus or similar (query/context/impact), LSP, `rg`; rules such as "run impact analysis before editing a symbol" |
| Focused commands | Re-run only failed tests, run one test verbose, analyzer on one file, build one target |
| Logs and local stack | Where server/worker/browser logs are; how the local stack is started and the rule about not touching stacks you did not start |
| Recent incidents | Bug-fix commits (`git log --grep='fix'`) — typical root causes in this codebase |
| Base inputs (read-only) | `references/base-rules.md` and `work-item-contract` §9 (verify step), `plugins/core/skills/incremental-implementation` (back-to-gate rule) |

## Step 2 — Map the base rules

Read `references/base-rules.md`, `references/techniques.md`, `references/tools-by-stack.md`. For each rule D1–D14: adopted, adapted, or "not adopted" with a reason. D1, D7, D8, D9, D12 are never "not adopted".

## Step 3 — Propose

- **Commands** per branch: reproduce one failure, rerun failed only, verbose single test, bisect.
- **Tracing:** the workspace's code-intelligence tool flow (if any) and its mandatory rules (e.g. impact analysis before editing).
- **Environment checks:** how to tell a broken environment from a code defect here, and what is `BLOCKED`.
- **Time-box and escalation:** attempts before stopping, who to escalate to, which fixes go back to the gate.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) commands per branch, (2) tracing tools and their rules, (3) environment checks and the BLOCKED rule, (4) time-box and escalation.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–06`; branched: `shared/01–04`, `shared/06`, `be/05`, `fe/05`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The loop and the never-list on one screen — read under pressure |
| `references/01-reproduce-and-read.md` | `shared/01-…` | `templates/shared/01-reproduce-and-read.md.tmpl` | **Mandatory** | Fixes without a reproduction are guesses |
| `references/02-isolate-and-hypothesize.md` | `shared/02-…` | `templates/shared/02-isolate-and-hypothesize.md.tmpl` | **Mandatory** | One falsifiable hypothesis at a time finds the cause fastest |
| `references/03-fix-and-prevent.md` | `shared/03-…` | `templates/shared/03-fix-and-prevent.md.tmpl` | **Mandatory** | Root cause at the right layer + regression test, never a green-washing fix |
| `references/04-stop-and-escalate.md` | `shared/04-…` | `templates/shared/04-stop-and-escalate.md.tmpl` | **Mandatory** | Environment vs code, time-box, back to the gate |
| `references/05-tools-and-commands.md` | `be/05-…`, `fe/05-…` | `templates/branch/05-tools-and-commands.md.tmpl` | **Mandatory** | Real commands and tracing tools per branch |
| `references/06-report.md` | `shared/06-…` | `templates/shared/06-report.md.tmpl` | Suggested | Debug report in the handoff; may merge into 03 |

Writing rules: keep each template's purpose, give every rule its reason, real commands/tools only, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Debugging
   When a check fails or a defect is confirmed, follow `.agents/skills/root-cause-debugging/SKILL.md`.
   ```
2. Offer to link it from the coder role file (P3).
3. If `incremental-implementation` exists, check its "when a check fails" section links here.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- A real failing test from the workspace (or a recent fix commit replayed on paper: "this test fails with <message> — plan the investigation").
- A failure caused by the environment (service down, missing env var) — does the agent report BLOCKED instead of changing code?
- A flaky/async failure — does the agent reproduce and control timing instead of adding sleeps/retries?

Compare: reproduction first, one hypothesis at a time, root cause named, regression test planned, never-list respected, stop rule applied.

## Step 8 — Description

Per the authoring guide: workspace name; situations (a test/build/analyzer is red, "why does this fail", a CONFIRMED bug-hunt finding to fix); team trigger words. Should not trigger for finding unknown bugs (bug-hunt) or new features.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, trial results.

## Update mode

Existing `.agents/skills/root-cause-debugging/` (or another debugging skill): registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep tool rules such as mandatory impact analysis).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — D1–D14 with reasons
- `references/techniques.md` — symptom → approach
- `references/tools-by-stack.md` — focused, verbose, rerun-failed and bisect commands per stack
- `templates/` — `SKILL.md.tmpl`, `shared/01–04, 06`, `branch/05` (suggested shapes)
- `checklist.md` — topic checks
