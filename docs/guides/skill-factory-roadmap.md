# Roadmap

The factory is a knowledge base the agent uses to write workspace-specific skills. Skills are named by **discipline**, not by role, because several roles share them; each role loads a **pack** (a list of skills). Generators are named `create-<skill>-skill`.

Every generator follows [core/workflow.md](../../src/skill_factory/library/core/workflow.md), writes `<workspace>/.agents/skills/<name>/`, supports the flat and branched (`shared/ + be/ + fe/`) layouts, and is versioned per [core/versioning.md](../../src/skill_factory/library/core/versioning.md), and is distributed with `skill-factory get` ([skill-factory.md](skill-factory.md)).

## Packs

| Pack | Role | Skills |
|---|---|---|
| **Engineering Pack** | Code Writer | clean-architecture · incremental-implementation · clean-code · unit-testing · code-simplification · bug-hunt (`quick`) · root-cause-debugging · database-migrations · secure-coding-standards · git-workflow |
| **Code Review Pack** (`-p reviewer`) | Code Reviewer | code-review · bug-hunt (`standard`/`deep`) · grades against clean-architecture, clean-code, unit-testing, secure-coding-standards, database-migrations ([reviewer-skill-family](../../src/skill_factory/library/core/reviewer-skill-family.md)) |
| **Application Security Pack** (`-p security`) | Security | security-review · secure-coding-standards ([security-skill-family](../../src/skill_factory/library/core/security-skill-family.md)) |
| **Quality Assurance Pack** (`-p quality`) | Quality Engineer (QA/QC) | quality-planning · quality-environment · quality-acceptance · quality-reporting · visual-quality (optional) |
| **Spec & Planning Pack** (`-p planning`) | Spec Writer, Planning | domain-knowledge · requirements-specification · change-impact-analysis · implementation-planning · api-contract-design ([planning-skill-family](../../src/skill_factory/library/core/planning-skill-family.md)) |

Each pack gets a `core/<pack>-skill-family.md` (ownership, vocabulary, who wins on conflict) when its first generator is built. Engineering uses [core/coder-skill-family.md](../../src/skill_factory/library/core/coder-skill-family.md).

## Status

All generators were reset to **1.0.0** on 2026-10-22 (first release; no workspace had synced an earlier version).

Distribution: `skill-factory list | get` (CLI, `src/skill_factory/`). Next distribution steps: `skill-factory diff`, then an extension command.

| # | Generator | Skill | Pack | Status |
|---|---|---|---|---|
| 0 | `create-clean-architecture-skill` | `clean-architecture` | Engineering | Built (1.0.0) |
| 1 | `create-incremental-implementation-skill` | `incremental-implementation` | Engineering | Built (1.0.0) |
| 2 | `create-clean-code-skill` | `clean-code` | Engineering | Built (1.0.0) |
| 3 | `create-unit-testing-skill` | `unit-testing` | Engineering | Built (1.0.0) |
| 4 | `create-code-simplification-skill` | `code-simplification` | Engineering | Built (1.0.0) |
| 5 | `create-bug-hunt-skill` | `bug-hunt` | Engineering, Code Review | Built (1.0.0) |
| 6 | `create-root-cause-debugging-skill` | `root-cause-debugging` | Engineering | Built (1.0.0) |
| 7 | `create-secure-coding-standards-skill` | `secure-coding-standards` | Engineering, Application Security | Built (1.0.0) |
| 8 | `create-database-migrations-skill` | `database-migrations` | Engineering (backend) | Built (1.0.0) |
| 9 | `create-code-review-skill` | `code-review` | Code Review | Built (1.0.0) |
| 10 | `create-security-review-skill` | `security-review` | Application Security, Code Review | Built (1.0.0) |
| 11 | `create-quality-planning-skill` | `quality-planning` | Quality Assurance | Built (1.0.0) |
| 12 | `create-quality-environment-skill` | `quality-environment` | Quality Assurance | Built (1.0.0) |
| 13 | `create-quality-acceptance-skill` | `quality-acceptance` | Quality Assurance | Built (1.0.0) |
| 14 | `create-quality-reporting-skill` | `quality-reporting` | Quality Assurance | Built (1.0.0) |
| 15 | `create-visual-quality-skill` | `visual-quality` | Quality Assurance (optional) | Built (1.0.0) |
| 16 | `create-git-workflow-skill` | `git-workflow` | Engineering, Code Review | Built (1.0.0); runtime steps in the fixed core skill `git-preflight` |
| 17 | `create-domain-knowledge-skill` | `domain-knowledge` | Spec & Planning, Quality | Built (1.0.0) |
| 18 | `create-requirements-specification-skill` | `requirements-specification` | Spec & Planning | Built (1.0.0) |
| 19 | `create-change-impact-analysis-skill` | `change-impact-analysis` | Spec & Planning | Built (1.0.0) |
| 20 | `create-implementation-planning-skill` | `implementation-planning` | Spec & Planning | Built (1.0.0) |
| 21 | `create-api-contract-design-skill` | `api-contract-design` | Spec & Planning, Engineering, Code Review | Built (1.0.0) |

None has been trial-run in a real workspace yet.

## Next — in this order

### Milestone A — Prove the Engineering Pack (before building more)

**A1. Trial run on erp-knowledge-platform** (already has matching skills → **adopt**; start with `skill-factory get -p coder`): run generators 0–5 one by one, record provenance, compare with/without skill (`core/trial-run.md`), fix the generators, release the batch. Why first: six generators are still unproven; finding a structural problem now is cheaper than repeating it in nine more.

### Milestone B — Complete the Engineering Pack (generators 6–8 built; git-hygiene minor pending)

| # | Generator | Why | Base inputs |
|---|---|---|---|
| 6 ✅ | `create-root-cause-debugging-skill` | Red checks are where the Code Writer spends most time; reproduce → isolate → hypothesise → smallest fix → regression test; no fake fallbacks or test edits to go green | Coder Nexus `bug-hunt` verify step, workspace incident fixes |
| 7 ✅ | `create-secure-coding-standards-skill` | Write it safe the first time: input validation at trust boundaries, object-level authorization, injection, secrets/PII, data-scope isolation. Shared with the Security pack | erp RBAC/scope rules, bug-hunt dimension 5 |
| 8 ✅ | `create-database-migrations-skill` | Hard-to-undo changes: idempotency, locks, backfills, ordering, rollback (BE only) | erp `be-database-migration` |
| — | incremental-implementation minor | Add git hygiene (scoped commits, messages, no unrelated files) instead of a new skill; release with the Unreleased patch | — |

### Milestone C — Code Review Pack (generator 9 built)

| # | Generator | Why |
|---|---|---|
| 9 ✅ | `create-code-review-skill` | Review process: fixed revision, order of axes (bug-hunt first, then compliance), finding format, verdicts, rounds and escalation; grades with the Engineering skills |

### Milestone D — Application Security Pack (generator 10 built)

| # | Generator | Why |
|---|---|---|
| 10 ✅ | `create-security-review-skill` | Threat-focused review: authorization matrix, data scopes, injection, secrets, dependency CVEs, PII in logs. Takes over bug-hunt dimension 5 when the Security role exists |

### Milestone E — Quality Assurance Pack (generators 11–15 built)

| # | Generator | Why |
|---|---|---|
| 11 ✅ | `create-quality-planning-skill` | Test cases from approved specs with AC → test traceability; flags untestable AC right after the requirements gate |
| 12 ✅ | `create-quality-environment-skill` | Stack up, seed/cleanup, stubs for external providers (labelled in reports), never touch others' stacks |
| 13 ✅ | `create-quality-acceptance-skill` | Acceptance tests, branched: `fe/` drives a real browser (states, permissions, environment switch, console/network), `be/` drives the real API (403 matrix, persistence, side effects, workers) |
| 14 ✅ | `create-quality-reporting-skill` | Revision-bound evidence, PASS / FAIL / BLOCKED / NOT_RUN, defects to the coder with reproduction; never fixes code |
| 15 ✅ | `create-visual-quality-skill` *(optional)* | Compare UI with the approved design/mockups |

Each milestone ends with a trial run in a real workspace before the next starts.

### Later

- `create-<pack>-skills` orchestrators: one Context Card and one question round for a whole pack.

## Reference sources

**Integrated on 2026-10-22** into the Spec & Planning generators (`requirements-specification`, `domain-knowledge`, `change-impact-analysis`, `implementation-planning`, `api-contract-design`) and the fixed core skills `grilling`, `requirements-elicitation`, `solution-options`, `cold-reader-check`, `gate-review`, `architecture-decision-records`, `work-item-contract`, `implementation-planning` and both `architecture-design` packs. Each one cites its sources, pinned to a commit, in `references/sources.md`, with the ideas not adopted and why. The git-workflow rows below are not integrated yet.

Ideas and structure only; rewrite them in the factory's Q-NN → D-NN and gate vocabulary, never copy text, and cite the source in the generator's `references/`. Stars checked on 2026-10-22.

| Source | Stars | Use for | Ideas to take |
|---|---|---|---|
| [github/spec-kit](https://github.com/github/spec-kit) (`templates/spec-template.md`, `plan-template.md`, `constitution-template.md`) | 142k | requirements-specification, implementation-planning | Prioritized independently testable user stories (P1/P2/P3), `FR-NNN`, `[NEEDS CLARIFICATION]` markers, measurable technology-agnostic success criteria, Key Entities, a per-project constitution checked before planning, task IDs `T001` with exact paths, complexity tracking |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (`spec-driven-development`, `planning-and-task-breakdown`, `api-and-interface-design`, `documentation-and-adrs`, `git-workflow-and-versioning`, `interview-me`) | 109k | spec, planning, api-contract, git-workflow | Gated phases with a scope check and capability map, Boundaries section, dependency graph and vertical slices with checkpoints, task sizing, ADRs; git: atomic commits, worktrees for parallel agents, semver, human changelog (defaults to trunk-based; gitflow teams adapt) |
| [obra/superpowers](https://github.com/obra/superpowers) (`writing-plans`, `finishing-a-development-branch`, `using-git-worktrees`, `brainstorming`) | 303k | implementation-planning, git-workflow | Scope check, right-sized tasks with file structure, global constraints, review focus, self-review before handoff; finishing a branch: verify tests, detect base, offer merge / PR / keep, then clean up |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | 73k | requirements-specification, change-impact-analysis | Spec deltas for changes to existing behavior (not yet read in detail) |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | 54k | spec, planning | PM / Architect roles, PRD → architecture → stories (idea level only) |
| [nvie/gitflow](https://github.com/nvie/gitflow) | 27k | git-workflow | The original Git Flow model and commands |
| [Conventional Commits](https://github.com/conventional-commits/conventionalcommits.org), [commitlint](https://github.com/conventional-changelog/commitlint), [commitizen](https://github.com/commitizen/cz-cli), [semantic-release](https://github.com/semantic-release/semantic-release), [release-please](https://github.com/googleapis/release-please) | 9k–24k | git-workflow | Commit format `type(scope): …`; detect these tools in a workspace and use them as the real checks |
| [netresearch/git-workflow-skill](https://github.com/netresearch/git-workflow-skill) | <100 | git-workflow | Git Flow / GitHub Flow / trunk-based presets in one skill (low adoption; reference only) |

## Open decisions

None at the moment.

## Decisions taken

0. **Browser and API tools are not fixed:** `create-quality-acceptance-skill` detects what the workspace has (chrome-devtools MCP, Playwright, Claude in Chrome, built-in browser; API tests, Postman/Newman, `.http`, curl) and the user chooses at the gate.
0. **Integration-test owner is chosen per workspace** at the quality-planning gate (default: Code Writer; the Quality Engineer owns API acceptance and UI end-to-end) — `core/quality-skill-family.md`.
0. **Security mode is chosen per workspace** at the security-review gate: a separate Security role (owns bug-hunt dimension 5) or the Code Reviewer runs it for triggered changes.
1. **Two kinds in one product.** Fixed packs (extension sync, `.agents/plugins/coder-nexus/`) and Skill Factory (`skill-factory get`, `.agents/skills/`, owned by the workspace). Workspace skills override fixed skills of the same name or topic (Code Writer and Code Reviewer roles); generators never write into `.agents/plugins/coder-nexus/`.
2. Coder Nexus `plugins/core/skills/*` and `plugins/packs/*/skills/*` (read from this repo) are **read-only base inputs** (P1).
3. Trial runs use a real workspace (erp-knowledge-platform first).
4. Names: discipline-based skills grouped into role packs; existing generators keep their names except `create-unit-testing-skill` (renamed 2026-10-22).
