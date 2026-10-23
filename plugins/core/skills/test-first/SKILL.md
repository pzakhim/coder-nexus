---
name: test-first
description: Decides when a failing test must come before production code and how to write tests that can actually catch a defect - right-reason failures, the break each test names, agreed Pass/Default, Fail and Empty data, doubles at port boundaries, and never editing an expectation to match the code. Use while executing a phase task that changes behavior, for every bug fix and review finding fix, and whenever a test is written or changed.
---

# Test First

A test proves something only if you have seen it fail for the reason it exists. Reason: a test written after the code passes at once, so nobody knows whether it can detect the defect it claims to guard. Stack tools, test paths, focused and full-suite commands come from `{{slot:unit-test}}`.

Detail: [writing tests that catch defects](references/writing-good-tests.md), [sources](references/sources.md).

## 1. When the test comes first

The plan wins where a task says so explicitly; otherwise this table decides.

| Change | Order | Reason |
|---|---|---|
| Domain rules, use cases, validation, calculations | Failing test first | Logic is where silent wrong results live |
| Mappers, parsers, serializers of a contract | Failing test first | A wrong key or null rule breaks the other side unseen |
| State machines and state holders (transitions, emitted states) | Failing test first | Missed transitions show up only on rare paths |
| **Every bug fix and every review finding fix** | Reproduce with a failing test first | The red run is the only proof the defect was real and is now gone |
| Changing existing code that has no test | Characterization test of current behavior first, then the change | Shows what the change really altered |
| Pure wiring (dependency registration, route tables, module exports) | May follow; covered by phase checks of `{{slot:verification}}` | No logic of its own to drive |
| Generated code | May follow; test the generator input or the first consumer | Testing generator output tests the generator's maintainers |
| UI layout and styling | May follow; covered by `{{slot:visual-verification}}` | Visual checks see layout; unit tests do not |
| Config, docs, constants with no behavior | No test | Nothing observable to break |

"May follow" never means "may skip" when the task's Acceptance Criteria name a test.

## 2. The loop

One behavior per cycle. Never write all tests first and all code after. Reason: bulk tests describe imagined behavior and harden before the design has taught you anything.

1. **Name the break.** Before the test body, write down which production change would make it fail (a wrong branch, a missing state change, a lost field). Cannot name one → the test checks nothing; pick an observable behavior.
2. **Write one test** at an agreed seam, with data from design (§3).
3. **Run it red** with the focused command. It must fail, not error, and the message must point at the missing behavior; compare it with the red run the task's Expected states. A test that passes now is testing existing behavior or nothing: fix the test. A compile or import error is not red: fix it and run again.
4. **Write the least code** that makes it pass. No options or branches no test demands.
5. **Run it green**, then the task's Acceptance Criteria. Read both outputs.
6. Next behavior. Clean-up belongs to `code-simplification` at phase end, not to this loop.

Production code written before a required failing test: set that change aside, run the test red against the old code, then restore the change. Reason: without the red run the test is unproven.

Record both runs as evidence rows (`evidence-before-claims`): red command, revision, exit code and the failure line; green the same.

## 3. Test data and seams

- Cases come from `design.md`: the agreed **Pass/Default**, **Fail** and **Empty** data (test-data table or verified API specification). Each changed behavior gets at least one Pass/Default, every Fail it handles, and Empty where a collection or optional value exists.
- Expected values come from an independent source: a literal from the design, a worked example, the spec. Never from the code under test or its helpers.
- Test at the seams the design names (public use case, mapper, state holder, port). A test that needs a seam the design does not have is `NEEDS_CONTEXT` or `plan-change-request`, not a new test-only hook in production code.
- Use the names from the `codebase-notes.md` Glossary in test names, so a failure reads as a rule.

## 4. Doubles

Prefer **real > fake > stub > mock**, and replace only at port boundaries (network, persistence, clock, randomness, external services). Never double the subject, its own collaborators, authorization or data-scope rules. A fake keeps the real contract: same result types, same errors for the same situations, complete data shapes. Detail and examples in [writing tests](references/writing-good-tests.md#doubles).

## 5. Never

| Never | Reason |
|---|---|
| Edit an expectation, delete an assertion or add a skip to match the code | Turns a found defect into a hidden one; if design is wrong it is `PLAN_WRONG` |
| Tautological asserts (expected recomputed like the code, value equal to itself, only "not null") | Passes by construction, cannot disagree with the code |
| Change detectors (a constant's value, exact wording, private structure) | Fail on every decision, sleep through every defect |
| Assertions on the mock itself | Proves the mock exists, says nothing about the code |
| Production methods only tests call | Test needs leak into the shipped surface |
| Counting a skipped, uncollected or not-run test as passing | A test that never ran is not evidence |

A green run that later fails in review or acceptance is `CODE_WRONG`: reproduce it with a failing test first, then `root-cause-debugging`.
