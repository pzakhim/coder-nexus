# Mode: execution
> Topic: Executing planned test cases in severity order on the reviewed revision and recording fresh observable evidence.

Run the plan's cases on the prepared environment, on the exact reviewed revision, and record what was observed.

## Preconditions

- The Code Review report is `APPROVED` for the same tree you are about to test. Otherwise stop: nothing to test yet.
- The environment record exists and names that revision ([environment.md](environment.md)).
- The browser, device or API tool the case needs is reachable. A missing tool makes the affected cases `BLOCKED`; never describe output you did not get.

## Order

1. Re-check the Reviewer's analyzer, test and visual evidence for the revision (read, do not trust blindly; rerun the cheapest command to confirm the tree).
2. Run the stack's checks from {{slot:verification}} that the plan lists (targeted integration / acceptance tests, affected regressions, build).
3. Run BLOCKER cases first, then MAJOR, then MINOR; guards and regression cases are part of the run, not optional.
4. Run visual cases with {{slot:visual-quality}}: same screen, state, viewport, data, role and theme as the approved `S-NN` reference. Open and inspect every captured image before judging it.

## Executing one case

- **As written.** Follow Given / When / Then; record any deviation; never soften or improvise an expectation.
- **Real path, then read back.** Use the real backend and storage; prove persistence by reading it again (reload, re-fetch, query through the public interface).
- **Produce states for real.** Empty, loading, error and populated states come from real conditions (empty seed, slow or failing provider stub, real error response), not from editing the code.
- **Per role.** Repeat permission cases with each role's account; include a direct call that bypasses the UI and expect the specified refusal.
- **Health after each flow.** Read logs, console and network output for errors the screen does not show.
- **Fresh evidence.** One evidence row per check, from this run, on this revision.

## Evidence

Store files under `vN/evidence/<phase-id>/<revision>/` with predictable names (`TC-NN-<step>.png`, `TC-NN-response.json`, `TC-NN.log`). Each case gets a row in the shared shape:

| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
|---|---|---|---|---|---|
| `TC-03` denies `viewer` delete | `<request or test command>` (`<cwd>`) | `<rev>` | `0` | `status 403, record still present on re-read` | `PASS` |

Rows from a stubbed provider add `stubbed: <provider>` in Key output. Redact tokens, cookies, passwords and personal data before saving any file; use test data only so screenshots stay clean.

## Expected vs observed triage (`FAIL-FAST` loop: `test_runner` ↔ `bug_fixer` ↔ `planning`)

Execute `E2E-01` → `E2E-02` → ... → `E2E-N` in `vN/test-plan.md` sequentially, one scenario at a time. Never edit, weaken, or skip any scenario in `test-plan.md`.

| Observation | Result | Next |
|---|---|---|
| Matches the expected result | `PASS` | Tick `- [x] **E2E-i**` with fresh evidence in `vN/test-plan.md` and proceed to `E2E-(i+1)` |
| Differs from the expected result | `FAIL` | Rerun once to rule out flakiness; if still `FAIL`, **STOP IMMEDIATELY (`FAIL-FAST`)**, write the defect (`FAILED_AT: E2E-i`, [reporting.md](reporting.md#defect-report)), and return `CHANGES_REQUESTED` so the coordinator invokes **`bug_fixer`** (`L1`/`L2` fix or `L3` `PCR-NN.md` escalation to **`planning`**) |
| Different outcomes on two runs | `FAIL`, labelled flaky with both outcomes | **STOP IMMEDIATELY (`FAIL-FAST`)**, report defect (`FAILED_AT: E2E-i`) for `bug_fixer`; never `PASS` |
| Tool, service, account, provider or reference missing | `BLOCKED` | Record owner and evidence, stop and return `BLOCKED` |
| State could not be produced, case skipped with a reason | `NOT_RUN` | Record why |
| Expected result looks wrong against another spec | Keep the result as observed | Question / `PLAN_CONFLICT` or `SCOPE_CHANGE` row to the coordinator for `planning`; never edit the expectation |

## Re-test (End-to-End from `E2E-01` to `E2E-N`)

After `bug_fixer` (and `planning` if `L3`, plus `code_reviewer` if `L2` or `L3`) commits a fix on a new revision: rebuild the environment record for the new revision, mark earlier evidence as superseded, and **re-run all scenarios in `vN/test-plan.md` sequentially from start to finish (`E2E-01` → `E2E-N`)** until 100% pass end-to-end.
