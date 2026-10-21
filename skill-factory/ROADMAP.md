# Roadmap

## Scope

The factory is a knowledge base the agent uses to write workspace-specific skills. It will hold many kinds of skills over time; the first goal is the **delivery agent system**, role by role:

| Order | Role | Skills (generators) | Status |
|---|---|---|---|
| 1 | **Code Writer** | clean-architecture, incremental-implementation, clean-code, unit-test, code-simplification, bug-hunt | **Current focus** (below) |
| 2 | Code Reviewer | review rubric, bug-hunt (review effort), architecture/clean-code review | Later |
| 3 | Test Runner | verification, integration tests, visual verification | Later |
| 4 | Planning | implementation planning, task breakdown | Later |
| 5 | Spec / Brainstorm | brainstorming, requirements specification | Later |

Each role gets its own `core/<role>-skill-family.md` (ownership + vocabulary) when its first generator is built.

---

# Code Writer skills

Each generator follows [core/workflow.md](core/workflow.md), writes `<workspace>/.agents/skills/<name>/`, supports the flat and branched layouts, and is versioned and synced like `create-clean-architecture-skill`. Rules every coder skill shares live in [core/coder-skill-family.md](core/coder-skill-family.md); topic knowledge that is the same for every workspace lives in the generator; only workspace facts go into the generated skill.

## Phases

| Phase | Generator | Generated skill | Status |
|---|---|---|---|
| 0 | `create-clean-architecture-skill` | `clean-architecture` | Built (1.1.1), trial in a manual workspace pending |
| 1 | `create-incremental-implementation-skill` | `incremental-implementation` | Built (1.1.0), trial in a manual workspace pending |
| 2 | `create-clean-code-skill` | `clean-code` | Built (1.0.0), trial in a manual workspace pending |
| 3 | `create-unit-test-skill` | `unit-test` | Planned |
| 4 | `create-code-simplification-skill` | `code-simplification` | Planned |
| 5 | `create-bug-hunt-skill` | `bug-hunt` | Planned |

Each phase ends with: generator `VERSION 1.0.0` + `CHANGELOG.md`, symlink in `~/.claude/skills/`, a trial run in a manual workspace, and the ROADMAP status updated.

## Phase 2 — `create-clean-code-skill`
- **Gate item:** naming table per stack + size thresholds + error/logging policy.
- **Generated content:** naming (files, classes, functions, variables, domain glossary) · size limits · errors & logging · types, constants, comments · dead/debug code · self-check (grep, linters, gates) · review severities (P1/P2/P3).
- **Base inputs:** Coder Nexus `plugins/core/skills/clean-code`, existing workspace `clean-code` skills, linter configs.

## Phase 3 — `create-unit-test-skill`
- **Gate item:** test layout (location, naming) + tooling + fake/mock policy.
- **Generated content:** what to test per layer (mapped to clean-architecture) · location & naming · AAA structure · fakes vs mocks · fixtures, factories, determinism · edge-case checklist · commands, coverage gate, TDD mode.
- **Base inputs:** Coder Nexus pack slot `<stack>-unit-test`, workspace `be-unit-testing` / `fe-testing-and-verification`.

## Phase 4 — `create-code-simplification-skill`
- **Gate item:** smell → technique catalog + stop criteria.
- **Generated content:** when/scope (diff only, after green tests) · smell catalog · behavior safety · stop criteria · report format.
- **Base inputs:** Coder Nexus `code-simplification`, `ponytail`, workspace no-wrapper rules.

## Phase 5 — `create-bug-hunt-skill`
- **Gate item:** effort levels + finding format + confirmation rule.
- **Generated content:** when to run (self-check at phase end, review) · effort levels · bug classes per stack · how a finding is confirmed (reproduction or failing test) · finding format and severity · fix loop.
- **Base inputs:** Coder Nexus `plugins/core/skills/bug-hunt`, workspace `bug-hunt` skills.

## Later
- `create-coder-skills` orchestrator: run phases 1–5 with one Context Card and one round of shared questions.
- `create-secure-coding-skill`, `create-integration-test-skill`.

## Decisions
1. **Manual workspaces only.** The factory generates, adopts and syncs skills only in workspaces whose agent setup is maintained by hand. A workspace synced by Coder Nexus (`.agents/plugins/coder-nexus/`, e.g. `AIFactory/examples/*`) gets its skills from the extension; changes for it belong in the Coder Nexus plugin sources. Every generator stops at Step 0 for such a workspace.
2. Coder Nexus `plugins/core/skills/*` (read from this repo) remain a **read-only base input** (P1) for the generators.
3. Trial runs for each phase use a manual workspace (e.g. a copy of a real project without Coder Nexus), not `AIFactory/examples`.
