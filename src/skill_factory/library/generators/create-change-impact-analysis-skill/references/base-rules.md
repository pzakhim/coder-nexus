# Base rules (generic, every workspace)

Each rule goes into the generated skill with the workspace's real tools and structure **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| CX1 | **Trace from what changes, with evidence.** Start from the changed entity field, contract, rule, component or permission; trace who uses it and what it uses; record each command run and its result. | Impact without evidence is a guess. | 02, SKILL |
| CX2 | **Fixed impact categories.** UI screens and flows; APIs and their consumers (other services, mobile versions in use, partners); data (tables, migrations, reports, exports); jobs, events and integrations; permissions and data scopes; documentation and analytics. Keep the ones the workspace has. | A whole category is the easiest thing to miss. | 01 |
| CX3 | **Classify every hit.** Path or name as evidence; "behavior changes" (needs a task) or "regression only" (needs a test); owner when outside the team. | Planning knows what is a task and what is a test. | 04 |
| CX4 | **Regression list.** The suites or cases that cover each affected place, with commands; handed to `quality-planning` for test cases. | Re-testing the right things, not everything or nothing. | 03 |
| CX5 | **Contract breaks are flagged** for versioning (the `git-workflow` contract list) and for consumers that must change. | The version must reflect the real risk. | 04 |
| CX6 | **Unknown is not "no impact".** When tracing cannot settle an impact, it becomes a `Q-NN`; "no impact" needs evidence. | Silent regressions start here. | 04, SKILL |
| CX7 | **Behavior and AC delta for v2+ (ADDED / MODIFIED / REMOVED).** Each affected behavior (`BR-NN`, `W-NN`, endpoint, screen) is ADDED (not in the built code), MODIFIED (built behavior that changes) or REMOVED (built behavior that goes away) in "Behavior delta", compared with the actual code at the baseline revision, not the old design; each row has a reason and evidence. REMOVED also says what happens to existing data and users (migrated, kept read-only, deleted, told). Each affected AC goes into "AC delta" as Add / Change / Remove (unaffected = Keep) and traces to a behavior row. The vocabulary is the one `requirements-specification` RS10 writes. | Reviewers see exactly what differs; one vocabulary from spec to impact; a wrong kind leaves nothing to compare. | 04 |

**Never "not adopted":** CX1, CX6.
