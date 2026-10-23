# Mode: environment

Prepare a safe, repeatable environment that runs exactly the reviewed revision. Readiness facts (services, ports, seed, accounts, providers) come from `phases/phase-00-prepare.md` and the stack's `{{slot:verification}}`; never guess a command, entry point, device or business record.

## Rules

| # | Rule | Reason |
|---|---|---|
| E1 | **Probe before starting.** Check ports and health first; reuse a stack that is already running and healthy. | Starting a second copy collides with the first. |
| E2 | **Never stop what you did not start.** Do not stop, restart or reset a stack, database or device another agent or the user started. Record which processes you started and where their logs go; clean up only those. | Killing someone else's stack destroys their work. |
| E3 | **Reviewed revision.** Record the revision from the `APPROVED` review report and confirm the running stack serves that tree (rebuild / restart only what you own). | A different revision proves nothing about the reviewed one. |
| E4 | **Migrations applied.** Apply the revision's schema changes to the local / disposable database with the stack's own runner before testing. | Old schema plus new code fails for reasons unrelated to the feature. |
| E5 | **Readiness check.** Wait for health endpoints or the first screen with a timeout; a stack that never becomes ready is `BLOCKED`, not retried forever. | Testing a half-started stack produces false failures. |
| E6 | **Isolated test data.** Use seeded fixtures, a dedicated tenant / workspace / run prefix, or a resettable database. Never production data; never clone, reset or overwrite shared business data without the user's approval. | Shared or real data makes results lie or causes damage. |
| E7 | **Accounts per role.** One test account for each role the plan needs, from approved local config. Never a real person's account; never print or report credentials. | Permission cases need every role; real accounts leak and get locked. |
| E8 | **External providers: sandbox, else labelled stub.** Prefer the provider's sandbox or test mode. Otherwise stub at the network edge with documented scenarios (success, error, timeout, malformed) configured outside application code. Every result from a stub is labelled `stubbed: <provider>`. No sandbox and no approved stub: the affected cases are `BLOCKED`. | A stub run proves the app's handling, not the integration; an unlabelled stub is a false pass. |
| E9 | **Secrets stay local.** Env files stay local and ignored by version control; values are never echoed, logged or pasted. | Evidence travels further than the environment. |
| E10 | **Environment failure is `BLOCKED`.** Port conflict you cannot resolve, missing credentials, service down, provider unreachable: report `BLOCKED` with evidence and the owner. Never change code or config under test to get past it. | A workaround changes the thing under test. |

## Environment record

Write it at the top of the run (see [reporting.md](reporting.md#environment-record)):

| Field | Example content |
|---|---|
| Revision | Reviewed revision + review report link |
| Services | Name, version, port, `started` or `reused` (owner) |
| Database | Disposable / local, migrations applied up to which step |
| Data | Seed or fixture name, run prefix |
| Accounts | Role names only (no usernames or passwords) |
| Providers | `live sandbox` / `stubbed: <provider>` per provider |
| Started at | Timestamp |

## Cleanup

Remove data you created when the workspace requires it, stop only your own processes, keep the logs as evidence.
