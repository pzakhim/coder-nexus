# 04 - Stop Criteria & Escalation

Recognize when an issue lies outside client application code and requires cross-team escalation.

## 1. When to Stop Debugging

Stop and escalate immediately when:
1. **Third-Party Package Bug:** The defect reproduces inside a pinned external package (e.g. `flutter_secure_storage` or an engine crash). Check upstream issue tracker.
2. **Backend API Contract Breach:** The server returns HTTP 200 with invalid schema, missing required fields, or HTTP 500 internal server errors.
3. **Hardware / OS Inconsistency:** Behavior is specific to a vendor-modified Android ROM or restricted iOS sandbox permission.

## 2. Escalation Artifact

Document the escalation clearly:
- **Reproduction steps / test case.**
- **Observed vs Expected behavior.**
- **Proof:** Exact HTTP request/response payload or upstream issue link.
