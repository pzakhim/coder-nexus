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

## Goal alignment

| Goal | Design elements that deliver it | Decision |
|---|---|---|
| G-01 | {{ModulesScreensContractsThatDeliverTheGoal}} | `D-NN` |

Every element in this design serves a goal from `requirements.md` → `## 0. Goals`. Elements that serve none are removed or recorded in `codebase-notes.md` with a reason.

## Architectural decision

- **Confirmed architecture (`D-NN`)**: {{ConfirmedArchitecturalDecisionAndRationale}}
- **Decision log reference**: All evaluated trade-offs and rejected alternatives are recorded in `codebase-notes.md` (`## 1. Decision Log (D-NN)`).

## Module and folder diff

- **Current structure and owners**: {{CurrentVerifiedPaths}}
- **Proposed structure and owners**: {{ProposedPathsAndResponsibilities}}
- **Cross-module and shared consumers**: {{AffectedConsumersOrReasonedNone}}

```text
{{ProposedDirectoryTreeWithCleanArchitectureLayout}}
```

- **Folder roles & layer responsibilities**:
{{FolderResponsibilitiesAndLayerExplanation}}

## Behavior, data, and state

### Screen, Routing & DI Contract
- **Screen Destination**: {{VerifiedScreenPathClassAndProfileSpecificBaseOrStandardFlutterWidget}}
- **Route Name & Args**: {{RouteNameArgumentsAndPopResultFromClientRouter}}
- **DI Registration**: {{OnlyTheDependenciesThisFeatureNeedsInClientDiFile}}

### State Machine & Domain Flow
- **State**: {{CubitStatesFollowingClientConvention}}
- **Domain Contracts**: {{EntitiesRepositoryAndUseCasesActuallyNeededOrReasonedNone}}

## Foundation reuse (Core usage / Client Core Mapping / standard Flutter)

- **Foundation evidence**: {{CompanyPackageRevisionsOrClientCoreMappingOrStandardFlutterRationale}}

| Need | Core API reused (package · GUIDE section) | Or Client location (Core gap + reason) |
|---|---|---|
{{CoreUsageRows}}

- **Gotchas affecting this design**: {{GuideGotchasOrNone}}

## UI design system

### UI Component Mapping
| UI Element / AC | Component | Source Package | Variant / Props | Rationale |
|---|---|---|---|---|
{{UiComponentRows}}

### Four Mandatory Visual States
- **1. Loading State**: {{LoadingSkeletonOrShimmerSpecification}}
- **2. Content State**: {{NormalContentStateLayout}}
- **3. Empty State**: {{EmptyStateViewSpecification}}
- **4. Error State**: {{ErrorViewAndRetryActionSpecification}}

## UI/UX mapping

> Only when `design-uiux/uiux.md` exists; delete this section otherwise. Approved UI/UX revision: {{UiuxRevision}}. Every `S-NN` (except `EXISTING`) and every `C-NN` appears here (`DESIGN-008`). Kit class → widget follows `{{slot:ux-kit}}` §3.

| Screen / component | Kind | Screen class & route / widget | Kit classes → widgets | Phase / task |
|---|---|---|---|---|
| S01 | {{NewOrChanged}} | {{ScreenClassRouteOrWidget}} | {{KitClassToWidgetMapping}} | {{PhaseOrTask}} |
| C01 | NEW COMPONENT | {{WidgetPathOrCoreGap}} | {{BuiltFromKitWidgets}} | {{ExplicitTask}} |

## Integration, errors, and risks

### Backend API Contract & Mockoon Strategy (Omit if no external API)
- **Status**: {{BE_API_READY_or_MOCKOON_MOCKED_or_NONE}} — source: {{BeApiSpecUrlFileOrMockoonConfig}}
- **Endpoints & Verification Status**:

  | Method | Path (relative to `ApiConfig.domain`) | Auth | Spec Verification / Status | Purpose / AC |
  |---|---|---|---|---|
  {{EndpointRows}}

- **Request / response payloads**: {{RequestBody200And400401500PayloadsOrLinkToRequirements}}
- **Mockoon Trigger & Test Data Table** *(when `MOCKOON_MOCKED` — agreed with User for `mocks/<feature>_mockoon.json` rules & Unit Tests)*:

  | Scenario ID | Case (Pass / Fail / Empty) | Endpoint | Input Trigger (`body` / `query` / `header`) | Mockoon Rule | HTTP Status & Latency | Response JSON Body |
  |---|---|---|---|---|---|---|
  {{MockoonTriggerAndTestDataRowsOrNA}}

- **Data pipeline**: {{VerifiedProfileSpecificRemoteDataSourcePipeline}}
- **`PHASE-00` consolidation & domain cutover plan**: {{Phase00ConsolidationModeExecuteOrInfoNoteAndMocksFeatureMockoonJson}}

### UX Error Handling & Storage Policy
- **Error Patterns**: {{UxErrorPatterns401_400_Timeout}}
- **Storage & Invalidation**: {{LocalStoragePolicyAndCacheInvalidation}}

## Verification strategy

Record UI/contract checks separately from required live integration checks, with contract/fixture provenance. Follow plugin-root `shared_contracts/api_handshake_protocol.md`; fixtures never prove live acceptance.

{{CodeTestsRuntimeVisualAndRegressionChecks}}

## Gate 2 approval

- **Decision summary**: {{UserFacingDesignSummary}}
- **Approved response**: NONE
- **Approved document revision**: NONE
