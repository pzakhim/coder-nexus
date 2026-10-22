# Security checks and read-only tools by stack

Checks for `04-checks.md`. Link the workspace's secure-coding-standards for the safe patterns; this file lists what to *look for* and which tools help. Run a tool only if it is installed; never install one without the user's agreement.

## Backend (Python / FastAPI and similar)

| Look for | How |
|---|---|
| Missing or wrong guard on a changed operation | Trace route → use case → guard call; compare with the authorization matrix |
| Query/cache/job without its scope | Read every changed query and cache key for the scope columns |
| String-built SQL / shell / paths | `rg -n "f\"SELECT|f'SELECT|shell=True|\.format\(.*(SELECT|INSERT|UPDATE|DELETE)" <changed files>` |
| Unsafe deserialization | `rg -n "pickle\.loads|yaml\.load\(|eval\(|exec\(" <changed files>` |
| Outbound calls with user URLs | Changed `httpx`/`requests` calls → is the workspace's network guard used? timeout set? |
| Secrets/PII in logs or errors | Changed logging and exception messages |
| Tools | `bandit -r <paths>`, `semgrep --config auto <paths>`, `pip-audit` / `uv pip audit`, `gitleaks detect --no-git -s <paths>` |

## Frontend (TypeScript / React / Next.js)

| Look for | How |
|---|---|
| Raw HTML from user content | `rg -n "dangerouslySetInnerHTML|innerHTML" <changed files>` |
| Redirects from params | `rg -n "router\.(push|replace)\(.*(searchParams|query)" <changed files>` |
| Secrets in the client graph | `NEXT_PUBLIC_*` usage, server-only imports reachable from `'use client'` files |
| Token storage | `localStorage`/`sessionStorage` with tokens |
| UI-only authorization | Role/capability checks without a server guard for the same action |
| Tools | `npm audit --omit=dev`, `eslint` with security plugin if configured, `semgrep` |

## Mobile (Flutter)

Secrets in source/assets, tokens in plain preferences, disabled certificate checks, deep links acting without server validation.

## Evidence without live exploitation

- Prefer existing tests (authorization 401/403 tests, scope tests) — run them read-only on a local/disposable stack.
- Otherwise trace the code path and state it as `PLAUSIBLE` with the evidence that would confirm it.
