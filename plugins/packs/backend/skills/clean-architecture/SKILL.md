---
name: clean-architecture
description: Layered Clean Architecture guidance for Backend services (Domain, UseCases, Repositories, Controllers).
---

# Backend Clean Architecture

Guides backend implementation to adhere to strict dependency rules:
1. **Domain**: Pure business entities and business invariants.
2. **UseCases (Application)**: Business workflows and orchestration.
3. **Infrastructure**: Database repositories, ORM mappers, third-party adapters.
4. **Presentation**: HTTP/gRPC handlers, serializers, routing.

## Layer contents (implementation)

- **Domain Layer**: Pure business entities, value objects, and repository interfaces. Strictly ZERO dependencies on database engines, ORMs, or web frameworks.
- **Application Layer**: UseCases orchestrating business flows and transactions.
- **Infrastructure & Data Layer**: Database repositories, external client adapters, and migrations.
- **Presentation & API Layer**: REST/GraphQL routers, controllers, request validation, and response serialization matching `api_contract.json`.

Full rules: [backend_clean_architecture_rules.md](../../rules/backend_clean_architecture_rules.md).
