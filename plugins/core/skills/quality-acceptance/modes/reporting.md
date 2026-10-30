# Mode: reporting
> Topic: Writing the acceptance report, per-AC results, defect blocks, and hand-off routing for the coordinator and Docs Writer.

Write one acceptance report per run at `vN/evidence/final_qa/<revision>/acceptance-report.md` (or `evidence/<phase-id>/<revision>/` for a phase the plan marks for its own run), verdict first. The evidence-row and status vocabulary are the shared ones in `work-item-contract` (`references/handoff-and-status.md` §7).

## Report shape

```markdown
# Acceptance report — <slug> vN — <phase-id> — round <n>

Verdict: ACCEPTED | CHANGES_REQUESTED | BLOCKED — <one-line reason>
Counts: <p> PASS · <f> FAIL · <b> BLOCKED · <r> NOT_RUN (of <total> cases)
AC: <a>/<total> PASS — not passing: <AC-NN list>
Open defects: <n> BLOCKER · <n> MAJOR · <n> MINOR
Limitations: <stubbed providers, cases not run and why, roles not covered, flaky cases>

## Environment record
## AC coverage
| AC-NN | Owning phase | Cases | Result | Evidence |
## Results
Case table: Case ID | AC ID | Layer | Severity (BLOCKER|MAJOR|MINOR) | Status | Evidence (command or screenshot) | Notes.
## Evidence
| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
## Defects
| ID | Severity | Confidence | Case | Status | Summary |
## Plan and spec conflicts
| Plan or spec line | Finding | Evidence | Class (`PLAN_CONFLICT` / `SCOPE_CHANGE`) | Options |
## Deviations from the plan
## Re-test history
| Round | Revision | Cases rerun | Result |
```

## Counting rules

- An AC result is derived from its cases (SKILL "Result words"), never claimed per feature. The AC coverage table is the SKILL "Per-AC results" table.
- `BLOCKED`, `NOT_RUN` and `UNVERIFIED` are never counted as `PASS`; percentages always show their denominator; no rounding up.
- A stubbed `PASS` is listed under Limitations with the cases that still need the live provider.
- The verdict follows the SKILL "Feature verdict" table mechanically.

## Environment record

Copy the fields from [environment.md](environment.md#environment-record). Accounts appear by role name only.

## Defect report (`FAIL-FAST` handoff to `bug_fixer` ↔ `planning`)

One block per failure (`FAILED_AT: E2E-i`), sent to the coordinator for **`bug_fixer`** (which fixes `L1`/`L2` root causes in production code or raises `plan-changes/PCR-NN.md` to **`planning`** when the failure is an `L3` architectural/design/plan flaw):

```
DEF-NN  scenario E2E-i / case TC-NN  covers AC-NN  owning phase PHASE-NN  severity BLOCKER|MAJOR|MINOR  CONFIRMED|PLAUSIBLE
Revision:   <rev>   Environment: <record link>   Role: <role name>   Failed at: E2E-i (FAIL-FAST)
Reproduce:  <minimal steps or request, from a clean state>
Expected:   <from test-plan.md / requirements.md, unchanged>
Actual:     <observed>
Evidence:   <files and evidence rows>
Area:       <suspected screen / endpoint / module, if obvious — never a code fix>
```

Severity and confidence follow the defect scale in `work-item-contract` (`references/handoff-and-status.md` §9). For a test defect, `CONFIRMED` means reproduced; `PLAUSIBLE` means seen once or dependent on something not visible, with what would confirm it.

Defect status: `open` → `fixed-awaiting-retest` (new revision from `bug_fixer`, reviewed by `code_reviewer` when `L2`/`L3`) → `verified` (full `E2E-01..E2E-N` re-test `PASS`), or `wont-fix` only with the user's recorded `D-NN`.

## Hand-off

- To the coordinator: verdict (`ACCEPTED`, `CHANGES_REQUESTED` with `FAILED_AT: E2E-i`, or `BLOCKED`), counts, report path, defect list, plan and spec conflict rows, open questions. On `CHANGES_REQUESTED`, the coordinator immediately invokes **`bug_fixer`** (Mode C: `L1` → `READY_FOR_TEST` → `test_runner`; `L2` → `READY_FOR_REVIEW` → `code_reviewer` → `test_runner`; `L3` → `PCR-NN.md` (`ESCALATED`) → **`planning`**) and then re-runs `test_runner` from `E2E-01` through `E2E-N`.
- To Docs Writer (via the coordinator): in `final_qa` when the verdict is `ACCEPTED`, the Coordinator dispatches `docs_writer` once with the report path to record `vN/as-built.md` (`RECORDED`).
- Never post results to Huly, chat or email; never present the run as finished while any case lacks a result.

## Hygiene

No secrets, tokens, cookies or personal data in the report, logs or images. Images and responses stay under `vN/evidence/`, never under `.agents/`.
