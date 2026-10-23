# 03 — Secrets and sensitive data

Why: leaked secrets and personal data cannot be un-leaked, and logs, caches and error pages are read by more people and kept longer than the database (SC6, SC8, SC12).

## Secrets (SC6)

- Loaded only from `Settings(BaseSettings)` (`pydantic-settings`) fields typed `SecretStr`, read from environment variables or the workspace `.env`. Call `.get_secret_value()` only at the line that needs the value. Reason: `SecretStr` prints as `**********` in logs and reprs.
- Never in code, commits, test fixtures, Alembic migrations, URLs, OpenAPI examples, Docker images or client-facing payloads. Fields have no default that contains a real secret.
- `.env`, `.env.*` (except a value-free `.env.example`) are git-ignored; check `git check-ignore .env` when adding one.
- Stored third-party credentials are encrypted at rest with the helper the design names; no homemade encryption.
- A secret that leaked (commit, log, screenshot, ticket) is **rotated**, not just deleted from the file. Reason: Git history and log stores keep the old value.
- Test fixtures use generated or obviously fake values (`"test-secret-not-real"`), never a copy of a real key.

```python
# Unsafe
JWT_SECRET = "change-me"                                     # in source (ruff S105)
logger.info("settings loaded %s", settings)                  # dumps everything
logger.debug("headers %s", request.headers)                  # Authorization header in logs

# Safe
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: SecretStr
    jwt_secret: SecretStr
    jwt_algorithm: Literal["HS256", "RS256"] = "HS256"

logger.info("settings loaded", extra={"environment": settings.environment})
```

## Sensitive data (SC8)

What counts as sensitive: credentials, tokens, API keys, session ids, passwords and hashes, personal data (names, emails, phone numbers, addresses, national ids), payment data, customer documents, and anything the design marks confidential.

- **Logs:** ids and context (`request_id`, `actor_id`, `tenant_id`, route, status, duration) yes; tokens, passwords, `Authorization` and `Cookie` headers, full request or response bodies, personal data no. Reason: log stores have wider access and longer retention.
- **User-facing errors:** a generic body with a request id; details only in server logs. `str(exc)` of a database or provider error never reaches the client. Reason: stack traces reveal paths, queries and library versions (OWASP API8).
- **Caches and analytics** carry the minimum: ids, not personal data; cache keys include the scope (see [02](02-authorization-and-data-scope.md#data-scopes-sc3)).
- **Responses** return only fields in the `response_model`; no password hash, internal flag or other tenant's data.

```python
# Unsafe
@app.exception_handler(Exception)
async def handler(request, exc):
    return JSONResponse({"error": str(exc), "trace": traceback.format_exc()}, status_code=500)

# Safe
@app.exception_handler(Exception)
async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
    request_id = request.state.request_id
    logger.exception("unhandled error", extra={"request_id": request_id, "path": request.url.path})
    return JSONResponse({"code": "internal_error", "request_id": request_id}, status_code=500)
```

Domain errors map to the contract's error codes in one handler (`api-contract-design`).

## Cryptography and random (SC12)

- Password hashing: Argon2 or bcrypt through the workspace's vetted library ([02](02-authorization-and-data-scope.md#authentication-sc7)).
- Tokens, reset codes, API keys: `secrets.token_urlsafe(32)` / `secrets.token_bytes`, never `random` (ruff S311). Reason: `random` is predictable.
- Comparing secrets or signatures: `hmac.compare_digest`, never `==`. Reason: `==` leaks timing.
- Hashes for integrity: `hashlib.sha256`; `md5` / `sha1` only with `usedforsecurity=False` for non-security checksums (ruff S324).
- Encryption: a vetted library (for example `cryptography`'s Fernet / AES-GCM) through the helper the design names; never homemade crypto or a hardcoded key.
