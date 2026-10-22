# Per-change threat model (STRIDE-lite)

Keep it to a few lines per change; specific beats complete.

## Template

```
Change:        <what changed, one line>
Assets:        <data or capability that matters: tenant documents, credentials, publish rights…>
Actors:        <who can reach it: anonymous, viewer, developer, admin, other tenant, worker, external provider>
Entry points:  <routes, actions, jobs, uploads, webhooks touched>
Boundaries:    <trust boundaries crossed: browser→API, API→DB, API→provider, tenant→tenant, env→env>
What could go wrong:
  - S <spoofing: acting as someone else>
  - T <tampering: changing data you should not>
  - R <repudiation: doing it without a trace>
  - I <information disclosure: seeing data you should not>
  - D <denial of service: making it unavailable / very slow>
  - E <elevation: gaining a role or capability>
Checks to run: <which of 03 / 04 apply>
```

## Prompts per letter

| Letter | Ask |
|---|---|
| **S** | Can the caller claim another identity, tenant or environment (headers, params, tokens)? |
| **T** | Can the caller change objects they do not own, or fields they should not (mass assignment), or bypass a draft/approval state? |
| **R** | Is the action audited with actor, scope and time where the workspace requires audit logs? |
| **I** | Can responses, errors, logs, exports or caches reveal another scope's data or secrets? |
| **D** | Can input make it unbounded (huge upload, unpaged query, regex, expensive provider call loops)? |
| **E** | Can a lower role reach a higher role's action (missing guard, UI-only check, environment rule skipped)? |

Skip letters that clearly do not apply; write "n/a".
