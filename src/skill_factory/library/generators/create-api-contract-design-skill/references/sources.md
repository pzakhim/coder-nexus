# Sources

External ideas behind the tightened AP3, AP6 and AP8. Ideas were rewritten in Coder Nexus vocabulary; nothing is copied. Stars as of 2026-10.

| Source (pinned) | Stars | Idea taken | Where used |
|---|---|---|---|
| [addyosmani/agent-skills `skills/api-and-interface-design/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/api-and-interface-design/SKILL.md) | 109k | Idempotency key derived from intent, claimed atomically by a unique constraint, changed payload rejected, deliberate in-flight duplicate answer, timeout = unknown outcome, retention from the longest retry path | AP8 → 01 "Safe mutations", 05 |
| same | 109k | Hyrum's Law: observable behavior becomes contract | AP6 → 04 |
| same | 109k | One-Version Rule: extend instead of forking versions | AP6 → 04 |
| same | 109k | Prefer addition over modification | AP6 → 04, SKILL |
| same | 109k | One error strategy everywhere | AP3 → 01 "Errors" (one envelope, referenced) |

## Not adopted

| Idea | Why not |
|---|---|
| Fixed naming table (camelCase fields, plural nouns, UPPER_SNAKE enums) | AP2 documents the workspace's own conventions; a generator default would fight an established API. |
| Validate only at boundaries, third-party responses untrusted | Owned by `secure-coding-standards` (input validation at trust boundaries). |
| Fixed status-code map and PATCH over PUT | The workspace's existing usage wins (Step 3, adopt mode keeps codes verbatim). |
| Branded ID types and discriminated unions | Language-specific; a stack-neutral generator leaves type idioms to the stack. |
| Mandatory pagination on every list | AP4 already covers lists in the workspace's style; "every list" is decided per workspace. |
