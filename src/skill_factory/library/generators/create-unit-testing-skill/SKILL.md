---
name: create-unit-testing-skill
description: Write a workspace's own unit-testing skill from the skill-factory knowledge base - what to test per layer, required happy/negative/edge cases, test location and naming, fakes vs mocks at port boundaries, fixtures and determinism, assertion quality, commands and evidence - for any stack and for fullstack repos with backend and frontend branches. Use whenever the user wants to set up, standardize or update how the coder agent writes developer unit tests in a workspace, or says things like "tạo skill unit test", "chuẩn viết test", "test cho coder", "quy chuẩn unit test", even if they do not say "skill". Detects the test framework, fixtures and layout, gets them confirmed, writes .agents/skills/unit-testing/, then trial-runs it on real code.
argument-hint: "[stack/framework] [test framework]"
---

# Create Unit Testing Skill

Goal: produce `<workspace>/.agents/skills/unit-testing/` — how the Code Writer proves its changes with **developer unit tests** in this workspace: what to test, where, with which doubles, and what counts as evidence. Integration, end-to-end and visual checks belong to the Test Runner role (a later skill family) and are only referenced here.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — unit-test decides how behavior is proven; clean-architecture decides which layer is tested at which boundary; clean-code rules also apply to test code.

## Step 1 — Context Card (+ test setup)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing test skills/docs | `.agents/skills/*test*`, `docs/*test*`, `CONTRIBUTING.md` |
| Framework & config | `pyproject.toml` (`pytest`, `pytest-asyncio`), `package.json` scripts and devDependencies (`vitest`, `jest`, `node --test`), `pubspec.yaml` (`flutter_test`, `mocktail`, `bloc_test`), `go.mod` |
| Test layout | `tests/unit`, `tests/integration`, `test/`, co-located `*.test.*`; how paths mirror source |
| Shared fixtures / factories / fakes | `conftest.py`, `tests/helpers`, `test/fixtures`, existing in-memory fakes of ports |
| Real test names | 10–20 test names to infer the naming convention |
| Gates | CI test steps, coverage thresholds, architecture tests |
| Base input (read-only) | Coder Nexus `plugins/packs/<stack>/skills/unit-test/SKILL.md` (and templates) from the repo |

## Step 2 — Map the base rules

Read `references/base-rules.md` and `references/cases-by-layer.md`. For each rule U1–U14: enforced by a gate (cite it), adopted, adapted to the workspace, or "not adopted" with a reason. U2, U4, U5, U6, U12 are never "not adopted".

## Step 3 — Propose

- **Per layer** (from the workspace's clean-architecture skill if it exists, otherwise its real folders): what is unit-tested, which boundary is doubled, required case types, what is left to integration tests.
- **Layout & naming** from the real test tree; resolve inconsistencies with one convention and list drift.
- **Doubles policy:** fakes for ports owned by the workspace, mocks only at external boundaries, the library in use (`unittest.mock`, `mocktail`, `vi.fn`…); never a second framework.
- **Commands:** focused (one file/test) and full; how to confirm a new test actually ran (`references/tooling-by-stack.md`).

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) per-layer test matrix and required cases, (2) location and naming, (3) doubles/fixtures policy, (4) commands, coverage gate (if any) and TDD mode (when the plan asks / always / never).

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–06`; branched: `be/01–05`, `fe/01–05`, `shared/06`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | Rule table + the per-change loop on one screen |
| `references/01-what-to-test.md` | `be/01-…`, `fe/01-…` | `templates/branch/01-what-to-test.md.tmpl` | **Mandatory** | Per-layer matrix with required happy/negative/edge cases — stops happy-path-only suites |
| `references/02-location-and-naming.md` | `be/02-…`, `fe/02-…` | `templates/branch/02-location-and-naming.md.tmpl` | **Mandatory** | Tests nobody can find are not run or maintained |
| `references/03-doubles-and-fixtures.md` | `be/03-…`, `fe/03-…` | `templates/branch/03-doubles-and-fixtures.md.tmpl` | **Mandatory** | Mocking the wrong thing makes green tests prove nothing |
| `references/04-test-quality.md` | `be/04-…`, `fe/04-…` | `templates/branch/04-test-quality.md.tmpl` | Suggested | AAA, determinism, assertion strength, regressions; may merge into 01 |
| `references/05-running-and-evidence.md` | `be/05-…`, `fe/05-…` | `templates/branch/05-running-and-evidence.md.tmpl` | **Mandatory** | Real commands and "the new test ran" — otherwise results are not evidence |
| `references/06-test-boundaries.md` | `shared/06-…` | `templates/shared/06-test-boundaries.md.tmpl` | Suggested | What unit tests cannot prove and who covers it; may merge into `SKILL.md` |

Writing rules: keep each template's purpose, give every rule its reason, real paths/fixtures/commands only, rules enforced by a gate cite it, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end. Short code snippets in the workspace's real framework are welcome where they show the pattern (mark them as shape if not copied from real tests).

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Unit tests
   Developer unit tests follow `.agents/skills/unit-testing/SKILL.md`.
   ```
2. Offer to link it from the coder and reviewer role files (P3).
3. If `incremental-implementation` exists, check its task-level check (02-C / 06) uses this skill's focused command.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Plan tests for a real use case/service: which cases (happy, each failure, edges), which doubles, which file.
- Plan tests for a real pure FE util or hook, and for a real data mapper.
- Plan the regression test for a bug fixed recently (from git log).

Compare: negative and edge cases present, doubles at the right boundary (no mocked subject, no mocked authorization), location/name per 02, focused command named, "test ran" check included.

## Step 8 — Description

Per the authoring guide: workspace name; situations (writing or changing code that needs tests, fixing a bug, reviewing tests); team trigger words. Should not trigger for E2E/visual verification requests — those belong to the Test Runner skills.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations from the suggested shape, rules adapted/not adopted, drift found, trial results.

## Update mode

Existing `.agents/skills/unit-testing/` (or a legacy `.agents/skills/unit-test/`, or workspace test skills such as `be-unit-testing`): registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep existing fixtures conventions, evidence locations, check ownership).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — U1–U14 with reasons, default severity, where each goes
- `references/cases-by-layer.md` — required cases per layer and stack
- `references/tooling-by-stack.md` — frameworks, doubles, layout and commands per stack
- `templates/` — `SKILL.md.tmpl`, `branch/01–05`, `shared/06` (suggested shapes)
- `checklist.md` — topic checks
