# 02 — Secrets, Sensitive Data & Cryptography

> Scope: Secret configuration (`SC6`), PII/log/error redaction (`SC8`), and vetted cryptography & CSPRNG (`SC12`).

---

## 1. Secrets Management (`SC6`)

1. **Typed `SecretStr` settings:** Load all credentials, signing keys, and database URLs exclusively through `Settings(BaseSettings)` (`pydantic-settings`) fields typed `SecretStr`, sourced from environment variables or a git-ignored `.env`.
2. **Unwrap at point of use only:** Call `.get_secret_value()` only on the exact line that passes the secret to the driver/client so `SecretStr` masks as `**********` in logs and tracebacks.
3. **Zero secrets in source or artifacts:** Never place real secrets in Python source, test fixtures, Alembic migrations, OpenAPI examples, URLs, or Dockerfiles. Test fixtures must use clearly synthetic values (`"test-secret-not-real"`).
4. **Git-ignore verification:** Ensure `.env` and `.env.*` (except a value-free `.env.example`) are git-ignored (`git check-ignore .env`).
5. **Rotate on exposure:** Any secret committed to Git history, printed in logs, or pasted into a ticket/screenshot must be **rotated immediately**, not merely deleted from the file.

```python
# Unsafe
JWT_SECRET = "change-me"                               # Hardcoded secret (ruff S105)
logger.info("settings loaded %s", settings)            # Dumps full configuration
logger.debug("headers %s", request.headers)            # Leaks Authorization header

# Safe
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: SecretStr
    jwt_secret: SecretStr
    jwt_algorithm: Literal["HS256", "RS256"] = "HS256"

logger.info("settings loaded", extra={"environment": settings.environment})
```

---

## 2. Sensitive Data, Logs & Error Redaction (`SC8`)

**Sensitive data includes:** credentials, tokens, API keys, session IDs, passwords/hashes, personal data (names, emails, phone numbers, addresses, national IDs), payment instruments, and confidential business documents.

1. **Structured logs:** Log correlation context (`request_id`, `actor_id`, `tenant_id`, route, HTTP status, duration_ms). Never log tokens, passwords, `Authorization`/`Cookie` headers, full request/response payloads, or unmasked PII.
2. **Generic 500 error responses:** Return a generic error body with `request_id`; log the exception server-side only. Never expose `str(exc)` or `traceback.format_exc()` to clients (OWASP API8).
3. **Scoped caches:** Store minimal identifiers rather than raw PII when possible, and prefix every cache key with its `tenant_id` / `owner_id` scope ([01](01-input-auth-and-data-scope.md#data-scopes-sc3)).

```python
# Unsafe: leaks internal database/provider error strings and stack traces to caller
@app.exception_handler(Exception)
async def handle_error(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({"error": str(exc), "trace": traceback.format_exc()}, status_code=500)

# Safe: logs traceback internally with request_id; returns generic envelope to caller
@app.exception_handler(Exception)
async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception("unhandled_error", extra={"request_id": request_id, "path": request.url.path})
    return JSONResponse({"code": "internal_error", "request_id": request_id}, status_code=500)
```

---

## 3. Cryptography & Secure Randomness (`SC12`)

- **Password hashing:** Argon2 or bcrypt via the workspace's vetted library (`pwdlib`).
- **Tokens, reset codes & nonces:** Use `secrets.token_urlsafe(32)` or `secrets.token_bytes(32)` — never `random` (`ruff S311`).
- **Constant-time comparison:** Always use `hmac.compare_digest(a, b)` when comparing signatures, webhook secrets, or digests — never `==`.
- **Integrity hashing:** Use `hashlib.sha256`; never use `md5` or `sha1` for security (`ruff S324`).
- **Encryption at rest:** Use vetted `cryptography` primitives (Fernet / AES-GCM) via the workspace's encryption helper with keys loaded from `SecretStr`.
