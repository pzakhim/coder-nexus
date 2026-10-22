# Base rules (generic, every workspace)

Generalised from a real workspace's live-stack practice and the Coder Nexus preparation phase (mock data before coding). Each rule goes into the generated skill with the workspace's services, commands and data rules **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| E1 | **Know the stack.** Services, ports, start/stop commands, health checks and start order (DB → API → workers → frontend). | Guessing commands starts the wrong thing or nothing. | 01 |
| E2 | **Probe before starting; never stop what you did not start.** Check ports/health first and reuse a running stack; never stop, restart or reset a stack someone else started (another agent or the user). | Killing someone else's stack destroys their work in progress. | 01, SKILL |
| E3 | **Start in the background, capture logs, record ownership.** Note which processes you started and where their logs are; stop only those. | Logs are evidence; ownership makes cleanup safe. | 01 |
| E4 | **Readiness before testing.** Wait for health endpoints / first page load with a timeout; slow first compiles are normal, endless waits are not. | Testing a half-started stack produces false failures. | 01 |
| E5 | **Isolated test data.** Dedicated tenant/workspace/run IDs or resettable fixtures; never production data; never run commands that clone, reset or overwrite shared business data without explicit approval. | Shared or real data makes results lie or causes damage. | 02 |
| E6 | **Accounts per role.** Seeded test users for each role/environment the plan needs; credentials from the approved local config, never printed or reported; never real users' accounts. | Permission tests need every role; real accounts leak and get locked. | 02 |
| E7 | **External providers: sandbox first, stub with a label.** Use provider sandboxes where they exist; otherwise stub at the network edge with documented scenarios (success, error, timeout); every result from a stub is labelled "stubbed". | A PASS against an unlabelled stub is a false PASS. | 03 |
| E8 | **Schema at the reviewed revision.** Apply the revision's migrations to the local/disposable DB (per database-migrations) before testing. | Old schema + new code fails for reasons unrelated to the feature. | 04 |
| E9 | **Run the reviewed revision.** The stack runs exactly the revision under test (checkout, install, build, restart what you own); record it. | Testing a different revision proves nothing about the reviewed one. | 04 |
| E10 | **Environment matrix.** Which environments the plan needs (e.g. DEV/STG/PROD selectors inside the app vs physical databases) and how to switch between them safely. | An environment switch in the UI is not a different database — confusing them breaks isolation. | 02, 04 |
| E11 | **Clean up.** Remove data you created when the workspace requires it, stop your own processes, keep the logs. | Leftovers poison the next run. | 05 |
| E12 | **Environment failure = `BLOCKED`.** Service down, port conflict you cannot resolve, missing credentials or provider unavailable → report `BLOCKED` with the evidence and the owner; never work around it with code changes. | A code workaround for an environment problem changes the thing under test. | 05 |
| E13 | **Secrets stay local.** Env files are local and git-ignored; values are never echoed, logged or pasted into reports. | Test logs are shared widely. | 02, 05 |
| E14 | **Record the environment.** Revision, services and versions, seed, stubs (labelled), accounts by role name, start time — in the evidence. | Results without their environment cannot be reproduced. | 05 |

**Never "not adopted":** E2, E5, E7, E9, E12, E13.
