# Clean Architecture & Delivery Rules for Backend Workspaces

Apply the active workspace profile from `.superpowers/setup.json` (`profile` / `architecture_profile`) and the profile-activated references in [clean-architecture](../skills/clean-architecture/SKILL.md).

> **Source:** Senior Backend Standards · AIFactory-Coder
> **Applies to:** Backend service code, schemas, repositories, and database migrations generated or changed under an approved feature version and behavior phase.

Read the current service module and the approved `.superpowers/work-items/<slug>/vN/` (or legacy `docs/features/<module>/<feature>/vN/`) requirements, design, and phase before changing code. Existing verified workspace conventions and the approved scope determine which files and layers need work; do not create speculative abstractions or single-implementation protocols solely to satisfy a checklist.

## 1. Department Routing & Approval Gates

- **Route requests to the matching entry skill**:
  - Full feature delivery (`v1` / `v2+`) → `dev-team`
  - L1 / L2 / L3 defect triage & fixing → `bug-squad`
  - Read-only bug or trace diagnosis → `debug-investigation`
  - Read-only scenario testing → `feature-testing`
  - API contract specification & schema handoff → [api-contract-design](../skills/api-contract-design/SKILL.md)
- **Explicit user approval gates**:
  - Never self-approve Gate 1 (Spec), Gate 2 (Architecture Design), or Gate 3 (Implementation Plan / `PCR-NN`).
- **Interactive clarification (`ask_question`)**:
  - Ask one focused question at a time (or the 4-item setup batch) and place `(Recommended)` first.

## 2. Unified Statuses, Severities & Evidence Gate

- **Canonical tokens**:
  - Enforce [flags_and_statuses.md](../../../shared_contracts/flags_and_statuses.md) and [api_handshake_protocol.md](../../../shared_contracts/api_handshake_protocol.md).
  - Deterministic CLI tool gates report binary `PASS` or `FAIL`; all code findings and test-case severities use `BLOCKER` / `MAJOR` / `MINOR` (never `P1` / `P2` / `P3`).
- **Fresh revision-bound evidence**:
  - Require fresh command or runtime evidence on the exact reviewed revision before claiming `PASS`, `FIXED`, `APPROVED`, `ACCEPTED`, or `RECORDED`.
  - `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` are never `PASS`; changing code or migrations invalidates affected earlier evidence.
- **Data provenance & fail-fast**:
  - Never fabricate business records, silent fallback defaults, or unlabelled stubs to mask missing data or broken contracts.
  - Outbound third-party integrations use approved contract fixtures (`3RD_PARTY_MOCKOON`) only when explicitly configured; never run destructive checks against an unclassified or production database.

## 3. Backend Clean Architecture & Layer Boundaries

- **Domain Purity**:
  - Entities, Value Objects, and Domain Errors must remain 100% independent of web frameworks (FastAPI), ORMs (SQLAlchemy), database drivers, and external SDKs.
  - Module imports must remain side-effect-free at import time; startup I/O, settings caching, and connection pools belong in explicit lifespan hooks.
- **Use Cases & Repository Ports**:
  - Application Use Cases / Services orchestrate business rules and own transaction boundaries (one atomic unit of work per request), depending exclusively on abstract Repository Interfaces (Ports) or verified repository boundaries rather than raw transport or ORM internals.
- **Controllers / Presentation Boundary**:
  - Routers and Controllers handle HTTP routing, request/response DTO validation (Pydantic schemas), authentication dependencies, and domain-error-to-status-code mapping only.
  - Business calculations, authorization branching, direct queries, and transaction commits never live inside Controllers.
- **Data / Persistence Adapters**:
  - Concrete repositories and migrations map explicitly between ORM models and Domain entities / schemas without leaking ORM instances directly from routers.
  - Preserve database and constraint errors explicitly without silent fallbacks, and load async relationships explicitly.

## 4. Contract-Driven API & Verification Integrity

- **Contract handshake compliance**:
  - Every public endpoint must conform to its approved `api_contract.json` or OpenAPI specification.
  - Breaking contract changes require an updated Handshake agreement with consumers before implementation.
- **Test & gate integrity**:
  - Never delete, disable, or weaken an assertion (`# noqa`, `# type: ignore`, `--exit-zero`, or lowered coverage thresholds) to make a failing check pass.
  - Verify formatter, linter, static type-check, import boundary, disposable-DB migration, and test gates on the reviewed revision per [verification](../skills/verification/SKILL.md).
