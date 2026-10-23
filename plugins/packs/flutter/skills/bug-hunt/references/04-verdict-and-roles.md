# 04 - Verdict Impact and Review Roles

How bug hunt findings affect the review decision per [work-item-contract handoff-and-status section 9](../../work-item-contract/references/handoff-and-status.md).

## 1. Verdict Thresholds

| Finding Conditions | Verdict Impact | Action Required |
|---|---|---|
| Any **`BLOCKER`** (CONFIRMED or PLAUSIBLE) | **`REQUEST_CHANGES`** | Author must fix defect before code can be approved. |
| Any **`MAJOR CONFIRMED`** | **`REQUEST_CHANGES`** | Author must fix defect. |
| Only **`MAJOR PLAUSIBLE`** or **`MINOR`** | **`APPROVED`** (with comments) | Author addresses in follow-up or confirms non-issue. |
| Zero findings | **`APPROVED`** | Code ready to merge. |

## 2. Reviewer vs Coder Responsibilities

- **Code Writer:** Runs bug hunt self-check on the diff before declaring `READY_FOR_REVIEW`.
- **Reviewer:** Independently audits the diff against the 7 dimensions, verifies findings, and issues the verdict.
