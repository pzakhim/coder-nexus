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

## 1. Scope & Alignment

- **Current baseline & problem**: {{ObservedBaselineAndDesiredResult}}
- **Scope in**: {{endpoints}}
- **Scope out**: {{ScopeOutOrReasonedNone}}
- **Handshake reference**: {{handshake_contract}}

## 2. Actors & Permissions

{{ActorsAndRbacExpectations}}

## 3. Business Rules

| Rule ID | Business Rule Description | Decision Ref |
|---|---|---|
| **BR-01** | {{ConciseBusinessRule}} | `D-01` |

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

| AC ID | Observable behavior | Source | Status |
|---|---|---|---|
{{AcceptanceCriteriaRows}}

## 6. Gate 1 approval

- **Decision summary**: {{UserFacingSummary}}
- **Approved response**: NONE
- **Approved document revision**: NONE
