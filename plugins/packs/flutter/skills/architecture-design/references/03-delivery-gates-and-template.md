# 03 — `PHASE-00`, Gate 2 Verification, Delivery Conventions, and `design.md` Template

> Topic: PHASE-00 readiness checklist, Gate 2 validation workflow, downstream Flutter delivery conventions, and copy-ready design.md template (`AD9`, `AD10`)

## 1. Flutter `PHASE-00` Readiness Checklist (`AD9`)

Before `PHASE-01` implementation begins, `PHASE-00` (`phases/phase-00-prepare.md`) verifies toolset readiness and prepares any required API mocks:

| Step | Scope | Verification Command (`cwd`: Client root) | Expected Result |
|---|---|---|---|
| `P0-00` | Flutter developer toolset | `coder-nexus setup tools --pack flutter --check` | `PASS` (`TOOLS: READY`) |
| `P0-01` | Profile foundation check | Active profile setup check (`coder-nexus setup flutter --check` for `imespro`; `pubspec.yaml` / `flutter pub get` check for external profiles) | `PASS` (`STATUS: READY`) |
| `P0-02` | Baseline analyzer health | `flutter analyze` | `PASS` (or pre-existing baseline warnings recorded) |
| `P0-03` | Mockoon preparation (`MOCKOON_MOCKED`) | Author `mocks/<feature>_mockoon.json` matching the `Mockoon Trigger & Test Data Table` in `design.md`, start `mockoon-cli`, and probe Pass/Fail/Empty rules | `PASS` (`phases/phase-00-prepare.md` ticked `[x] PREPARED / COMPLETED`) |

---

## 2. Gate 2 Validation & Approval Workflow (`AD10`)

1. Render `design.md` using the template in Section 4 below **only** after all pre-design `Q-NN` items in `codebase-notes.md` are closed into `D-NN`.
2. Run `validate_proposal_spec` on both `codebase-notes.md` and `design.md` (`PASS` required).
3. Run `gate-review` (`modes/design.md`) and `cold-reader-check` on `design.md`. Fix any self-owned findings; queue any genuine user-choice question as `Q-NN`, ask one at a time via `ask_question`, and close into `D-NN`.
4. Present `design.md` to the user for **Gate 2 (Architecture Approval)** only when `OPEN` `Q-NN` count is **0**.
5. Once approved, retain `codebase-notes.md` permanently in `vN/` and hand off to `implementation-planning` (Gate 3).

---

## 3. Flutter Delivery Conventions for Downstream Roles

- **Code Writer (`incremental-implementation`):** Implements one phase at a time following `{{slot:clean-architecture}}`, `{{slot:clean-code}}`, and the active profile's foundation mapping in `design.md`. Writes AAA developer unit and cubit tests (`{{slot:unit-testing}}`) covering both Pass/Default and Fail/Empty scenarios under `test/unit/` (or `test/modules/<feature>/`), then runs `dart format --output=none --set-exit-if-changed`, `flutter analyze`, and `flutter test`.
- **Code Reviewer (`{{slot:code-review}}`):** Runs `{{slot:bug-hunt}}` cold, executes Hub MCP validators (`validate_architecture_code`, `validate_module_architecture` with explicit `architecture_profile`) and `flutter analyze`, audits `test/` for happy-path bias and `TEST-TAMPER-001`, and inspects runtime visual screenshots/golden baselines (`{{slot:visual-quality}}`) against Visual AC.
- **Test Runner (`{{slot:verification}}`):** Runs widget and integration test suites (`flutter test`) and runtime visual acceptance on the approved revision after `APPROVED`.
- **Docs Writer (`user-documentation`):** Documents real shipped routes, UI states, and setup only where relevant to the reader's task.

---

## 4. Copy-Ready Flutter `design.md` Template

```markdown
# Design: {{FeatureTitle}} — {{Version}}

> **Document type**: DESIGN
> **Feature**: {{module}}/{{feature}}
> **Version**: {{Version}}
> **Created**: {{CreatedDate}}
> **Source references**: {{SourceReferences}}
> **Status**: PENDING_REVIEW
> **Approval reference**: NONE

- **Requirements reference**: `requirements.md`
- **Context reference**: `codebase-notes.md`
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

## Goal alignment

| Goal | Design elements that deliver it | Decision |
|---|---|---|
| G-01 | {{ModulesScreensContractsThatDeliverTheGoal}} | `D-NN` |

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

| Need | Core API reused (package · guide/path) | Or Client location (Core gap + reason) |
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

## Integration, errors, and risks

### Backend API Contract & Mockoon Strategy (Omit if no external API)
- **Status**: {{BE_API_READY_or_MOCKOON_MOCKED_or_NONE}} — source: {{BeApiSpecUrlFileOrMockoonConfig}}
- **Endpoints & Verification Status**:

  | Method | Path | Auth | Spec Verification / Status | Purpose / AC |
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

Record UI/contract checks separately from required live integration checks, with contract/fixture provenance. Follow `shared_contracts/api_handshake_protocol.md`; fixtures never prove live acceptance.

{{CodeTestsRuntimeVisualAndRegressionChecks}}

## Gate 2 approval

- **Decision summary**: {{UserFacingDesignSummary}}
- **Approved response**: NONE
- **Approved document revision**: NONE
```
