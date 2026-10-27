---
name: create-unit-testing-skill
description: Write a workspace's own unit-testing skill from the skill-factory knowledge base - test-first discipline, per-layer test matrix (Pass/Default, Fail, Empty/Edge cases), test tree and naming, doubles policy (Real > Fake > Stub > Mock) at port boundaries, deterministic fixtures, assertion quality, focused/full test commands, red-to-green evidence rows, and unified review severities - for any stack. Use whenever the user wants to set up, standardize, or update how the coder agent writes developer unit tests in a workspace, or says things like "tạo skill unit test", "chuẩn viết test", "test cho coder", "quy chuẩn unit test", even if they do not say "skill". Detects the test runner, fixtures, and layout, gets them confirmed, writes .agents/skills/unit-testing/, then trial-runs it on real code.
argument-hint: "[stack/framework] [test framework]"
---

# Create Unit Testing Skill

Goal: produce `<workspace>/.agents/skills/unit-testing/` — how the Code Writer proves its changes with **developer unit tests** in this workspace: when a failing test comes first, what to test per layer, where tests live, which doubles are allowed at port boundaries, and what counts as red-to-green evidence. Integration, end-to-end, and visual checks belong to the Test Runner role and are referenced as boundaries.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — `unit-testing` decides how behavior is proven; `clean-architecture` decides which layer is tested at which port boundary; `clean-code` rules also apply to test code.

## Step 1 — Context Card (+ test setup)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect using `references/deriving-the-model.md`:

| Field | Where to look |
|---|---|
| Existing test skills/docs | `.agents/skills/*test*`, `docs/*test*`, `CONTRIBUTING.md`, `AGENTS.md` |
| Runner & configuration | Project manifests, test runner config files, installed mocking/assertion/async plugins |
| Test layout | Unit vs integration test roots, how test file paths mirror source paths, file naming pattern |
| Shared fixtures / builders / fakes | Shared test setup files, data builders/factories, existing in-memory fakes of ports |
| Real test names | 10–20 existing test names to infer the workspace's naming convention |
| Automated gates | CI test commands, randomized test order plugins, coverage reporting commands |
| Base inputs (read-only) | `references/base-rules.md` and `references/deriving-the-model.md` |

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule `U1`–`U14`: enforced by an automated gate (cite it), adopted, adapted to the workspace's contracts, or "not adopted" with a stated reason. `U2`, `U4`, `U5`, `U6`, and `U12` are mandatory and never "not adopted".

## Step 3 — Propose

Using `references/deriving-the-model.md`:
- **Test-First & Per-Layer Matrix:** When a failing test must come first, what each architectural layer tests, which port boundary is doubled, required Pass/Default + Fail + Empty/Edge cases, and what is left to integration tests.
- **Layout & Naming:** The workspace's real test tree (drawn with `├──`/`└──`) and naming convention (`EXTEND` follows existing workspace conventions; `INIT` uses stack defaults).
- **Doubles & Quality Policy:** `Real > Fake > Stub > Mock` hierarchy, fakes for workspace-owned ports, mocks only at external edges, assertion rules, and determinism helpers.
- **Execution & Evidence:** Focused (single test/file) and full unit commands (`PASS` / `FAIL`), how to prove a new test actually ran, red-to-green evidence rows, and unified review grading (`BLOCKER` / `MAJOR` / `MINOR`).

## Step 4 — Gate (user confirms)

One confirmation round where possible: (1) test-first order and per-layer test matrix, (2) test directory tree and naming, (3) doubles/fixtures policy, (4) CLI test commands (`PASS` / `FAIL`) and review grading (`BLOCKER` / `MAJOR` / `MINOR`).

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Keep `SKILL.md` concise (< 120 lines) and group `references/` into 3 cohesive topic files:

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | CLI test gates (`PASS`/`FAIL`), test-first matrix, mandatory rules `U1`–`U14`, and routing table |
| `references/01-test-matrix-and-structure.md` | `templates/references/01-test-matrix-and-structure.md.tmpl` | **Mandatory** | `EXTEND` vs `INIT` rule, per-layer Pass/Fail/Empty matrix, `├──`/`└──` test tree, and test naming |
| `references/02-doubles-fixtures-and-quality.md` | `templates/references/02-doubles-fixtures-and-quality.md.tmpl` | **Mandatory** | `Real > Fake > Stub > Mock` policy, concrete code templates, AAA, independent expectations, right-reason red, and determinism |
| `references/03-execution-boundaries-and-review.md` | `templates/references/03-execution-boundaries-and-review.md.tmpl` | **Mandatory** | Focused/full CLI commands, proving tests ran, red-to-green evidence rows, unit test boundaries, and `BLOCKER`/`MAJOR`/`MINOR` review grading |
| `profiles/<profile>/*.md` (optional, pack skills) | — | **Suggested** | Profile-specific testing contracts synced into `references/` and linked at `<!-- {{profile_references}} -->` |

Writing rules: keep each template's purpose, give every rule its rationale, use real paths/fixtures/commands, draw directory trees with `├──`/`└──`, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Unit Tests
   Developer unit tests follow `.agents/skills/unit-testing/SKILL.md`.
   ```
2. Offer to link it from the coder and reviewer role files (P3).
3. If `incremental-implementation` exists, verify its task-level check step uses this skill's focused command.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:
- Plan unit tests for a real use case/service: which cases (Pass/Default, each Fail, Empty/Edge), which doubles, which file path.
- Plan unit tests for a data mapper/schema and a presentation state holder or controller.
- Plan the red-to-green regression test for a recently fixed bug.

Compare: Pass/Fail/Empty cases present, doubles at port boundaries (no mocked subject, no mocked authorization/DB), path and name per `01`, focused command named, "new test ran" check included.

## Step 8 — Description

Per the authoring guide: workspace name; situations (writing or changing code that needs tests, fixing a bug or review finding, reviewing tests); team trigger words. Should not trigger for integration, E2E, or visual verification requests.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations from the suggested shape, rules adapted, and trial results.

## Update mode

Existing `.agents/skills/unit-testing/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep existing fixture conventions, evidence locations, check ownership).

## Changing this generator

Bump `VERSION` and add a `CHANGELOG.md` entry with **Affects** and **Migration** (`~/.claude/skill-factory/core/versioning.md`).

## Resources

- [Base Rules](references/base-rules.md) — `U1`–`U14` mandatory rules, binary `PASS`/`FAIL` gates, and unified `BLOCKER`/`MAJOR`/`MINOR` review scale
- [Deriving the Model](references/deriving-the-model.md) — discovering test runners, per-layer cases, doubles, and commands from any workspace
- `templates/` — `SKILL.md.tmpl` and `references/01–03.md.tmpl`
- [Checklist](checklist.md) — topic verification checks
