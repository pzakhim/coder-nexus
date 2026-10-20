> **LEGACY read-only migration template.** New execution uses versioned `phases/*.md` and coordinator-owned `as-built.md`. Do not create a new global task list from this file.

# Legacy Task List: {{FeatureTitle}}

> **Plan:** [implementation_plan.md](implementation_plan.md)
> **Approved plan revision, if independently verified:** `{{ApprovedPlanRevision}}`
> **Last updated:** {{LastUpdated}}

{{#slices}}
## Slice {{slice_id}}: {{slice_title}}

- [ ] **Task {{task_id}}**: {{task_title}}
  - Status: `{{task_status}}`
  - Depends on: `{{task_dependencies}}`
  - READY when: `{{task_ready_conditions}}`
  - Files: `{{files_summary}}`
  - Verification command: `{{verification_command}}`
  - Verified revision: `{{verified_revision}}`
  - Verification evidence: `NOT_RUN` / `BLOCKED` / `PASS` / `FAILED` — {{verification_evidence}}
  - UI impact: `{{ui_impact_yes_no}}` — {{ui_impact_reason}}
  - Visual target/states: `{{visual_target}}` — {{required_ui_states}}
  - Visual evidence: `NOT_RUN` / `BLOCKED` / `PASS` / `FAILED` — {{visual_evidence}}
{{/slices}}

## Feature Sign-Off

- [ ] Actual targeted tests and analyzer pass on the recorded revision.
- [ ] Required UI states were opened on the approved target with inspected visual evidence.
- [ ] ACs and Visual AC match the approved design; missing evidence remains `BLOCKED` or `NOT_RUN`.
