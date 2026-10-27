# Mode: Plan — Gate 3 Pre-Gate Verification (`planning` in `dev-team`)

Reviews `implementation-plan.md` and every linked `phases/phase-NN-*.md` against the approved `requirements.md`, `design.md`, and `codebase-notes.md`. Pass 1 (`validate_plan_slices` = `PASS`, including `PLAN-V-001`…`PLAN-V-010`) must be clean before starting Pass 2. Findings use `GR-P-NN`.

The approved spec and design are binding authority; when the plan disagrees with them, the plan is wrong unless the user confirms a change through a `Q-NN`.

---

## Pass 2 — Plan Checklist (`P1`–`P5`)

### P1. Interface Pre-Flight Table (`Produces` ↔ `Consumes`)
Construct one row for every pair of tasks (within a phase or across phases) that share a file or symbol:

| Task A | Task B | Shared File / Symbol | A Produces | B Consumes | Match? | Finding |
|---|---|---|---|---|---|---|
| `1.2` | `2.1` | `OrderRepository.fetchPage` | `(page, size) -> Page<Order>` | `fetchPage(cursor)` | No — parameter mismatch | `GR-P-01` (`BLOCKER`) |

- Verify exact names, parameter/return types, nullability, error types, JSON keys, and route contracts. Any mismatch is **`BLOCKER`**.
- Any consumer task ordered before its producer task (within a phase or in an earlier phase) is **`BLOCKER`**.
- Any task whose internal instructions contradict themselves (e.g., test vs implementation signature, creating a file a later task assumes already existed) is **`BLOCKER`**.

### P2. Complete `AC-NN`, `BR-NN`, and `NEW COMPONENT` Delivery
- Every `AC-NN` mapped to a phase must have both a task that builds the behavior and a decisive check that would fail without it. Listing an `AC-NN` ID in the phase header without a building task and check is **`BLOCKER`**.
- Every behavioral `BR-NN`, every `NEW COMPONENT` (`C-NN`) in `design.md` → `## UI/UX mapping`, and every divergence rule (`D-NN`) must be implemented by an explicit task (**`BLOCKER`** if missing).

### P3. Plan Proportion & Anti-Pattern Check
- A plan more than ~3× the combined length of `requirements.md` + `design.md`, or tasks that paste full function bodies instead of concise direction + `Produces` signatures, is **`MAJOR`**.
- Any task that instructs `code_writer` to write something `code_reviewer` would reject — a tautological test, duplicated logic, or a hardcoded fallback masking errors — is **`BLOCKER`**.

### P4. Global Constraints & Value Alignment
Every constant or constraint repeated in `implementation-plan.md` or `phases/*.md` (limits, page sizes, timeouts, roles, data scopes, messages, API fields/status codes) must match `requirements.md`, `codebase-notes.md` (`## 4`, `## 5`), and `design.md` exactly (**`BLOCKER`** on mismatch).

### P5. Falsifiable Task Checks & `## Review focus`
- Every task must specify an **Acceptance Criteria** command with its `cwd` and a falsifiable **Expected** sourced from approved documents ([`plan-and-task-contract.md`](../../work-item-contract/references/plan-and-task-contract.md) §2). Missing `cwd`, unfalsifiable `Expected` (*"works"*, *"no errors"*), or `Expected` copied blindly from unverified current output is **`BLOCKER`**.
- `## Review focus` must either list concrete risk items naming their owning task or state `None found after checking every AC and BR` (**`BLOCKER`** if blank).

---

## P6. Pass 3 — Cold-Reader Subagent Check (Reader Plays `code_writer`)

After Pass 1 (`PASS`) and Pass 2 (`0 BLOCKER`, `0 MAJOR`), spawn one fresh read-only subagent with this exact prompt:

```text
You are the Code Writer of this team. You have been handed the implementation
plan of a work item and must next execute it: PHASE-00 first, then each phase,
task by task, from top to bottom. You cannot talk to the author, and you have
no chat history.

Read the documents under review:
- {{vN_path}}/implementation-plan.md
- {{vN_path}}/phases/   (every phase file)

Already approved Gate 1 & Gate 2 context (do not question unless the plan contradicts it):
- {{vN_path}}/requirements.md
- {{vN_path}}/codebase-notes.md
- {{vN_path}}/design.md

You may open files these documents cite by path, read-only, only to verify that
a cited file, symbol, or command exists. Do not use the codebase to fill gaps
left by the plan. Do not write or modify any file and do not run builds or tests.

Walk the plan as if executing it task by task. Report only the questions you
would still need answered to finish every task without guessing: missing files
or symbols, a task depending on something not yet produced, a check command
that cannot decide PASS or FAIL, or an AC/goal no phase delivers.
For each question provide:
1. The question
2. Where it comes from (phase, task, AC-NN, PHASE-00 item)
3. Why the answer changes what you do
4. What you would guess if forced
Rank by importance, at most 10.

Skip local variable naming and wording nits.
If nothing important is left, reply: nothing important left
```

Sort every returned question per [`SKILL.md` §5](../SKILL.md#5-pass-3--fresh-cold-reader-subagent-check) (`Answered already`, `Minor — Agent's call`, or `User's call — OPEN Q-NN`).
