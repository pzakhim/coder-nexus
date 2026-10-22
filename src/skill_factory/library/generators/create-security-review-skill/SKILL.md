---
name: create-security-review-skill
description: Write a workspace's own security-review skill from the skill-factory knowledge base - a threat-focused review of a fixed revision - when it is triggered, a per-change threat model, the authorization matrix (role x environment x action x object), data-scope isolation, injection and deserialization, XSS and client-side secrets, secrets and personal data, outbound calls and files, dependencies and crypto, exploit scenarios with CONFIRMED/PLAUSIBLE and CRITICAL-to-LOW severity, a security sign-off verdict and safe-testing boundaries - mapped onto the workspace's auth model, scopes and stack, for fullstack repos. Use whenever the user wants to set up, standardize or update how a security agent or the reviewer reviews security in a workspace, or says things like "tạo skill security review", "review bảo mật", "kiểm tra phân quyền", "threat model", even if they do not say "skill". Writes .agents/skills/security-review/, then trial-runs it on a real diff.
argument-hint: "[stack/framework] [security role: separate | reviewer]"
---

# Create Security Review Skill

Goal: produce `<workspace>/.agents/skills/security-review/` — how security-relevant changes are reviewed in this workspace: when the review runs, who runs it, the threat model per change, the checks against the workspace's real auth model and scopes, exploit-scenario findings and the security sign-off.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/security-skill-family.md` — secure-coding-standards is how to write it safe; this skill is how to review it; bug-hunt dimension 5 is handed over when a Security role exists.

## Step 1 — Context Card (+ security context)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Security model | The workspace's `secure-coding-standards` skill if present; otherwise derive it as in that generator's `references/deriving-the-model.md` (auth, RBAC contract, scopes, secrets, protections) |
| Security role | Separate security agent/role, or the Code Reviewer runs this skill |
| Review triggers | Triggers listed in secure-coding-standards / handoff format |
| Risk areas | Auth flows, multi-tenant data, payments, migrations/backfills, external providers, file/URL handling |
| Tools available (read-only) | Security linters (bandit, semgrep, eslint-plugin-security), dependency audit (`pip-audit`, `npm audit`, `uv pip` audit), secret scanners (gitleaks, trufflehog) — only if installed |
| Authorization tests | Existing tests for 401/403 per role/environment, integration test suite |
| Vocabulary | Verdict words, finding IDs, report location, disclosure channel |

## Step 2 — Map the base rules

Read `references/base-rules.md`, `references/threat-model.md`, `references/checks-by-stack.md`. For each rule SR1–SR14: adopted, adapted, or "not adopted" with a reason. SR1, SR3, SR4, SR11, SR12, SR13 are never "not adopted".

## Step 3 — Propose

- **Mode:** separate Security role (parallel to the Code Reviewer, owns bug-hunt dimension 5) or Code Reviewer calls this skill for triggered changes.
- **Triggers and effort:** which changes require it, and which run deep (auth, RBAC, scopes, migrations of sensitive data).
- **Authorization matrix** from the RBAC contract (role × environment × action) and how each cell is evidenced (existing tests, read-only reasoning, local runs).
- **Checks per branch** with the workspace's safe patterns and available tools.
- **Severity mapping** and the sign-off criteria.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) mode and triggers, (2) authorization matrix and scopes, (3) checks and tools per branch, (4) severity, sign-off criteria and the disclosure channel.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–06`; branched: `shared/01, 02, 03, 05, 06`, `be/04`, `fe/04`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | When it runs, who runs it, the order and the sign-off on one screen |
| `references/01-scope-and-triggers.md` | `shared/01-…` | `templates/shared/01-scope-and-triggers.md.tmpl` | **Mandatory** | Reviewing the right changes at the right depth |
| `references/02-threat-model.md` | `shared/02-…` | `templates/shared/02-threat-model.md.tmpl` | **Mandatory** | A few minutes of "who could abuse this, how" finds what checklists miss |
| `references/03-authorization-and-scope.md` | `shared/03-…` | `templates/shared/03-authorization-and-scope.md.tmpl` | **Mandatory** | The matrix is where access-control bugs become visible |
| `references/04-checks.md` | `be/04-…`, `fe/04-…` | `templates/branch/04-checks.md.tmpl` | **Mandatory** | Stack-specific checks with the workspace's safe patterns and tools |
| `references/05-findings-and-verdict.md` | `shared/05-…` | `templates/shared/05-findings-and-verdict.md.tmpl` | **Mandatory** | Exploit scenarios and a sign-off everyone reads the same way |
| `references/06-report.md` | `shared/06-…` | `templates/shared/06-report.md.tmpl` | Suggested | Report and disclosure; may merge into 05 |

Writing rules: keep each template's purpose, give every rule its reason, real guards/scopes/tools, link secure-coding-standards instead of repeating its rules, never a real secret or personal data in examples, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Security review
   Security-relevant changes are reviewed per `.agents/skills/security-review/SKILL.md`.
   ```
2. Offer to link it from the security role file (or the reviewer role file in reviewer mode) (P3).
3. If `bug-hunt` and a separate Security role exist, offer to note in bug-hunt that dimension 5 is handed over here.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Review a real diff that adds or changes a mutating endpoint — is the authorization matrix filled for it?
- A diff with a seeded missing scope filter or a role-string check — found, CONFIRMED, with an exploit scenario?
- A diff adding a dependency or a file upload — checks applied with available tools?
- A diff with no security impact — "no security finding" instead of generic advice?

Compare: triggers recognised, threat model short and specific, matrix complete, findings have exploit scenarios, no unsafe testing, correct sign-off.

## Step 8 — Description

Per the authoring guide: workspace name; situations (review auth/permission/scope changes, new endpoint, file upload, external URL, dependency, "is this secure"); team trigger words. Should not trigger for writing code (secure-coding-standards does that).

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, trial results.

## Update mode

Existing `.agents/skills/security-review/` or security review sections: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep the RBAC matrix, triggers, severity scale and disclosure channel).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — SR1–SR14 with reasons
- `references/threat-model.md` — per-change threat model prompts (STRIDE-lite)
- `references/checks-by-stack.md` — security checks and read-only tools per stack
- `templates/` — `SKILL.md.tmpl`, `shared/01, 02, 03, 05, 06`, `branch/04` (suggested shapes)
- `checklist.md` — topic checks
