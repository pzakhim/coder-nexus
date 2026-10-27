# Report Template (Stack-Agnostic)

Use this structure as the starting shape for the workspace's acceptance / QA test report. Defect severities follow the unified 3-tier scale **`BLOCKER` / `MAJOR` / `MINOR`** (`shared_contracts/flags_and_statuses.md`).

```markdown
# Test Report — <feature> — Round <N>

**Verdict:** ACCEPTED | CHANGES_REQUESTED | BLOCKED — <one-line reason>
**Counts:** <p> PASS · <f> FAIL · <b> BLOCKED · <n> NOT_RUN (of <total> cases)
**AC Coverage:** <a_pass>/<a_total> PASS — failing/blocked: <AC IDs or none>
**Open Defects:** <blocker_count> BLOCKER · <major_count> MAJOR · <minor_count> MINOR
**Limitations:** <stubbed providers, cases not run and why, roles/environments not covered, flaky cases — or "None">

## 1. Context & Environment (`RP1`)
- **Revision:** `<commit_sha>` (Code Review: `<review_report_link>`)
- **Test Plan:** `<plan_link @ version>`
- **Environment:** `<services@versions, data/seed state, stubbed dependencies, accounts by role, started vs reused>`

## 2. Acceptance Criteria Roll-Up (`RP3`)
| AC ID | Mapped Cases | AC Result (`PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`) |
|---|---|---|
| `AC-01` | `TC-01`, `TC-02` | `PASS` |

## 3. Per-Case Execution Results (`RP2`)
### API / Service Surface (or unified table for single-surface workspaces)
| Case ID | AC ID | Surface / Level | Result | Evidence Link | Defect ID |
|---|---|---|---|---|---|
| `TC-01` | `AC-01` | API / Service | `PASS` | `[log]({{evidence_path}}/tc-01.txt)` | — |

### UI / Client Surface (omit when workspace has no UI surface)
| Case ID | AC ID | Surface / Level | Result | Evidence Link | Defect ID |
|---|---|---|---|---|---|
| `TC-02` | `AC-01` | UI / Client | `PASS` | `[shot]({{evidence_path}}/tc-02.png)` | — |

## 4. Defects (`RP5`)
| Defect ID | Severity (`BLOCKER` / `MAJOR` / `MINOR`) | Case ID | Status | Summary | Reproduction Link |
|---|---|---|---|---|---|
| `DEF-01` | `MAJOR` | `TC-03` | `open` | <one-sentence summary> | `[repro]({{evidence_path}}/def-01.md)` |

## 5. Deviations from the Plan (`RP12`)
- `<Case ID or "None">`: `<what differed from the approved plan and why — expected results are never edited>`

## 6. Re-Test History (`RP10`)
| Round | Revision SHA | Cases Rerun | Open `BLOCKER`/`MAJOR` | Round Verdict |
|---|---|---|---|---|
| `1` | `<sha_1>` | `All (<total>)` | `1 MAJOR` | `CHANGES_REQUESTED` |
| `2` | `<sha_2>` | `TC-03 (+ regression TC-01)` | `0` | `ACCEPTED` |
```
