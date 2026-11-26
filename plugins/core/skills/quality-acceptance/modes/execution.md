# Mode: execution
> Topic: Executing existing local `integration_test/` suites (when present) and planned `E2E-01..E2E-N` scenarios in strict sequential Fail-Fast order on the reviewed revision, recording fresh observable evidence.

Run the plan's scenarios on the prepared environment, on the exact reviewed revision, and record what was observed.

## Preconditions

- The Code Review report is `APPROVED` for the same tree you are about to test. Otherwise stop: nothing to test yet.
- The environment record exists and names that revision ([environment.md](environment.md)).
- The browser (`browser` subagent / `chrome-devtools` MCP), simulator/emulator, or API tool the scenario needs is reachable. A missing tool makes the affected scenarios `BLOCKED`; never describe output you did not get.

## Order (Hybrid E2E + Strict Sequential `E2E-01` → `E2E-N` Fail-Fast)

1. Re-check the Reviewer's analyzer, test, and visual evidence for the revision (read, do not trust blindly; rerun the cheapest command to confirm the tree).
2. **Existing local `integration_test/` & stack checks (Hybrid E2E, read-only):** Run existing local `integration_test/` suites if present in the repo (authored by `code_writer` under Gate 3; `test_runner` never writes or edits test files) plus the required stack checks from `{{slot:verification}}` (affected regressions, build).
3. **Strict Sequential `E2E-01` → `E2E-N` Fail-Fast:** Execute every scenario in `vN/test-plan.md` strictly in listed order **`E2E-01` → `E2E-02` → ... → `E2E-N`** (never reorder by severity; guards, permissions, and regression scenarios are part of the sequence). For **web targets**, drive and verify live flows via Antigravity's builtin **`browser` subagent** or **`chrome-devtools` MCP** (`navigate_page`, `click`, `fill`, `take_screenshot`, console & network checks); for **mobile/desktop targets**, drive via native simulator/emulator commands and capture live screenshots.
4. **Visual scenarios (`{{slot:visual-quality}}`):** Capture independent live screenshots for each `S-NN` screen/state/viewport/role/theme and compare them via multimodal **`read_file`** against the approved **Figma** (`figma/<stem>-SNN.png`) **or HTML sitemap** (`sitemap/screens/*.png`) reference. Never reuse `code_writer`'s or `code_reviewer`'s screenshots as QA proof.

## Executing one scenario

- **As written.** Follow Given / When / Then; record any deviation; never soften or improvise an expectation.
- **Real path, then read back.** Use the real backend and storage; prove persistence by reading it again (reload, re-fetch, query through the public interface).
- **Produce states for real.** Empty, loading, error and populated states come from real conditions (empty seed, slow or failing provider stub, real error response), not from editing the code.
- **Per role.** Repeat permission cases with each role's account; include a direct call that bypasses the UI and expect the specified refusal.
- **Health after each flow.** Read logs, console and network output for errors the screen does not show.
- **Fresh evidence.** One evidence row per check, from this run, on this revision.

## Evidence

Store files under `vN/evidence/final_qa/<revision>/` (or `vN/evidence/<phase-id>/<revision>/` for a phase run) with predictable names (`E2E-NN-<step>.png`, `E2E-NN-response.json`, `E2E-NN.log`, plus canonical `acceptance-report.md`). Each scenario gets a row in the shared shape:

| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
|---|---|---|---|---|---|
| `E2E-03` denies `viewer` delete | `<request or test command>` (`<cwd>`) | `<rev>` | `0` | `status 403, record still present on re-read` | `PASS` |

Rows from a stubbed provider add `stubbed: <provider>` in Key output. Redact tokens, cookies, passwords and personal data before saving any file; use test data only so screenshots stay clean.

## Expected vs observed triage (`FAIL-FAST` loop: `test_runner` ↔ `bug_fixer` ↔ `planning` → `code_writer`)

Execute `E2E-01` → `E2E-02` → ... → `E2E-N` in `vN/test-plan.md` sequentially, one scenario at a time. Never edit, weaken, or skip any scenario in `test-plan.md`.

| Observation | Result | Next |
|---|---|---|
| Matches the expected result | `PASS` | Tick `- [x] **E2E-i**` with fresh evidence in `vN/test-plan.md` and proceed to `E2E-(i+1)` |
| Differs from the expected result | `FAIL` | Rerun once to rule out flakiness; if still `FAIL`, **STOP IMMEDIATELY (`FAIL-FAST`)**, write `acceptance-report.md` with defect (`FAILED_AT: E2E-i`, [reporting.md](reporting.md#defect-report)), and return `CHANGES_REQUESTED` to **`bug_fixer`** (`L1` max 3 rounds before `L3`, `L2` via `code_reviewer`, or `L3` `PCR-NN.md` → **`planning`** → **`code_writer`** → `code_reviewer`) |
| Different outcomes on two runs | `FAIL`, labelled flaky with both outcomes | **STOP IMMEDIATELY (`FAIL-FAST`)**, report defect (`FAILED_AT: E2E-i`) for `bug_fixer`; never `PASS` |
| Tool, service, account, provider or reference missing | `BLOCKED` | Record owner and evidence, stop and return `BLOCKED` |
| State could not be produced, scenario skipped with a reason | `NOT_RUN` | Record why |
| Expected result looks wrong against another spec | Keep the result as observed | Question / `PLAN_CONFLICT` or `SCOPE_CHANGE` row to the coordinator for `planning`; never edit the expectation |

## Re-test (End-to-End from `E2E-01` to `E2E-N`)

After `bug_fixer` (or **`code_writer`** after an `L3` `planning` amendment, plus `code_reviewer` if `L2` or `L3`) commits a fix on a new revision: rebuild the environment record for the new revision, mark earlier evidence as superseded, and **re-run all scenarios in `vN/test-plan.md` sequentially from start to finish (`E2E-01` → `E2E-N`)** (plus existing local `integration_test/` suites when present) until 100% pass end-to-end.
