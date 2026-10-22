# Base rules (generic, every workspace)

Each rule goes into the generated skill with the workspace's locations, words and IDs **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| RP1 | **Revision-bound.** Every report names the tested revision, the plan version and the environment record (services, data, stubs, accounts by role). | A result without its revision and environment cannot be trusted or reproduced. | 01 |
| RP2 | **Per-case results with evidence links.** One row per case: ID, AC, level, result, evidence, defect. | Readers verify any line without re-running it. | 01 |
| RP3 | **AC coverage derived from cases.** An AC is `PASS` only if all its cases pass; any `FAIL` → `FAIL`; otherwise any `BLOCKED`/`NOT_RUN` → that status. | Coverage claimed per feature hides the failing criterion. | 02 |
| RP4 | **Verdict by criteria.** `ACCEPTED` only when every AC is `PASS`, all P1 cases pass and no open BLOCKER/HIGH defect remains; `CHANGES_REQUESTED` when defects block; `BLOCKED` when required evidence could not be produced. | Criteria make the verdict reproducible and non-negotiable. | 02 |
| RP5 | **Defects tracked.** ID, severity, case, status (open / fixed-awaiting-retest / verified / won't fix with the user's decision), reproduction link. | Untracked defects silently ship. | 03 |
| RP6 | **Limitations are explicit.** Stubbed providers, cases not run and why, environments or roles not covered, known flaky cases. | A clean report with hidden gaps is worse than an honest partial one. | 02 |
| RP7 | **Honest counting.** `NOT_RUN` and `BLOCKED` are never counted as passed; no rounding up ("almost all passed"); percentages show their denominator. | Counting is where reports most often mislead. | 02, SKILL |
| RP8 | **Evidence hygiene.** No secrets, tokens or personal data in screenshots, logs or response bodies (redact); files in the allowed locations. | Reports are shared more widely than test environments. | 04 |
| RP9 | **Right destination.** The report goes to the workspace's location and owner; posting it outside the workspace (chat, tracker, email) only with the user's authorisation. | Results can contain sensitive details. | 04 |
| RP10 | **Re-test history.** Each round with its revision and the cases rerun; earlier failures stay visible. | A history shows whether fixes held. | 03 |
| RP11 | **Verdict first.** Top of the report: verdict, counts, blockers, limitations; details after. | Most readers read only the top. | 01 |
| RP12 | **No edited expectations.** The report never changes a case's expected result; deviations from the plan are listed as deviations. | Moving the goalposts in the report hides defects. | 02 |

**Never "not adopted":** RP1, RP3, RP4, RP7, RP8.
