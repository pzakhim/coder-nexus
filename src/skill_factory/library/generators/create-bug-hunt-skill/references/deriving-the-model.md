# Deriving the Bug-Hunt Model for Target Stacks

> Topic: Translating the 7 defect dimensions and workspace risk areas into stack-specific bug patterns and disproof checks

## 1. The Seven Defect Dimensions (`H5`)

Walk the fixed scope once per dimension. The generated skill adapts the prompts below to the target stack's runtime, framework, and architecture:

| # | Dimension | Core Question | How to Adapt to the Target Stack |
|---|---|---|---|
| **1** | **Logic and data flow** | Wrong condition or operator? Off-by-one? Inverted flag? Wrong variable? Value lost or overwritten? Unit, timezone, or rounding mismatch? | Name the stack's numeric/decimal types, falsiness traps, pagination index convention (0-based vs 1-based), and timezone handling. |
| **2** | **Error and edge paths** | Null/missing key? Empty collection? First/last page? Failed external call, timeout, retry, partial success? Validation bypassed on a secondary path? | Name how the stack represents absent values, empty query/list results, network timeouts, and partial batch writes. |
| **3** | **State, async, and lifecycle** | Awaits in the right order (and awaited at all)? Work after commit/rollback/dispose/unmount? Stale response overwriting a newer one? Double submit? Resource/subscription/session not released? Shared mutable state? | Name the stack's async primitives, transaction/session boundaries, UI/component mount lifecycle, and stream/timer/client cleanup hooks. |
| **4** | **Contract and caller breakage** | Do callers now receive another type, null, error, status, or state? Do serialized keys, routes, or events still match the other side? | Name the public symbol boundaries in the workspace (function signatures, DTO/schema fields, route arguments, state classes, DB migrations) and the exact `rg` / code-intelligence commands to locate callers. |
| **5** | **Security, scope, and data safety** | Authorization checked on the object, not just the entry point? Data scope (tenant, environment, owner) enforced? Injection? Secrets or PII in logs/responses/storage? Unsafe parsing silently substituting defaults? | Name the workspace's auth guard mechanism, tenant/owner scoping convention, secret storage rules, and safe parsing utilities. |
| **6** | **Stack and project bug patterns** | Does the diff hit any known failure mode in the stack/project pattern tables (`01-scope-dimensions-and-patterns.md`)? | Populate 3–5 categorized tables (*Looks like* → *Goes wrong when* → *Check*) covering the stack's async/lifecycle, data/storage, framework/UI, and project-specific risk areas. |
| **7** | **Test blind spots** | Would an existing test fail if this candidate were real? Are mocks/fakes hiding the bug? | Name common false-green test traps in the stack (over-mocked repositories/cubits, skipped async assertions, missing error-branch tests) and require naming the missing regression test. |

`quick` effort runs dimensions **1–4** on changed hunks only. `standard` and `deep` run dimensions **1–7**.

---

## 2. Deriving Project-Specific Bug Patterns (`Dimension 6`)

Inspect `CLAUDE.md`, `AGENTS.md`, architecture docs, and recent bug-fix commits (`git log --grep="fix" -n 20`) to derive concrete pattern rows for the workspace:

| Workspace Risk Area | Pattern Row to Derive (*Looks like* → *Goes wrong when* → *Check*) |
|---|---|
| **Multi-tenant / owner data scope** | Query, cache, or local storage lookup missing the tenant/owner/environment filter → leaks or overwrites another scope's data → check every query/cache key for scope binding |
| **Lifecycle & state holders** | Async callback mutating state or UI after disposal/close, or in-place mutation of an immutable state collection → crash or silent UI non-rebuild → check lifecycle guards and state equality |
| **Transactions & multi-step mutations** | Partial write committed before a subsequent step fails, or external side-effect fired before commit → inconsistent state on failure → check transaction/unit-of-work boundaries |
| **Serialization & boundary parsing** | Unsafe cast or silent default on nullable/mistyped external payload fields → runtime type crash or silent data corruption → check schema validation and safe parser usage |
| **Concurrency & idempotency** | Rapid user taps, retried webhook/job, or concurrent requests executing non-idempotent state transitions → duplicate records or lost updates → check loading/lock guards and idempotency keys |
| **Schema & state migrations** | Non-null column/field added without default/migration, or destructive rename while readers still expect old shape → upgrade or runtime failure → check migration compatibility |

---

## 3. Deriving Typical Disproofs (`02-verify-and-disprove.md`)

For every target stack, include a **Typical Disproofs** table in `02-verify-and-disprove.md` showing common false alarms and what upstream guard refutes them (e.g., schema/type validation at the entry boundary, framework lifecycle auto-cleanup, database constraint + conflict handler, or parent widget constraint), reminding the agent to **verify the guard in actual code rather than assuming it exists**.
