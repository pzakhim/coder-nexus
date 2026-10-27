# Stack Recipes (Generic Service Categories)

Orientation for `references/01-stack-lifecycle-and-revision.md`; the workspace's own task runner targets and scripts always take precedence.

## 1. Probe Before Starting (`E2`)

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN          # check which process is listening (macOS/Linux)
curl -fsS http://127.0.0.1:<port>/health    # probe HTTP health endpoint, if exposed
docker compose ps                           # check containerized service status
```

- **Listening and healthy** → **reuse** the running service; do not restart or reset it.
- **Listening, unhealthy, and not started by you** → report **`BLOCKED`** and notify the stack owner.

## 2. Start by Generic Service Category (Only When Missing, `E1`–`E4`)

Inspect any task runner target (`Makefile`, taskfile, scripts) before running it — some targets kill or reset existing processes.

| Service Category | Typical Start Pattern | Readiness Check (`PASS` / `FAIL`) |
|---|---|---|
| **Containerized Services** (DB, cache, queue, full compose stack) | `docker compose up -d <services>` | `docker compose ps` reports healthy; datastore accepts connections |
| **API / Backend Process** | Workspace server command in background with log capture | Health or readiness endpoint returns HTTP `200` within timeout |
| **Background Worker Process** | Workspace worker command in background with log capture | Worker log or status check confirms queue subscription / ready state |
| **Client / UI Dev Server** | Workspace client dev/run command in background with log capture | Dev server URL responds or application renders ready state on target device |

Always start missing services in the background with output redirected to a log file, and record the PIDs or container names you started.

## 3. Stop Only What You Started (`E2`, `E3`, `E11`)

Stop only the PIDs or containers recorded in your ownership log (`kill <pid>` or `docker compose stop <service>`). Never run a "stop all" or "reset all" target unless you started the entire stack yourself and no other user or agent shares it.

## 4. Hosts and Loopback Binding

Use the exact host documented by the workspace (`localhost` vs. `127.0.0.1`), as some local servers bind exclusively to IPv4 or IPv6 loopback interfaces.
