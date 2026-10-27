# Where API Facts Are Discovered (Read-Only)

Use these read-only checks to inspect the workspace's existing API conventions in `{{target_dir}}`:

| Fact | Typical Locations |
|---|---|
| **Contract files** | `openapi.y*ml`, `openapi.json`, `*.proto`, `schema.graphql`, JSON Schemas, and approved `design.md` / `api_contract.json` files |
| **Routes & Controllers** | FastAPI/Flask routers, Django `urls.py` + views, NestJS/Spring controllers, Go handlers |
| **Request/Response Schemas** | Pydantic v2 models, DRF serializers, DTO classes, Zod schemas |
| **Error Envelope & Handlers** | Centralized exception handlers (`app/api/error_handlers.py`), error middleware, error-code enums |
| **Pagination & Filtering** | Shared pagination models (`Page[T]`), `limit`/`offset` or `cursor` query parameters |
| **Auth, RBAC & Scopes** | Security dependencies (`HTTPBearer`, `OAuth2PasswordBearer`), auth guards, tenant/owner scope filters |
| **Versioning & Deprecation** | `/api/v1` prefixes, `deprecated=True` flags, `generate_unique_id_function` |
| **Idempotency** | `Idempotency-Key` headers, atomic request-deduplication tables/unique constraints, retry interceptors |
| **Clients & Mocks** | Generated SDKs, HTTP client wrappers (`httpx`, `dio`, `fetch`), Mockoon environments (`mocks/*.json`) |

```sh
rg --files -g "*openapi*" -g "*swagger*" -g "*.proto" -g "schema.graphql" {{target_dir}}
rg -n "@(app|router)\.(get|post|put|patch|delete)|@(Get|Post|Put|Patch|Delete)\(|path\(" {{target_dir}}
rg -n "exception_handler|ErrorHandler|@Catch|errorCode" {{target_dir}}
rg -n -i "idempotency|request_id|dedup" {{target_dir}}
```
