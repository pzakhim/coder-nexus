# Generic edge-case catalog

Keep only the categories the workspace really has; give each kept category one example from the workspace. Neutral wording here; real wording in the generated skill.

| Category | Ask about |
|---|---|
| Permissions | Each role in `domain-knowledge`; users outside the data scope; a permission removed mid-flow |
| Empty and first use | No data yet, a filter with no result, a first-time user |
| Validation | Required fields, formats, limits, duplicate values, server-side vs client-side errors |
| Concurrency | Two users editing the same record, double submit, stale data after another user's change |
| Volume | Long lists, large files, slow queries, pagination boundaries |
| Lifecycle | Every status transition the change touches; actions not allowed in a status; undo/cancel |
| Numbers and money | Rounding, currency, negative values, units |
| Time | Time zones, dates at day/month boundaries, expiry, scheduling |
| Language and locale | Translations, number/date formats, right-to-left if relevant |
| Connectivity | Timeouts, offline (mobile), retries, partial failure of an external service |
| Integrations | Another system sends unexpected data, is down, or receives the change |
| Audit and history | Who changed what, whether history must be kept |
| Notifications | Who is told, when, through which channel, and when not |
