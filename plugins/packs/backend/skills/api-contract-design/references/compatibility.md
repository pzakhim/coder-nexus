# Compatibility: additive vs breaking

Detail for [api-contract-design](../SKILL.md) CT7–CT8. Judge every change from the client's side: what the client **sends** (request) and what it **reads** (response). Any observable behaviour (error text, ordering, defaults, timing, extra fields) may already be relied on (Hyrum's Law): when unsure, treat it as breaking and ask.

## 1. Classification

| Change in `openapi.json` | Class | Why |
|---|---|---|
| New path or operation | Additive | Existing clients do not call it |
| New optional request field or query parameter | Additive | Old requests stay valid |
| New response field | Additive **if** the contract says clients ignore unknown fields (state it in `design.md`) | Strict clients fail on unknown fields |
| Looser request validation (higher `max_length`, wider range) | Additive | Old requests stay valid |
| New enum value in a **request** field | Additive | Old clients never send it |
| New error status on an existing operation | Breaking unless it replaces nothing and the client handles unknown 4xx generically | Clients branch on status |
| New enum value in a **response** field | Breaking by default | Generated clients and `switch` statements reject unknown values |
| Request field optional → required, or a new required parameter | Breaking | Old requests now fail with 422 |
| Stricter request validation (lower `max_length`, new pattern) | Breaking | Previously valid data is rejected |
| Response field removed, renamed, or required → optional / nullable | Breaking | Clients that read it fail |
| Type or format change (`int` → `str`, `date` → `date-time`) | Breaking | Parsing fails |
| Status code changed for the same outcome | Breaking | Client branches move |
| Auth added to an endpoint, or scope narrowed | Breaking | Calls that worked are refused |
| Error envelope shape changed | Breaking | Every client's error handling |
| `operationId`, tag or schema component name changed (incl. toggling `separate_input_output_schemas`) | Breaking for generated clients | Method and type names change |
| Default value changed, ordering changed, pagination style changed | Breaking (Hyrum) | Behaviour clients observed changes |
| Path or operation removed | Breaking | Calls get 404/405 |

## 2. Doing a breaking change

1. It is a `D-NN` approved at Gate 2 (a breaking change discovered during build is a `DESIGN_CHANGE` through `change-control`).
2. Give a compatible path first: add the new field or endpoint next to the old one; mark the old one `deprecated=True` with a removal date in `design.md`.
3. Notify the frontend through the handshake: a new contract revision, back to `IN_BE_REVIEW` / `APPROVED_BY_BE` for the changed endpoints.
4. Remove the deprecated element only in a later item, after the frontend confirms it no longer calls it.

## 3. One-Version Rule

Keep one live version of each API and extend it. A `/v2` router is allowed only when a compatible path is impossible, as a `D-NN` that also sets the retirement date of `/v1`. Reason: every parallel version doubles the code, tests and client confusion, and old versions are rarely retired once forked.

## 4. Review questions

- Does every breaking row in `contract-change.md` cite an approved `D-NN`?
- Is there a compatible path and a deprecation date?
- Did a "refactor" task change an `operationId`, schema name, default or ordering?
- Does the frontend handshake record a new contract revision for breaking rows?
