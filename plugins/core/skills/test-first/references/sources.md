# Sources

External ideas adapted into [test-first](../SKILL.md), rewritten in this repo's vocabulary (design test data, seams named in `design.md`, Expected triage, evidence rows). Internal base input: `src/skill_factory/library/generators/create-unit-testing-skill/` (rules U1-U14, doubles table), read-only.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/test-driven-development/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/test-driven-development/SKILL.md) | 303k | Watch the test fail; it must fail (not error) for the expected reason; a test that passes at once is a finding about the test | SKILL §2 step 3, [right-reason table](writing-good-tests.md#right-reason-failure) |
| same | 303k | Least code to pass; no speculative options | SKILL §2 step 4 |
| same | 303k | Code written before the test does not get to skip the red run | SKILL §2 "set that change aside" (softened: restore after red, not delete) |
| same | 303k | Bug found: reproduce with a failing test before fixing | SKILL §1 bug fix row |
| [obra/superpowers `skills/test-driven-development/writing-good-tests.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/test-driven-development/writing-good-tests.md) | 303k | Name the production change that would make the test fail; defect vs decision | SKILL §2 step 1, [name the break](writing-good-tests.md#name-the-break) |
| same | 303k | No change detectors; behavior, not text; test your boundary, not the framework | SKILL §5, [behavior](writing-good-tests.md#behavior-not-implementation) |
| same | 303k | No assertions on mocks; complete data shapes; learn side effects before mocking; test-only methods stay out of production | SKILL §4, §5, [doubles](writing-good-tests.md#doubles) |
| same | 303k | Mutation check before finishing | [mutation check](writing-good-tests.md#mutation-check) |
| [mattpocock/skills `skills/engineering/tdd/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/tdd/SKILL.md) | 300k | Tests live at agreed seams; tautological tests; vertical slices, not all tests first; refactoring is outside the red/green loop | SKILL §2 intro and step 6, §3 seams, §5 |
| same | 300k | Use the project glossary for test vocabulary | SKILL §3 last bullet (`codebase-notes.md` Glossary) |
| [mattpocock/skills `skills/engineering/tdd/tests.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/tdd/tests.md) | 300k | Verify through the interface, not a side channel; independent literal expectations | [independent expectations](writing-good-tests.md#independent-expectations), [behavior](writing-good-tests.md#behavior-not-implementation) |
| [mattpocock/skills `skills/engineering/tdd/mocking.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/tdd/mocking.md) | 300k | Mock only at system boundaries; never your own modules | SKILL §4, [doubles](writing-good-tests.md#doubles) |
| [addyosmani/agent-skills `skills/test-driven-development/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/test-driven-development/SKILL.md) | 109k | Real > fake > stub > mock preference order | SKILL §4 |
| same | 109k | Prove-it pattern for bugs; when not to test (config, docs, static content) | SKILL §1 table |
| same | 109k | Readable self-contained cases over over-shared setup; snapshot abuse; deterministic, isolated tests | [independent expectations](writing-good-tests.md#independent-expectations), [behavior](writing-good-tests.md#behavior-not-implementation), [determinism](writing-good-tests.md#determinism) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| "No production code without a failing test" for every change, exceptions only by asking the human | superpowers TDD | Wiring, generated code and layout have better checks (phase verification, visual verification); the plan and the §1 table decide instead of ad-hoc permission requests |
| Delete code written before the test, never look at it again | superpowers TDD | Same proof is reached by setting the change aside, running red, restoring; deleting approved-scope work wastes it without adding evidence |
| Refactor step inside each cycle | superpowers TDD, addyosmani TDD | Clean-up is a separate, evidence-bound pass (`code-simplification`) at phase end, so behavior change and refactoring stay apart for review |
| Confirm seams with the user before writing any test | mattpocock tdd | Seams are agreed once in `design.md` at Gate 2; a missing seam goes back through `NEEDS_CONTEXT` / `plan-change-request` instead of mid-phase questions |
| SDK-style interfaces to make mocking easy | mattpocock mocking | A port design decision, owned by Planning in `design.md` and `{{slot:clean-architecture}}` |
| Test pyramid percentages and test-size classes | addyosmani TDD | Test levels per case are set in the plan's test strategy and by the Test Runner; fixed ratios do not fit both packs |
| Browser DevTools runtime checks | addyosmani TDD | Belongs to `{{slot:visual-verification}}` and acceptance testing, not developer tests |
| Language discovery steps (find the build file, the runner) | addyosmani TDD | The pack provides the exact tools and commands in `{{slot:unit-test}}` |
