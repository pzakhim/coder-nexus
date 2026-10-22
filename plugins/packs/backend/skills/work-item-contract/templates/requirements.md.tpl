# Requirements: {{Title}} — {{version}}

> **Document type**: REQUIREMENTS
> **Work Item**: {{slug}}
> **Target Service**: {{service}}
> **Type**: {{type}}
> **Version**: {{version}}
> **Created**: {{CreatedDate}}
> **Source references**: {{SourceReferences}}
> **Context file**: `codebase-notes.md`
> **Status**: PENDING_REVIEW
> **Approval reference**: NONE

## 0. Goals

> Confirmed with the user before any other question (core `goal-framing`). Every BR, AC, design element and phase serves one of these. Anything else is a non-goal.

| Goal ID | Goal (outcome: actor + result) | Success signal (observable) | Source | Status |
|---|---|---|---|---|
| G-01 | {{OutcomeGoal}} | {{ObservableSuccessSignal}} | {{SourcesAndConfirmingDecision_D-NN}} | CONFIRMED |

- **Non-goals**: {{NonGoalsWithReasonOrNone}}

## 1. Scope & Alignment

- **Current baseline & problem**: {{ObservedBaselineAndDesiredResult}}
- **Scope in**: {{endpoints}}
- **Scope out**: {{ScopeOutOrReasonedNone}}
- **Handshake reference**: {{handshake_contract}}

## 2. Actors & Permissions

{{ActorsAndRbacExpectations}}

## 3. Business Rules

| Rule ID | Business Rule Description | Goal | Decision Ref |
|---|---|---|---|
| **BR-01** | {{ConciseBusinessRule}} | G-01 | `D-01` |

## 4. Behavioral Scenarios

### Scenario 1: {{HappyPathTitle}} (`AC-01`, `D-01`)
- **Given**: {{Precondition}}
- **When**: {{ApiRequestOrTrigger}}
- **Then**: {{ExpectedResponseAndSideEffects}}

### Scenario 2: {{UnhappyOrEdgeCaseTitle}} (`AC-02`, `D-01`)
- **Given**: {{Precondition}}
- **When**: {{InvalidPayloadOrUnauthorizedTrigger}}
- **Then**: {{ExpectedErrorResponseAndRollback}}

## 5. Acceptance criteria

| AC ID | Observable behavior | Source | Status | Goal |
|---|---|---|---|---|
{{AcceptanceCriteriaRows}}

## 6. Gate 1 approval

- **Decision summary**: {{UserFacingSummary}}
- **Approved response**: NONE
- **Approved document revision**: NONE
