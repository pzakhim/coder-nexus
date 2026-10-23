# 06 — Review triggers and checklist

Why: reviewers spend extra attention where it matters only when the handoff tells them where it is (SC14). Release 3.2.0 has no separate security role: the Code Writer flags, the Code Reviewer checks.

## Flag in the handoff

In the Code Writer handoff ([handoff-and-status §2](../../work-item-contract/references/handoff-and-status.md)), list each item below that the diff touches, with the guard that protects it (`SC2: OrderService.get_for_actor checks tenant via get_in_scope`):

- [ ] Authentication, sessions, tokens, password hashing
- [ ] Authorization guards, capability mappings, new or changed routes
- [ ] Data-scope filters, cache keys, background jobs or events crossing scopes
- [ ] Alembic migrations touching sensitive columns or scope columns
- [ ] Sensitive data (storage, logging, export, new response fields)
- [ ] Cryptography, secret handling, settings fields
- [ ] File uploads or parsing, user-influenced URLs, redirects, `subprocess`
- [ ] CORS, debug, docs exposure, exception handlers
- [ ] New or upgraded dependencies, any `# noqa: S...`

## Three questions first

1. Which new or changed entry points does the diff add (route, webhook, consumer, job, file import)?
2. For each, which actor may call it, on which objects, in which scope, and where in the diff is that enforced on the server?
3. What leaves the process (responses, logs, caches, outbound calls, files), and does it carry more than needed?

## Reviewer checklist

Walk it over the task diff (Code Writer self-check) or the phase diff (Code Reviewer, after `bug-hunt`). Skip a row only with a reason (`N/A: no file handling in this diff`).

| Area | Check | Rule |
|---|---|---|
| Input | Every new entry point validates type, schema, size and allowed values; input schemas `extra="forbid"`, no server-owned fields; invalid input rejected, not repaired | SC1 |
| Input | Webhook signatures, queue messages and provider responses validated like request input | SC1 |
| Authorization | The service checks the actor against this object and scope; a direct call with another actor's id is refused, with a test | SC2 |
| Authorization | No role strings in routers; no actor, tenant or role from the request body | SC2 |
| Data scope | Every query, update, delete, cache key, file path, job and event in the diff carries its scope; no default scope | SC3 |
| Injection | No SQL, shell command, path or template built from input by string joining; identifiers through an allow-list; no `yaml.load` / `pickle` / `eval` on input | SC4 |
| Output | `response_model` on every route; no raw HTML from input without a sanitiser; redirect targets allow-listed | SC5 |
| Secrets | No key, token or password in code, fixtures, migrations, URLs or log lines; settings use `SecretStr` | SC6 |
| Authentication | Tokens and hashing go through the workspace's auth module; algorithms pinned from settings | SC7 |
| Sensitive data | Logs, errors and caches carry ids, not personal data or tokens; 500 bodies are generic with a request id | SC8 |
| Outbound calls | User-influenced URLs pass the allow-list; explicit timeout; `follow_redirects=False`; no `verify=False` | SC9 |
| Files | Size cap, type by content, generated name, stored outside served paths, never executed | SC10 |
| Dependencies | Reason given, lockfile updated and checked, `pip-audit` run or `NOT_RUN`, changelog read | SC11 |
| Crypto | `secrets` for tokens, `hmac.compare_digest` for secrets, vetted hashing and encryption | SC12 |
| Fail closed | Errors in validation, authorization or a dependency deny; no default or fake data on failure | SC13 |
| Handoff | Every trigger above that the diff touches is listed with its guard | SC14 |

## Grading and evidence

Grade every finding on [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) as mapped in [SKILL.md § Code Reviewer](../SKILL.md#code-reviewer): defects `BLOCKER` / `MAJOR` / `MINOR` with `CONFIRMED` / `PLAUSIBLE` and a `given → when → then` exploit scenario; rule breaks without a traced exploit as `P1`. A secret in source or a bundle is always `BLOCKER CONFIRMED`.

Record what you ran ([04 § Gates](04-stack-risks.md#gates), the authorization test, `pip-audit`) as evidence rows per `evidence-standard`. A check you could not run is `NOT_RUN` with the reason, never PASS. No live exploitation of shared or production environments, and no real credentials or personal data in reports.
