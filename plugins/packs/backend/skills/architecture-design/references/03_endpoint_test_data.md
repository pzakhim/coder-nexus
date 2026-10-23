# Test Data per Endpoint

Detail for [backend architecture design](../SKILL.md) §4.

Every endpoint defined in `design.md` must have explicit test scenarios specified before Gate 2 approval. These tables provide deterministic test fixtures and prevent happy-path bias.

## 1. Scenario Categories

For each path operation:
1. **Pass / Default**: Valid request with nominal inputs; returns 200/201.
2. **Fail (Validation)**: Invalid payload types, missing required fields, boundary violations; returns 422.
3. **Fail (Authentication / Authorization)**: Missing or invalid token (401), unauthorized role or cross-tenant access attempt (403/404).
4. **Fail (Business Rule / Conflict)**: State transition violation, duplicate key, or missing parent entity; returns 400/409/404.
5. **Empty (Queries & Lists)**: Search or list request where no records match; returns 200 with empty list `[]` (never 404).

## 2. Table Format

Include the following columns in `design.md` under `### Test data per endpoint`:

| Endpoint | Scenario | Role / Actor | Precondition | Input Payload / Query | Expected Status | Expected Body / Code |
|---|---|---|---|---|---|---|
| `POST /orders` | Pass nominal | `buyer` | User exists with balance >= 100 | `{"item_id": "item_1", "qty": 1}` | `201 Created` | `{"id": "...", "status": "pending"}` |
| `POST /orders` | Fail out of stock | `buyer` | `item_2` stock is 0 | `{"item_id": "item_2", "qty": 1}` | `400 Bad Request` | `{"detail": "OUT_OF_STOCK"}` |
| `POST /orders` | Fail forbidden | `guest` | Unauthenticated | `{"item_id": "item_1", "qty": 1}` | `401 Unauthorized` | `{"detail": "UNAUTHENTICATED"}` |
| `GET /orders` | Empty list | `buyer` | User has 0 orders | `page=1&limit=20` | `200 OK` | `{"items": [], "total": 0}` |

## 3. Usage Across Roles

- **Planning**: Drafts and validates tables with user at Gate 2.
- **Code Writer**: Uses preconditions to seed test fixtures in `PHASE-00` and unit tests in `{{slot:unit-testing}}`.
- **Code Reviewer**: Rejects with `CHANGES_REQUESTED` if any endpoint lacks error or boundary test cases.
- **Test Runner**: Executes acceptance probes against real deployment.
