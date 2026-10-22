# The Quality Engineer skill family (QA / QC)

Rules shared by the Quality Assurance Pack generators. The Quality Engineer verifies **user-observable behavior against the approved specs**, independently from the implementation. Developer unit tests belong to the Code Writer (`unit-testing`) and are graded by the Code Reviewer.

## Ownership

| Skill (`.agents/skills/<name>/`) | Side | Answers | When |
|---|---|---|---|
| `quality-planning` | QA | Which test cases prove each acceptance criterion, at which level, with which data | After the requirements gate (testability), then before execution |
| `quality-environment` | QA | How the stack, data and stubs are prepared safely | Before execution |
| `quality-acceptance` | QC | How cases are executed: `fe/` real browser, `be/` real API — tools detected per workspace | Once per feature (and after fixes) |
| `quality-reporting` | QC | Evidence, verdicts and defect reports | After execution |
| `visual-quality` *(optional)* | QC | Comparison with the approved design | UI features |

## Test levels and owners (default — confirmed per workspace)

| Level | Proves | Owner |
|---|---|---|
| Unit | Logic in isolation | Code Writer (`unit-testing`) |
| Integration | Repositories, transactions, adapters on a real DB/service | Code Writer by default; the workspace may assign it to the Quality Engineer |
| API acceptance (backend) | AC through the real API: status codes, persistence, side effects, permission matrix | Quality Engineer |
| UI end-to-end (frontend) | User flows in a real browser: states, permissions, environment switch | Quality Engineer |
| Visual | Fidelity to the approved design | Quality Engineer |

## Vocabulary

| Term | Meaning |
|---|---|
| AC | An approved acceptance criterion (`AC-NN` or the workspace's IDs) |
| Test case | One scenario with data, steps and an observable expected result (`TC-NN` / `E2E-NN`) |
| Traceability | AC → test cases and back; every case cites its AC (or "regression" / "out-of-scope guard") |
| `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` | Case result; only `PASS` is a pass |

Keep the workspace's own IDs and words when it has them (P5).

## Boundaries

- Specs (brief, requirements, AC, BDD scenarios, design states, decisions) are the source of truth — not the implementation plan or the code.
- Read-only toward application code and tests; defects go to the Code Writer with a reproduction.
- Never adjust an expected result to match what the code does.
- No production data, no fabricated "successful" data for a missing source.
