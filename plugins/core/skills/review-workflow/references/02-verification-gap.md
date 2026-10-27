# 02 — Finding Verification Gaps

> Topic: Finding changed behaviour that could regress with no test failing, plus broken or stale verification checks.

Goal: find behaviour this phase changed that could later break with no test failing. This is not a second bug hunt; a defect you meet while tracing goes into the findings table as usual.

A gap is filed only when you can name the specific regression one added or changed test would catch. "Coverage could be higher" is not a gap.

## Gap shapes

| Shape | Meaning |
|---|---|
| Regression | The changed code could regress where it is used and no test would fail |
| Missing adoption | A site that should use the new behaviour still does it its own way, and no test notices |
| Broken verification | A test looks like it covers the change but is skipped, flaky, not run by the stack's test runner by default, or too weak to see the regression |
| Stale verification | A test this change made wrong or moot; it may still pass |

## Steps

1. **Screen.** Take each part of the diff. Skip parts that change no observable behaviour (formatting, renames, type-only, comments) and static text. Never skip test-only parts: deleted or weakened tests are checked in step 4.
2. **Name the changed behaviour** per part: output, error path, side effect, default, validation rule, schema or event shape, state emitted.
3. **Find the consumers** (callers, registered entry points, contract readers). One to three hops is usually enough; stop when a test there would catch the regression or the next hop is a guess.
4. **Name the smallest realistic regression** for each consumer (branch inverted, default dropped, field omitted, old error returned). If there is none, drop the path. Then read the relevant test: would that regression make an assertion fail?
5. **Check every touched test**: does it assert what the code must do after this change?
6. **Confirm** before filing: re-open the test or search result you rely on and state why it misses the regression.

## What does not count as a test

Assertions on source text; success / no-throw / snapshot-only checks; checks that a mock or log was called; tests that mock away the integration under test; end-to-end runs that never inspect the changed output; assertions that pass whatever the input (for example a fallback that equals the expected value). Before saying no test exists, search the repo for the symbol and its imports — an expected file location is not enough.

`{{slot:unit-testing}}` test-first compliance belongs here too: a new behaviour whose test was never seen failing for the right reason is a broken-verification gap.

## Severity and output

Each gap becomes a finding row in the report (pass `5 gap`): changed surface file:line, impacted consumer file:line, existing test evidence, the missing assertion, the regression demonstration, and the test to add or change in the stack's style (`{{slot:unit-testing}}`). Severity: `MAJOR` when the unprotected behaviour is an AC of this phase or a Produces contract; otherwise `MINOR`. Gaps are `CONFIRMED` only when you read the test and showed it would not fail.

Do not file: cases the compiler or analyzer enforces, behaviour an existing integration or acceptance check already pins, untested code the change did not touch.
