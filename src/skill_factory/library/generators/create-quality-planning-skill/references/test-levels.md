# Choosing the test level

| Level | Proves | Typical tools | Owner (default) | Choose when |
|---|---|---|---|---|
| Unit | Logic in isolation | pytest, vitest, flutter_test | Code Writer | Never planned by the Quality Engineer; referenced only |
| Integration | Repository/transaction/adapter behavior on a real DB or service | pytest + local DB, testcontainers | Code Writer (workspace may assign to Quality Engineer) | Data integrity and SQL behavior that the API cannot show directly |
| **API acceptance** (backend) | AC through the real HTTP API with real auth per role: status codes, response shape, persisted data, side effects (jobs, audit logs), permission matrix | HTTP test client, Postman/Newman collections, curl scripts | Quality Engineer | Business rules, permissions (`403` per role × environment), persistence, idempotency, error codes |
| **UI end-to-end** (frontend) | User flows in a real browser: navigation, forms, the four UI states, capability-driven visibility, environment switch, console/network health | Browser automation via MCP (e.g. chrome-devtools), Playwright | Quality Engineer | Anything the user sees or does |
| **Visual** | Fidelity to the approved design at given viewports/states | Screenshots compared with mockups/baseline | Quality Engineer | UI features with an approved design |
| Manual | What cannot be automated now | Checklist with evidence | Quality Engineer | Only with a written reason |

## Fullstack

One UI end-to-end case can cover FE and BE together; add API acceptance cases for what the UI cannot reach (direct forbidden calls, error codes, concurrency, workers).

## Backend-only workspaces

"End-to-end" for a backend is API acceptance against the running service with real persistence — not unit tests with mocks.

## External providers

Prefer a sandbox; otherwise stub at the network edge (mock server). Every case run against a stub is labelled so in the results.
