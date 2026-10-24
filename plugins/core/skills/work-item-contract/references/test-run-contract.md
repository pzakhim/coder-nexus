# Test run contract

The single home of what a scenario test run exchanges: the folder, how a user's scenario becomes cases, the default checks, status words and hand-offs. The process lives in `feature-testing`; the Test Runner's execution discipline stays in `quality-acceptance`. Formats shared with work items (evidence row, case results) stay in [handoff-and-status](handoff-and-status.md).

A test run answers **"does the app behave as this scenario expects, right now?"** It is not acceptance of a work item (that stays in `dev-team` with approved AC) and it never fixes anything.

## 1. Folder

One run = one folder `${workspaceFolder}/.superpowers/test-runs/<slug>/`, `<slug>` = `<yyyymmdd>-<short-kebab-title>`, never reused. A re-run of the same scenario is a new folder that links the old one.

| File | Written by | Read by |
|---|---|---|
| `scenario.md` (the user's words as given, or the path of the supplied file; the optional [template](../templates/test-scenario.md.tpl)) | coordinator | `test_runner` |
| `test-plan.md` ([template](../templates/test-plan.md.tpl)) | `test_runner` | user, coordinator |
| `test-run-report.md` ([template](../templates/test-run-report.md.tpl)) | `test_runner` | user, coordinator |
| `evidence/<revision>/` | `test_runner` | user, coordinator |

## 2. From scenario to cases

The scenario has no required format: free text ("test function A going from page B to C to D"), a `.md` / `.txt` / spreadsheet file, or Given/When/Then.

1. **Keep the user's intent.** One case `TC-NN` per flow or check the scenario names, with precondition, steps, expected result, data / account and target. Nothing is added or dropped.
2. **Expected result.** When the scenario states it, use it. When it does not, the case uses the default checks (§3) and carries the label `expected inferred`.
3. **Ask only for business outcomes.** Ask the user only when a case needs a business result that cannot be inferred (which value is right, which role may do it), one question at a time. Missing target, environment or account is asked the same way.
4. **No approval round.** A scenario that needs no question is run as soon as `test-plan.md` is written.

## 3. Default checks (`expected inferred`)

| ID | Check |
|---|---|
| DC1 | The flow completes; no step is blocked |
| DC2 | No crash, unhandled error, or error in the console or log during the flow |
| DC3 | Each screen or response shows the right state for its data (the stack's or layer's state list where one exists) |
| DC4 | Data shown is consistent across the steps of the flow |

A layer or stack may add checks in its `test_runner` rules; it never removes these.

## 4. Status words

| Word | Level | Returned by | Means |
|---|---|---|---|
| `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` | case | `test_runner` | As in [handoff-and-status](handoff-and-status.md) §3; a `FAIL` names expected vs actual and the evidence |
| `COMPLETED` | run | `test_runner` | Every case has a result and `test-run-report.md` is written; some cases may be `FAIL`, `BLOCKED` or `NOT_RUN` |
| `BLOCKED` | run | `test_runner` | No case could run (target, environment or access missing); names the blocker |

`COMPLETED` is not "all passed": the report's counts say that. `NOT_RUN`, `BLOCKED` and `UNVERIFIED` never count as `PASS`.

## 5. Hand-offs

| From → To | Status | Carries | Lives at |
|---|---|---|---|
| User → coordinator | — | The scenario, the target and environment when known | `scenario.md` |
| Coordinator → `test_runner` | — | The folder, the target, the revision under test (current `HEAD` plus its uncommitted scope, recorded as found) | `test-plan.md` header |
| `test_runner` → coordinator | `COMPLETED` / `BLOCKED` | Per-case results with evidence, gaps, suggested cases | `test-run-report.md`, `evidence/<revision>/` |

## 6. Rules

- **Read-only**: no edit to code, tests, fixtures or baselines, and no new test files. A case with no automated test is recorded as a **gap**; it is still checked by hand on the running app or API.
- **No review needed**: a test run tests whatever revision is current and records it, including uncommitted changes. Its result is evidence about that revision only.
- **Environment**: follow `quality-acceptance` → `modes/environment.md` rules on probing and never stopping what you did not start; the reviewed-revision rule is replaced by recording the current revision.
- **Suggested cases** (missing flows, empty or error states, permissions, boundaries) are listed only after the run, at the end of the report, and are not executed unless the user adds them to the scenario.
- **Failures are reported, not routed**: the user decides whether a `FAIL` goes to `defect-resolution`.
