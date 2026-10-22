# Base rules (generic, every workspace)

Secure-by-default rules for code being written. Aligned with common OWASP guidance (Top 10, ASVS) in plain terms. Each rule goes into the generated skill with the workspace's real guards, scopes and helpers **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| SC1 | **Validate untrusted input at the trust boundary.** Schema/type, allow-lists, length and size limits; reject invalid input instead of guessing a fix. | Every injection, overflow and logic abuse starts with input nobody checked. | 01 |
| SC2 | **Authorize every operation on the server, per object.** Check the actor may do this action on *this* record (owner, tenant, role/capability), deny by default; UI hiding is never authorization. | Broken access control is the most common serious web flaw. | 02 |
| SC3 | **Isolate data scopes.** Every query, cache key, file path and background job carries the scope (tenant, environment, owner, release state); never infer a default scope. | One missing filter leaks another customer's data. | 02 |
| SC4 | **No injection.** Parameterised queries; no string-built SQL, shell commands, templates, regexes or paths from input; safe path joins (no traversal); never `eval`/dynamic import of input. | Injection turns data into code. | 04 |
| SC5 | **Encode output.** Rely on framework auto-escaping; untrusted HTML only through a sanitiser; validate URLs before using them in links/redirects. | XSS and open redirects run attacker code in your users' sessions. | 04 (fe) |
| SC6 | **Keep secrets secret.** Never in code, commits, logs, URLs, client bundles, error messages or test fixtures; load from the settings/secret store; encrypt at rest when stored. | Leaked secrets cannot be un-leaked; rotation is costly. | 03 |
| SC7 | **Use the workspace's authentication, not your own.** Sessions/tokens via the existing mechanism; secure cookie flags; CSRF protection when cookies authenticate; no homemade token formats. | Hand-rolled auth is where account takeovers come from. | 02, 04 |
| SC8 | **No sensitive data in logs or user errors.** Users get a generic message (+ request id); logs get context without tokens, passwords or personal data. | Logs and error pages are read by more people than the database. | 03 |
| SC9 | **Control outbound calls.** User-supplied URLs go through the allow-list/SSRF guard; timeouts on every call; no following redirects into internal ranges. | SSRF reaches internal services and cloud metadata. | 04 (be) |
| SC10 | **Handle files defensively.** Type and size limits, safe parsers, no execution, storage outside served paths, generated names; never silently substitute data on a parse error. | Uploads and parsers are a classic entry point. | 04 (be) |
| SC11 | **Dependencies with care.** New dependency only with a reason; locked versions; check advisories; avoid abandoned packages. | Every dependency is code you run without reading it. | 05 |
| SC12 | **Use platform cryptography.** Vetted libraries for hashing (e.g. argon2/bcrypt), encryption and random; never homemade crypto or `Math.random`/`random` for secrets. | Crypto mistakes are invisible until exploited. | 03, 04 |
| SC13 | **Fail closed.** If validation or an authorization check errors, deny; never "allow on exception" or skip a guard on a fallback path. | Attackers aim for the error path. | 02 |
| SC14 | **Flag security-relevant changes.** Auth, guards, scopes, sensitive data, crypto, file/URL handling, new dependencies → named in the handoff for the reviewer/security role. | Reviewers spend extra attention where it matters only if they know where it is. | 06 |

**Never "not adopted":** SC1, SC2, SC3, SC4, SC6, SC13.
