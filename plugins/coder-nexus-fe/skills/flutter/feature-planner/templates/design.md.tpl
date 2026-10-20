# Design: {{FeatureTitle}} — {{Version}}

> **Document type**: DESIGN  
> **Feature**: {{module}}/{{feature}}  
> **Version**: {{Version}}  
> **Created**: {{CreatedDate}}  
> **Source references**: {{SourceReferences}}  
> **Status**: PENDING_REVIEW  
> **Approval reference**: NONE

- **Requirements reference**: [requirements.md](requirements.md)
- **Context reference**: [codebase-notes.md](codebase-notes.md)
- **Gate 1 approval reference**: {{ActualUserApprovalReference}}
- **Scope classification**: {{INIT_OR_EXTEND_OR_CORE_IMPACT}}

## Architecture profile

```yaml
architecture_profile:
  mode: {{imespro_or_external_structured_or_external_standard}}
  core_source: {{VerifiedPackageOrClientSourceOrNone}}
  evidence: {{ActualDependencyBaseAndConsumerPaths}}
```

- **Selection rationale / existing approval**: {{ProfileEvidenceAndApprovalReference}}
- Company setup/GUIDEs apply only to iMESPro. External profiles use Client mappings or standard Flutter; create only necessary layers.

## Architectural decision

- **Confirmed architecture (`D-NN`)**: {{ConfirmedArchitecturalDecisionAndRationale}}
- **Decision log reference**: All evaluated trade-offs and rejected alternatives are recorded in `codebase-notes.md` (`## 1. Decision Log (D-NN)`).

## Module and folder diff

- **Current structure and owners**: {{CurrentVerifiedPaths}}
- **Proposed structure and owners**: {{ProposedPathsAndResponsibilities}}
- **Cross-module and shared consumers**: {{AffectedConsumersOrReasonedNone}}

For each screen destination, record the selected profile’s naming, superclass, lifecycle and route contract. Only iMESPro requires `BaseScreen`/`BaseScreenState`; external-structured follows Client conventions and external-standard may use standard Flutter. Classify dialogs/child widgets separately.

## Behavior, data, and state

{{StateTransitionsDataContractsAndErrorHandling}}

## UI design system

{{DesignSourceVisualACAndVerifiedComponentMatrixOrReasonedNA}}

## Integration, errors, and risks

{{DiRouterLifecyclePermissionsRisksAndBlockers}}

## Verification strategy

Record UI/contract checks separately from required live integration checks, with contract/fixture provenance. Follow plugin-root `shared_contracts/api_handshake_protocol.md`; fixtures never prove live acceptance.

{{CodeTestsRuntimeVisualAndRegressionChecks}}

## Gate 2 approval

- **Decision summary**: {{UserFacingDesignSummary}}
- **Approved response**: NONE
- **Approved document revision**: NONE

Use `get_project_structure` as a blueprint and inspect the real Flutter workspace before naming files, APIs, constructors, DI anchors, or routes. Keep unverified contracts BLOCKED; do not fill sections with invented examples.
