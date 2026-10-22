# Detecting and mapping test tools

Never fix the tool in advance: detect what the workspace (and the agent host) actually has, offer those at the gate, and write the generated skill for the chosen one, with the others as fallbacks.

## Frontend (browser)

| Tool | How to detect | Notes |
|---|---|---|
| **chrome-devtools MCP** | MCP config mentions `chrome-devtools` (`.mcp.json`, host MCP settings, `AGENTS.md`/skills naming its tools like `new_page`, `take_snapshot`) | Pages need a `pageId`; screenshots may be restricted to workspace paths |
| **Playwright** | `@playwright/test` or `playwright` in `package.json`, `playwright.config.*`, an `e2e/` folder | Scripted specs; good for repeatable regression; headless in CI |
| **Claude in Chrome** | Host exposes `mcp__claude-in-chrome__*` tools | Drives the user's real Chrome; ask before acting on logged-in sessions |
| **Host built-in browser** | Host exposes a browser pane tool (navigate / read page / click / screenshot) | Isolated from the user's Chrome |

### Operations map (fill for the chosen tool)

| Operation | chrome-devtools MCP | Playwright | Claude in Chrome / built-in |
|---|---|---|---|
| Open / navigate | `new_page`, `navigate_page` | `page.goto` | navigate |
| Read the page | `take_snapshot` | `page.getByRole…`, `locator` | read page / find |
| Fill / click / key | `fill`, `click`, `press_key` | `fill`, `click`, `press` | form input / click / key |
| Wait | `wait_for` | `expect(…).toBeVisible()` | wait / re-read |
| Screenshot | `take_screenshot` | `page.screenshot` | screenshot |
| Console | `list_console_messages` | `page.on('console')` | read console |
| Network | `list_network_requests` | `page.on('response')` | read network |
| Viewport | `resize_page` | `setViewportSize` | resize |

## Backend (API)

| Tool | How to detect |
|---|---|
| API tests in the repo | `tests/api`, `tests/integration` with an HTTP client (httpx/requests TestClient, supertest) |
| Postman / Newman | `*.postman_collection.json`, `docs/postman/` |
| `.http` files | `*.http` / `*.rest` (REST Client) |
| curl / httpie | Always available as a fallback; scripts saved with the evidence |

Authentication per role: how a test token/session is obtained for each role (login endpoint with test accounts, token helper) — never paste tokens into evidence.

## At the gate

Offer only detected tools, recommended first (the one already used by the workspace's skills, else the most repeatable). Record the fallback order. If none is available for a branch, that branch's cases are `BLOCKED` until a tool is set up.
