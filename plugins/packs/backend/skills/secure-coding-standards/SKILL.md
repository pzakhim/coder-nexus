---
name: secure-coding-standards
description: Secure coding standards for a Backend (Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2 async, PostgreSQL) service — covering boundary input validation, object-level authorization, tenant/owner data-scope isolation, secrets and PII protection, cryptography, injection/SSRF/upload defenses, dependency auditing, deterministic PASS/FAIL gates, and BLOCKER/MAJOR/MINOR review grading.
---

# Secure Coding Standards — Backend (FastAPI · Pydantic v2 · SQLAlchemy 2 Async)

Use this skill when writing or reviewing backend code that touches endpoints, schemas, authentication, authorization, repository queries, settings/secrets, logging, background jobs, outbound HTTP calls, file uploads, or dependencies. Where each guard lives follows `{{slot:clean-architecture}}`.

---

## 1. Deterministic Security Gates (`PASS` / `FAIL`)

Run these checks on touched files before handoff (`READY_FOR_REVIEW`) and during Code Review. Each gate produces a binary **`PASS`** or **`FAIL`** status (`plugins/shared_contracts/flags_and_statuses.md` §1; mark `NOT_RUN` with an explicit reason only when a tool/network is unavailable—never `PASS` when unrun):

| Check | Command | Gate Status |
|---|---|---|
| **Static Security Linter (`flake8-bandit`)** | `uv run ruff check --select S app/ tests/` | `PASS` / `FAIL` |
| **Injection & Unsafe Deserialization Audit (`rg`)** | `rg -n 'text\(f"|execute\(f"|shell=True|yaml\.load\(|pickle\.loads?\(|eval\(|exec\(' app/` (expect 0 matches) | `PASS` / `FAIL` |
| **Mass Assignment Audit (`rg`)** | `rg -n '\*\*\w+\.(model_dump|dict)\(\)' app/` (expect 0 matches) | `PASS` / `FAIL` |
| **CORS / Debug / TLS Bypass Audit (`rg`)** | `rg -n 'allow_origins=\["\*"\]|debug=True|verify=False|follow_redirects=True' app/` (expect 0 matches) | `PASS` / `FAIL` |
| **Sensitive Logging Audit (`rg`)** | `rg -n -i '(logger|logging)\.\w+\(.*(token|password|secret|authorization)' app/` (expect 0 matches) | `PASS` / `FAIL` |
| **Lockfile & Dependency Advisory Audit** | `uv lock --check && uv run pip-audit` | `PASS` / `FAIL` |

---

## 2. Core Security Rules (`SC1`–`SC14` — Mandatory Compliance)

All 14 rules are **mandatory compliance** (`SC1`, `SC2`, `SC3`, `SC4`, `SC6`, and `SC13` have zero exceptions). During Code Review, findings are graded on the unified 3-tier scale (`BLOCKER` / `MAJOR` / `MINOR` — see [03-runtime-risks-deps-and-review.md](references/03-runtime-risks-deps-and-review.md)):

| ID | Rule | FastAPI / Pydantic / SQLAlchemy Contract | Reference |
|---|---|---|---|
| **SC1** | **Validate Untrusted Input at the Boundary** | Validate all request bodies, query/path params, webhooks, and queue payloads with Pydantic v2 schemas (`ConfigDict(extra="forbid")`); separate `*Create`/`*Update` from `*Read`; bound list/page limits (`Query(ge=1, le=MAX_PAGE_SIZE)`); reject invalid input instead of repairing | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md) |
| **SC2** | **Authorize Every Operation per Object** | Authenticate on the router (`CurrentUserDep`), but enforce object-level and capability-level authorization inside the Service (`app/services/`) against the loaded record; never scatter `if user.role == "admin"` in routers | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md) |
| **SC3** | **Isolate Data Scopes Explicitly** | Pass `tenant_id` / `owner_id` / environment scope explicitly from `CurrentUser` → Service → Repository and filter every `select`, `update`, `delete`, cache key, and background job; never call unscoped `session.get(Model, id)` on scoped tables | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md) |
| **SC4** | **Prevent Injection (`SQL`, `Shell`, `Path`, `YAML`)** | Use SQLAlchemy ORM expressions or bound parameters (`text("... :id")`), allow-list dicts for dynamic `ORDER BY` columns, argument lists without `shell=True`, `Path.resolve().is_relative_to(BASE)`, and `yaml.safe_load` | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC5** | **Encode Output & Validate Redirects** | Declare `response_model=` on every route; sanitize untrusted HTML with `nh3`; validate `RedirectResponse` targets against an explicit host/path allow-list | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md), [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC6** | **Keep Secrets Secret** | Load secrets only via `Settings(BaseSettings)` fields typed `SecretStr` from env / git-ignored `.env`; never commit secrets in code, fixtures, or Alembic migrations; rotate any exposed secret immediately | [02 — Secrets, Data & Crypto](references/02-secrets-data-and-crypto.md) |
| **SC7** | **Use Verified Authentication** | Decode JWTs with pinned `algorithms=[settings.jwt_algorithm]`, `audience`, `issuer`, and `options={"require": ["exp", "sub"]}`; hash passwords with Argon2/bcrypt (`pwdlib`) and verify a dummy hash for unknown users | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md) |
| **SC8** | **Redact Sensitive Data & PII from Logs & Errors** | Log `request_id`, `actor_id`, `tenant_id`, and status codes—never tokens, passwords, `Authorization` headers, or PII; return generic 500 error bodies with `request_id` (never `str(exc)` or tracebacks) | [02 — Secrets, Data & Crypto](references/02-secrets-data-and-crypto.md) |
| **SC9** | **Guard Outbound Calls (`SSRF` & `TLS`)** | Validate user-influenced URLs against scheme (`https`), host allow-lists, and global IP checks; set explicit `timeout=`, `follow_redirects=False`, and keep TLS `verify=True` on `httpx.AsyncClient` | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC10** | **Handle File Uploads Defensively** | Enforce byte-size caps (`read(MAX_BYTES + 1)`), sniff content types by magic bytes, generate UUID filenames, and store outside publicly served paths | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC11** | **Vet Dependencies & Lock Supply Chain** | Require design approval before changing `pyproject.toml`; keep `uv.lock` synchronized (`uv lock --check`) and audit advisories with `uv run pip-audit` | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC12** | **Use Vetted Cryptography & CSPRNG** | Generate tokens/nonces with `secrets.token_urlsafe(32)`, compare digests with `hmac.compare_digest`, and encrypt with vetted `cryptography` (Fernet / AES-GCM) | [02 — Secrets, Data & Crypto](references/02-secrets-data-and-crypto.md) |
| **SC13** | **Fail Closed** | Any exception in validation, auth, or upstream dependencies denies the request (`401`/`403`/`404`/`503`)—never catch and return `[]` or permissive fallback data | [01 — Input, Auth & Data Scope](references/01-input-auth-and-data-scope.md), [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |
| **SC14** | **Flag Security-Sensitive Changes in Handoff** | List every security touchpoint and its protecting guard in the Code Writer handoff (`work-item-contract`) | [03 — Runtime Risks, Deps & Review](references/03-runtime-risks-deps-and-review.md) |

---

## 3. Reference Guides

Load only the reference file needed for the current task:

| Reference | Topics Covered |
|---|---|
| [01 — Input, Authentication, Authorization & Data Scope](references/01-input-auth-and-data-scope.md) | Trust boundaries, Pydantic `extra="forbid"` input/output separation (`SC1`, `SC5`), router auth vs. service per-object authorization (`SC2`), tenant/owner/env repository scope isolation (`SC3`), JWT/Argon2 auth (`SC7`), and fail-closed rules (`SC13`) |
| [02 — Secrets, Sensitive Data & Cryptography](references/02-secrets-data-and-crypto.md) | `SecretStr` settings & `.env` hygiene (`SC6`), PII/log/error redaction (`SC8`), and `secrets` / `hmac.compare_digest` / vetted cryptography (`SC12`) |
| [03 — Runtime Risks, Dependencies & Review Rubric](references/03-runtime-risks-deps-and-review.md) | Unsafe-vs-safe patterns for SQL/shell/path/YAML injection (`SC4`), SSRF (`SC9`), file uploads (`SC10`), CORS/debug (`SC13`), `pip-audit` (`SC11`), `SC14` handoff triggers, and `BLOCKER` / `MAJOR` / `MINOR` review rubric |
<!-- {{profile_references}} -->
