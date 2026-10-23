> **LEGACY read-only migration template.** New work belongs in `docs/features/<module>/<feature>/vN/` using requirements, design, plan and phase templates. Historical approval markers do not establish user consent.

# Technical Proposal: {{FeatureTitle}}

> **Source task:** {{HulyTaskId}} — {{FeatureTitle}}
> **Owner module:** `lib/modules/{{feature_name}}/`
> **Created:** {{CreatedDate}}
> **Design approval status:** `PENDING_REVIEW`

## 1. Business context and Acceptance Criteria

- **Actual Huly task:** [{{HulyTaskId}}]({{HulyTaskUrl}})
- **Business description:** {{BusinessDescription}}
- **Source-backed ACs:** {{AcceptanceCriteriaList}}

## 2. Context Scan

- **Scope:** `{{ScopeClassification}}` <!-- INIT | EXTEND | CORE IMPACT -->
- **Client package:** `{{PackageName}}` (from the Client's dependency manifest)
- **State pattern:** `{{StatePattern}}` <!-- BaseBlocState | Equatable -->
- **Owner path:** `lib/modules/{{feature_name}}/`
- **Existing files:** {{RelatedExistingFiles}}
- **DI anchor:** {{ResolvedDiAnchors}}
- **Router anchor:** {{ResolvedRouterAnchors}}

## 3. Visual Intake Gate and Visual AC

- **Inspected design source:** {{DesignVisualSource}}
- **Visual intake status:** `{{VisualIntakeStatus}}`
- **Layout:** {{VisualLayoutHierarchy}}
- **Spacing:** {{VisualSpacingGrid}}
- **Typography and colors:** {{VisualTypographyAndColors}}
- **Required visual states:** {{VisualStates}}
- **Visual AC:** {{VisualAcceptanceCriteriaList}}

A material difference from the approved Designer visual is `FAILED`, even if the code compiles.

## 4. Architectural Options and Trade-Offs

### Option A: {{OptionATitle}}
- Description: {{OptionADescription}}
- Benefits: verified architecture and UI reuse where applicable.
- Costs and risks: {{OptionACons}}

### Option B: {{OptionBTitle}}
- Description: {{OptionBDescription}}
- Benefits: {{OptionBPros}}
- Costs and risks: {{OptionBCons}}

**Chosen option and reason:** {{OptionARationale}}

## 5. Component Discovery Matrix

| UI element / AC | Classification | Component and variant | Client import | Source and revision | Tokens / accessibility | Gap or custom decision |
|---|---|---|---|---|---|---|
{{ComponentDiscoveryRows}}

- **Design-system differences:** {{DesignSystemAlignments}}
- **Approved feature-private widgets:** {{CustomWidgetsReport}}

## 6. Error Handling and UX Patterns

{{UXPatternsSection}}

## 7. State and Data Contracts

- **State pattern:** {{StatePatternClass}}
- **State source:** {{BlocStateCodeSnippet}}
- **Data flow:** {{DataFlowDescription}}

## 8. Multi-Screen Flow and Navigation Lifecycle

- **Flow State Architecture:** {{FlowStateArchitecture}}
- **Navigation Lifecycle and Back Button:** {{NavigationLifecycleSpec}}
- **Unhappy Paths and Failure Scenarios:** {{UnhappyPathsSpec}}
- **Inter-field Dependencies and Validation Timing:** {{InterFieldDependenciesSpec}}
- **Step-up Security:** {{StepUpSecuritySpec}}
- **Post-flow Cache Invalidation and Side Effects:** {{PostFlowSideEffectsSpec}}

Mark irrelevant axes N/A with a reason; do not invent security or cache behavior.

## 9. Pre-Review Self-Checklist

- [ ] ACs, contracts, component APIs and visual sources are real or marked `BLOCKED`.
- [ ] Scope, module owner, state convention and affected consumers were inspected.
- [ ] UI Kit candidates were searched and package APIs verified.
- [ ] No code or user approval was fabricated.

## 10. Design Approval Gate

- **Status:** `PENDING_REVIEW`
- **Actual user response and document revision:** {{ActualApprovalReferenceOrNone}}
