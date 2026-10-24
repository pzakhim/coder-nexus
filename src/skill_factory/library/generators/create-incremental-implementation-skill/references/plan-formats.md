# Detecting plan artifacts

Find how the workspace writes approved plans before proposing anything. Record each item as found (path) or missing.

## Known formats

| Format | Signals | Phase / task shape |
|---|---|---|
| **Work-items dossier** (Coder Nexus style) | `.superpowers/work-items/<slug>/vN/` with `brief.md`, `design.md`, `implementation-plan.md`, `phases/phase-XX-*.md`, `as-built.md`; a `work-item(s)` skill; a validator script | `phases/phase-XX-<behavior>.md`, tasks `- [ ] **Task X.Y**` with Scope/Files, Reused Components, Produces, AC |
| **Versioned feature docs** | `docs/features/<module>/<feature>/vN/` with requirements/design/plan | Phase files or sections; checkboxes |
| **Plain plan file** | `PLAN.md`, `plans/<slug>/plan.md`, `docs/plans/*.md` | `## Phase N` headings, `- [ ]` tasks |
| **Issue / PR checklists** | GitHub/Jira issues with task lists, PR templates with checklists | Issue = phase, checklist item = task |
| **None** | No plan artifacts | Propose the plain plan file (lightest) |

```bash
ls -d .superpowers/work-items docs/features plans docs/plans 2>/dev/null
ls .agents/skills .claude/skills 2>/dev/null | rg -i "work|plan|implement|dev-team|feature"
rg -l "^- \[ \] \*\*Task" -g "*.md" . 2>/dev/null | rg -v node_modules | head
```

## What to record

| Item | Example |
|---|---|
| Plan root | `.superpowers/work-items/<slug>/vN/` |
| Phase file pattern | `phases/phase-XX-<behavior>.md` |
| Task format | `- [ ] **Task X.Y**` + Scope / Files, Produces, AC |
| Gates before coding | Requirements, design, plan approved by the user |
| Preparation phase | `PHASE-00` (mock server, test data) or none |
| Dependency notation | `Depends on: PHASE-01` |
| Where results go | `as-built.md` by the coordinator; handoff `H-NN` |
| Vocabulary | `PASSED`, `NOT_RUN`, `BLOCKED`, `UNVERIFIED`, `D-NN`, `H-NN` |
| Validators | `python3 .agents/skills/work-item-management/scripts/validate_dossier.py <dossier> --gate <g>` |
| Roles | Coordinator, Code Writer, Reviewer, Test Runner |

## Rules

- The workspace's format and vocabulary win; map them to `core/coder-skill-family.md` terms, do not rename them.
- Never create a dossier format for a workspace that does not need one.
- A task without file scope or check is reported as a planning gap in the generated `01` ("ask the planner"), not filled in by the Code Writer.
