# Preset: TypeScript / NestJS

> A starting point, not a final answer. Always tailor to the project and confirm with the user.

## Detect

`package.json` containing `@nestjs/core`. Check ORM: `@prisma/client`, `typeorm`, `@mikro-orm/core`, `drizzle-orm`.

## Framework-enforced conventions

`main.ts` bootstrap, `AppModule`, `@Module` per feature, decorators for controllers/providers. Nest CLI default naming: `<name>.<role>.ts`.

## Concept mapping

| Concept | In this stack |
|---|---|
| Presentation | `@Controller` + DTO classes (class-validator) |
| Use case | `@Injectable()` class with one `execute()` method |
| Domain entity | Plain TS class (no ORM decorators at `full`) |
| Repository interface | `abstract class` (usable as a DI token) |
| Repository implementation | `@Injectable()` class in `infrastructure/` |
| Input validation | DTO + `ValidationPipe` |
| DI / composition root | The feature's `*.module.ts` (`{ provide: OrderRepository, useClass: PrismaOrderRepository }`) |
| Config | `@nestjs/config` in `config/` |

## Standard tree (feature-first)

```
src/
  main.ts
  app.module.ts
  config/                          # config module, env validation
  common/                          # filters, guards, interceptors, pipes (technical shared)
  modules/
    orders/
      orders.module.ts             # composition root of the feature
      presentation/
        orders.controller.ts
        dto/create-order.dto.ts
      application/
        create-order.use-case.ts
      domain/
        order.entity.ts
        order.repository.ts        # abstract class
        order.errors.ts
      infrastructure/
        prisma-order.repository.ts
        order.mapper.ts
      index.ts                     # public API (module + exported providers)
test/                              # e2e
```

## Lite / full variations

- **lite:** Nest default — `orders.controller.ts`, `orders.service.ts`, `orders.module.ts`, `dto/` per feature.
- **full:** pure domain with value objects and domain events; CQRS (`@nestjs/cqrs`) only if the user wants it.

## Naming

| Kind | Pattern |
|---|---|
| File | `kebab-case.<role>.ts` (`.controller`, `.use-case`, `.entity`, `.repository`, `.dto`, `.module`) |
| Class | `PascalCase` + role (`CreateOrderUseCase`) |

## Enforcing import rules

`dependency-cruiser` (`.dependency-cruiser.js`):
```js
module.exports = {
  forbidden: [
    { name: 'domain-is-pure', severity: 'error',
      from: { path: '^src/modules/[^/]+/domain' },
      to: { path: ['^src/modules/[^/]+/(infrastructure|presentation)', '@nestjs', '@prisma'] } },
    { name: 'no-feature-internals', severity: 'error',
      from: { path: '^src/modules/([^/]+)/' },
      to: { path: '^src/modules/[^/]+/(?!index\\.ts)', pathNot: '^src/modules/$1/' } },
  ],
};
```
Verify the regex during generation; adjust to the confirmed tree.

## Stack-specific pitfalls

- Fat services doing everything (the Nest default grows into this).
- Injecting the ORM client directly into controllers or use cases.
- Exporting every provider from a module, making internals public.
- Circular module imports solved with `forwardRef` instead of fixing boundaries.

## Reference sources

Candidates to verify: NestJS official docs (modules, custom providers), well-starred NestJS clean/hexagonal architecture repos found via `gh search repos`.
