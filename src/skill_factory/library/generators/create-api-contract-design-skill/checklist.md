# Checklist — api-contract-design

Run this checklist alongside [../../core/checklist-common.md](../../core/checklist-common.md):

- [ ] All mandatory rules **AP1–AP9** are enforced (zero `"not adopted"` carve-outs)
- [ ] Contract source of truth (`design.md` API section + generated `openapi.json` snapshot) is explicit and never hand-edited
- [ ] Route conventions, separate input/output schemas (`extra="forbid"` on inputs), and the single centralized error envelope are defined with concrete examples
- [ ] Bounded pagination (`limit` max cap + deterministic tie-breaker sort) and allow-listed filter/sort fields are specified
- [ ] Every endpoint rule enforces explicit authentication declarations (`security` in OpenAPI), RBAC, and anti-IDOR data-scope isolation (`404` when an object belongs to another tenant/scope)
- [ ] Retried mutations define atomic `Idempotency-Key` claiming, payload-mismatch rejection (`409` / `422`), in-flight duplicate handling, and timeout-as-unknown-outcome rules
- [ ] Additive vs. breaking classification table, Hyrum's Law, One-Version Rule, and the breaking-change `D-NN` transition protocol are included
- [ ] CLI verification gates use binary **`PASS` / `FAIL`** flags and review findings use **`BLOCKER` / `MAJOR` / `MINOR`** (`shared_contracts/flags_and_statuses.md`)
- [ ] Cohesive 3-file `references/` layout (`01-conventions-schemas-and-idempotency.md`, `02-auth-scopes-and-compatibility.md`, `03-snapshot-handshake-and-review.md`) with zero hardcoded `be_dir` / `fe_dir`
