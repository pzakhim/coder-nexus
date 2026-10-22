# Base rules (generic, every workspace)

Generalised from Coder Nexus `plugins/core/agents/test_runner.md` and a real workspace's interactive end-to-end practice. Each rule goes into the generated skill with the workspace's tools, URLs, roles and evidence paths **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| A1 | **Approved plan, reviewed revision, prepared environment.** Run only after the code review approved this revision; use the approved plan's cases; environment per quality-environment. | Testing an unreviewed or different revision proves nothing about what ships. | 01 |
| A2 | **Read-only.** Never edit application code or tests; defects go to the Code Writer with a reproduction. | A tester who fixes code stops being independent. | 01, SKILL |
| A3 | **Execute cases as written.** Follow the steps and expected results; note any deviation; never improvise or soften an expectation. | Improvised tests cannot be compared across runs. | 02 |
| A4 | **Real paths and persistence.** Use the real backend and storage; verify persistence by reading back (reload the page / fetch again). | A green screen without persisted data is a false PASS. | 02, 03 |
| A5 | **Frontend in a real browser.** Produce the UI states for real (loading, empty, error, populated), check capability-driven visibility per role, switch environments, and read console and network after each flow. | Users see the browser, not the component tree. | 03 (fe) |
| A6 | **Backend through the real API.** Real auth per role; check status code, response shape, persisted data and side effects (jobs, audit logs); run the permission matrix including direct forbidden calls expecting `403`; repeat/idempotency where relevant. | Rules and permissions live in the API, whatever the UI hides. | 03 (be) |
| A7 | **No tool output, no result.** If the browser or API tool is unreachable, the affected cases are `BLOCKED`; never describe results you did not observe. | Reported-but-unobserved results are fabricated evidence. | 01, 03 |
| A8 | **Evidence per case.** Steps executed, observations, screenshots/responses saved under the workspace's evidence path, console/network excerpts, revision, environment record, `stubbed` labels. | Evidence lets reviewers and users trust and reproduce the result. | 02 |
| A9 | **Result words.** `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` per case (or the workspace's words); a missing state, target or service is never `PASS`. | One vocabulary keeps reports honest. | 02 |
| A10 | **Actionable failures.** Exact step, expected vs actual, evidence, reproduction, severity, suspected area — sent to the Code Writer via the workspace's channel. | Vague failures come back as questions and cost a round. | 04 |
| A11 | **Run guard and regression cases too.** Out-of-scope guards and the plan's regression set are part of the run. | Breakage next to the feature is still breakage. | 02 |
| A12 | **Re-test on the new revision.** After a fix: rerun the failed cases and the affected regression cases on the fixed, re-reviewed revision. | A fix can break neighbours. | 04 |
| A13 | **Safety.** Only test accounts; never mutate production; never destructive actions on shared environments beyond the plan; no secrets in evidence. | Acceptance testing must not cause incidents. | 01 |
| A14 | **Flakiness is reported.** Rerun a failing case once to classify; an intermittent result is reported as flaky with both outcomes, never as `PASS`. | Hidden flakiness becomes a production surprise. | 04 |

**Never "not adopted":** A1, A2, A4, A7, A9, A13.
