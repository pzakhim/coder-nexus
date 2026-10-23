# 04 — Stack risks (Python / FastAPI / SQLAlchemy)

Why: injection, SSRF, unsafe parsing and file handling are stack-specific; the safe pattern must sit next to the unsafe one (SC4, SC5, SC9, SC10). Names are illustrative; prefer the workspace's existing helper when one exists.

| Risk | Unsafe | Safe here | Rule |
|---|---|---|---|
| SQL injection | f-string, `%` or `+` into `text()` or `execute()` | SQLAlchemy expressions; `text("... :id")` with bound parameters | SC4 |
| SQL identifiers | `order_by(text(sort))` from the request | Allow-list dict of columns; `sort: Literal[...]` | SC4 |
| Shell injection | `subprocess.run(f"...", shell=True)`, `os.system` | Argument list, no shell, `timeout=`, allow-listed binary | SC4 |
| Path traversal | `open(BASE / user_path)` | Generated names; or `(BASE / name).resolve()` checked with `is_relative_to(BASE.resolve())` | SC4, SC10 |
| Unsafe deserialization | `yaml.load`, `pickle.loads`, `marshal`, `eval`, `exec` on input | `yaml.safe_load`; JSON into a Pydantic model | SC4 |
| Mass assignment | `Row(**body.model_dump())` | Explicit fields from an `extra="forbid"` schema ([01](01-trust-boundaries-and-input.md)) | SC1 |
| Open redirect | `RedirectResponse(request.query_params["next"])` | Allow-list of internal paths or hosts from settings | SC5 |
| HTML output | Building HTML strings with input; Jinja2 `autoescape=False`, `\|safe` on user content | JSON responses; Jinja2 autoescape on; a sanitiser (`nh3`) for required rich text | SC5 |
| SSRF | `httpx.get(body.url)` | Allow-list, `https`, resolved IP global, `follow_redirects=False`, timeout | SC9 |
| TLS | `verify=False` | Default certificate validation | SC9 |
| Uploads | `await file.read()` unbounded, `file.filename` as path | Size cap, content sniffing, generated name, storage outside served paths | SC10 |
| Misconfiguration | `debug=True`, `allow_origins=["*"]` with credentials, docs exposed against the design | Values from settings; explicit origins, methods, headers | SC8, SC13 |
| Secrets | `print(settings)`, logging headers | `SecretStr`, redacted logging ([03](03-secrets-and-sensitive-data.md)) | SC6 |

## Injection (SC4)

```python
# Unsafe
await session.execute(text(f"SELECT * FROM orders WHERE number = '{number}'"))
await session.execute(text("... ORDER BY " + sort))         # identifier from the request
subprocess.run(f"convert {filename} out.pdf", shell=True)
data = yaml.load(raw)                                        # can build arbitrary objects

# Safe
await session.execute(text("SELECT id FROM orders WHERE number = :number"), {"number": number})
SORT_COLUMNS = {"created": OrderRow.created_at, "total": OrderRow.total}
stmt = select(OrderRow).order_by(SORT_COLUMNS[sort])         # sort: Literal["created", "total"]
subprocess.run(["convert", str(path), "out.pdf"], check=True, timeout=30)
data = yaml.safe_load(raw)
```

Alembic migrations follow the same rule: `op.execute(sa.text(...).bindparams(...))`, never string-built SQL with data values.

## SSRF in outbound calls (SC9)

```python
# Unsafe
resp = httpx.get(body.webhook_url)                          # internal hosts, cloud metadata

# Safe
def _require_allowed_url(raw: str) -> httpx.URL:
    url = httpx.URL(raw)
    if url.scheme != "https" or url.host not in settings.webhook_allowed_hosts:
        raise WebhookUrlNotAllowedError(raw)
    for info in socket.getaddrinfo(url.host, url.port or 443):
        if not ipaddress.ip_address(info[4][0]).is_global:
            raise WebhookUrlNotAllowedError(raw)
    return url

async with httpx.AsyncClient(timeout=settings.http_timeout_seconds, follow_redirects=False) as client:
    resp = await client.post(_require_allowed_url(body.webhook_url), json=payload)
resp.raise_for_status()
event = ProviderEvent.model_validate(resp.json())           # third-party data validated like input
```

Every outbound client sets an explicit timeout, including calls to internal services. Reason: a hung dependency becomes a hung worker.

## File uploads (SC10)

```python
# Unsafe
@router.post("/files")
async def upload(file: UploadFile):
    data = await file.read()                                 # unbounded memory
    (UPLOAD_DIR / file.filename).write_bytes(data)           # "../../app/main.py"

# Safe
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
ALLOWED_TYPES = {"image/png": ".png", "application/pdf": ".pdf"}

async def store_upload(file: UploadFile, *, tenant_id: UUID) -> StoredFile:
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise UploadTooLargeError()                          # 413
    extension = ALLOWED_TYPES.get(_sniff_content_type(data))  # by content, not the header
    if extension is None:
        raise UnsupportedUploadTypeError()                   # 415
    name = f"{uuid4()}{extension}"                           # generated, outside served paths
    return await storage.put(tenant_id=tenant_id, name=name, data=data)
```

Uploaded files are never executed or imported; parse errors fail the import, never substitute data.

## CORS, debug, rate limits (SC13)

```python
# Unsafe
app = FastAPI(debug=True)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

# Safe
app = FastAPI(debug=settings.debug)                          # false outside local
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_allowed_origins,
                   allow_credentials=True, allow_methods=["GET", "POST", "PATCH", "DELETE"],
                   allow_headers=["Authorization", "Content-Type"])
```

Rate limits come from the mechanism the workspace already uses (gateway, reverse proxy, existing middleware) and return 429; a new rate-limiting dependency is a `D-NN`. Every route appears in OpenAPI and the API contract; removed routes are deleted, not hidden (OWASP API9).

## Existing protections to reuse

Before writing a guard, search for the workspace's own: auth dependency, capability guard, scoped repository base, outbound URL guard, upload storage helper, error handler. Record them in `codebase-notes.md`; reuse instead of writing a second one.

## Gates

No security gate is assumed in the pack baseline; run these on changed files and record each as an evidence row (`evidence-standard`). A command that cannot run (tool missing, no network) is `NOT_RUN` with the reason, never PASS.

```bash
uv run ruff check --select S <changed files>     # flake8-bandit rules, even if pyproject does not enable S
rg -n 'text\(f"|execute\(f"|shell=True|yaml\.load\(|pickle\.loads?\(|eval\(' <changed files>
rg -n 'allow_origins=\["\*"\]|debug=True|verify=False|follow_redirects=True' <changed files>
rg -n '\*\*\w+\.(model_dump|dict)\(\)' <changed files>                       # mass assignment
rg -n -i '(logger|logging)\.\w+\(.*(token|password|secret|authorization)' <changed files>
uv run pip-audit                                  # dependency advisories (needs network)
```

Ruff codes that map here: `S105`/`S106` hardcoded password, `S301` pickle, `S307` eval, `S311` non-crypto random, `S324` insecure hash, `S501` `verify=False`, `S506` `yaml.load`, `S602` `shell=True`, `S608` string-built SQL. Use the workspace's runner prefix (`uv run`, `poetry run`) when it differs. A `# noqa: S...` needs a reason on the same line and is a review trigger.
