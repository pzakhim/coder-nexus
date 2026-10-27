# Plan and task contract

The single home of the **format** of `implementation-plan.md` and `phases/phase-NN-*.md`: plan-level sections, task fields, how a task check is judged, what is frozen at Gate 3 and how plan changes are logged. Planning writes these files; Code Writer, Code Reviewer and Test Runner read them. How to plan *well* (slicing, sizing, order) stays in [`implementation-planning`](../../implementation-planning/SKILL.md); how to *change* an approved plan is [`change-control`](../../change-control/SKILL.md). Other files point here instead of restating these rules.

## 1. Plan-level sections (`implementation-plan.md`)

| Section | Holds | Rule |
|---|---|---|
| `## Global constraints` | Rules every task implicitly includes, one line each, citing `BR-NN` / `D-NN` / foundation profile with the exact pinned value | Only rules that apply to more than one task; never a rule the sources do not contain. Reason: the source stays the one home of the fact |
| `## Review focus` | Up to five input classes or failure modes the ACs imply but no decisive check exercises, each naming its owning task | `None found after checking every AC and BR` when nothing qualifies; an empty section means skipped, not checked |
| `## AC coverage`, `## Phase order`, `## Checkpoints and shared files`, `## Test and visual strategy`, `## Gate 3 approval` | AC → phase mapping, linked phase files, shared-file order, real commands and targets, the user's approval | Validated by `validate_plan_slices` (`PLAN-V-002`); never rename or remove these headings |
| `## Plan change log` | Every amendment after Gate 3 (§5) | Always the last section; append-only |

`## Global constraints` and `## Review focus` sit above `## AC coverage`. The validator does not check them; `gate-review` `modes/plan.md` and the Code Reviewer do.

### `PHASE-00` readiness tick

`PHASE-00` (`phases/phase-00-prepare.md`) is done only when its tick reads one of:

| Accepted tick | Means |
|---|---|
| `[x] PREPARED / COMPLETED` | Every `[EXECUTE]` item ran and its evidence is recorded |
| `[x] PREPARED (INFO_READY)` | Only `[INFO_NOTE]` items; the information is linked and confirmed |
| `[x] PREPARED (NO_EXTERNAL_API)` | The item calls no external API, so there is nothing to prepare beyond the recorded reason |

Any other text, or an unticked box, means `PHASE-01` may not start. The Code Writer ticks it before its `PHASE-00` hand-off; the Code Reviewer only confirms the tick against the evidence and never edits plan documents.

## 2. Task fields (`phases/phase-NN-*.md` → `## Tasks`)

```markdown
- [ ] **Task X.Y**: <actionable title>
  - **Scope / Files**: `path/one`, `path/two` (create / modify)
  - **Reused Components**: entries from the design's reuse mapping, or `none`
  - **Consumes**: exact signatures from earlier tasks or existing code, or `none`
  - **Produces**: public symbols later tasks consume (name, parameters, return type), or `none`
  - **Acceptance Criteria**: `<exact check command>` (cwd: `<directory>`)
  - **Expected**: <the observable result of that check>
```

| Field | Rule | Reason |
|---|---|---|
| Scope / Files | Every file the task creates or modifies; nothing outside it is edited | Edits outside the list are unreviewed scope |
| Reused Components | Spelled as in `design.md`'s reuse mapping (`{{slot:architecture-design}}` where the stack defines one) | The Code Writer must not choose a different foundation locally |
| Consumes | Character-for-character equal to an earlier **Produces** line or to a symbol that exists in the code | The Code Writer sees one task at a time and must not guess a neighbour's names |
| Produces | Only symbols a later task or phase consumes | Anything else is an internal detail, not a contract |
| Acceptance Criteria | One runnable check (the stack's analyzer on the touched path, a named test, a request against a running target) plus its cwd. The heading word stays "Acceptance Criteria" | A check without a cwd cannot be re-run identically by the reviewer |
| Expected | What the check prints or shows when the task is right: exit code, test count or name, the exact error text a negative case must produce, the response status, the file that must exist | Without a stated result, "it ran" is mistaken for "it passed" |

Rules for **Expected**:

- It must be able to fail. "No errors" is valid only for a check that reports errors; "works" is never valid.
- For a test-first task (`{{slot:unit-testing}}`), state both runs: the red run and the reason it fails, then the green run.
- It comes from the approved documents (`AC-NN`, `BR-NN`, `D-NN`, design), never from what the current code happens to output.

## 3. Triage after every check

The Code Writer compares the real output with **Expected** and records one of:

| Triage | Means | Action |
|---|---|---|
| `MATCH` | The output is the Expected result | Record the evidence row, tick `- [x]`, re-read the plan, take the next task |
| `CODE_WRONG` | Correct code would produce Expected; this code does not | Fix through `{{slot:root-cause-debugging}}`; never tick on a partial match |
| `PLAN_WRONG` | Correct code cannot produce Expected (broken command, missing symbol, contradicts a `D-NN`) | Stop and raise a plan change request (`change-control`); the task stays unticked |

Never edit the check, the test or the **Expected** line to make the output match. Reason: a check bent to the code proves nothing, and only Planning may amend the plan.

## 4. Frozen and amendable after Gate 3

| Frozen (change only through the gate that approved it) | Amendable by Planning alone (`TASK_DETAIL`) |
|---|---|
| Goals `G-NN`, the AC → phase mapping, the phase list and each phase's outcome | The file list of a task, inside the same component |
| `## Global constraints`, `## Review focus` | A broken check command (same intent, same Expected meaning) |
| | A task's Acceptance Criteria or Expected brought into line with an unchanged approved source (the row cites the source) |
| Every `D-NN` in `codebase-notes.md` | Task order inside a phase, when no **Consumes** edge breaks |
| The approved `design.md` | Splitting one task into several with the same combined outcome |

A change to a frozen item is `DESIGN_CHANGE` (back to Gate 2, and Gate 3 for the re-derived plan) or `SCOPE_CHANGE` (back to Spec Writer and Gate 1). When in doubt, the higher class applies. Every amendment, including `TASK_DETAIL`, produces a new plan revision: review and test evidence for the affected tasks is invalid until re-run.

## 5. `## Plan change log`

| Date | Trigger (task, finding) | Class | What changed | Bad state avoided | Authority |
|---|---|---|---|---|---|
| 2026-01-31 | `PCR-01`, Task 2.3 check command | `TASK_DETAIL` | Task 2.3 Acceptance Criteria: cwd corrected to the service root | A check that could never run from the stated cwd | `TASK_DETAIL` (Planning, no approval needed); user informed at the `PHASE-02` checkpoint |

- At Gate 3 the table has one row: `None yet`. Never leave a template placeholder in it.
- Append-only: never edit or delete a row. A later correction is a new row that cites the earlier one.
- Before any amendment, Planning reads every row and keeps every earlier constraint. Reason: an amendment that silently undoes an earlier one reintroduces the bad state it avoided.
- **Authority** names what allowed the change: `TASK_DETAIL (Planning, no approval needed)`, or `User at Gate N` with the user's real response reference for a `DESIGN_CHANGE` / `SCOPE_CHANGE` row. An agent never records its own approval.
- Progress and results never go here; they go to `as-built.md` and the reports in [handoff-and-status](handoff-and-status.md).

## 6. Phase-free items

A small item without a plan keeps its tasks in `brief.md` → `## Tasks and verification`, using the same task fields and triage. Its frozen set is the approved brief; any change to it is a new approval, not a `TASK_DETAIL`.
