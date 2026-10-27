# 02 — Plan Sections, Ordered Task Structure & Re-Grounding Loop

> Topic: Plan-level sections (`Global constraints`, `Review focus`, `Plan change log`), single-writer task breakdown, task right-sizing and risk-first ordering, no-transcribed-code rule, and the mandatory task-by-task re-grounding loop.

## 1. Plan-Level Sections (`implementation-plan.md`)

Author `implementation-plan.md` from `work-item-contract` → `templates/implementation-plan.md.tpl`. Keep every validated heading (`## AC coverage`, `## Phase order`, `## Checkpoints and shared files`, `## Test and visual strategy`, `## Gate 3 approval`; `PLAN-V-002`) plus the three contract sections defined in `work-item-contract` → `references/plan-and-task-contract.md` §1, §4, §5:

### `## Global constraints` (above `## AC coverage`)
Rules every task implicitly obeys so no task repeats or forgets them:

| Rule | Why |
|---|---|
| One line per constraint citing its source (`BR-NN`, `D-NN`, foundation profile, `{{slot:clean-architecture}}`) | The source remains the single home of the fact; the line is a pointer |
| State the exact value pinned by the source (limit, timeout, status code, copy text, version floor) | Paraphrased values drift; pinned values are verifiable |
| Include only rules that apply to more than one task | A single-task rule belongs inside that task |
| Never invent a rule not present in the approved sources | New rules are scope (`requirements.md` at Gate 1) or architecture (`design.md` at Gate 2) |

### `## Review focus` (above `## AC coverage`)
Up to five input classes or failure modes that `requirements.md` implies but no `AC-NN` decisive check exercises directly (e.g., empty list after applying a filter, duplicate submit, boundary value at a `BR-NN` limit, slow response, revoked permission):
- Write one line per risk: the input/condition, the expected behavior per an existing `BR-NN` / `AC-NN` / `D-NN`, and the **owning task ID** whose check verifies it.
- If the expected behavior is not specified in any approved source, do not guess — queue an `OPEN` `Q-NN` in `codebase-notes.md`.
- Write `None found after checking every AC and BR` when nothing qualifies. Leaving the section blank is a `BLOCKER` in `gate-review` (`modes/plan.md` `P5`).
- `code_reviewer` deliberately checks every `## Review focus` item during phase review.

### `## Plan change log` (last section of `implementation-plan.md`)
- Initialized at Gate 3 with a single row: `| <CreatedDate> | None yet | - | - | - | - |`.
- Append-only after Gate 3 per `work-item-contract` → `references/plan-and-task-contract.md` §5 and `change-control`.

---

## 2. Ordered Single-Writer Task Breakdown (`## Tasks`)

Inside each phase file (`phases/phase-NN-*.md`), break `## Tasks` into an ordered list of discrete micro-tasks executed sequentially from top to bottom by a **single `code_writer`** (e.g., Domain $\to$ Data $\to$ State $\to$ Screen/Components & Route/DI $\to$ Developer Unit Tests):
- **Never** split tasks into `[PARALLEL]` / `[SEQUENTIAL]` tracks or `Join points`.
- Every task (`- [ ] **Task X.Y**: <Actionable Title>`) MUST include the 6 mandatory task fields defined in `work-item-contract` → `references/plan-and-task-contract.md` §2 (do not restate or vary the field names):
  1. **Scope / Files**: Every file the task creates or modifies; edits outside this list are out-of-scope.
  2. **Reused Components**: Exact entries from `design.md`'s reuse/foundation mapping table, or `none`.
  3. **Consumes**: Exact signatures from earlier tasks or existing code (character-for-character match with an earlier **Produces** line), or `none`.
  4. **Produces**: Public symbols (name, parameters, return type) that later tasks or phases consume, or `none`.
  5. **Acceptance Criteria**: One runnable check command and its explicit `cwd` (`<exact check command>` (cwd: `<directory>`)).
  6. **Expected**: Falsifiable observable output sourced from approved documents (exit code, test name/count, exact error text, HTTP status, or generated artifact path — never *"works"* or unverified current output).

---

## 3. Task Right-Sizing, Risk-First Ordering & `Expand → Migrate → Contract`

### Right-Sizing Tasks
A task is the smallest unit that has its own falsifiable check and that a reviewer could reject while accepting its neighbor:
- **Fold setup into the deliverable**: Fold configuration, registration, and boilerplate into the task whose deliverable needs them. A setup-only task with nothing verifiable cannot fail its **Acceptance Criteria**.
- **Split independent failure points**: Split a task when one part could be wrong while the other is right.
- **One behavior per phase**: If a phase delivers more than one user-observable behavior, split it into separate vertical phases.

### Ordering Rules

| Rule | What to Do | Why |
|---|---|---|
| **Highest risk first** | Immediately after `PHASE-00`, schedule the behavior with the highest uncertainty (unproven integration, hardest `AC-NN`, new foundation widget) as `PHASE-01`'s walking skeleton | Discovering a broken assumption in the final phase forces rework across all prior phases |
| **Prefactor first** | When existing code must be reshaped before adding behavior, place the behavior-preserving refactor as the first task(s) inside the phase that needs it, verified by existing tests staying green | Mixing structural refactoring and new behavior in one task hides which change broke a test; prefactor is never a standalone phase |
| **Dependencies only backwards** | A phase may depend only on earlier phases (`PLAN-V-009-DEPENDENCY`); a task may depend only on earlier tasks | A single `code_writer` executes strictly top to bottom |

### Exception: `Expand → Migrate → Contract` (Within Owning Repo Only)
When a storage schema or public contract with live consumers inside the **same repository** must change, a single cut would break existing callers. Split the change across three steps:
1. **Expand**: Add the new field, column, endpoint, or format alongside the old one (backward compatible) in the first phase that needs it.
2. **Migrate**: Move callers and data to the new path in the same or a subsequent phase.
3. **Contract**: Remove the deprecated path only after every consumer has migrated (in the final phase, or deferred to a later `vN` recorded as a `D-NN`).

Never combine **Expand** and **Contract** in the same task. This is the only case where a phase may include work that is not itself a new user behavior (the **Contract** step). The cross-repo prohibition in `01-readiness-and-phase-slicing.md` §3 still applies: never mutate another repository.

---

## 4. No Transcribed Code

A plan records architectural and contract decisions that `code_writer` cannot infer alone — it never writes the program inside the plan:

| A task gives | A task never gives |
|---|---|
| Target file path and class/function name | Full function, method, or widget bodies already determined by signature and test |
| Exact signature: symbol name, parameters, return type | Vague placeholders (*"TBD"*, *"handle edge cases"*, *"add validation as needed"*) |
| Exact values pinned by `requirements.md` / `design.md` (limits, status codes, copy keys, routes) | A type or symbol that neither exists in the codebase nor appears in an earlier **Produces** |
| Named test file/case and the exact assertion it checks | Paraphrased approximations of pinned spec values |

Code blocks are allowed only for a non-obvious algorithm that signature + test do not determine, or exact literal copy fixed by the spec. A plan exceeding ~3× the combined length of `requirements.md` + `design.md` is flagged as **`MAJOR`** in `gate-review` (`modes/plan.md` `P3`).

---

## 5. Mandatory Task-by-Task Plan Re-Grounding Loop & Commit Checkpoints

### Anti-Bulk Coding Re-Grounding Loop (`incremental-implementation`)
Tasks must be structured so `code_writer` executes them one by one using the strict re-grounding loop defined in `work-item-contract` → `references/plan-and-task-contract.md` §3:
1. Confirm all preceding tasks in `phases/phase-NN-*.md` are ticked `- [x]`.
2. Implement only the current task's **Scope / Files** and run its **Acceptance Criteria** command from the stated `cwd`.
3. Triage the real output against **Expected**:
   - `MATCH`: Record the evidence row for `writer-handoff.md` (`evidence/<phase-id>/<REVIEW_REVISION>/writer-handoff.md`), return to `phases/phase-NN-*.md` to tick `- [x]`, and **re-read the phase plan and next task specification** before writing any code for the next task.
   - `CODE_WRONG`: Diagnose and fix via `{{slot:root-cause-debugging}}`; never tick `- [x]` on a partial match.
   - `PLAN_WRONG`: Stop immediately and file a plan change request (`plan-changes/PCR-NN.md`) via `change-control`; never alter the task check or **Expected** line to match broken output.
4. Executing multiple tasks in a single unverified pass without returning to re-read and tick `phases/phase-NN-*.md` between tasks is prohibited.

### Branch & Phase Commit Checkpoints (`git-preflight`)
- Copy the confirmed branch decision (`D-NN`: work branch, base branch, merge targets) recorded by `git-preflight` into `implementation-plan.md` → `## Checkpoints and shared files`.
- For a production hotfix (`hotfix/*`), include explicit tasks/notes for bringing the fix back into active `release/*` and `develop`.
- Each completed phase is committed on the work branch before handing off `READY_FOR_REVIEW` so `code_reviewer` inspects an exact commit hash (`git rev-parse HEAD`).
- Never plan merges into `main` / `develop` / `release/*`, git tags (`v*`), or production deployments as automated agent tasks; list them only as user-approved commands.
