# Requirements: {{FeatureTitle}} — {{Version}}

> **Document type**: REQUIREMENTS
> **Work Item**: {{slug}}
> **Feature**: {{module}}/{{feature}}
> **Type**: {{Type}}
> **Version**: {{Version}}
> **Created**: {{CreatedDate}}
> **Source references**: {{SourceReferences}}
> **Context file**: `codebase-notes.md`
> **Status**: PENDING_REVIEW
> **Approval reference**: NONE

## 0. Goals

> Confirmed with the user before any other question ([goal framing](../../requirements-elicitation/SKILL.md)). Every BR, AC, design element and phase serves one of these. Anything else is a non-goal.

| Goal ID | Goal (outcome: actor + result) | Success signal (observable) | Source | Status |
|---|---|---|---|---|
| G-01 | {{OutcomeGoal}} | {{ObservableSuccessSignal}} | {{SourcesAndConfirmingDecision_D-NN}} | CONFIRMED |

- **Non-goals**: {{NonGoalsWithReasonOrNone}}
- **Anti-goals**: {{OutcomesThatCountAsFailureEvenIfItWorksOrNone}}

## 1. Scope & Alignment

- **Current baseline & problem**: {{ObservedBaselineAndDesiredResult}}
- **Scope in**: {{ScopeIn}}
- **Scope out**: {{ScopeOutOrReasonedNone}}
- **API & Design sources**: {{ApiStatusReadyMockedOrNoExternalApiHandshakeReferenceAndVisualSourceOrNA}}

## 2. Actors & Permissions

{{ActorsAndPermissions}}

## 3. Business Rules

| Rule ID | Business / UX Rule Description | Goal | Decision Ref |
|---|---|---|---|
| **BR-01** | {{ConciseBusinessOrUxRule}} | G-01 | `D-01` |

## Workflows

> Only for items with an approved UI/UX design (`design-uiux/uiux.md`, revision {{UiuxRevision}}); delete this section otherwise. Every `W-NN` of the approved revision appears here (`validate_proposal_spec` rule `REQ-006`).

| Workflow | Goal | Steps → screens | Scenarios / AC |
|---|---|---|---|
| W-01 | G-01 | {{OrderedStepsWithScreenIds}} | {{ScenarioAndAcIds}} |

## 4. Behavioral Scenarios & Visual States

### Scenario 1: {{HappyPathTitle}} (`AC-01`, `D-01`)
- **Given**: {{Precondition}}
- **When**: {{UserActionRequestOrTrigger}}
- **Then**: {{ExpectedOutcomeAndSideEffects}}

### Scenario 2: {{UnhappyOrEdgeCaseTitle}} (`AC-02`, `D-01`)
- **Given**: {{Precondition}}
- **When**: {{InvalidInputUnauthorizedOrFailureTrigger}}
- **Then**: {{ExpectedErrorEmptyStateOrRollbackBehavior}}

### Four Mandatory Visual States (UI Work Items)

> Delete this subsection for items with no UI impact.

- **Default / Content**: {{NormalContentExpectation}}
- **Loading**: {{LoadingExpectation}}
- **Empty**: {{EmptyStateExpectation}}
- **Error**: {{ErrorStateAndRetryExpectation}}

## 5. Acceptance criteria

| AC ID | Observable behavior | Source | Status | Goal |
|---|---|---|---|---|
{{AcceptanceCriteriaRows}}

## 6. Gate 1 approval

- **Decision summary**: {{UserFacingSummary}}
- **Approved response**: NONE
- **Approved document revision**: NONE

Keep Huly read-only. Every `BR-NN` must trace to a confirmed `D-NN` in `codebase-notes.md`. Never leave `Option A / Option B`, `Open Questions`, or `TBD` in this document.
