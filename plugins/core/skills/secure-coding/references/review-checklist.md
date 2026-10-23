# Secure-coding checklist

Walk it over the diff of the task (Code Writer) or phase (Code Reviewer). Skip a row only with a reason (`N/A: no file handling in this diff`). The stack's unsafe patterns to search for come from `{{slot:secure-coding}}`.

## Per change: three questions first

1. Which new or changed entry points does the diff add (endpoint, screen action, message handler, job, deep link, file import)?
2. For each one, which actor may call it, on which objects, in which data scope? Where in the diff is that enforced on the server?
3. What leaves the process (responses, logs, caches, outbound calls, files, analytics), and does it carry more than needed?

## Rows

| Area | Check | Rule |
|---|---|---|
| Input | Every new entry point validates type, schema, size and allowed values before use; invalid input is rejected, not repaired | SC1 |
| Input | Data from third-party responses and stored user content is validated like request input | SC1 |
| Authorization | The server checks the actor against this object and its scope; a direct call with another actor's id is refused | SC2 |
| Authorization | Client checks exist only to shape the UI; nothing relies on them | SC2 |
| Data scope | Every query, cache key, file path, job and event in the diff carries its scope; no default scope | SC3 |
| Injection | No query, command, path, template or pattern built from input by string joining | SC4 |
| Output | No raw HTML from input without a sanitiser; redirect targets validated against an allow-list | SC4 |
| Secrets | No key, token or password in code, fixtures, client configuration, URLs or log lines | SC5 |
| Sensitive data | Logs, errors and caches carry ids, not personal data or tokens; user-facing errors are generic | SC6 |
| Authentication | Sessions, tokens, hashing, encryption and random values come from the workspace's mechanism and vetted libraries | SC7 |
| Fail closed | Errors in validation, authorization or a dependency deny the operation; no default or fake data on failure | SC8 |
| Outbound calls | User-influenced URLs pass the allow-list; every call has a timeout; redirects into internal ranges are not followed | SC9 |
| Files | Type and size limits, safe parser, generated name, stored outside served paths, never executed | SC9 |
| Dependencies | New or upgraded package has a reason, a lockfile pin, no known advisory, and its changelog was read | SC10 |
| Handoff | Every security-relevant change is listed with the guard that protects it | SC11 |

## Evidence

Record what you ran (search for the stack's unsafe patterns, the authorization test, the dependency audit command if the workspace has one) as evidence rows per `evidence-before-claims`. A check you could not run is `NOT_RUN` with the reason, never PASS.
