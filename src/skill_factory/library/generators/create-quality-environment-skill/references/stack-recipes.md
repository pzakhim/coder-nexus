# Stack recipes

Orientation for `01-stack-and-lifecycle.md`; the workspace's own make targets and scripts win.

## Probe

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN          # who is listening (macOS/Linux)
curl -fsS http://127.0.0.1:<port>/health    # health endpoint, if any
docker compose ps                           # compose services and state
```

Listening and healthy → **reuse**; do not restart. Listening but unhealthy and not yours → `BLOCKED`, tell the owner.

## Start (only when nothing is running)

| Stack | Typical start | Readiness |
|---|---|---|
| Docker Compose | `docker compose up -d <services>` | `docker compose ps` healthy; service health endpoint |
| Make-based | `make start` / `make dev` (read what it does first — some targets stop other processes) | Health URLs listed in the Makefile/README |
| FastAPI | `uv run uvicorn app.main:app --port <p>` (background) | `curl /health` or `/docs` returns 200 |
| Workers | Worker command from the workspace (background) | Worker log shows "ready"/subscribed |
| Next.js | `npm run dev` (background) | First page responds; first compile can take ~60 s |
| Vite | `npm run dev` | Dev server URL responds |
| Flutter | `flutter run -d <device>` | App visible on the target device/simulator |

Run starts in the background with output to a log file; record PIDs/containers you started.

## Stop (only what you started)

`kill <pid>` / `docker compose stop <service>` for your own processes. Never a target that stops "everything" unless you started everything and no one else uses it.

## Hosts and ports

Use the URL the workspace documents (e.g. `localhost` vs `127.0.0.1` matters when a dev server listens on IPv6 only).
