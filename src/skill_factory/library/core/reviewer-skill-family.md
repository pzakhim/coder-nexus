# The Code Reviewer skill family

Rules shared by the Code Review Pack generators. The reviewer reuses the Engineering skills as **grading rubrics**; it does not get separate copies of them. See [coder-skill-family.md](coder-skill-family.md) for those skills.

## Ownership

| Skill (`.agents/skills/<name>/`) | Role in review | Used when |
|---|---|---|
| `code-review` | The review process: fixed revision, order of passes, axes, findings, verdicts, rounds, report | Every review |
| `bug-hunt` | First pass: real defects (`standard` / `deep` effort) | Before the compliance axes |
| `clean-architecture` | Rubric for placement and dependency rules (+ its gates) | Architecture axis |
| `clean-code` | Rubric for naming, size, errors, types (+ its severities) | Code quality axis |
| `unit-testing` | Rubric for case coverage and assertion strength; rerun the suite | Tests axis |
| `secure-coding-standards` | Rubric for input, authorization, scopes, secrets | Security axis |
| `database-migrations` | Rubric for schema/data changes | Migrations axis (backend) |
| `security-review` | Threat-focused review (Security role, or the reviewer in reviewer mode) — see [security-skill-family.md](security-skill-family.md) | Changes matching the review triggers |

When a rubric skill is missing in the workspace, `code-review` falls back to its own short checklist for that axis and says "not set up in this workspace".

## Vocabulary

| Term | Meaning |
|---|---|
| Review revision | The exact tree under review (base + review revision + uncommitted scope) |
| Axis | One independent dimension of the review (plan, architecture, quality, tests, security, contract, UI, migrations) |
| Finding | One problem with rule/axis, location, reason, severity and fix direction |
| `APPROVED` | Every applicable check passed on the review revision |
| `CHANGES_REQUESTED` | At least one blocking finding |
| `BLOCKED` | Required evidence is missing (cannot decide) |

Keep the workspace's own verdict words and finding IDs when it has them (P5) and map them to this table.

## Boundaries

- The reviewer is **read-only** toward application code and tests; any edit creates a new revision to review.
- The reviewer has **no authority to waive** a rule; disagreements go back to planning or the user.
- Gates and tests are rerun by the reviewer on the review revision; the writer's evidence is input, not proof.
