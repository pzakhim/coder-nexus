# Deriving the Code Review Model for Target Stacks

> Topic: Translating R1–R14 into stack-specific verification gates, review axes, and rubric linkages

## 1. Deriving Deterministic Verification Gates (`01-scope-gates-and-validators.md`)

Identify the workspace's read-only verification tools and wire them into `01-scope-gates-and-validators.md`:

| Gate Category | What to Discover in the Workspace | Gate Output |
|---|---|---|
| **Preparation / Mock Gate (`PHASE-00`)** | Contract/mock server definition files (e.g., `mocks/*_mockoon.json`, OpenAPI/contract fixtures) and how they map to `design.md` trigger tables | `PASS` / `FAIL` (`N/A` when phase has no mock prep) |
| **Architecture & Boundary Validators** | MCP architecture validators (`validate_architecture_code`, `validate_module_architecture`), import-linter, dependency-cruiser, or custom boundary scripts | `PASS` / `FAIL` (handle `UNVERIFIED` via manual inspection + static analyzer) |
| **Static Analyzer & Typechecker** | Stack compiler/analyzer and linter commands (e.g., `flutter analyze`, `ruff check`, `mypy`, `bandit`, `tsc --noEmit`, `golangci-lint`) | `PASS` / `FAIL` (`exit 0`) |
| **Independent Test Execution** | Focused and module test commands rerun by the reviewer on `REVIEW_REVISION` | `PASS` / `FAIL` |
| **Schema / Migration / Visual Verification** | Offline migration SQL check (`alembic upgrade --sql`), API contract diff, or runtime visual inspection (`visual-quality` when UI is touched) | `PASS` / `FAIL` / `N/A` |

---

## 2. Deriving the Five Review Axes (`02-review-axes-and-rubric.md`)

Map the stack's rubric skills to 5 cohesive review axes so the Reviewer checks every dimension without duplicating rule text:

| Axis | Core Audit Focus | Linked Rubric Skill | Typical `BLOCKER` / `MAJOR` Triggers |
|---|---|---|---|
| **1. Plan, Scope & AC Traceability** | Tasks ticked `- [x]` with real evidence; locked decisions (`D-NN`) honored; every AC mapped to code + test; no out-of-scope edits; zero fake/mocked data sources inside production source (`lib/` or `app/`) | `incremental-implementation`, `work-item-contract` | Untraced AC; contradicted `D-NN` decision; fake/mock provider committed inside production code |
| **2. Clean Architecture & Boundaries** | Dependency direction points inward; Domain stays pure; transaction/unit-of-work or state/screen contracts respected; DI lifetimes and cross-module boundaries (`CRX-001..004`) clean | `{{slot:clean-architecture}}` | Domain importing framework/ORM/UI; cross-module private import; transaction committed inside repository; screen/state lifecycle contract broken |
| **3. Code Quality & Simplicity** | Naming, function focus, explicit error propagation, type safety, zero leftover debug code (`print`, `breakpoint`), no redundant wrappers | `{{slot:clean-code}}`, `{{slot:code-simplification}}` | Swallowed exceptions returning fake empty success; leftover debug statements; untyped/unsafe casts |
| **4. Adversarial Unit & Integration Tests** | Happy + negative + edge/boundary coverage per changed behavior; test doubles only at architectural seams; `TEST-TAMPER-001` check (no deleted/weakened assertions) | `{{slot:unit-testing}}` | Happy-path-only tests ignoring 4xx/5xx/failure/rollback paths; mocking the unit under test; weakened assertions (`TEST-TAMPER-001`) |
| **5. Security, Contracts, Migrations & UI** | Object-level auth & tenant/owner scoping, secret hygiene, safe parsing (`{{slot:secure-coding-standards}}`); API schema / migration safety (`api-contract-design`, `database-migrations`); or runtime visual fidelity & resource disposal (`{{slot:visual-quality}}`) | `{{slot:secure-coding-standards}}` + stack skills | Missing auth/owner filter (IDOR); SQL/command injection; breaking schema/migration change; undisposed controller/subscription; material visual mismatch against approved UI design |

---

## 3. Handling Profile-Specific Rules (`profiles/<profile>/`)

When a pack supports multiple workspace profiles (`imespro`, `external-structured`, `external-standard`):
- Keep `SKILL.md` and `references/01..03.md` **100% stack-generic**.
- Place profile-specific validator codes, base class checks, and foundation reuse audits inside `profiles/{imespro,external-structured,external-standard}/review-contracts.md` and include `<!-- {{profile_references}} -->` at the bottom of the Reference Guides table in `SKILL.md`.
