# Sources

Ideas rewritten in Coder Nexus vocabulary (SC1–SC14, `BLOCKER` / `MAJOR` / `MINOR`, `CONFIRMED` / `PLAUSIBLE`, `P1`–`P3`, `D-NN`). Nothing is copied.

Internal base inputs (read-only): the Skill Factory generator `create-secure-coding-standards-skill` (`base-rules.md` SC1–SC14, `risks-by-stack.md` Python table, `deriving-the-model.md`, templates); the former stack-neutral `secure-coding` skill and its review checklist (rules, severity mapping, checklist rows); the parked Backend `secure-coding` draft (FastAPI unsafe/safe pairs, OWASP API mapping).

| Source (doc URL + date read) | Idea taken | Where used |
|---|---|---|
| [OWASP API Security Top 10 (2023)](https://api-security.owasp.org/editions/2023/en/0x11-t10), read 2026-10-23 | API1–API10 as the review map | [01](01-trust-boundaries-and-input.md), [02](02-authorization-and-data-scope.md), [04](04-stack-risks.md) |
| [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html), read 2026-10-23 | Algorithm from configuration, never the token header; validate `iss`, `aud`, `exp`; generic error bodies; CORS only for needed origins; 429 / 413 / 415; no tokens in URLs | [02](02-authorization-and-data-scope.md), [03](03-secrets-and-sensitive-data.md), [04](04-stack-risks.md) |
| [FastAPI: OAuth2 with Password and JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), read 2026-10-23 | PyJWT with pinned `algorithms`; `InvalidTokenError` → 401 with `WWW-Authenticate: Bearer`; `pwdlib` with Argon2; dummy-hash verification against username enumeration | [02](02-authorization-and-data-scope.md#authentication-sc7) |
| [Ruff rules: flake8-bandit (`S`)](https://docs.astral.sh/ruff/rules/#flake8-bandit-s), read 2026-10-23 | Rule codes S105, S106, S301, S307, S311, S324, S501, S506, S602, S608 as the static gate | [04 § Gates](04-stack-risks.md#gates) |
| [Pydantic v2 configuration (`extra`)](https://docs.pydantic.dev/latest/api/config/), read 2026-10-23 | `ConfigDict(extra="forbid")` on input schemas; `SecretStr` | [01](01-trust-boundaries-and-input.md), [03](03-secrets-and-sensitive-data.md) |
| [pip-audit](https://pypi.org/project/pip-audit/), read 2026-10-23 | Dependency advisory check | [05](05-dependencies.md) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Security headers (HSTS, CSP, `X-Frame-Options`) as code rules | REST Security Cheat Sheet | Usually set by the gateway or reverse proxy; a service-level change is a `D-NN` |
| API keys on every protected endpoint | REST Security Cheat Sheet | The workspace's auth model decides the credential type (SC7) |
| XML hardening against XXE | REST Security Cheat Sheet | The pack's APIs are JSON; a workspace that parses XML adds it in its own override |
| Hardcoded example `SECRET_KEY` from the tutorial | FastAPI JWT tutorial | Secrets come from settings (`SecretStr`) |
| A specific rate-limiting library | — | Rate limiting belongs to the existing gateway or middleware; adding one is a design decision |
| A separate security sign-off role (`security-review`) | generator SC14 / security skill family | Release 3.2.0 has no security agent; the Code Reviewer runs the checklist |
| `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` security severities | security skill family | Findings use the shared scale in handoff-and-status §9 |
