# Review axes

Starting points for `02-review-axes.md`. Keep the axes that apply; each names its rubric skill (or the fallback), its gate, and what usually blocks.

## Shared axes (backend and frontend)

| Axis | Check | Rubric skill / fallback | Gate | Typically blocking |
|---|---|---|---|---|
| **Plan & scope** | Tasks ticked with real evidence; decisions (`D-NN`) honored; nothing outside approved goals; no files outside the item's scope | incremental-implementation / plan file | — | Contradicted decision, scope creep, cross-repo or out-of-scope edits |
| **Acceptance criteria** | Each applicable AC → implementation → test or manual check → evidence | plan / requirements | — | AC without implementation or evidence |
| **Architecture** | Placement, dependency direction, module/feature boundaries, no wrappers | clean-architecture | architecture tests / boundary script | Gate failure, inward-rule violation, deep import |
| **Code quality** | Names, size, errors, types, dead/debug code | clean-code | linters, analyzer | Swallowed errors, debug code, `any`/ignores without reason |
| **Tests** | Happy + negative + edge per changed behavior; doubles at boundaries; assertions specific; suite passes | unit-testing | test suite (rerun) | Happy-path-only tests, failing tests, mocked authorization |
| **Security** | Input validation, object-level authorization, data scopes, secrets, injection | secure-coding-standards | security linters if any | Missing guard or scope filter, secret in code/logs, string-built SQL |
| **Simplicity** | Unnecessary complexity in the diff | code-simplification | — | Only wrapper/alias violations (otherwise non-blocking) |

## Backend axes

| Axis | Check | Rubric / fallback | Gate | Typically blocking |
|---|---|---|---|---|
| **API contract** | Request/response shapes, status codes, error shapes match the approved contract | contract file / design | contract tests if any | Silent schema change, wrong status codes |
| **Transactions & data** | Use case owns the transaction; rollback on failure; no ORM leaks | clean-architecture `08-runtime` | integration tests | Partial writes, commits in repositories |
| **Migrations** | Expand/backfill/contract, locks, verification, state | database-migrations | migration verify | Unverified migration, destructive change without plan |

## Frontend axes

| Axis | Check | Rubric / fallback | Gate | Typically blocking |
|---|---|---|---|---|
| **UI states** | Loading, empty, error+retry, populated, forbidden — real, not mocked away | unit-testing / UI standards | component tests if any | Missing error/empty state |
| **Server/client boundary** | No server-only code or secrets in the client graph; thin routes | clean-architecture `fe/08` | build | Secret in bundle, fat route |
| **Approved design** | Matches the approved UI/UX at the same viewport and state | design files | visual check | Deviation without a decision |
| **Permissions in UI** | Capabilities, not role strings; server still decides | secure-coding-standards | boundary script | Role-string checks |

## Fallback when a rubric skill is missing

Use the "Typically blocking" column as the checklist and add a note: "<skill> not set up in this workspace".
