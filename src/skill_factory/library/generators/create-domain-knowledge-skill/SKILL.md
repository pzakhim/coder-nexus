---
name: create-domain-knowledge-skill
description: "Write a workspace's own domain-knowledge skill from the skill-factory knowledge base - the business glossary (ubiquitous language and code identifiers), entity status lifecycles, roles and data scopes, business rules with code locations, and upkeep discipline - found in the repository and confirmed by the user, for any domain and any stack. Use whenever the user wants to set up, standardize, or update shared business knowledge that Spec Writer, Planning, QA, and reviewers rely on, or says things like 'tạo skill domain', 'thuật ngữ nghiệp vụ', 'glossary', 'quy tắc nghiệp vụ nằm ở đâu', 'phân quyền dữ liệu', even if they do not say 'skill'. Writes .agents/skills/domain-knowledge/, then trial-runs it on real requests."
argument-hint: "[module or area]"
---

# Create Domain Knowledge Skill

Goal: produce `<workspace>/.agents/skills/domain-knowledge/` — what the workspace's business words mean, which entities exist and how their statuses change, who may do what on which data, where each business rule is enforced, and how deterministic CLI gates (`PASS` / `FAIL`) and reviewers (`BLOCKER` / `MAJOR` / `MINOR`) verify compliance.

User input: $ARGUMENTS

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0**. Ownership and the generic-vs-specific rule: [../../core/planning-skill-family.md](../../core/planning-skill-family.md) — this generator stays domain-neutral; every concrete entity, role, and data scope comes from the workspace.

## Step 1 — Context Card (+ domain sources)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and existing-project discovery ([../../core/existing-project.md](../../core/existing-project.md)). Then collect, read-only, the sources in [references/detection.md](references/detection.md): entities and fields, status values and transitions, roles and permission checks, data-scope conditions, user-facing labels, business documents, and existing glossaries. Reading closed tracker tickets is optional (only when a tracker is configured and the user agrees).

If the repository is large, list its modules with a one-line purpose each and confirm the scope at the gate before reading deeply.

## Step 2 — Map the base rules

Read [references/base-rules.md](references/base-rules.md). All rules `DK1`–`DK9` are **mandatory compliance**. Map each rule to the workspace's real artifacts and enforcement points. If a workspace has no RBAC roles or data scopes, satisfy `DK3` with a one-line `N/A for this workspace` entry in `03-roles-scopes-and-upkeep.md`.

## Step 3 — Propose

- Draft glossary rows (`DK1`) from labels, entity names, and documents; mark each `VERIFIED` (path) or `OPEN`. Populate `"Avoid saying"` from synonymous words used across UI labels, code, documents, or tickets.
- List overloaded or fuzzy words (`DK9`) as candidates for `Q-NN` → `D-NN` resolution examples.
- Draft entity cards (`DK2`) with status values, allowed/forbidden transitions, triggers, and `file:symbol` enforcement points, plus the business-rule catalog (`DK4`, `BR-NN` / `DR-NN`).
- Draft the `Role × Scope × Action` matrix (`DK3`) from permission checks; mark unknown cells `OPEN` (or state `N/A for this workspace` in one line).
- Propose deterministic CLI gates (`PASS` / `FAIL`) and the `BLOCKER` / `MAJOR` / `MINOR` review rubric.

## Step 4 — Gate (user confirms)

AskUserQuestion, ≤ 4 questions per round, recommendation first:

| # | Question | Default proposal |
|---|---|---|
| Q1 | Modules/areas in scope (large repositories) | Modules with the most recent work items |
| Q2 | Glossary languages (team language ↔ code names) | Team language + English code identifiers |
| Q3 | Confirm the `Role × Scope × Action` matrix | As read from code; `OPEN` cells asked one by one |
| Q4 | Upkeep owner and trigger | Spec Writer in the same work item when an entity, role, scope, or rule changes; verified at Gate 1 |

Unclear terms and rules found in Step 3 are asked one at a time after the matrix; anything still unknown stays `OPEN`.

## Step 5 — Author

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Layout: **flat**; when the domain is large, split per module into `references/modules/<module>.md` following [../../core/splitting-protocol.md](../../core/splitting-protocol.md), keeping `01`–`03` as the cohesive index.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | Deterministic CLI gates (`PASS`/`FAIL`), mandatory `DK1`–`DK9` index, and reference table on one screen |
| `references/01-glossary-and-ubiquitous-language.md` | `templates/references/01-glossary-and-ubiquitous-language.md.tmpl` | **Mandatory** | Ubiquitous language glossary (`DK1`), banned synonyms (`"Avoid saying"`), and challenging fuzzy words (`DK9`) |
| `references/02-entities-lifecycles-and-rules.md` | `templates/references/02-entities-lifecycles-and-rules.md.tmpl` | **Mandatory** | Entity cards with status lifecycles (`DK2`) and the business-rule catalog with `file:symbol` (`DK4`) |
| `references/03-roles-scopes-and-upkeep.md` | `templates/references/03-roles-scopes-and-upkeep.md.tmpl` | **Mandatory** | `Role × Scope × Action` matrix (`DK3`), fact labels (`DK5`), volatile links (`DK6`), upkeep (`DK7`), PII hygiene (`DK8`), and `BLOCKER`/`MAJOR`/`MINOR` rubric |
| `profiles/<profile>/*.md` (optional, pack skills) | — | **Suggested** | Profile-specific contracts (`imespro`, `external-structured`, `external-standard`) synced into `references/` at `<!-- {{profile_references}} -->` |

Writing rules: only labelled facts (`VERIFIED` + path, `CONFIRMED`, `OPEN`); zero personal data or secrets (`DK8`); link volatile facts (`DK6`); replace every `{{…}}`, delete every `<!-- GEN … -->`, English body (glossary terms include team language), < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Domain knowledge
   Business terms, entities, roles, and rules: `.agents/skills/domain-knowledge/SKILL.md`.
   ```
2. Offer to link it from existing requirements, planning, and quality skills without clobbering user content.

## Step 7 — Trial run

Follow [../../core/trial-run.md](../../core/trial-run.md) on real workspace prompts:
- Adding a status to a lifecycle entity — are all transitions, triggers, and enforcement locations checked?
- Asking who may view or mutate restricted data — is the `Role × Scope × Action` matrix applied?
- Using a banned `"Avoid saying"` synonym or overloaded word — does the agent raise a `Q-NN` choice (`D-NN`) and check code claims?

## Step 8 — Description

Per [../../core/authoring-guide.md](../../core/authoring-guide.md): workspace name, situations (writing/reviewing requirements, planning, test design, naming in code), and team trigger words.

## Step 9 — Verify, record & report

Run [checklist.md](checklist.md) + [../../core/checklist-common.md](../../core/checklist-common.md); record provenance ([../../core/provenance.md](../../core/provenance.md)); report `OPEN` items, rule mappings, and trial results (`PASS` / `FAIL`).

## Update mode & Versioning

Existing `.agents/skills/domain-knowledge/` or workspace glossary: registered → sync ([../../core/sync-protocol.md](../../core/sync-protocol.md)); unregistered → adopt preserving existing terms, IDs, and confirmed rules verbatim. When changing this generator, follow [../../core/versioning.md](../../core/versioning.md).

## Resources

- [references/base-rules.md](references/base-rules.md) — Mandatory `DK1`–`DK9` rules, `PASS`/`FAIL` CLI gates, and `BLOCKER`/`MAJOR`/`MINOR` rubric
- [references/detection.md](references/detection.md) — Stack-agnostic discovery guide (`<src>`)
- [checklist.md](checklist.md) — Topic verification checks
