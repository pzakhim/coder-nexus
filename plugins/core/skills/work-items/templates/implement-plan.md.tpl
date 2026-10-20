# Implementation plan — {{Title}} {{Version}}

- **Brief:** [brief.md](brief.md)
- **Design:** {{DesignLinkOrReasonedNA}}
- **Target Platform:** {{Platform}}
- **Stack / Framework:** {{Framework}}
- **UI Kit Authority:** {{KitAuthority}}
- **Accepted document revisions:** {{RealRevisionsAndApprovalReferences}}
- **Status:** PENDING_REVIEW
- **Approval reference:** NONE

## Technical context & `PHASE-00` (`phase-00-prepare.md`) API / context consolidation

{{ApiIntegrationStrategy}}
<!-- E.g.,
- PHASE-00 (`phases/phase-00-prepare.md`): Single source consolidation of Huly context (fetched once) and API readiness:
  - Case 1 (BE_API_READY — `[INFO_NOTE]`): summarizes existing BE endpoints, verification status, and alignment with user spec; pre-ticked `[x] PREPARED (INFO_READY)`.
  - Case 2 (MOCKOON_MOCKED — `[EXECUTE]`): prepares `mocks/<feature>_mockoon.json` with agreed Pass/Default & Fail rules and verifies `mockoon-cli`; once executed by `code_writer` and approved by `code_reviewer`, tick `[x] PREPARED / COMPLETED` before starting `PHASE-01`.
  - Case 3 (No external API — `[INFO_NOTE]`): omits API section; pre-ticked `[x] PREPARED (NO_EXTERNAL_API)`.
-->

## Dependency order and ownership

{{OrderedBoundedTasksAndOptionalLinkedBehaviorPhases}}

## Acceptance coverage

| AC ID | Task or phase | Decisive check | Evidence target |
|---|---|---|---|
{{AcMapping}}

## Client checks and recovery

{{ActualWorkspaceCommandsVisualTargetsRisksAndRecoveryOrReasonedNA}}

For screen work, include affected screen/registry/route paths and the screen-level checks the stack's verification skill requires (analyzer, lifecycle/tracking, layout targets). A missing active base-screen API required by the approved profile blocks the phase.

