# Roadmap

The factory is a knowledge base the agent uses to write workspace-specific skills. Skills are named by **discipline**, not by role, because several roles share them; each role loads a **pack** (a list of skills). Generators are named `create-<skill>-skill`.

Every generator follows [core/workflow.md](../../src/skill_factory/library/core/workflow.md), writes `<workspace>/.agents/skills/<name>/`, supports the flat and branched (`shared/ + be/ + fe/`) layouts, and is versioned per [core/versioning.md](../../src/skill_factory/library/core/versioning.md), and is distributed with `skill-factory get` ([skill-factory.md](skill-factory.md)).

## Packs

| Pack | Role | Skills |
|---|---|---|
| **Engineering Pack** | Code Writer | clean-architecture · incremental-implementation · clean-code · unit-testing · code-simplification · bug-hunt (`quick`) · root-cause-debugging · database-migrations · secure-coding-standards |
| **Code Review Pack** | Code Reviewer | code-review · bug-hunt (`standard`/`deep`) · grades against clean-architecture, clean-code, unit-testing |
| **Application Security Pack** | Security | security-review · secure-coding-standards |
| **Quality Assurance Pack** | Quality Engineer (QA/QC) | quality-planning · quality-environment · quality-acceptance · quality-reporting · visual-quality (optional) |
| *Later:* Delivery Planning Pack | Planning, Spec | requirements-specification · implementation-planning · api-contract-design |

Each pack gets a `core/<pack>-skill-family.md` (ownership, vocabulary, who wins on conflict) when its first generator is built. Engineering uses [core/coder-skill-family.md](../../src/skill_factory/library/core/coder-skill-family.md).

## Status

Distribution: `skill-factory list | get` (CLI, `src/skill_factory/`). Next distribution steps: `skill-factory diff`, then an extension command.

| # | Generator | Skill | Pack | Status |
|---|---|---|---|---|
| 0 | `create-clean-architecture-skill` | `clean-architecture` | Engineering | Built (1.1.1) |
| 1 | `create-incremental-implementation-skill` | `incremental-implementation` | Engineering | Built (1.1.0) + Unreleased (patch, minor) |
| 2 | `create-clean-code-skill` | `clean-code` | Engineering | Built (1.0.0) |
| 3 | `create-unit-testing-skill` | `unit-testing` | Engineering | Built (2.0.0, renamed) |
| 4 | `create-code-simplification-skill` | `code-simplification` | Engineering | Built (1.0.0) |
| 5 | `create-bug-hunt-skill` | `bug-hunt` | Engineering, Code Review | Built (1.0.0) |
| 6 | `create-root-cause-debugging-skill` | `root-cause-debugging` | Engineering | Built (1.0.0) |
| 7 | `create-secure-coding-standards-skill` | `secure-coding-standards` | Engineering, Application Security | Built (1.0.0) |

None has been trial-run in a real workspace yet.

## Next — in this order

### Milestone A — Prove the Engineering Pack (before building more)

**A1. Trial run on erp-knowledge-platform** (already has matching skills → **adopt**; start with `skill-factory get -p coder`): run generators 0–5 one by one, record provenance, compare with/without skill (`core/trial-run.md`), fix the generators, release the batch. Why first: six generators are still unproven; finding a structural problem now is cheaper than repeating it in nine more.

### Milestone B — Complete the Engineering Pack

| # | Generator | Why | Base inputs |
|---|---|---|---|
| 6 ✅ | `create-root-cause-debugging-skill` | Red checks are where the Code Writer spends most time; reproduce → isolate → hypothesise → smallest fix → regression test; no fake fallbacks or test edits to go green | Coder Nexus `bug-hunt` verify step, workspace incident fixes |
| 7 ✅ | `create-secure-coding-standards-skill` | Write it safe the first time: input validation at trust boundaries, object-level authorization, injection, secrets/PII, data-scope isolation. Shared with the Security pack | erp RBAC/scope rules, bug-hunt dimension 5 |
| 8 | `create-database-migrations-skill` | Hard-to-undo changes: idempotency, locks, backfills, ordering, rollback (BE only) | erp `be-database-migration` |
| — | incremental-implementation minor | Add git hygiene (scoped commits, messages, no unrelated files) instead of a new skill; release with the Unreleased patch | — |

### Milestone C — Code Review Pack

| # | Generator | Why |
|---|---|---|
| 9 | `create-code-review-skill` | Review process: fixed revision, order of axes (bug-hunt first, then compliance), finding format, verdicts, rounds and escalation; grades with the Engineering skills |

### Milestone D — Application Security Pack

| # | Generator | Why |
|---|---|---|
| 10 | `create-security-review-skill` | Threat-focused review: authorization matrix, data scopes, injection, secrets, dependency CVEs, PII in logs. Takes over bug-hunt dimension 5 when the Security role exists |

### Milestone E — Quality Assurance Pack

| # | Generator | Why |
|---|---|---|
| 11 | `create-quality-planning-skill` | Test cases from approved specs with AC → test traceability; flags untestable AC right after the requirements gate |
| 12 | `create-quality-environment-skill` | Stack up, seed/cleanup, stubs for external providers (labelled in reports), never touch others' stacks |
| 13 | `create-quality-acceptance-skill` | Acceptance tests, branched: `fe/` drives a real browser (states, permissions, environment switch, console/network), `be/` drives the real API (403 matrix, persistence, side effects, workers) |
| 14 | `create-quality-reporting-skill` | Revision-bound evidence, PASS / FAIL / BLOCKED / NOT_RUN, defects to the coder with reproduction; never fixes code |
| 15 | `create-visual-quality-skill` *(optional)* | Compare UI with the approved design/mockups |

Each milestone ends with a trial run in a real workspace before the next starts.

### Later

- `create-<pack>-skills` orchestrators: one Context Card and one question round for a whole pack.
- Delivery Planning Pack.

## Open decisions

1. **Security:** a separate agent reviewing in parallel with the Reviewer, or a skill the Reviewer calls for sensitive code?
2. **Integration tests** (repositories on a real DB): written by the Code Writer (as in erp) or by the Quality Engineer?
3. **Browser tool for `quality-acceptance` fe/:** chrome-devtools MCP, Playwright, or Claude in Chrome.

## Decisions taken

1. **Two kinds in one product.** Fixed packs (extension sync, `.agents/plugins/coder-nexus/`) and Skill Factory (`skill-factory get`, `.agents/skills/`, owned by the workspace). Workspace skills override fixed skills of the same name or topic (Code Writer and Code Reviewer roles); generators never write into `.agents/plugins/coder-nexus/`.
2. Coder Nexus `plugins/core/skills/*` and `plugins/packs/*/skills/*` (read from this repo) are **read-only base inputs** (P1).
3. Trial runs use a real workspace (erp-knowledge-platform first).
4. Names: discipline-based skills grouped into role packs; existing generators keep their names except `create-unit-testing-skill` (renamed 2026-10-22).
