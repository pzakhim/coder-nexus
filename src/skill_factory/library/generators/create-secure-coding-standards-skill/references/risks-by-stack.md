# Safe vs unsafe patterns by stack

Starting points for `04-stack-risks.md`. The generated file shows the workspace's own safe helper next to each unsafe pattern.

## Python / FastAPI / SQLAlchemy

| Risk | Unsafe | Safe |
|---|---|---|
| SQL injection | f-string / `%` / `+` into `text()` | `text("... :id")` with bind params; ORM expressions |
| Shell injection | `subprocess(..., shell=True)` with input | Argument list, no shell; allow-listed commands |
| Path traversal | `open(base + user_path)` | `Path(base).joinpath(name).resolve()` checked to stay under `base` |
| Mass assignment | `Model(**request.dict())` | Explicit request schema → explicit fields |
| Authorization | `if role == "admin"` in a router | Capability guard in the use case; object loaded **with** its scope |
| SSRF | `httpx.get(user_url)` | The workspace's URL allow-list/network guard, timeout, no redirects to private ranges |
| Unsafe parsing | `yaml.load`, `pickle.loads` on input | `yaml.safe_load`; JSON with a schema |
| Secrets | `print(settings)` / logging headers | Settings with secret types; redacted logging |

## TypeScript / React / Next.js

| Risk | Unsafe | Safe |
|---|---|---|
| XSS | `dangerouslySetInnerHTML` with user content; building HTML strings | JSX auto-escaping; a sanitiser (e.g. DOMPurify) for required rich text |
| Open redirect | `router.push(searchParams.get("next"))` | Allow-list of internal paths |
| Secrets in bundle | Secret in a `NEXT_PUBLIC_*` variable or a client component | Server-only module (`server-only`), secrets read on the server |
| Token storage | Long-lived tokens in `localStorage` | HttpOnly secure cookies / the workspace's auth client |
| Authorization | Hiding a button as the only check | Server/API guard; UI reads capabilities for UX only |
| CSRF | Cookie-authenticated mutation with no protection | Framework CSRF protection / same-site cookies / tokens |
| Server actions / route handlers | Trusting form data and the session blindly | Validate input, authorize per request and per object |

## Flutter / mobile

| Risk | Unsafe | Safe |
|---|---|---|
| Secrets | API keys in source or assets | Backend-issued tokens; secure storage |
| Token storage | `SharedPreferences` | `flutter_secure_storage` (or platform keychain) |
| Transport | Accepting bad certificates in debug code left in release | Default TLS validation |
| Deep links | Acting on link parameters without validation | Validate and authorize on the server |

## Go

`database/sql` placeholders not string formatting; `filepath.Clean` + prefix check for paths; `http.Client` with timeout; `crypto/rand` not `math/rand` for tokens.
