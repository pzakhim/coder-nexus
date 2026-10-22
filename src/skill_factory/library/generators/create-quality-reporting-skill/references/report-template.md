# Report template

```markdown
# Test report — <feature> — round <N>

**Verdict:** ACCEPTED | CHANGES_REQUESTED | BLOCKED — <one-line reason>
**Counts:** <p> PASS · <f> FAIL · <b> BLOCKED · <n> NOT_RUN  (of <total> cases)
**AC coverage:** <a_pass>/<a_total> PASS — failing/blocked: <AC IDs>
**Open defects:** <BLOCKER/HIGH count> blocking, <others> non-blocking
**Limitations:** <stubbed providers, cases not run and why, roles/environments not covered, flaky cases>

## Context
- Revision: <commit> (review: <review report link>)
- Plan: <plan link @ version>
- Environment: <services@versions, data/seed, stubs, accounts by role, started/reused>

## AC coverage
| AC | Cases | Result |
|---|---|---|

## Results
### Backend (API)
| Case | AC | Priority | Result | Evidence | Defect |
|---|---|---|---|---|---|

### Frontend (browser)
| Case | AC | Priority | Result | Evidence | Defect |
|---|---|---|---|---|---|

## Defects
| ID | Severity | Case | Status | Summary | Reproduction |
|---|---|---|---|---|---|

## Deviations from the plan
- <case>: <what differed and why>

## Re-test history
| Round | Revision | Cases rerun | Result |
|---|---|---|---|
```

Single-branch workspaces keep one results table.
