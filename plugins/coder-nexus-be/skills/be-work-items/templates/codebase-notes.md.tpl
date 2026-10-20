# Codebase Notes & Decision Log: {{Title}} — {{version}}

- **Document Type:** `CODEBASE_NOTES`
- **Work Item:** `{{slug}}`
- **Target Service:** `{{service}}`
- **Type:** `{{type}}`
- **Version:** `{{version}}`
- **Status:** `PENDING_REVIEW`
- **Created:** `{{CreatedDate}}`
- **Updated:** `{{UpdatedDate}}`
- **Grill-Me Rounds:** `{{GrillMeRoundsCount}}`
- **Related Docs:** `requirements.md` | `design.md` | `implement-plan.md`

---

## 0. Question Queue (Q-NN)

| ID | Status (`OPEN` \| `CLOSED -> D-NN`) | Dimension | Question / Inference to Confirm | Recommended Option |
|---|---|---|---|---|
| **Q-01** | `CLOSED -> D-01` | {{Dimension}} | {{QuestionAskedToUser}} | {{RecommendedOptionPresented}} |

---

## 1. Decision Log (D-NN)

| ID | Round | Dimension | Question Asked | Options Considered | User Confirmed Decision | Impacted `BR` / `AC` / Design | Owner |
|---|---|---|---|---|---|---|---|
| **D-01** | R1 | {{Dimension}} | {{QuestionAsked}} | 1. (Recommended) {{Opt1}}<br>2. {{Opt2}} | {{ConfirmedDecision}} | `BR-01`, `AC-01` | `spec_writer` |

---

## 2. Glossary

| Business Term | Technical Equivalent (Table / Entity / Endpoint / Field) | Notes |
|---|---|---|
| {{BusinessTerm}} | `{{TechnicalSymbolOrPath}}` | {{DefinitionAndRules}} |

---

## 3. Verified Baseline Facts & Cross-Agent Notes

- **Verified Service & Route Paths:** {{VerifiedServicePaths}}
- **Database Tables & Models:** {{tables}}
- **Handshake Reference:** {{handshake_contract}}

---

## 4. Constraints & External Integrations

- **External APIs & Auth Requirements:** {{endpoints}}
- **Dependencies & Blockers:** {{dependencies}}

---

## 5. Extended Rule Details

{{ExtendedValidationSchemasAndErrorCodes}}

---

## 6. Change Log

| Date | Role | Summary |
|---|---|---|
| {{CreatedDate}} | `spec_writer` | Initialized `codebase-notes.md` and completed Gate 1 `grill-me` decision log. |
