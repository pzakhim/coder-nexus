# Change Impact: {{FeatureTitle}} — {{Version}}

> **Document type**: CHANGE_IMPACT  
> **Feature**: {{module}}/{{feature}}  
> **Version**: {{Version}}  
> **Created**: {{CreatedDate}}  
> **Source references**: {{SourceReferences}}  
> **Status**: PENDING_REVIEW  
> **Approval reference**: NONE

## Baseline

- **Previous version**: {{PreviousVersion}}
- **Previous requirements/design/as-built**: {{PreviousDocumentLinks}}
- **Baseline code revision**: {{ActualCodeRevision}}
- **Design versus actual code differences**: {{AsBuiltDifferencesOrReasonedNone}}

## Behavior delta

> List only behavior that users or downstream systems observe (rules, workflows, API responses, screens, data), not implementation steps. `ADDED` = new, `MODIFIED` = previous → new, `REMOVED` = no longer offered. Every row serves a confirmed goal or cites the `D-NN` that put it in scope.

| Delta | Behavior (`BR-NN` / `W-NN` / endpoint / screen) | Previous (as built) | New | Goal / `D-NN` | Reason and effect on existing data and users |
|---|---|---|---|---|---|
{{BehaviorDeltaRows}}

A `REMOVED` row is incomplete without its reason and what happens to existing data and users (migrated, kept read-only, deleted, or told). Reason: removal is the delta most likely to break someone silently.

## AC delta

| AC ID | Keep / Add / Change / Remove | Previous behavior | Proposed behavior | Source | Goal |
|---|---|---|---|---|---|
{{AcDeltaRows}}

`Add` / `Change` / `Remove` rows trace to an `ADDED` / `MODIFIED` / `REMOVED` behavior above.

## Code impact

| Module / file / consumer | API / data / state / route / UI / DI impact | Evidence | Risk |
|---|---|---|---|
{{CodeImpactRows}}

## Regression and migration

{{RegressionAndMigrationOrReasonedNone}}

## Decision

- **Why the change is reasonable**: {{ChangeRationale}}
- **Unresolved blockers**: {{BlockersOrReasonedNone}}

This document is part of Gate 1 for v2+. Compare the previous approved documents with actual code at the baseline revision; do not silently treat old design as implemented behavior.
