# Discovery of Plan Artifacts & Check Commands

Stack-neutral guide for finding how the workspace writes approved plans and which commands prove a task and a phase. Record each item as **found** (with path) or **missing**; the workspace's format and vocabulary win over anything proposed here.

---

## 1. Plan Artifacts (For `01-preconditions-and-preflight.md`)

### Known formats

| Format | Signals | Phase / task shape |
|---|---|---|
| **Work-items dossier** (Coder Nexus style) | `.superpowers/work-items/<slug>/vN/` with `brief.md`, `design.md`, `implementation-plan.md`, `phases/phase-NN-*.md`, `as-built.md`; a validator script | Phase files; tasks `- [ ] **Task X.Y**` with Scope / Files, Reused Components, Consumes, Produces, Acceptance Criteria, Expected |
| **Versioned feature docs** | `docs/features/<module>/<feature>/vN/` with requirements/design/plan | Phase files or sections; checkboxes |
| **Plain plan file** | `PLAN.md`, `plans/<slug>/plan.md`, `docs/plans/*.md` | `## Phase N` headings, `- [ ]` tasks |
| **Issue / PR checklists** | Issues with task lists, PR templates with checklists | Issue = phase, checklist item = task |
| **None** | No plan artifacts | Propose the plain plan file (lightest) |

```bash
ls -d .superpowers/work-items docs/features plans docs/plans 2>/dev/null
ls .agents/skills .claude/skills 2>/dev/null | rg -i "work|plan|implement|dev-team|feature"
rg -l "^- \[ \] \*\*Task" -g "*.md" . 2>/dev/null | head
```

### What to record

| Item | Example |
|---|---|
| Plan root | `.superpowers/work-items/<slug>/vN/` |
| Phase file pattern | `phases/phase-NN-<behavior>.md` |
| Task format and fields | `- [ ] **Task X.Y**` + Scope / Files, Consumes, Produces, check, expected result |
| Global constraints / review focus | Sections of the plan every task must honor (I15) |
| Gates before coding | Requirements, design, plan approved by the user |
| Preparation phase | `PHASE-00` or none |
| Dependency notation | `Depends on: PHASE-01` |
| Plan change process | Who answers a plan defect and with which words (e.g. `PCR-NN` → `AMENDED` / `ESCALATED`) |
| Tick line | What a ticked task records (revision, command, result) |
| Where results go | `as-built.md`, hand-off file, issue comment |
| Vocabulary | Statuses and evidence results (`PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`, `UNVERIFIED`), decision and hand-off IDs |
| Roles | Coordinator, Planner, Code Writer, Reviewer, Test Runner |

### Rules
- Map the workspace's words to `core/coder-skill-family.md` terms; do not rename them.
- Never create a dossier format for a workspace that does not need one.
- A task without file scope, check or expected result is a planning gap reported in `01`, not filled in by the Code Writer.

---

## 2. Check Commands (For `02-task-loop-and-checks.md` and `03-phase-end-and-handoff.md`)

Take commands from the workspace's own scripts first (task runner files, package scripts, CI steps, gates found in P2), then from the sibling skills (clean-code self-check, unit-testing focused command, verification). Confirm them at the gate; never list a tool the workspace does not have installed.

| Level | Purpose | Where to find it |
|---|---|---|
| **Task check** (I6) | Prove one task: analyzer on the changed files and the task's focused test | unit-testing skill's focused command; analyzer/linter config |
| **Phase suite** (I7) | Formatter (check mode), analyzer/linter, type checker, full tests, build | clean-code self-check gates; CI pipeline |
| **Architecture gate** | Import/boundary rules | clean-architecture skill; boundary test or lint config |
| **Visual check** (I8) | Approved targets and states on the approved device or browser | visual-quality skill; design references |

Each command records its working directory. Results are binary for tools (`exit 0` = `PASS`, otherwise `FAIL`).

### Evidence line

```
<command> (cwd <dir>) @ <revision> → PASS | FAIL | NOT_RUN | BLOCKED | UNVERIFIED (<short reason>)
```

- A command that was not run is `NOT_RUN`, never omitted.
- A command that cannot run (missing service, credentials, device) is `BLOCKED` with the reason.
- Visual checks name the target (screen or route, state, device or browser) and the revision.
