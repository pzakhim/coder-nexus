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
| Exploit scenario | `given <attacker/role/state> → when <action> → then <impact>` with concrete values |
| `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` | Security severity (impact × likelihood), mapped to the workspace's finding levels |
| `CONFIRMED` / `PLAUSIBLE` | Same meaning as in bug-hunt |
| Security sign-off | The Security verdict on a revision: `APPROVED`, `CHANGES_REQUESTED`, `BLOCKED` |

## Boundaries

- Read-only toward code and tests; findings go to the report and to the Code Writer with a fix direction.
- **No live exploitation** of shared or production environments, no real credentials or personal data in reports; verification only with existing tests, local/disposable environments or read-only reasoning.
- Sensitive findings are shared only through the channel the user approves.
