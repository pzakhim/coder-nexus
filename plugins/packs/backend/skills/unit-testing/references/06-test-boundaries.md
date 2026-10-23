# 06 — What unit tests cannot prove

Detail for [unit-testing](../SKILL.md). Rule U13. Over-claiming unit results hides untested risk from reviewers and testers.

| Concern | Proven by | Owner |
|---|---|---|
| Business rules, validation, mapping, state transitions, error mapping of routers and adapters | Unit tests (this skill) | Code Writer |
| SQL queries, owner / tenant filters in SQL, constraints and their mapping, `ON CONFLICT`, eager loading / N+1 | Integration tests on a real PostgreSQL test database (never SQLite) — `{{slot:verification}}` | As the plan assigns: Code Writer for a task that names a developer integration test, Test Runner for independent verification |
| Alembic migrations, transaction isolation, locks, concurrent writes | `{{slot:verification}}` | Test Runner |
| API authorization matrix (role × object × environment), contract compliance of real responses, live API | `{{slot:verification}}`, `quality-acceptance` | Test Runner |
| Lifespan, settings loading, real outbound integrations | `{{slot:verification}}` phase checks | Test Runner |
| Security review of the change | `secure-coding` / `{{slot:secure-coding-standards}}` | Code Writer self-check, Code Reviewer |

When a phase task names a developer integration test, its database fixtures (test-database guard, `alembic upgrade head`, per-test rollback) follow `{{slot:verification}}`; this skill does not redefine them. Reason: one home per fixture set keeps the guard against non-test databases in one place.

When reporting unit results, say which of these rows the change touches and were **not** covered, for example: "Unit: 14 passed. Not covered: owner filter in `OrderRepository.list_for_owner` (SQL) — left to integration." Reason: the reviewer and Test Runner need to know where the risk still is.

Unit results are developer evidence; they are cited by the Test Runner but never counted as acceptance (`quality-acceptance`).

## Review

The Code Reviewer grades case coverage against [01](01-what-to-test.md) and the design rows, assertion strength against [04](04-test-quality.md), doubles against [03](03-doubles-and-fixtures.md), and reruns the unit suite on the reviewed revision (`review-workflow`). Broken rules are graded `P1`/`P2`/`P3` per the [SKILL rule table](../SKILL.md#rules); defects use the scale of [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md).
