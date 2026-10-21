# Backend Bug Patterns

Stack checklist for dimension 6 of `bug-hunt`. Check only the patterns the changed code can hit; each hit still needs a failure scenario and verification.

## Data integrity

- Multi-table write without a transaction, or a transaction whose failure path commits partial work.
- Check-then-act race (read, decide, write) without a lock, unique constraint or conditional update; lost update on concurrent edits.
- Non-idempotent handler behind a client or queue retry: duplicate rows, double charges, repeated notifications.
- Migration that breaks the running version (dropped/renamed column still read, non-null column without default).
- Float used for money; rounding applied at different layers.

## Authorization and input

- Authentication present but object-level authorization missing: user A reads or edits user B's record by changing an ID.
- SQL, shell or template built by string concatenation with request data.
- Mass assignment: request body bound straight to a model, letting the client set owner, role or status.
- Unbounded `limit`/page size or query without pagination on a growing table.

## Queries and resources

- N+1 queries inside a loop over a result set.
- Connection, session, file or cursor not released on the error path.
- Exceptions swallowed or mapped to `200` with an empty body; status code differs from `api_contract.json`.

## Time and contract

- Naive datetimes mixed with aware ones; "today" computed in server timezone instead of the user's.
- Response field renamed, removed or changed in nullability without updating `api_contract.json` and its consumers.
