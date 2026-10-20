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

## 1. Scope & Alignment

- **Current baseline & problem**: {{ObservedBaselineAndDesiredResult}}
- **Scope in**: {{ScopeIn}}
- **Scope out**: {{ScopeOutOrReasonedNone}}
- **API & Design sources**: {{BeApiReadyOrMockoonMockedAndVisualSource}}

## 2. Actors & Permissions

{{ActorsAndPermissions}}

## 3. Business Rules

| Rule ID | Business / UX Rule Description | Decision Ref |
|---|---|---|
| **BR-01** | {{ConciseBusinessOrUxRule}} | `D-01` |

## 4. Behavioral Scenarios & Visual States

### Scenario 1: {{HappyPathTitle}} (`AC-01`, `D-01`)
- **Given**: {{Precondition}}
- **When**: {{UserAction}}
- **Then**: {{ExpectedOutcome}}

### Scenario 2: {{UnhappyOrEdgeCaseTitle}} (`AC-02`, `D-01`)
- **Given**: {{Precondition}}
- **When**: {{InvalidInputOrFailureTrigger}}
- **Then**: {{ExpectedErrorOrEmptyStateBehavior}}

### Four Mandatory Visual States (UI Work Items)
- **Default / Content**: {{NormalContentExpectation}}
- **Loading**: {{LoadingExpectation}}
- **Empty**: {{EmptyStateExpectation}}
- **Error**: {{ErrorStateAndRetryExpectation}}

## 5. Acceptance criteria

| AC ID | Observable behavior | Source | Status |
|---|---|---|---|
{{AcceptanceCriteriaRows}}

## 6. Gate 1 approval

- **Decision summary**: {{UserFacingSummary}}
- **Approved response**: NONE
- **Approved document revision**: NONE
