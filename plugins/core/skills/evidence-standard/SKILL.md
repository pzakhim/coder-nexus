---
name: evidence-standard
description: "Require fresh command or runtime evidence on the current revision before any role (Code Writer, Bug Fixer, Code Reviewer, Test Runner, Docs Writer, or Coordinator) claims PASS, FIXED, APPROVED, ACCEPTED, or RECORDED."
---

# Evidence Before Claims

Answer one question before any positive statement: **which command, run just now on this revision, shows it?** No fresh evidence, no claim. Confidence, an earlier run, another agent's report or "should pass" are not evidence.

## 1. The gate

| Step | Do |
|---|---|
| 1. Identify | Write the exact claim ("AC-03 passes", "analyzer clean", "bug fixed"). Find the check that proves **this** claim: the task's Acceptance Criteria command + cwd, or the command from `{{slot:verification}}` |
| 2. Run | Run the full command fresh, on the revision you will name. Not a subset, not a cached result |
| 3. Read | Read the exit code and the output: failures, skips, warnings, test count, the line that matches **Expected** |
| 4. Compare | Does the output prove the claim as written? Partly → narrow the claim to what it proves |
| 5. Record | Write the evidence row (section 3), then state the claim with it |

Skip any step and the claim is `UNVERIFIED`, whatever the wording.

## 2. Which evidence proves which claim

One kind of check never stands in for another:

| Claim | Proven by | Not proven by |
|---|---|---|
| Tests pass | Test run of the named scope: exit 0, 0 failures, skip count read | An earlier run, a narrower scope, "no errors shown" |
| Build passes | Build command exit 0 | Tests or analyzer passing |
| Analyzer / lint clean | Analyzer run: 0 errors, warnings read | Build passing, editor showing no red |
| Behaviour works | The behaviour exercised on the real path (request, UI action, CLI) with the observed result | Unit tests alone; a fixture or mock run |
| Live integration works | A run against the real service in the agreed environment | A stub, fake, recorded response or mock server |
| Bug fixed | The original reproduction now passes | Code changed, a new test passes |
| Regression test guards the bug | Red with the fix undone, green with it (both runs recorded) | The test passes once |
| Task done | Its check output matches **Expected** (triage `MATCH`) | Check exit 0 with a different output |
| Phase or feature done | Plan and AC list re-read line by line, each item with its own row | "All tests pass" |
| Another agent's work is done | Diff and checks inspected on that revision yourself | Its status message |
| UI matches the design | Revision-bound capture per `{{slot:visual-quality}}` | Reading the UI code |

A fixture, mock or stubbed run is labelled as such in the row and never reported as a live run.

## 3. Evidence row

Use the format from `work-item-contract` (`references/handoff-and-status.md` §4):

| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
|---|---|---|---|---|---|
| AC-03 empty list shows the empty state | `<check command>` (cwd `app/`) | `a1b2c3d` | 0 | `12 passed, 0 skipped` | PASS |
| Live payment call succeeds | not run: sandbox credentials missing | `a1b2c3d` | - | - | BLOCKED |

- **Revision** is the commit the claim is about; if the tree has uncommitted changes, say so (`<sha>+dirty`, allowed only on intermediate task ticks: `READY_FOR_REVIEW` needs a committed `REVIEW_REVISION`, per `work-item-contract` (`references/handoff-and-status.md` §2 and §4)). Evidence from another revision is stale: a new revision invalidates every row for the code it touched.
- **Key output** is the shortest quote that proves the result, secrets and personal data replaced with `<REDACTED>`.
- **Result** uses the shared status words. `NOT_RUN` (not executed), `BLOCKED` (could not execute, with the reason) and `UNVERIFIED` (claimed without a check that proves it) are **never** counted, rounded or summarised as `PASS`. A verdict over items that include them cannot be `ACCEPTED` / `APPROVED` for those items.

## 4. Before saying done

1. Re-open the plan (the phase file, its tasks and Expected results) and the AC list. Do not work from memory.
2. Walk them **line by line**; for each line point to its evidence row or mark it `NOT_RUN` / `BLOCKED` / `UNVERIFIED` with the reason.
3. Report gaps first, then what passed. A hand-off with a gap says so in its status, never in a footnote.

## 5. Red flags

Stop and run the gate when you notice: "should", "probably", "seems to", "looks good"; satisfaction before output ("done", "all green"); quoting a run from before the last edit; trusting a status message; a summary count that hides a skip or a not-run item; a claim wider than the command (suite green but only one file ran).

## 6. Per role

| Role | Applies the gate to |
|---|---|
| Code Writer | Every task tick, `READY_FOR_REVIEW` (phase checks re-run on the committed `REVIEW_REVISION`), every `FIXED` reply in `review-resolution`, every fix in `{{slot:root-cause-debugging}}` |
| Bug Fixer | Reproduction before fix (`red`), fix verification (`green`), regression checks via `{{slot:verification}}`, and `READY_FOR_REVIEW` / `VERIFIED_FIXED` hand-off in `.superpowers/debug/<bug-slug>/` |
| Code Reviewer | Reruns the checks independently on the review revision; never copies the writer's rows as its own evidence |
| Test Runner | One row per AC with PASS / FAIL / BLOCKED / NOT_RUN; the feature verdict follows the rows |
| Docs Writer | Every claim that a command, link, path or behaviour in a document works: run or open it on the stated revision |
