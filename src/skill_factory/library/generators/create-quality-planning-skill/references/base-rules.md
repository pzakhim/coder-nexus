# Base rules (generic, every workspace)

Generalised from Coder Nexus `plugins/core/agents/test_runner.md` and a real workspace's verification practice. Each rule goes into the generated skill with the workspace's spec paths, IDs and roles **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| Q1 | **Specs are the source of truth.** Design cases from the brief (scope in/out), requirements (AC, BDD scenarios), design (states), decisions and glossary — not from the implementation plan or the code. | Cases derived from the code only prove the code does what it does. | 01 |
| Q2 | **Review testability early.** Right after the requirements gate, flag AC without an observable outcome, with vague words ("fast", "user-friendly") or missing data, and send questions back. | An untestable AC found late blocks the release. | 01 |
| Q3 | **Two-way traceability.** Every AC and BDD scenario → at least one case; every case cites its AC, or is marked "regression" or "out-of-scope guard". | Gaps and orphan tests both hide risk. | 02 |
| Q4 | **Cover the categories.** Happy path; validation errors; permission denials per role and environment; empty / loading / error / populated states; boundaries; external failures and timeouts; repeated submit where relevant. | Most escaped defects live off the happy path. | 03 |
| Q5 | **Cheapest level that proves it.** API acceptance for rules and permissions, UI end-to-end for user flows and states, visual for fidelity, manual only with a reason; unit tests are the Code Writer's. | Every case at the UI level makes the suite slow and flaky. | 04 |
| Q6 | **Safe, repeatable data.** Seeded per case or per run, from safe sources; no production data; never fabricate "successful" data for a missing source; clean up. | Shared or fake data makes results lie. | 05 |
| Q7 | **Named environments.** Which stack/environment each case runs on; external providers stubbed only where the plan says so, and labelled in results. | A PASS against a stub is not a PASS against the real provider. | 05 |
| Q8 | **Risk-based priority.** Critical flows, permissions/scopes and data integrity first; plan the run order. | When time runs out, the important cases are done. | 03 |
| Q9 | **Out-of-scope guards.** Cases proving nothing listed under "scope out" was implemented. | Unasked-for changes are untested risk. | 03 |
| Q10 | **Regression set.** Existing flows likely affected by the change (shared components, same tables, same permissions). | Changes break neighbours more often than themselves. | 03 |
| Q11 | **Concrete expected results.** Observable state, message, persisted data, status code — never "works correctly". | Vague expectations cannot fail, so they prove nothing. | 03 |
| Q12 | **One ID scheme.** The workspace's IDs for AC and cases, used in plan, results and defects. | Shared IDs make reports and fixes traceable. | 02 |
| Q13 | **The plan is reviewed before execution;** AC changes → plan update. | Executing an outdated plan wastes a run. | 06 |
| Q14 | **Independence.** Read the implementation only to find targets (routes, selectors), never to choose expectations; never adjust an expectation to match the code. | The Quality Engineer is the user's advocate, not the code's. | 01, SKILL |

**Never "not adopted":** Q1, Q2, Q3, Q4, Q11, Q14.
