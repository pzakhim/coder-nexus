---
name: be-clean-architecture
description: Layered Clean Architecture guidance for Backend services (Domain, UseCases, Repositories, Controllers).
---

# Backend Clean Architecture

Guides backend implementation to adhere to strict dependency rules:
1. **Domain**: Pure business entities and business invariants.
2. **UseCases (Application)**: Business workflows and orchestration.
3. **Infrastructure**: Database repositories, ORM mappers, third-party adapters.
4. **Presentation**: HTTP/gRPC handlers, serializers, routing.
