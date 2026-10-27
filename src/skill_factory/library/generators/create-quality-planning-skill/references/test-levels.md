# Choosing the Test Level (`Q5` — Stack-Neutral Verification Boundaries)

Select the lowest, fastest test level that deterministically proves the acceptance criterion (`Q5`). Keep level definitions stack-neutral in base guidance and bind concrete workspace commands in the generated skill.

| Test Level | What It Proves | Architectural Boundary | Default Owner | Choose When |
|---|---|---|---|---|
| **Unit** | Isolated domain logic, pure functions, state reducers/controllers, and value validation | In-process class/function boundary (mocked/faked collaborators) | **Code Writer** | Never planned case-by-case by the Quality Engineer; referenced as a prerequisite CLI gate |
| **Integration** | Repository queries, database constraints, transactions, migrations, and message/cache adapters | Component + real local database/broker boundary | **Code Writer** (or Quality Engineer if assigned by workspace) | Proving data integrity, query scoping (`tenant_id`/`owner_id`), and transaction rollback that surface below the public API |
| **API / Service Acceptance** | End-to-end service contracts with real auth per role: status codes, payload schemas, persisted state, side effects (audit logs, jobs), and `Role × Environment × Action × Object` permission matrix | Public HTTP / RPC / GraphQL / message entrypoint against running service + real storage | **Quality Engineer** | Business rules, authorization denials (`401`/`403`/scoped `404`), idempotency, concurrency, boundary validation, and `security-review` (`SR14`) runtime checks |
| **UI / Client End-to-End** | User journeys through the rendered client: navigation, form submission, the 4 UI states (`loading`, `empty`, `error`, `populated`), role-based UI visibility, and runtime error health | Rendered client application (browser / mobile / desktop runner) connected to backend or explicit edge stub | **Quality Engineer** | Multi-step user workflows, client-side state transitions, and user-observable feedback |
| **Visual Fidelity** | Layout, spacing, typography, responsive viewports, and theme states against the approved design | Rendered screen/frame capture vs approved design baseline | **Quality Engineer** | UI features with approved visual specs or design tokens |
| **Manual Verification** | Scenarios that cannot yet be deterministically automated (e.g. hardware peripherals, external physical callbacks) | Human-executed step-by-step protocol with captured evidence | **Quality Engineer** | Allowed **only** with a written justification in the test plan and recorded artifact evidence |

---

## Level Selection Rules

1. **Client + Service Workspaces**: Cover critical user journeys with UI/Client End-to-End cases, and push combinatorial business rules, `Role × Environment × Action × Object` permission denials, error codes, and concurrency down to **API / Service Acceptance** so the suite stays fast and diagnostic.
2. **Service / Backend-Only Workspaces**: End-to-end verification is **API / Service Acceptance** against the running service and real persistence — never unit tests with mocked repositories.
3. **Client-Only Workspaces**: Verify user flows, state matrices, and visual fidelity at the **UI / Client End-to-End** and **Visual Fidelity** levels against a real dev backend or a contract-verified network-edge stub.
4. **External Third-Party Providers (`Q7`)**: Prefer an isolated provider sandbox; otherwise stub at the network/adapter boundary and label every stubbed test case in the plan and execution report.
