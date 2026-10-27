# 03 — Phase-End Verification, Hand-off & Review Rounds

> Scope: Five mandatory phase-end gates (`I7`–`I12`), revision-bound `writer-handoff.md` format (`I13`), hand-off statuses, and review round resolution.

---

## 1. Five Mandatory Phase-End Gates (`I7`–`I12`)

When every task in the phase file is ticked (`- [x]`), run these 5 gates in order before handing off:

| # | Gate | Skill / Slot | Mandatory Action |
|---|---|---|---|
| **1** | **Full Phase Suite (`I7`)** | `{{slot:verification}}` | Run the stack's full phase checks (formatter check, static analyzer, type checker, unit tests, architecture validator, and build as applicable). Task checks are narrow; the phase suite verifies cross-task interactions |
| **2** | **Visual Verification (`I8`)** | `{{slot:visual-quality}}` | For UI-impacting phases, run runtime visual verification across the approved targets and states |
| **3** | **Self Bug-Hunt (`I9`)** | `{{slot:bug-hunt}}` | Run a `quick`-effort bug hunt on the phase diff; grade findings per [handoff-and-status.md](../../work-item-contract/references/handoff-and-status.md) §9. Fix every `CONFIRMED` defect with a reproducing test first (`{{slot:unit-testing}}`) and re-run affected checks; carry `PLAUSIBLE` items under `Concerns` |
| **4** | **Targeted Simplicity Pass (`I12`)** | `{{slot:code-simplification}}` | Inspect changed code only; apply simplification **only** when a named smell (from its 4-lens catalog or `{{slot:clean-code}}`) is present. Re-run affected checks afterward and record the §9 `simplify:` line |
| **5** | **Evidence Audit (`I10`)** | [`evidence-standard`](../../evidence-standard/SKILL.md) | Verify every claim has a complete evidence row on the committed revision (`NOT_RUN`, `BLOCKED`, and `UNVERIFIED` are never `PASS`) |

> **Contract boundary (`I11`):** If any phase-end fix requires altering approved behavior, API contracts, architecture boundaries, dependencies, or mapped components, stop and route through [`change-control`](../../change-control/SKILL.md) (`PCR-NN`).

---

## 2. Revision-Bound Hand-off (`I13`)

1. **Commit first:** Stage and commit the phase's in-scope files (`git-preflight`), then re-run the phase verification checks on that clean commit so `REVIEW_REVISION` is a committed Git SHA (never `+dirty`).
2. **Write the hand-off artifact:** Create `evidence/<phase-id>/<REVIEW_REVISION>/writer-handoff.md` using the common header in [handoff-and-status.md](../../work-item-contract/references/handoff-and-status.md) §1 plus these fields:

```markdown
Status: READY_FOR_REVIEW | BLOCKED | NEEDS_CONTEXT
Phase: PHASE-NN (<phase file>)   Branch: <branch from git-preflight D-NN>
BASE_REVISION..REVIEW_REVISION: <base-sha>..<review-sha>
Pre-flight: <Consumes/Produces table from 01> | Pre-flight: no shared interfaces
Tasks: ticked <list>; unticked <list with reason>
Evidence:
| Claim | Command (+cwd) | Revision | Exit Code | Key Output | Result |
|---|---|---|---|---|---|
| <task or phase check> | `<cmd>` (cwd `<dir>`) | `<review-sha>` | 0 | <summary> | PASS |
bug-hunt: <handoff-and-status §9 bug-hunt summary line; CONFIRMED fixed with tests, PLAUSIBLE carried as Concerns>
simplify: <handoff-and-status §9 simplify summary line; skipped findings carried as Concerns>
PCR raised: <PCR-NN - class - answer (AMENDED / ESCALATED / open)> | none
Concerns: <list> | none                                                       (READY_FOR_REVIEW only)
Tried / needed: <files read, commands run> / <exact fact or access needed>    (NEEDS_CONTEXT only)
Blocker: <what is missing and who can unblock>                                (BLOCKED only)
Noticed but not touching: <path - observation> | none
```

### Hand-off Status Rules

| Status | When to Return |
|---|---|
| **`READY_FOR_REVIEW`** | Every task achieved `MATCH` and all phase-end checks ran on the committed `REVIEW_REVISION` |
| **`BLOCKED`** | A missing precondition, environment failure, missing approval, or open `PCR-NN` halts execution and cannot be resolved within task scope |
| **`NEEDS_CONTEXT`** | A specific external fact or access is missing (never use `NEEDS_CONTEXT` for a plan defect—plan defects use `PCR-NN` + `BLOCKED`) |

---

## 3. Review Resolution & Revision Invalidation

- **Review replies (`round N`):** When Code Reviewer returns `CHANGES_REQUESTED`, apply [`review-resolution`](../../review-resolution/SKILL.md). Every code fix creates a **new `REVIEW_REVISION`**, invalidates affected prior review/test/visual evidence, and writes a new `evidence/<phase-id>/<NEW_REVIEW_REVISION>/writer-handoff.md` containing `## Review reply (round N)` (using the reply vocabulary in [handoff-and-status.md](../../work-item-contract/references/handoff-and-status.md) §3).
- **Three-round escalation:** Three review rounds on the same phase without `APPROVED` must escalate via [`change-control`](../../change-control/SKILL.md) or the coordinator.
- **Plan stability:** Never rewrite `implementation-plan.md` to match as-built deviations; Docs Writer records final implementation outcomes in `as-built.md`.
