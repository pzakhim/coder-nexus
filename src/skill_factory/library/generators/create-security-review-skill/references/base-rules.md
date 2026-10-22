# Base rules (generic, every workspace)

A threat-focused review of a fixed revision. Each rule goes into the generated skill with the workspace's auth model, scopes, tools and vocabulary **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| SR1 | **Triggered scope on a fixed revision, read-only.** Run for changes matching the review triggers (and always for risky areas); review the exact revision; never edit code or tests. | Security review must target the code that ships and stay independent of it. | 01 |
| SR2 | **Threat model per change.** Assets, actors (roles, anonymous, other tenants), entry points, trust boundaries crossed, and what could go wrong (STRIDE-lite) — a few lines, specific to this change. | Checklists miss abuse paths that a two-minute "who could misuse this" finds. | 02 |
| SR3 | **Authorization matrix.** For each changed operation: role × environment × action × object (own/other tenant/other owner) → expected allow/deny, and the evidence (test, code path). | Broken access control hides in the cells nobody wrote down. | 03 |
| SR4 | **Data-scope isolation.** Every changed query, cache key, file path, background job and export carries its scope; cross-scope reads/writes are impossible by construction. | One missing filter leaks another customer's data. | 03 |
| SR5 | **Injection and deserialization.** SQL/shell/template/path/regex built from input; unsafe deserialization (pickle, yaml.load); mass assignment. | Injection turns data into code. | 04 |
| SR6 | **Client-side risks** (frontend): XSS, open redirects, secrets in bundles, token storage, CSRF, trusting UI-only checks. | The browser is attacker-controlled. | 04 (fe) |
| SR7 | **Secrets and personal data.** In code, config, fixtures, logs, error messages, responses and the diff's history; encryption at rest where required. | Leaks are permanent. | 04 |
| SR8 | **Outbound calls and files.** SSRF (user-supplied URLs, redirects, internal ranges), timeouts; uploads and parsers (type, size, storage, execution). | Classic entry points into internal systems. | 04 (be) |
| SR9 | **Dependencies.** New or upgraded packages: need, maintenance, advisories (run the audit tool if installed). | Supply-chain risk enters through the lock file. | 04 |
| SR10 | **Crypto and auth flows.** Platform crypto only, secure random, session/token lifetime and invalidation, password/credential handling. | Subtle flaws here defeat every other control. | 04 |
| SR11 | **Exploit-scenario findings.** `given <attacker/role/state> → when <action> → then <impact>` with concrete values; `CONFIRMED` (path traced or demonstrated safely) or `PLAUSIBLE` (name the missing evidence); severity `CRITICAL`/`HIGH`/`MEDIUM`/`LOW`; fix direction. No scenario, no finding. | Scenarios are actionable and testable; generic advice is noise. | 05 |
| SR12 | **Security sign-off.** CONFIRMED CRITICAL/HIGH → `CHANGES_REQUESTED`; PLAUSIBLE CRITICAL/HIGH → `BLOCKED` until the evidence arrives; MEDIUM/LOW listed, fixed when cheap. Map to the workspace's verdict words. | Clear criteria keep security from being either ignored or endless. | 05 |
| SR13 | **Safe testing only.** No exploitation of shared or production environments, no real credentials or personal data in reports; verify with existing tests, local/disposable stacks or read-only reasoning; share findings only through the approved channel. | A security review must not cause the incident it is looking for. | 01, 06 |
| SR14 | **Hand-over and feedback.** With a Security role, bug-hunt dimension 5 is handed over here; recurring finding types become rules in secure-coding-standards (promote to the base when general). | Fixing the class, not just the instance, is what improves security over time. | 01, 06 |

**Never "not adopted":** SR1, SR3, SR4, SR11, SR12, SR13.
