# Backend Clean Architecture Rules

1. **Domain Purity**:
   - Entities and Value Objects must not import or depend on web frameworks (e.g. FastAPI, Express, Gin), ORMs (SQLAlchemy, Prisma, GORM), or external SDKs.
   - Domain errors and exceptions must remain framework-agnostic.

2. **Repository Abstraction**:
   - Use Cases / Services depend exclusively on Repository interfaces (ports), never on concrete database implementations (adapters).

3. **Controller / Presentation Boundary**:
   - Controllers handle HTTP routing, serialization, parameter parsing, and status code mapping.
   - Business calculations and validation logic must reside in Use Cases or Domain Entities, never inside Controllers.

4. **Contract-Driven API**:
   - Every public endpoint must conform to its agreed `api_contract.json` or OpenAPI specification.
   - Breaking contract changes require an updated Handshake agreement with Frontend consumers.
