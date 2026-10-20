> **LEGACY read-only migration template.** New plans use `docs/features/<module>/<feature>/vN/implementation-plan.md` and linked behavior phases. Do not render this template for new work or infer user approval from an old status field.

# Legacy Implementation Plan: {{FeatureTitle}}

> **Source task:** {{HulyTaskId}} — {{FeatureTitle}}
> **Legacy proposal:** [{{feature_name}}_proposal.md](../brainstorm/{{feature_name}}_proposal.md)
> **Approved proposal revision, if independently verified:** `{{ApprovedProposalRevision}}`
> **Plan status:** `PENDING_REVIEW`

## 1. Vertical Slices Overview

| Slice ID | Observable behavior | Affected layers | Files | Checkpoint |
|---|---|---|---|---|
{{VerticalSlicesSummaryRows}}

## 2. Slice Breakdown

{{#slices}}
### Slice {{slice_id}}: {{slice_title}}

- **Behavior:** {{slice_goal}}
- **Task:** {{task_id}} — {{task_title}} ({{task_size}})
- **Description:** {{task_description}}
- **Status:** `{{task_status}}`
- **Depends on:** {{task_dependencies}}
- **READY when:** {{task_ready_conditions}}
- **ACs:** {{task_ac_1}}; {{task_ac_2}}
- **Files:** `{{file_path_1}}`, `{{file_path_2}}`, `{{file_path_3}}`
- **Verified base class/import:** `{{base_class}}`; `package:{{package_name}}/...`
- **Package source/revision:** `{{source_revision_and_verification_status}}`
- **Verification command:** `{{verification_command}}`
- **UI impact and reason:** `{{ui_impact_yes_no}}` — {{ui_impact_reason}}
- **Approved visual target:** {{target_platform}} / {{target_device_or_viewport}} / {{target_flavor}} / {{target_entrypoint}}
- **Required UI states:** {{required_ui_states}}
- **Visual reference and AC:** {{visual_acceptance_reference}}; {{visual_acceptance_criteria}}

{{#has_checkpoint}}
**CHECKPOINT {{checkpoint_id}}:** Verify the behavior after task {{task_id}} and preserve actual revision-bound evidence.
{{/has_checkpoint}}
{{/slices}}

## 3. Verification Strategy

Use the actual Client commands for targeted tests, analyzer, conditional code generation and runtime visual review. A material difference from approved Visual AC is `FAILED`. Record missing tools or target as `BLOCKED`.

## 4. Plan Approval Gate

- **Status:** `PENDING_REVIEW`
- **Actual user response and plan revision:** {{ActualApprovalReferenceOrNone}}
