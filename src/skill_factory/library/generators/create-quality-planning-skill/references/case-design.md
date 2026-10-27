# Case Design & Security Hand-Off (`Q4`, `Q8`–`Q11`)

Techniques for `references/02-case-design-and-test-levels.md`. Select the techniques required by the feature's acceptance criteria and threat surface; every case must state a concrete, observable expected outcome (`Q11`).

## 1. Case Design Techniques

| Technique | Use For | Concrete Example |
|---|---|---|
| **BDD Scenario Mapping** | Every approved requirement scenario | `Given a draft change set in staging, when an authorized editor saves a revision, then status 200 is returned and the new revision version is persisted and visible on reload` |
| **Equivalence Partitioning** | Input classes handled identically | Valid identifier / malformed identifier / empty value / unknown identifier (`404`) |
| **Boundary Value Analysis** | Numeric, length, time, and pagination limits | `0`, `1`, `max`, `max + 1`; first page, empty page, last page |
| **State Transition Testing** | Lifecycle and workflow state machines | `DRAFT → SUBMITTED → APPROVED`; verify forbidden transition `APPROVED → DRAFT` is rejected |
| **Decision Table** | Combining business rules and conditions | `Actor Role × Resource State × Feature Flag → Allowed / Denied` |
| **Permission & Scope Matrix (`Q4`, `SR3`, `SR4`)** | Every mutating or sensitive read operation | `Role × Environment × Action × Object` (including cross-tenant/cross-owner access attempts expecting `403` or scoped `404` at the API/service boundary) |
| **`security-review` Runtime Hand-Off (`SR14`)** | Runtime-dependent security scenarios | Convert `PLAUSIBLE` exploit scenarios or auth/rate-limit/concurrency checks flagged by `security-review` (`SR14`) into executable API/Service or E2E test cases |
| **UI / Client State Matrix** | Every user-facing view or screen | `loading` (no layout shift), `empty` (zero records vs zero filter matches), `error + retry`, `populated` |
| **Failure & Timeout Injection** | External provider or downstream calls | Upstream timeout, `5xx` error, malformed payload (stubbed at network boundary and labelled `stubbed` in report) |
| **Idempotency & Concurrency** | Mutating actions and shared resources | Duplicate submission with same idempotency key, concurrent updates to the same record (`409` or deterministic lock) |

---

## 2. Standard Case Format

```text
<TC-ID>  [traces: <AC-ID> | regression | out-of-scope-guard | security-handoff:<SR-ID>]   risk: <BLOCKER | MAJOR | MINOR>   level: <api | ui | visual | integration | manual>
Given:   <preconditions, seeded test data, and data source>
When:    <exact action performed by the user or API/service caller>
Then:    <observable outcome: status code, response body, persisted state, emitted event, or UI state>
Target:  <named environment, endpoint/route/screen, Role × Scope>
```

---

## 3. Unified Risk Tiers (`BLOCKER` / `MAJOR` / `MINOR` — `Q8`)

Test cases and plan-review gaps use the unified 3-tier severity scale from `shared_contracts/flags_and_statuses.md`:

| Risk Tier | Scope of Test Cases | Execution & Release Impact |
|---|---|---|
| **`BLOCKER`** | Core happy-path acceptance criteria, `Role × Environment × Action × Object` permission denials and tenant/scope isolation, `security-review` (`SR14`) runtime verification cases, financial/data-integrity mutations | Executed first; any missing or failing `BLOCKER` case blocks release sign-off |
| **`MAJOR`** | Input validation rules, UI/client state matrix (`loading`, `empty`, `error`, `populated`), boundary values, external failure handling, targeted regressions (`Q10`), out-of-scope guards (`Q9`) | Executed after `BLOCKER` cases; failures require fix or explicit waiver before sign-off |
| **`MINOR`** | Non-blocking cosmetic variations, secondary copy/formatting details, rare non-destructive edge conditions | Executed last; tracked as minor defects without blocking core verification |
