# Where Domain Facts Usually Are

Read-only discovery guide. Inspect only the sources the workspace actually has; record `N/A for this workspace` when a category does not exist. All search commands use `<src>` so discovery stays 100% stack-agnostic.

| Fact | Typical Places in `<src>` | What to Extract |
|---|---|---|
| Entities and fields | Domain models, ORM entities, database schemas/migrations, DTOs, state/model classes | Entity names, owning module, key fields, relations |
| Status values | Enums, `status`/`state` columns, constants, state machines, workflow definitions | Allowed status values and terminal states |
| Transitions | Domain/application services that mutate status, state-machine tables, transition guards | `From → To`, trigger actor/event, `file:symbol` where enforced |
| Roles | Role enums/tables, authorization decorators, policy/guard classes, route guards | Role names and permitted actions |
| Data scopes | Query filters applied per request (tenant, organization, branch, owner), row-level security, base repositories | Filtering condition, bypass roles, `file:symbol` enforcement point |
| User-facing words | Localization/translation files (`i18n`, `l10n`, `.arb`, `locales/*.json`), UI labels, validation messages | Team-language business names mapped to code identifiers |
| Business documents | `docs/`, BA specifications, approved `requirements.md` in `.superpowers/work-items/` or `docs/features/`, `README.md` | Definitions, invariants, candidate business rules |
| Existing glossary | `GLOSSARY.md`, `docs/*glossary*`, `codebase-notes.md` → Glossary | Existing terms, IDs, and confirmed meanings to preserve verbatim |
| Tracker history (optional) | Closed tickets, only when a tracker is configured and the user agrees | Recurring domain terms, synonyms, and business rules |

Stack-agnostic `rg` searches (adapt globs to the workspace):

```sh
rg -n "class .*\(.*Model\)|@Entity|model [A-Z]|struct [A-Z]" <src>
rg -n "status|state" -g "*enum*" -g "*const*" <src>
rg -n "permission|has_role|@roles|can\(|authorize|guard" <src>
rg --files -g "*locale*" -g "*i18n*" -g "*.arb" <src>
```
