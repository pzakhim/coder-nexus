# Mode: reporting

Write one acceptance report per run at `vN/evidence/final_qa/<revision>/acceptance-report.md` (or `evidence/<phase-id>/<revision>/` for a phase the plan marks for its own run), verdict first. The evidence-row and status vocabulary are the shared ones in `work-item-contract` → [handoff-and-status.md](../../work-item-contract/references/handoff-and-status.md).

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
| Case | Covers | Priority | Level | Result | Evidence | Defect |
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

## Defect report

One block per failure, sent to the coordinator for the Code Writer:

```
DEF-NN  case TC-NN  covers AC-NN  owning phase PHASE-NN  severity BLOCKER|MAJOR|MINOR  CONFIRMED|PLAUSIBLE
Revision:   <rev>   Environment: <record link>   Role: <role name>
Reproduce:  <minimal steps or request, from a clean state>
Expected:   <from the plan, unchanged>
Actual:     <observed>
Evidence:   <files and evidence rows>
Area:       <suspected screen / endpoint / module, if obvious — never a code fix>
```

Severity and confidence follow the defect scale in [handoff-and-status.md](../../work-item-contract/references/handoff-and-status.md) §9. For a test defect, `CONFIRMED` means reproduced; `PLAUSIBLE` means seen once or dependent on something not visible, with what would confirm it.

Defect status: `open` → `fixed-awaiting-retest` (new reviewed revision) → `verified` (re-test `PASS`), or `wont-fix` only with the user's recorded `D-NN`.

## Hand-off

- To the coordinator: verdict, counts, report path, defect list, plan and spec conflict rows, open questions. The coordinator routes defects to the Code Writer under the owning phase, writes `PCR-NN` from conflict rows, and takes the verdict to the user.
- To Docs Writer (via the coordinator): the report path for `as-built.md`.
- Never post results to Huly, chat or email; never present the run as finished while any case lacks a result.

## Hygiene

No secrets, tokens, cookies or personal data in the report, logs or images. Images and responses stay under `vN/evidence/`, never under `.agents/`.
