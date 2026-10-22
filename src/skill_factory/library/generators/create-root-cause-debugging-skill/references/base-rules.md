# Base rules (generic, every workspace)

How a Code Writer fixes a **known** failure (a red check, a CONFIRMED bug-hunt finding, a reported defect). Finding unknown defects is bug-hunt's job. Each rule goes into the generated skill with the workspace's facts **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| D1 | **Reproduce first.** Get one command that fails reliably (the failing test, a minimal script, a request); record it. Cannot reproduce → say so and gather evidence, do not "fix" blind. | A fix you cannot see fail and then pass is a guess. | 01 |
| D2 | **Read the real error.** The whole message, the first error (not the last), the stack trace down to your code, the relevant log lines. | Most time is lost fixing the wrong line of a long trace. | 01 |
| D3 | **One failure at a time, first one first.** Later failures are often consequences of the first. | Fixing cascades in parallel hides which change fixed what. | 01 |
| D4 | **Isolate.** Narrow the input, the code path and the change: what changed since the last green run (`git diff`, `git log`), smallest failing case, `git bisect` for regressions. | A small search space turns a hunt into a lookup. | 02 |
| D5 | **One falsifiable hypothesis at a time.** Write it down, design the check that would prove it wrong, change one variable, observe. | Several changes at once make every result ambiguous. | 02 |
| D6 | **Find the root cause, not the symptom.** Ask "why" until you reach the defect; check whether the same mistake exists elsewhere in the diff. | Patching the symptom moves the bug and leaves its siblings. | 02, 03 |
| D7 | **Smallest fix at the right layer, inside the approved scope.** Placement per clean-architecture; no unrelated refactor in the same change. | Fixes in the wrong layer re-break on the next change and bloat review. | 03 |
| D8 | **Regression test.** A test that fails before the fix and passes after (per unit-testing), unless truly impractical — then say why. | Without it the bug returns silently. | 03 |
| D9 | **Never green-wash.** Do not edit/skip/xfail tests to pass, add fake fallbacks or broad catches, loosen types or assertions, add sleeps/retries to hide races, or disable lint/gates. | These hide the defect and remove the protection that found it. | 03, SKILL |
| D10 | **Environment vs code.** Missing service, credentials, env var, stale build/cache, dependency drift → `BLOCKED` with the evidence, not a code change. Never stop/restart a stack you did not start or change shared configuration. | Code "fixes" for environment problems break the code for everyone else. | 04 |
| D11 | **Temporary instrumentation is removed.** Debug prints/logs/breakpoints used to investigate are deleted before handoff (clean-code C3). | Leftover debug output leaks data and noise. | 03 |
| D12 | **Time-box and escalate.** After the agreed number of hypotheses/attempts without progress, stop and report what was tried and ruled out. A fix that changes behavior, API, architecture, dependencies or a component contract goes back to the gate. | Endless attempts burn time and drift out of scope. | 04 |
| D13 | **Use the workspace's tracing tools** (code-intelligence queries, impact analysis before editing a symbol, caller search) and their mandatory rules. | Tools trace call paths faster and safer than reading by hand. | 05 |
| D14 | **Report the fix.** Symptom, reproduction, root cause, fix, regression test, evidence lines, what was ruled out. | Reviewers verify the reasoning, not just the diff. | 06 |

**Never "not adopted":** D1, D7, D8, D9, D12.
