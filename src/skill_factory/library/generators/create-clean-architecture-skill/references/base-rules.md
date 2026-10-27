# Base Clean Architecture Rules (Universal)

Universal architectural rules for any codebase. Every rule goes into the generated skill with the workspace's verified paths and types **and its rationale**, adapted to the workspace's contracts, or marked "not adopted" with a stated reason. If an automated CLI gate or architecture validator already enforces a rule, cite that gate.

| # | Rule | Why | Goes into |
|---|---|---|---|
| A1 | **Separate contracts, domain entities, and storage/DTO models.** External transport schemas/DTOs and persistence models are distinct from internal domain contracts; map explicitly at layer boundaries. | Exposing storage or transport models across layers couples external contracts to internal schema changes and leaks unintended fields. | `SKILL`, `01`, `02` |
| A2 | **Thin delivery / entry boundary.** Entry handlers (controllers, routes, screens, views, CLI commands) validate/bind input, invoke one use case / application service action, and render/return the result—no raw persistence queries, transaction commits, or embedded domain rules. | Keeps business rules reusable across entrypoints and testable without UI or transport scaffolding. | `SKILL`, `01`, `02` |
| A3 | **Single owner for unit-of-work and state transitions.** The application service / use case / state holder owns transaction boundaries and state mutations; data/repository layers execute queries and flush/map results without committing or mutating UI state on their own. | One action = one atomic unit of work or state transition; partial failures leave no inconsistent state behind. | `SKILL`, `02` |
| A4 | **Scoped lifecycle for stateful resources.** Database sessions, network clients, and state controllers are scoped to the request or view lifecycle and disposed deterministically—never stored as mutable module-level globals or shared unsafely across concurrent tasks. | Prevents race conditions, connection leaks, and stale state across requests or screens. | `SKILL`, `02` |
| A5 | **Explicit dependency injection and composition root.** Wire dependencies through the workspace's designated composition root / DI mechanism in topological order (Leaf mappers/clients → Data sources/Repositories → Use cases/Services → Entry handlers/State holders). | Makes dependencies explicit and replaceable in tests without monkey-patching internals. | `SKILL`, `01`, `02` |
| A6 | **Domain errors cross boundaries cleanly.** Inner layers raise or return typed domain/application failures; only the outermost delivery boundary translates them into transport status codes or user-facing UI feedback. | Inner layers remain independent of delivery protocols and UI presentation. | `SKILL`, `02` |
| A7 | **Pure import and bootstrap sequence.** Importing a module must not read environment variables, open network/database connections, or trigger heavy I/O; configuration and long-lived resources are initialized in the explicit startup/lifespan hook and torn down on exit (`clean-code` C12). | Allows tests, analyzers, and CLI tools to import any module safely without live infrastructure. | `SKILL`, `01`, `02` |
| A8 | **Explicit module and cross-feature boundaries.** A feature module communicates with another feature only through its published contract (public service/use case or domain contract), never by importing another feature's internal data models, private state, or implementation files (`clean-code` C17). | Prevents tangled cross-feature coupling and preserves independent module evolution. | `SKILL`, `02` |
| A9 | **Explicit data loading and no hidden I/O.** Declare relationship/nested data loading explicitly in repositories/data sources and forbid implicit lazy-loading during serialization or UI rendering. | Hidden lazy loads trigger N+1 queries or runtime async context errors outside the data layer. | `SKILL`, `02` |
| A10 | **No speculative layers or single-implementation wrappers.** Introduce an interface/port or layer file only when required by the approved feature or when multiple implementations (e.g., production adapter + test fake) exist (`clean-code` C1). | Unused pass-through layers add indirection and maintenance cost without architectural benefit. | `SKILL`, `01`, `03` |

**Mandatory rules (never "not adopted"):** A1, A2, A3, A5, A6, A7, A8, A10.

---

## Unified Tool Gate (`PASS` / `FAIL`) & Review Severity (`BLOCKER` / `MAJOR` / `MINOR`)

Automated architecture checks (import-boundary linters, architecture validators, static analyzers, `rg` boundary scans) are strictly binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`). Architectural rules written in the skill are mandatory compliance; reviewers grade violations on the unified 3-tier scale (`shared_contracts/flags_and_statuses.md` §2):

| Severity | Meaning | Review Verdict Impact |
|---|---|---|
| `BLOCKER` | Any failed architecture validator or import-linter gate (`FAIL`), upward/forbidden layer import, missing unit-of-work/lifecycle cleanup, or violation of a mandatory architecture rule (A1–A8, A10) | `CHANGES_REQUESTED` (blocks approval) |
| `MAJOR` | Misplaced file/responsibility, unapproved cross-module coupling, or oversized module needing decomposition (A9, splitting rules) | Must be fixed in the same revision when inside task scope |
| `MINOR` | Non-blocking structural polish or naming alignment within the right layer | Optional (never blocks approval) |

Reviewers grade only files created or modified in the current phase diff; pre-existing architectural drift outside the diff is recorded in `Concerns`, never as a blocker.
