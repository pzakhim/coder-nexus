---
name: secure-coding
description: Stack-neutral secure-coding principles for code written or changed inside an approved task - trust boundaries and input validation, the client is untrusted, server-side object-level and data-scope authorization, secrets never in source, bundles or logs, sensitive-data minimisation, the workspace's own authentication, fail closed, outbound calls and files, dependencies, and what to flag for review - with findings graded on the bug-hunt scale. Use while the Code Writer implements anything that touches input, authorization, data scopes, secrets, personal data, outbound calls, files or dependencies, during the self-check before READY_FOR_REVIEW, and when the Code Reviewer checks security. The stack's risks come from the stack's secure-coding slot.
---

# Secure Coding

Goal: code that is safe the first time it is written, so security review finds confirmations, not rewrites. The stack's unsafe patterns and their safe counterparts come from `{{slot:secure-coding}}`; the workspace's real auth model, scopes and secret store come from the workspace (`.agents/skills/secure-coding-standards/` when it exists) and the approved design. Neither may relax a rule below.

## Rules

| # | Rule | Why |
|---|---|---|
| SC1 | **Know the trust boundaries.** Anything from outside the process is untrusted: requests, client state, files, messages, deep links, third-party responses, user-editable configuration. Validate at the boundary: type and schema, allow-lists, length and size limits. Reject invalid input; never repair or guess it. | Injection, overflow and logic abuse all start with input nobody checked. |
| SC2 | **The client is untrusted.** Every operation is authorized on the server, per object (this record, not just this kind of record) and per data scope (tenant, environment, owner, release state), deny by default. Client-side checks only shape the UI. | Hiding a button stops nobody; a direct call skips the client entirely. |
| SC3 | **Carry the data scope everywhere.** Every query, cache key, file path, background job and event carries its scope explicitly; never infer a default scope. | One missing filter leaks another customer's data. |
| SC4 | **No injection, encode output.** Parameterised queries, argument lists for commands, safe path joins that stay under their base, no evaluation of input as code or templates; rely on the stack's auto-escaping and a sanitiser for required rich text; validate redirect targets. | Injection turns data into code; unencoded output runs attacker code in a user's session. |
| SC5 | **Secrets never in source, bundles or logs.** No keys, tokens or passwords in code, commits, client bundles or app packages, URLs, logs, error messages or test fixtures; load them from the workspace's secret store or settings. | A leaked secret cannot be un-leaked; anything shipped to a client is public. |
| SC6 | **Minimise sensitive data.** Logs, errors, caches and analytics carry the minimum needed (ids, not personal data or tokens); users get a generic message with a request id. | Logs, caches and error pages are read by more people and kept longer than the database. |
| SC7 | **Use the workspace's authentication, never homemade.** Sessions, tokens, password hashing, encryption and secure random come from the existing mechanism and vetted libraries. | Hand-rolled auth and crypto fail invisibly until exploited. |
| SC8 | **Fail closed.** When validation, authorization or a dependency errors, deny; no fallback path that skips a guard; never substitute default or fake data to look successful. | Attackers aim for the error path. |
| SC9 | **Control outbound calls and files.** User-influenced URLs pass the workspace's allow-list; every outbound call has a timeout; files get type and size limits, safe parsers, generated names and storage outside served paths, and are never executed. | Server-side request forgery reaches internal services; uploads and parsers are a classic entry point. |
| SC10 | **Dependencies with care.** A new dependency needs a reason in the handoff, a pinned version through the lockfile, no known advisory and an active maintainer; upgrades are reviewed from the changelog, one package per change. | Every dependency is code you run without reading it. |
| SC11 | **Flag security-relevant changes.** List in the handoff every change to authentication, authorization, data scopes, secrets, personal data, crypto, outbound calls, file handling or dependencies, with the guard that protects it. | Reviewers spend extra attention where it matters only when they know where it is. |

Rules SC1–SC5 and SC8 have no exceptions. Anything the design does not settle (who may see what, which scope applies) is a question for Planning through `plan-change-request`, never a guess in code.

## Code Writer

1. Before editing, read the task's `Consumes`, the design's auth and scope decisions, and the stack risks of `{{slot:secure-coding}}` that apply to the files in scope.
2. Write the guard with the code it protects, plus a test that a forbidden actor or a wrong scope is refused (`test-first` when the task asks for it).
3. In the self-check, walk [references/review-checklist.md](references/review-checklist.md) over the diff; fix every hit inside scope and list SC11 items in the handoff.

## Code Reviewer

Run the checklist on the phase's diff after `bug-hunt`. Report each finding with a `given → when → then` exploit or failure scenario, `CONFIRMED` or `PLAUSIBLE`, on the bug-hunt scale:

| Severity | Security meaning |
|---|---|
| `BLOCKER` | Authorization or data-scope bypass, injection, authentication bypass, secret in source/bundle/log, fail-open on a normal path |
| `MAJOR` | Exploitable only on a realistic edge path; sensitive personal data in logs or errors; user-influenced outbound call or file without its guard; unvalidated input that corrupts stored data |
| `MINOR` | Defense-in-depth gap with no traced path (missing timeout on an internal call, verbose error without sensitive data) |

A secret in source or a client bundle is always `BLOCKER CONFIRMED`: the exposure is the failure. Verdict impact follows `bug-hunt` section 6. The reviewer never edits code.

## Sources

[references/sources.md](references/sources.md)
