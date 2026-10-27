# 02 — Task Loop, Triage & Tick Format

> Scope: Step-by-step A–E task execution loop (`I4`–`I6`), `MATCH` / `CODE_WRONG` / `PLAN_WRONG` triage (`I16`), phase-file tick format, hard implementation rules (`I14`), and session resume protocol (`I17`).

---

## 1. The Per-Task Loop (`A` → `E` — `I4`, `I5`, `I6`)

Execute tasks strictly top to bottom. **Never implement two tasks in one pass.**

| Step | Action | Why It Matters |
|---|---|---|
| **A. Read & Ground** | Re-open the phase file; select the first unticked task; confirm all earlier tasks are ticked (`- [x]`); note `Scope / Files`, `Reused Components`, `Consumes`, `Produces`, `Acceptance Criteria` (command + cwd), and `Expected` | Memory drifts across tasks; re-reading reloads exact paths and contracts |
| **B. Code in Scope** | Edit **only** files listed in `Scope / Files`. Apply `{{slot:clean-architecture}}`, `{{slot:clean-code}}`, and `{{slot:secure-coding-standards}}`. Write the failing unit test first where `{{slot:unit-testing}}` requires it | Editing files outside `Scope / Files` introduces unreviewed design drift |
| **C. Run Check** | Run the task's `Acceptance Criteria` command in its specified working directory (`cwd`) and read the complete output | Only an executed command whose output you inspected counts as evidence (`evidence-standard`) |
| **D. Triage** | Compare the actual command output against the task's `Expected` result using the Triage Matrix (§2) | Silent deviation from `Expected` bypasses the approved plan |
| **E. Tick & Re-read** | Record `- [x]` on the task in the phase file using the exact Tick Line Format (§3), then re-read the phase file before starting the next task | The phase-file tick is the persistent ledger across sessions |

---

## 2. Check Triage Matrix (`I16`)

| Outcome | Meaning | Required Action |
|---|---|---|
| **`MATCH`** | Actual command output matches `Expected` | Tick the task (`- [x]`) and proceed to the next task |
| **`CODE_WRONG`** | The plan is valid, but the implementation has a bug or lint/test failure | Apply `{{slot:root-cause-debugging}}`, fix the root cause inside `Scope / Files`, and re-run Step C. **Never** hardcode or patch output merely to mimic `Expected` |
| **`PLAN_WRONG`** | `Expected`, a consumed signature, `Scope / Files`, or the check command itself is impossible or contradicts reality | Leave the task **unticked** (`- [ ]`), raise a `PCR-NN` via [`change-control`](../../change-control/SKILL.md), and return `BLOCKED` naming the `PCR-NN`. Resume only after `AMENDED` |

---

## 3. Phase-File Tick Line Format

When a task achieves `MATCH`, update its checkbox line in the phase file using this exact format:

```markdown
- [x] **Task 2.3**: <title> - rev <short-sha>[+dirty] - `<command>` (cwd `<dir>`) - exit 0 - MATCH
```

- **`rev`:** Write `<HEAD short-sha>+dirty` when ticking an uncommitted intermediate task. Before returning `READY_FOR_REVIEW`, commit the phase and re-run phase-end checks on the clean commit so `REVIEW_REVISION` in `writer-handoff.md` is never `+dirty`.
- **Single-source ledger:** Ticking task lines is the **only** edit Code Writer makes to plan/phase files. Every ticked task also receives a full evidence row in `writer-handoff.md`.
- **Amended tasks:** After Planning answers a `PCR-NN` with `AMENDED`, tick against the amended task text and cite the `## Plan change log` entry.

---

## 4. Seven Hard Rules for Every Task (`I5`, `I14`)

1. **No bulk coding, no context drift:** One task → one check → one tick → re-read.
2. **No bypassing mapped components:** If a component mapped in `design.md` does not fit, classify as `PLAN_WRONG` (`PCR-NN`)—never invent a local substitute widget or service.
3. **No dependency construction in entry points:** Screens, route handlers, and controllers receive dependencies through the approved DI wiring (`{{slot:clean-architecture}}`).
4. **Never weaken tests:** Never delete assertions, loosen expected values, or add `skip` annotations to turn a failing check green (`{{slot:unit-testing}}`).
5. **No fake success (`I14`):** Never fabricate business data, mock fallbacks in production code, or silent empty defaults to hide a missing dependency or parse failure.
6. **Keep the tree buildable:** After every tick, the project must compile and earlier task checks must still pass.
7. **Noticed but not touching:** Record any unrelated defect or cleanup outside `Scope / Files` under `Noticed but not touching` in the hand-off—never fold it into the current diff.

---

## 5. Resuming Across Sessions (`I17`)

When resuming in a new session or after context compaction:
1. Treat the phase file's `- [x]` ticks and `git log` / `git status` as the authoritative record—never rely on conversational memory.
2. Resume at the **first unticked task (`- [ ]`)**.
3. If the working tree changed since the last ticked task, re-run that predecessor task's check once to confirm the baseline is still `MATCH` before coding.
