# Backend PHASE-00 Readiness Checklist

Detail for [backend architecture design](../SKILL.md) §6 and [verification](01_backend_codebase_scan.md).

Before starting feature implementation in `PHASE-01`, `PHASE-00` establishes an independently verifiable runtime and test baseline.

## 1. Readiness Tasks

A standard backend `PHASE-00` includes the following `[EXECUTE]` tasks:

| Step | Scope | Check Command (cwd: service root) | Expected Result |
|---|---|---|---|
| P0-01: Baseline verification | Existing codebase health | `uv run ruff check . && uv run pytest -q` | Baseline passes cleanly |
| P0-02: Test database setup | PostgreSQL container / test DB | `docker compose up -d postgres && uv run alembic upgrade head` | Migrations apply cleanly to head |
| P0-03: Contract snapshot | Base OpenAPI contract | `git show HEAD:openapi.json > contracts/openapi.base.json` (or export) | Base snapshot recorded |
| P0-04: Seed accounts & fixtures | Multi-tenant test accounts | `uv run python scripts/seed_test_data.py` | Required test roles seeded |
| P0-05: Provider sandboxes | Third-party test credentials / stubs | `curl -f https://sandbox.provider.com/health` | Provider sandbox reachable (stubs only if an approved `D-NN` mandates) |

## 2. Environment Rules

- Never connect test runs to production or shared development databases.
- No mock server is planned on the backend side; external providers use real sandbox credentials, and stubs are used only when an approved `D-NN` explicitly requires it.
- Test suites must use isolated transactional rollbacks or disposable schemas.
- If dependencies, database services, or seed credentials fail, mark `PHASE-00` as `BLOCKED` with explicit error output. Never proceed to feature coding with an unverified baseline.
