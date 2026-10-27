# 03 — Runtime Risks, Dependencies, Audit Gates & Review Rubric

> Scope: Injection (`SC4`), output/redirects (`SC5`), outbound SSRF/TLS (`SC9`), file uploads (`SC10`), supply-chain dependencies (`SC11`), CORS/debug (`SC13`), handoff triggers (`SC14`), and the unified `BLOCKER` / `MAJOR` / `MINOR` review rubric.

---

## 1. Backend Stack Risk Matrix — Unsafe vs. Safe (`SC4`, `SC5`, `SC9`, `SC10`, `SC13`)

| Risk | Unsafe Pattern (Forbidden) | Safe Pattern | Rule |
|---|---|---|---|
| **SQL Injection** | `f"SELECT ... {val}"`, `%`, or `+` inside `text()` / `execute()` | SQLAlchemy ORM expressions or `text("... :id")` with bound params | `SC4` |
| **SQL Identifiers** | `order_by(text(request_sort))` | Allow-list dict mapping `Literal[...]` keys to ORM column attributes | `SC4` |
| **Shell Injection** | `subprocess.run(f"...", shell=True)`, `os.system` | Argument list `["cmd", arg]`, `shell=False`, explicit `timeout=` | `SC4` |
| **Path Traversal** | `open(BASE / user_filename)` | Generated UUID names, or `(BASE / name).resolve().is_relative_to(BASE.resolve())` | `SC4`, `SC10` |
| **Unsafe Deserialization** | `yaml.load`, `pickle.loads`, `marshal`, `eval`, `exec` | `yaml.safe_load`; JSON validated through a Pydantic v2 schema | `SC4` |
| **Open Redirect / HTML** | `RedirectResponse(request.query_params["next"])`; unescaped HTML | Allow-list of internal paths/hosts; JSON responses or `nh3` sanitizer | `SC5` |
| **Outbound SSRF & TLS** | `httpx.get(body.url)`, `verify=False`, or missing timeout | Host allow-list + global IP check, `https` only, `follow_redirects=False`, explicit `timeout=` | `SC9` |
| **File Uploads** | `await file.read()` unbounded; trusting `file.filename` | `await file.read(MAX_BYTES + 1)`, magic-byte content sniffing, generated UUID name outside served paths | `SC10` |
| **CORS & Debug** | `FastAPI(debug=True)`, `allow_origins=["*"]` with credentials | `debug=settings.debug` (`False` outside local); explicit origin/method/header lists | `SC13` |

---

## 2. Code Examples: Injection, SSRF & File Uploads

### Injection Prevention (`SC4`)
```python
# Unsafe
await session.execute(text(f"SELECT * FROM orders WHERE number = '{number}'"))
subprocess.run(f"convert {filename} out.pdf", shell=True)

# Safe
await session.execute(text("SELECT id FROM orders WHERE number = :number"), {"number": number})
SORT_COLUMNS = {"created": Order.created_at, "total": Order.total}
stmt = select(Order).order_by(SORT_COLUMNS[sort])  # sort: Literal["created", "total"]
subprocess.run(["convert", str(safe_path), "out.pdf"], check=True, timeout=30)
```

### Outbound SSRF Guard (`SC9`)
```python
def require_allowed_url(raw: str, allowed_hosts: set[str]) -> httpx.URL:
    url = httpx.URL(raw)
    if url.scheme != "https" or url.host not in allowed_hosts:
        raise WebhookUrlNotAllowedError(raw)
    for info in socket.getaddrinfo(url.host, url.port or 443):
        if not ipaddress.ip_address(info[4][0]).is_global:
            raise WebhookUrlNotAllowedError(raw)
    return url

async with httpx.AsyncClient(timeout=settings.http_timeout_seconds, follow_redirects=False) as client:
    resp = await client.post(require_allowed_url(body.webhook_url, settings.allowed_hosts), json=payload)
```

### Bounded File Uploads (`SC10`)
```python
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
ALLOWED_TYPES = {"image/png": ".png", "application/pdf": ".pdf"}

async def store_upload(file: UploadFile, *, tenant_id: UUID) -> StoredFile:
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise UploadTooLargeError()
    ext = ALLOWED_TYPES.get(sniff_content_type(data))
    if ext is None:
        raise UnsupportedUploadTypeError()
    return await storage.put(tenant_id=tenant_id, name=f"{uuid4()}{ext}", data=data)
```

---

## 3. Dependency Supply-Chain Vetting (`SC11`)

1. **Minimize additions:** Add a package to `pyproject.toml` only when standard library or existing dependencies cannot solve the problem, and only with explicit approval (`AGENTS.md` §4).
2. **Lockfile integrity:** Keep `uv.lock` synchronized (`uv lock --check`) and review lockfile diffs alongside `pyproject.toml`.
3. **Vulnerability audit:** Run `uv run pip-audit` (record `NOT_RUN` with reason if sandboxed without network; never mark `PASS` when unrun).

---

## 4. Handoff Triggers (`SC14`) & Review Severity Rubric (`BLOCKER` / `MAJOR` / `MINOR`)

### Handoff Triggers (`SC14`)
In the Code Writer handoff (`work-item-contract`), flag every touched area below together with its guard:
- [ ] Authentication, JWT decoding, sessions, or password hashing (`SC7`)
- [ ] Object-level authorization guards, capability checks, or new/modified routes (`SC2`)
- [ ] Tenant/owner/environment scope filters, cache keys, or background jobs (`SC3`)
- [ ] Alembic migrations touching auth, credential, or scope columns (`SC3`, `SC6`)
- [ ] Settings (`SecretStr`), encryption, logging, or exception handlers (`SC6`, `SC8`, `SC12`)
- [ ] File uploads/parsers, outbound `httpx` calls, redirects, or `subprocess` (`SC4`, `SC5`, `SC9`, `SC10`)
- [ ] CORS, debug flags, or new/upgraded dependencies and `# noqa: S...` suppressions (`SC11`, `SC13`)

### Unified Review Severity Rubric (`BLOCKER` / `MAJOR` / `MINOR`)

Grade all security findings on the unified scale from `plugins/shared_contracts/flags_and_statuses.md` §3 (never use `P1`/`P2`/`P3`):

| Severity | Security Triggers |
|---|---|
| **`BLOCKER`** | • Object-level authorization or tenant/owner data-scope bypass (`SC2`, `SC3`)<br>• SQL, shell, path traversal, or `eval`/`pickle`/`yaml.load` injection (`SC4`)<br>• Authentication bypass, unverified JWT signature, or weak password hash (`SC7`, `SC12`)<br>• Hardcoded secret in source, fixture, migration, or logs (`SC6`)<br>• `verify=False` TLS bypass, `allow_origins=["*"]` with credentials, or fail-open exception handler (`SC9`, `SC13`) |
| **`MAJOR`** | • Request schema missing `ConfigDict(extra="forbid")`, exposing server-owned fields, or unbounded list query (`SC1`)<br>• Role check placed in a router instead of the service, or missing negative authorization test (`SC2`)<br>• Sensitive PII, headers, or raw `str(exc)` tracebacks exposed in logs or error responses (`SC8`)<br>• Outbound `httpx` call without explicit timeout / SSRF allow-list, or unbounded file upload (`SC9`, `SC10`)<br>• Unapproved or unlocked dependency change (`SC11`) |
| **`MINOR`** | • Defense-in-depth tightening or missing `SC14` handoff trigger note when the runtime security guard itself is verified |
