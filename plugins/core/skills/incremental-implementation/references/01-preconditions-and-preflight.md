# 01 — Preconditions & Pre-Flight Before Task 1

> Scope: Mandatory readiness checks (`I1`–`I3`), `PHASE-00 [EXECUTE]` rules, authoritative sources of truth (`I14`), and the Consumes / Produces interface pre-flight (`I15`).

---

## 1. Preconditions Before Writing Any Code (`I1`, `I2`, `I3`)

Stop immediately and return `BLOCKED` if any precondition below is missing. Code built on an unapproved or unverified baseline will be rejected at review:

| Precondition | Where to Verify | Action if Missing |
|---|---|---|
| **Gate 1, 2, 3 Approvals** cover this `vN` (or approved `brief.md` for a phase-free item) | `implementation-plan.md` approval references (`work-item-contract`) | Stop and return `BLOCKED` |
| **`PHASE-00` Readiness Tick** carries an accepted tick (`[x] PREPARED / COMPLETED`, `[x] PREPARED (INFO_READY)`, or `[x] PREPARED (NO_EXTERNAL_API)`) and every phase in `Depends on` has passed | `phases/phase-00-prepare.md`, `implementation-plan.md` ([plan-and-task-contract.md](../../work-item-contract/references/plan-and-task-contract.md)) | Stop and return `BLOCKED` |
| **Active Git Branch** (`git branch --show-current`) matches the branch recorded in the `git-preflight` `D-NN` decision | `codebase-notes.md` | Switch to the approved branch or return `BLOCKED` |
| **Concrete Task Fields** (`Scope / Files`, `Acceptance Criteria` command + cwd, and `Expected`) exist for every task in the phase | `phases/phase-NN-*.md` | Raise a `PCR-NN` via [`change-control`](../../change-control/SKILL.md) and return `BLOCKED` (never guess missing fields) |

### When Assigned `PHASE-00 [EXECUTE]` Itself
- Execute `PHASE-00` tasks using the exact same A–E task loop ([02 — Task Loop & Checks](02-task-loop-and-checks.md)).
- Tick `[x] PREPARED / COMPLETED` in both `phases/phase-00-prepare.md` and `implementation-plan.md` before handing off; the Reviewer confirms that tick before `PHASE-01+` unlocks.
- Stack-specific preparation steps (e.g., Mockoon mock environment, fixture servers, smoke checks) follow the Code Writer stack profile and `{{slot:verification}}`.

---

## 2. Authoritative Sources of Truth (`I14`)

- Read Huly task details and baseline repository facts exclusively from `codebase-notes.md`.
- Read API contracts, schemas, and trigger rules from `design.md` (following plugin-root `shared_contracts/api_handshake_protocol.md`).
- **Never** re-query Huly during implementation or fabricate business records, fallback stubs, or hardcoded responses when a source is missing (`I14`).

---

## 3. Consumes / Produces Pre-Flight Before Task 1 (`I15`)

Before starting Task 1:
1. **Read `## Global constraints` and `## Review focus`** in `implementation-plan.md`. Global constraints bind every task; Review focus lists the exact edge cases and inputs the Code Reviewer will probe, so plan guards and unit tests for them upfront.
2. **Build the Consumes / Produces Table** in your working notes (and copy it into `writer-handoff.md` at phase end). Create one row per interface edge between tasks in the phase, or between a task and existing repository code:

| Consumer Task | Consumes (as stated in the plan) | Producer (task or existing `path:symbol`) | Produces (real signature verified in code) | Finding |
|---|---|---|---|---|
| Task 2.3 | `loadOrders(ownerId) -> list of Order` | existing `orders/repository:loadOrders` | `loadOrders(ownerId, page) -> Page of Order` | Mismatch: extra `page`, different return → raise `PCR-01` |
| Task 2.4 | `OrderSummary` from Task 2.2 | Task 2.2 | `OrderSummary` (planned) | OK |

3. **Verify existing producers in source:** For every existing producer, locate it with `rg -n "<symbol>" <path>` and open the file to inspect the real signature—never trust the plan's prose summary alone.
4. **Also flag internal task contradictions:** Add a row if a task lists a file as both newly created and pre-existing, runs a check outside its `Scope / Files`, or contradicts a `## Global constraints` rule.
5. **Stop on any mismatch:** If any row shows a mismatch, missing producer, or impossible check command, raise a `PCR-NN` via [`change-control`](../../change-control/SKILL.md) before writing code and return `BLOCKED` naming the `PCR-NN`. Resume only after Planning responds with `AMENDED` (`TASK_DETAIL`) or `ESCALATED`.
6. **Always record the result:** Even when all signatures match, include the table in `writer-handoff.md` (or write `Pre-flight: no shared interfaces` when tasks share no interfaces).
