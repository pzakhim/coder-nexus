# Where domain facts usually are

Read-only. Use only what the workspace has; skip a row when the category does not exist. Names below are illustrations.

| Fact | Typical places | What to extract |
|---|---|---|
| Entities and fields | ORM models (SQLAlchemy, Django, Prisma, TypeORM, Entity Framework, Frappe DocTypes), migrations, DTOs/schemas, mobile/web model classes | Entity names, key fields, relations |
| Status values | Enums, `status`/`state` columns, constants, state machines, workflow configs | The values and their order |
| Transitions | Service methods that change status, state-machine tables, workflow definitions, guards | From → to, trigger (user action, job, event), where enforced |
| Roles | Role enums/tables, permission decorators or guards, policy classes, route guards in the front end | Role names and the actions they allow |
| Data scopes | Query filters added for every request (by customer, organization, owner, environment…), row-level security, repository base classes | The condition and which roles bypass it |
| User-facing words | Translation files (`i18n`, `l10n`, `.arb`, `locales/*.json`), UI labels, error messages | Business names for code keys |
| Business documents | `docs/`, BA specs, approved `requirements.md` in `.superpowers/work-items/` or `docs/features/`, README sections | Definitions, rules, glossary drafts |
| Existing glossary | `GLOSSARY.md`, `docs/*glossary*`, `codebase-notes.md` → Glossary | Terms to keep verbatim (P5) |
| Tracker history (optional) | Closed tickets, with the user's agreement and a configured tracker | Recurring terms and rules |

Useful searches (adapt to the stack):

```sh
rg -n "class .*\(.*Model\)|@Entity|model [A-Z]" <be_dir>
rg -n "status|state" -g "*enum*" -g "*constants*" <src>
rg -n "permission|has_role|@roles|can\(|authorize" <src>
rg --files -g "*locale*" -g "*i18n*" -g "*.arb"
```
