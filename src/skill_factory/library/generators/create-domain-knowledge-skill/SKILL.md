---
name: create-domain-knowledge-skill
description: Write a workspace's own domain-knowledge skill from the skill-factory knowledge base - the business glossary (business words and their names in code), the entities and how their status changes, roles and the data scopes that limit who sees what, the business rules and where each one lives in the code, and how the skill is kept current - found in the repository and confirmed by the user, for any domain and any stack. Use whenever the user wants to set up, standardize or update the shared business knowledge that Spec Writer, Planning, QA and reviewers rely on, or says things like "tạo skill domain", "thuật ngữ nghiệp vụ", "glossary", "quy tắc nghiệp vụ nằm ở đâu", "phân quyền dữ liệu", even if they do not say "skill". Writes .agents/skills/domain-knowledge/, then trial-runs it on real requests.
argument-hint: "[module or area]"
---

# Create Domain Knowledge Skill

Goal: produce `<workspace>/.agents/skills/domain-knowledge/` — what the workspace's business words mean, which entities exist and how their status changes, who may do what on which data, and where each business rule lives. Other Spec & Planning skills read it, so it comes first.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0**. Ownership and the generic-vs-specific rule: `~/.claude/skill-factory/core/planning-skill-family.md` — this generator stays domain-neutral; every concrete entity, role and scope comes from the workspace.

## Step 1 — Context Card (+ domain sources)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Then collect, read-only, the sources in `references/detection.md`: entities and fields, status values and transitions, roles and permission checks, data-scope conditions, user-facing labels, business documents, existing glossaries. Reading closed tracker tickets is optional: only when a tracker is configured and the user agrees.

If the repository is large, list its modules with a one-line purpose each and go to the gate with that list before reading deeply.

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule DK1–DK8: adopted, adapted, or "not adopted" with a reason. DK5 (labels, no invention) and DK8 (no personal data or secrets) are never "not adopted".

## Step 3 — Propose

- Draft glossary rows from labels, entity names and documents; mark each `VERIFIED` (path) or `OPEN`.
- Draft entity cards with status values and the transitions found in code (who triggers each, where).
- Draft the roles × scopes × actions matrix from permission checks; mark gaps `OPEN`.
- Draft the business-rule catalog with `file:symbol` locations.
- Show what is missing: categories the workspace does not have are stated in one line, not filled.

## Step 4 — Gate (user confirms)

AskUserQuestion, ≤ 4 questions per round, recommendation first:

| # | Question | Default proposal |
|---|---|---|
| Q1 | Which modules/areas are in scope (large repositories) | The modules with the most recent work items |
| Q2 | Glossary languages (team language ↔ code names) | Team language + English code names |
| Q3 | Confirm the roles × scopes × actions matrix (show it) | As read from code; `OPEN` rows asked one by one |
| Q4 | Who updates the skill and when | Spec Writer when a work item changes an entity or rule; reviewed at Gate 1 |

Unclear terms and rules found in Step 3 are asked one at a time after the matrix; anything still unknown stays `OPEN`.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Layout: **flat**; when the domain is large, split per module into `references/modules/<module>.md` following `~/.claude/skill-factory/core/splitting-protocol.md`, keeping `01`–`05` as the index.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | How to use the knowledge and the labels on one screen |
| `references/01-glossary.md` | `templates/01-glossary.md.tmpl` | **Mandatory** | One word, one meaning, across spec and code |
| `references/02-entities-and-lifecycles.md` | `templates/02-entities-and-lifecycles.md.tmpl` | **Mandatory** | Status transitions are where specs miss most |
| `references/03-roles-and-scopes.md` | `templates/03-roles-and-scopes.md.tmpl` | **Mandatory** (one line when the workspace has no roles) | Wrong permissions are the costliest defects |
| `references/04-business-rules.md` | `templates/04-business-rules.md.tmpl` | **Mandatory** | Planning finds the right place to change |
| `references/05-sources-and-upkeep.md` | `templates/05-sources-and-upkeep.md.tmpl` | **Mandatory** | The skill stays true as the code changes |

Writing rules: only facts with a label (`VERIFIED` + path, `CONFIRMED`, `OPEN`); no personal data, no real customer names unless they are product terms the user confirms; volatile facts are links, not copies; replace every `{{…}}`, delete every `<!-- GEN … -->`, English body (glossary terms in the team language too), < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Domain knowledge
   Business terms, entities, roles and rules: `.agents/skills/domain-knowledge/SKILL.md`.
   ```
2. Offer to link it from existing requirements, planning and quality skills (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Pick tasks from this workspace, for example:

- A request to add a status to an entity that has a lifecycle — are all transitions and who triggers them asked?
- A request about who may see or change some data — is the roles × scopes matrix used?
- A request that uses a synonym of a glossary term — is it mapped to the right entity?

## Step 8 — Description

Per the authoring guide: workspace name; situations (writing or reviewing requirements, planning, test design, naming in code); the team's trigger words. Should not trigger for pure tooling questions.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report `OPEN` items, rules adapted or not adopted, trial results.

## Update mode

Existing `.agents/skills/domain-knowledge/` or a workspace glossary/domain doc: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep the team's terms, IDs and confirmed rules verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — DK1–DK8 with reasons
- `references/detection.md` — where each kind of domain fact is usually found, per stack
- `templates/` — `SKILL.md.tmpl`, `01–05` (suggested shapes)
- `checklist.md` — topic checks
