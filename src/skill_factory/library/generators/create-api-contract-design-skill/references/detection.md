# Where API facts are found

Read-only. Skip what the workspace does not have.

| Fact | Typical places |
|---|---|
| Contract files | `openapi.y*ml`, `swagger.json`, `*.proto`, `schema.graphql`, JSON Schemas, the API section of approved `design.md` files |
| Routes | FastAPI/Flask routers, Django `urls.py` + views/serializers, NestJS controllers, Express routers, Spring controllers, Go handlers, Frappe whitelisted methods |
| Request/response models | Pydantic models, DRF serializers, DTO classes, Zod schemas |
| Errors | Exception handlers, error middleware, error-code enums, translation keys for messages |
| Pagination | Shared pagination helpers, base list views, `page`/`limit`/`cursor` parameters |
| Auth and scopes | Auth middleware, dependency injectors, guards, permission decorators, query scope filters |
| Versioning | `/v1/` prefixes, version headers, changelogs, deprecation headers |
| Clients | Generated SDKs, `axios`/`fetch` wrappers, `dio`/`retrofit` services, API service classes in mobile apps |
| Mocks | Mockoon environments, MSW handlers, WireMock stubs, fixture folders |
| Consumers | Other apps in the repo, documented partners, mobile versions still supported (ask the user) |

```sh
rg --files -g "*openapi*" -g "*swagger*" -g "*.proto" -g "schema.graphql"
rg -n "@(app|router)\.(get|post|put|patch|delete)|@(Get|Post|Put|Patch|Delete)\(|path\(" <be_dir>
rg -n "exception_handler|ErrorHandler|@Catch|errorCode" <be_dir>
```
