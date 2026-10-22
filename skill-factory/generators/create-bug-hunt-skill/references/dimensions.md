# The seven defect dimensions

Walk the scope once per dimension. Prompts are starting points; the generated skill adds the workspace's examples.

| # | Dimension | Ask |
|---|---|---|
| 1 | **Logic and data flow** | Wrong condition or operator? Off-by-one? Inverted flag? Wrong variable? Value lost or overwritten? Unit, timezone or rounding mismatch? |
| 2 | **Error and edge paths** | Null/missing key? Empty collection? First/last page? Failed external call, timeout, retry, partial success? Validation bypassed on some path? |
| 3 | **State, async and lifecycle** | Awaits in the right order (and awaited at all)? Work after commit/rollback/dispose? Stale response overwriting a newer one? Double submit? Resource or connection not released? Shared mutable state? |
| 4 | **Contract and caller breakage** | Do callers now receive another type, null, error or status? Do serialized keys, routes or events still match the other side (FE ↔ BE, producer ↔ consumer)? |
| 5 | **Security, scope and data safety** | Authorization checked on the object, not just the route? Data scope (tenant, environment, owner) enforced? Injection (SQL, shell, template)? Secrets or personal data in logs or responses? Unsafe parsing silently substituting data? |
| 6 | **Stack and project bug patterns** | Every applicable item in the workspace's `05-bug-patterns.md`. No patterns file for a stack → record `N/A` with the reason; the other dimensions still run. |
| 7 | **Test blind spots** | For each surviving candidate: would an existing test fail if it were real? If not, record the missing test with the finding. |

`quick` effort runs dimensions 1–4 on the changed hunks only.
