---
name: feature-testing
description: "Entry point for testing a feature against a scenario the user gives - free text such as 'test function A going from page B to C to D', a file, or Given/When/Then - where test_runner turns it into cases, uses default checks when no expected result is stated, runs them for real on the app or API, and reports PASS/FAIL per case with evidence, gaps and suggested extra cases. Read-only - it never writes tests or fixes code. Use when the user wants something tested, or says things like 'test chức năng', 'chạy test', 'kiểm thử theo kịch bản', 'test giúp tôi luồng', even if they do not say 'scenario'. Not for accepting a work item against approved AC (that is dev-team) and not for investigating or fixing a bug (debug-investigation, bug-squad)."
---

# Feature testing

Act as the **coordinator** for one test run. The folder structure, how a scenario becomes test cases, the default checks, status words, templates, and rules are defined once in `work-item-contract` (`references/test-run-contract.md`, `templates/test-scenario.md.tpl`, `templates/test-plan.md.tpl`, `templates/test-run-report.md.tpl`); this skill decides **who runs when** and never restates them.

The work is done by **`test_runner`**; the coordinator never edits code, tests, or expected results.

## 1. Intake & Scenario Lock

1. Create `.superpowers/test-runs/<slug>/` and save the user's scenario in `scenario.md` exactly as given (or the path of the supplied file). Offer `templates/test-scenario.md.tpl` only when the user asks how to write one.
2. When the scenario does not name them, ask for the target (device, emulator, browser, or API), the environment (`DEV` / `STG` / `PROD`), and the account/role, one question at a time.
3. Run `git-preflight` Step A (read-only) to record the branch and revision under test.
4. Start `test_runner` with the folder and target. It writes `test-plan.md` (applying default checks labeled `expected inferred` when no expected outcome is stated), asks the coordinator for any business outcome it cannot infer (relay to the user), executes the cases on the real app, browser, or API target (using the stack's runtime/browser/API tools per `quality-acceptance` and workspace `quality-*` skills), writes `test-run-report.md` with captured evidence in `evidence/`, and returns one status.

## 2. Routing & Zero-Re-Ask Handoff to bug-squad (coordinator only)

| `test_runner` returns | Coordinator does |
|---|---|
| `COMPLETED` | Report the counts (`PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`), each `FAIL` with steps, expected vs actual, and evidence path, `## Gaps`, and `## Suggested cases`. For each `FAIL`, offer **`bug-squad`** — when the user says yes, pass the `FAIL` row, steps, expected vs actual, and evidence path from `test-run-report.md` directly to `bug-squad` via **Zero-Re-Ask Handoff** per `test-run-contract`. Offer to add suggested cases to `scenario.md` for another run. |
| `BLOCKED` | Resolve the named blocker (target, environment, or account/access) before re-assigning. Re-assigning unchanged repeats the failure. |

## 3. Never

- Add, drop, or reword the user's cases, or run suggested cases the user did not add.
- Fix code, write tests, update a baseline, or start `bug-squad` without the user's yes.
- Report `COMPLETED` as "all passed", or count `NOT_RUN`, `BLOCKED`, or `UNVERIFIED` as `PASS`.
