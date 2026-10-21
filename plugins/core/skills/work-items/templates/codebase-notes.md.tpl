# Codebase Notes & Decision Log: {{FeatureTitle}} — {{Version}}

- **Document Type:** `CODEBASE_NOTES`
- **Work Item:** `{{slug}}`
- **Feature:** `{{module}}/{{feature}}`
- **Type:** `{{Type}}`
- **Version:** `{{Version}}`
- **Status:** `PENDING_REVIEW`
- **Created:** `{{CreatedDate}}`
- **Updated:** `{{UpdatedDate}}`
- **Grill-Me Rounds:** `{{GrillMeRoundsCount}}`
- **Related Docs:** `requirements.md` | `design.md` | `implementation-plan.md`

---

## 0. Question Queue (Q-NN)

> Queue every ambiguity, inference, API/UX gap, or architectural trade-off here before asking via `ask_question` (1 question per turn). Before presenting Gate 1 or Gate 2 for approval, **0 rows may remain `OPEN`**.

| ID | Status (`OPEN` \| `CLOSED -> D-NN`) | Dimension (order: grill-me §2.2) | Owner (`spec_writer` \| `designer` \| `planning`) | Question / Inference to Confirm | Recommended Option |
|---|---|---|---|---|---|
| **Q-01** | `CLOSED -> D-01` | {{Dimension}} | {{Owner}} | {{QuestionAskedToUser}} | {{RecommendedOptionPresented}} |

---

## 0A. Source Inventory

> Every source read or missing for this work item ([goal framing](../../feature-planner/references/03_goal_framing.md)). Never infer the content of an `UNREACHABLE` / `NOT_PROVIDED` source from its title.

| Source | Kind | Read status (`READ` \| `UNREACHABLE` \| `NOT_PROVIDED`) | What it contributes / conflicts |
|---|---|---|---|
| {{HulyIdOrDocOrFile}} | {{Kind}} | {{ReadStatus}} | {{ContributionOrConflict}} |

---

## 1. Decision Log (D-NN)

> Single Source of Truth for every decision confirmed by the user during `grill-me` rounds (Gate 1 `spec_writer` and Gate 2 `planning`). Options considered and ruled out live here, never as `Option A / Option B` headings in `requirements.md` or `design.md`.

| ID | Round | Dimension | Question Asked | Options Considered | User Confirmed Decision | Impacted `BR` / `AC` / Design | Owner |
|---|---|---|---|---|---|---|---|
| **D-01** | R1 | {{Dimension}} | {{QuestionAsked}} | 1. (Recommended) {{Opt1}}<br>2. {{Opt2}} | {{ConfirmedDecision}} | `BR-01`, `AC-01` | `spec_writer` |

---

## 2. Glossary

| Business / UX Term | Technical Equivalent (Entity / State / Field / Endpoint) | Notes |
|---|---|---|
| {{BusinessTerm}} | `{{TechnicalSymbolOrPath}}` | {{DefinitionAndRules}} |

---

## 3. Verified Baseline Facts & Cross-Agent Notes

- **Target Stack & Architecture Profile:** `{{StackOrFramework}}` (`{{FoundationProfileDefinedByStackPack}}`)
- **Verified Module & Routing Paths:** {{VerifiedPathsFromCodebaseScan}}
- **Core / UI Kit Discovery (stack foundation skill):** {{VerifiedCoreAndUiKitCandidates}}
- **Cross-Agent Technical Consultation Notes (`planning` / `code_writer`):** {{VerifiedCrossAgentAnswersOrNone}}

---

## 4. Constraints & External Integrations

- **Backend API Integration Status:** `{{BE_API_READY_or_MOCKOON_MOCKED}}`
- **API / Handshake Source:** {{BeApiSpecOrMockoonJsonRef}}
- **Performance / Security / Offline Constraints:** {{VerifiedConstraintsOrReasonedNone}}

---

## 5. Extended Rule Details

{{DetailedValidationTablesPayloadFieldMappingsOrStateRulesReferencedByBrIds}}

---

## 6. Change Log

| Date | Role | Summary |
|---|---|---|
| {{CreatedDate}} | `spec_writer` | Initialized `codebase-notes.md` and completed Gate 1 `grill-me` decision log. |
