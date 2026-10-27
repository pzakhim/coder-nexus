# Detecting and Mapping Runtime Verification Tools

Never hardcode verification tools in advance: detect which UI/client and API/service tools exist in the workspace (and agent host), confirm the selection and fallback order with the user at the gate, and bind the generated skill to those real tools.

## 1. UI / Client Surface Tools (`A5`)

| Tool Category | How to Detect | Operational Notes |
|---|---|---|
| **Chrome DevTools MCP (`chrome-devtools`)** | MCP configuration mentions `chrome-devtools` (`.mcp.json`, host MCP settings, or workspace docs naming `new_page`, `take_snapshot`, `take_screenshot`) | Requires tracking `pageId`; saves DOM snapshots, screenshots, console messages, and network requests |
| **End-to-End UI Automation Runner** | E2E config or specs in repo (e.g., Playwright, Cypress, WebdriverIO, Maestro, Patrol, or native integration test runner) | Repeatable scripted browser/client runs and headless CLI execution gates |
| **Host Browser / Client Inspection Tool** | Agent host exposes built-in browser or client inspection tools (`navigate`, `snapshot`, `click`, `screenshot`, `console`) | Isolated browser session managed by the host |

### UI / Client Operations Map (Fill for Confirmed Tool)

| Operation | Chrome DevTools MCP | Scripted E2E Runner | Host Browser Tool |
|---|---|---|---|
| Open / Navigate | `new_page`, `navigate_page` | Runner navigate / launch API | Host navigate action |
| Inspect UI / DOM | `take_snapshot` | Accessibility / locator tree query | Host read-page / snapshot |
| Interact (fill / click / key) | `fill`, `click`, `press_key` | Locator `fill`, `click`, `press` | Host input / click / key |
| Wait for State | `wait_for` | Explicit state/visibility assertion | Host wait / poll |
| Capture Screenshot | `take_screenshot` | Runner screenshot capture | Host screenshot |
| Inspect Console / Logs | `list_console_messages`, `get_console_message` | Runtime console/error listener | Host console log reader |
| Inspect Network | `list_network_requests`, `get_network_request` | Network response/request listener | Host network inspector |
| Resize / Viewport | `resize_page`, `emulate` | Viewport / device configuration | Host viewport resize |

---

## 2. API / Service Surface Tools (`A6`)

| Tool Category | How to Detect | Operational Notes |
|---|---|---|
| **In-Repo API / Contract Test Runner** | `tests/api/`, `tests/integration/`, `tests/e2e/` with an HTTP/RPC client harness | Runs directly in CLI gates and captures status codes, headers, and bodies |
| **API Collection Runner** | Postman/Newman (`*.postman_collection.json`), Bruno, Hurl, or `.http` / `.rest` files | Repeatable collection runs across roles and environments |
| **CLI HTTP / RPC Client** | `curl`, `httpie`, `grpcurl` available in shell | Universal fallback; commands and redacted responses saved in evidence |

### Authentication & Scope Setup (`A6`, `A13`)
- Document how test credentials or tokens are acquired per role (`Role × Environment × Action × Object` matrix) using test accounts or token helpers.
- Never hardcode or log raw token values, passwords, or secrets in skill files or saved evidence (`A13`).

---

## 3. Gate Confirmation Rules

Offer only tools detected as available in the workspace or host, ordered with the workspace's established tool first. Record:
1. Primary tool and fallback tool for **UI / Client Surface (`A5`)**.
2. Primary tool and fallback tool for **API / Service Surface (`A6`)**.
3. If no tool is reachable for a required surface at runtime, affected test cases must be marked **`BLOCKED`** (`A7`).
