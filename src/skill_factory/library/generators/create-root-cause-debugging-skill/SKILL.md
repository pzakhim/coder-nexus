---
name: create-root-cause-debugging-skill
description: Write a workspace's own root-cause-debugging skill from the skill-factory knowledge base - how the Code Writer fixes a failing check or a confirmed defect - deterministic reproduction, reading the first real error, isolating and testing one falsifiable hypothesis at a time, fixing the root cause at the owning layer with a regression test, never green-washing, telling environment problems (BLOCKED) from code problems, stopping and escalating on time, and reporting with unified review severities - for any stack. Use whenever the user wants to set up, standardize, or update how the coder agent debugs in a workspace, or says things like "tạo skill debug", "quy trình sửa lỗi", "test đỏ thì làm gì", "tìm nguyên nhân gốc", even if they do not say "skill". Writes .agents/skills/root-cause-debugging/, then trial-runs it on real failures.
argument-hint: "[stack/framework]"
---

# Create Root Cause Debugging Skill

Goal: produce `<workspace>/.agents/skills/root-cause-debugging/` — how the Code Writer turns a red check or a confirmed defect into a root-cause fix with a regression test, using this workspace's CLI commands and tracing tools, and when it must stop and escalate instead.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — `bug-hunt` *finds* unknown defects; `root-cause-debugging` *fixes* a failure that is already known; `incremental-implementation` and `change-control` govern when a fix exceeds task scope and returns to the gate.

## Step 1 — Context Card (+ debugging inputs)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect using `references/deriving-the-model.md`:

| Field | Where to look |
|---|---|
| Existing debugging guidance | `.agents/skills/*debug*`, `.claude/skills/*debug*`, `AGENTS.md`/`CLAUDE.md` sections on fixing failures |
| Code-intelligence & tracing tools | GitNexus (`query`, `context`, `impact`, `detect_changes`), LSP, `rg`; mandatory pre-edit impact rules |
| Non-interactive CLI diagnostic commands | Reproduce one failing test, rerun failed only, verbose stack/locals output, single-file analyzer/linter, git bisect in a disposable worktree |
| Logs & local environment checks | Where app/worker/test logs live; how to verify DB/service/device readiness without restarting shared stacks |
| Recent bug-fix commits | `git log --grep='fix' -n 15` — recurring root-cause patterns in this codebase |
| Base inputs (read-only) | `references/base-rules.md` and `references/deriving-the-model.md` |

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule `D1`–`D14`: enforced by an automated gate (cite it), adopted, adapted to the workspace, or "not adopted" with a stated reason. `D1`, `D7`, `D8`, `D9`, and `D12` are mandatory and never "not adopted".

## Step 3 — Propose

Using `references/deriving-the-model.md`:
- **Reproduction, Reading & CLI Tools (`01`):** Reproduction hierarchy, reading the first real frame in source code, untrusted log redaction, and non-interactive CLI diagnostic/tracing commands (`EXTEND` vs `INIT`).
- **Isolation, Hypotheses & Symptom Matrix (`02`):** Input/diff isolation, 3–5 ranked falsifiable hypotheses (`H1`..`H3`), temporary tagged logging (`[DEBUG-xxxx]`) with mandatory removal check, and the workspace's Symptom → First Moves → Typical Root Cause matrix.
- **Root-Cause Fix, Escalation & Report (`03`):** Red-to-Green regression test at the right seam, smallest fix at the owning layer, Never Green-Wash table, Environment (`BLOCKED`) vs Code table, 3-attempt time-box, `change-control` escalation classes, hand-off Debug Report block, and unified `BLOCKER` / `MAJOR` / `MINOR` review grading.

## Step 4 — Gate (user confirms)

One confirmation round where possible: (1) CLI diagnostic and tracing commands, (2) symptom matrix and tagged debug cleanup rule, (3) environment (`BLOCKED`) vs code checks, 3-attempt time-box, and `BLOCKER` / `MAJOR` / `MINOR` review grading.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Keep `SKILL.md` concise (< 120 lines) and group `references/` into 3 cohesive chronological files:

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | CLI diagnostic gates (`PASS`/`FAIL`), the 6-step loop, Never Green-Wash list, mandatory rules `D1`–`D14`, and routing table |
| `references/01-reproduce-read-and-tools.md` | `templates/references/01-reproduce-read-and-tools.md.tmpl` | **Mandatory** | `EXTEND` vs `INIT` rule, deterministic reproduction hierarchy, reading the first real error, untrusted log redaction, and CLI/tracing commands |
| `references/02-isolate-and-hypothesize.md` | `templates/references/02-isolate-and-hypothesize.md.tmpl` | **Mandatory** | Diff/layer isolation, 3–5 ranked falsifiable hypotheses, tagged `[DEBUG-xxxx]` cleanup, and Symptom → First Moves → Cause matrix |
| `references/03-fix-escalate-and-report.md` | `templates/references/03-fix-escalate-and-report.md.tmpl` | **Mandatory** | Red-to-Green regression fix, Never Green-Wash table, Environment (`BLOCKED`) vs Code, 3-attempt time-box, `change-control` escalation, Debug Report block, and `BLOCKER`/`MAJOR`/`MINOR` review grading |
| `profiles/<profile>/*.md` (optional, pack skills) | — | **Suggested** | Profile-specific debugging contracts synced into `references/` and linked at `<!-- {{profile_references}} -->` |

Writing rules: keep each template's purpose, give every rule its rationale, use real non-interactive commands/tools only, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Root-Cause Debugging
   When a check fails or a defect is confirmed, follow `.agents/skills/root-cause-debugging/SKILL.md`.
   ```
2. Offer to link it from the coder and bug-fixer role files (P3).
3. If `incremental-implementation` exists, verify its "when a check fails" (`CODE_WRONG`) path links here.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:
- Replay a real failing test or recent bug-fix commit: reproduction command, 3 ranked hypotheses, root cause, owning layer fix, and regression test.
- Diagnose an environment failure (service down, missing env var, unapplied migration/codegen) — verify the agent returns `BLOCKED` with evidence instead of patching code.
- Diagnose an async/flaky failure — verify the agent isolates shared state/timing instead of adding sleeps or retries.

## Step 8 — Description

Per the authoring guide: workspace name; situations (a test/build/analyzer check is red with `CODE_WRONG`, "why does this fail", a `CONFIRMED` review or bug-hunt finding); team trigger words. Should not trigger for cold code hunting (`bug-hunt`) or new feature development.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted, and trial results.

## Update mode

Existing `.agents/skills/root-cause-debugging/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep workspace tracing rules such as mandatory impact analysis).

## Changing this generator

Bump `VERSION` and add a `CHANGELOG.md` entry with **Affects** and **Migration** (`~/.claude/skill-factory/core/versioning.md`).

## Resources

- [Base Rules](references/base-rules.md) — `D1`–`D14` mandatory rules, binary `PASS`/`FAIL` gates, and unified `BLOCKER`/`MAJOR`/`MINOR` review scale
- [Deriving the Model](references/deriving-the-model.md) — discovering diagnostic CLI commands, tracing tools, symptom matrices, and environment checks from any workspace
- `templates/` — `SKILL.md.tmpl` and `references/01–03.md.tmpl`
- [Checklist](checklist.md) — topic verification checks
