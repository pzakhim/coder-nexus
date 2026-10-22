# Case design

Techniques for `03-case-design.md`. Pick what the AC needs; do not apply all of them mechanically.

| Technique | Use for | Example |
|---|---|---|
| **BDD scenario → case** | Every approved scenario | `Given a draft change set on DEV, when a PO edits a doc, then the revision is saved and visible after reload` |
| **Equivalence classes** | Inputs with groups behaving the same | valid email / invalid format / empty |
| **Boundary values** | Limits | 0, 1, max, max+1; first/last page |
| **State transitions** | Workflows with states | draft → published; published cannot be edited |
| **Decision table** | Several conditions combine | role × environment × draft state → allowed? |
| **Permission matrix** | Every mutating operation | each role × environment, including a direct API call expecting `403` |
| **UI state set** | Every data view | loading (no layout jump), empty (no data vs no match), error + retry, populated |
| **Failure injection** | External dependencies | provider timeout, 500, malformed response (stubbed, labelled) |
| **Concurrency** | Shared resources | double submit, two editors, stale tab after environment switch |

## Case format

```
<CASE-ID>  (covers <AC-ID> | regression | out-of-scope guard)   priority <P1|P2|P3>   level <api | ui | visual | manual>
Given:    <data and state, with its source>
When:     <action, as the user or API caller>
Then:     <observable result: screen state / message / persisted data / status code>
Target:   <environment, route or endpoint, role>
```

## Priority

| Priority | Cases |
|---|---|
| P1 | Critical user flows, permissions and data scopes, data integrity, money/quantities |
| P2 | Validation, states, regression of shared components |
| P3 | Cosmetic, rare edge cases |
