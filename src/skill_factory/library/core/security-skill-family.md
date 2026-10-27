# The Application Security skill family

Rules shared by the Application Security Pack generators.

## Ownership

| Skill (`.agents/skills/<name>/`) | Answers | Used by | When |
|---|---|---|---|
| `secure-coding-standards` | How to write it safe the first time | Code Writer (writing), Code Reviewer (rubric), Security | Every change touching input, permissions, scopes, secrets, files, URLs |
| `security-review` | Is this change exploitable, and how badly? | Security role — or the Code Reviewer when the workspace has no separate Security role | Changes matching the review triggers; risky areas at `deep` |
| `bug-hunt` (dimension 5) | Obvious security defects in the diff | Code Writer (quick), Code Reviewer | Every review; **handed over** to security-review when a Security role exists |
| `code-review` | Flags security-relevant changes and routes them | Code Reviewer | Every review |

Findings that keep recurring become rules in `secure-coding-standards` (contribute back to the base when they are general).

## Vocabulary

| Term | Meaning |
|---|---|
| Trigger | A change type that requires security review (auth, guards, scopes, sensitive data, crypto, files/URLs, dependencies…) |
| Threat model (per change) | Assets, actors, entry points, trust boundaries and what could go wrong for this change |
| Coverage ledger | Deterministic inventory of every changed entrypoint, query, job, and trust boundary unit audited (`COVERED` / `UNCOVERED`) so zero high-risk units are skipped |
| Adversarial disproof (`Source → Guard → Sink`) | Mandatory refutation step where every candidate vulnerability is traced against upstream guards, validators, and middleware to try to disprove it before reporting |
| Exploit scenario | `given <attacker/role/state> → when <action> → then <impact>` with concrete values |
| `BLOCKER` / `MAJOR` / `MINOR` | Unified 3-tier security finding severity (`shared_contracts/flags_and_statuses.md`): `BLOCKER` (cross-tenant access, auth bypass, RCE/injection, secret leak), `MAJOR` (privilege/scope escalation under conditions, missing rate/size/replay bounds, unsafe outbound/file handling), `MINOR` (defense-in-depth hardening gap without direct exploit path) |
| `CONFIRMED` / `PLAUSIBLE` / `REJECTED` | `CONFIRMED` = complete source-to-sink trace + exploit scenario; `PLAUSIBLE` = concrete missing runtime/config evidence named (and handed to QA/QC when runtime verification is needed); `REJECTED` = disproved by an identified upstream guard |
| `PASS` / `FAIL` | Deterministic read-only security CLI/scanner check result |
| Security sign-off | The Security verdict on a revision: `APPROVED` (`0` `BLOCKER` and `0` `MAJOR`), `CHANGES_REQUESTED` (`CONFIRMED BLOCKER` or `CONFIRMED MAJOR`), `BLOCKED` (`PLAUSIBLE BLOCKER` or `PLAUSIBLE MAJOR` awaiting evidence) |

## Boundaries

- Read-only toward code and tests; findings go to the report and to the Code Writer with a fix direction.
- **No live exploitation** of shared or production environments, no real credentials or personal data in reports; verification only with existing tests, local/disposable environments or read-only reasoning.
- Sensitive findings are shared only through the channel the user approves.
