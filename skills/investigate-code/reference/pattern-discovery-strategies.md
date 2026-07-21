# Pattern Discovery Strategies

## Structural Fingerprint

Capture these dimensions when extracting a feature's fingerprint:

| Dimension | Example |
|---|---|
| **Entry point** | REST `POST /orders`, Kafka `OrderPlaced` listener, `@Scheduled` job |
| **Layer chain** | Controller → Orchestrator → Service → Adapter → External |
| **Stereotypes** | `@RestController`, `@Service`, `@Repository`, `@Component` |
| **External interactions** | HTTP REST, Kafka publish, JDBC write |
| **Error handling** | `try/catch` → retry (3×), circuit breaker, DLQ, `@Transactional` rollback |
| **Configuration** | Route prefix `/api/v1/orders`, topic `order.*`, feature flag |

## Search Heuristics (priority order)

1. **Package naming** — Features in sibling packages often follow the same pattern
2. **Suffix matching** — `*Controller`, `*Orchestrator`, `*Adapter`, `*Repository`
3. **Interface implementations** — All classes implementing the same interface
4. **Annotation presence** — Classes sharing `@RestController`, `@KafkaListener`, etc.
5. **Dependency mirroring** — Services calling the same adapters or siblings

## Comparison Matrix

```
Feature: Order Checkout (fingerprint)
├─ Controller: CheckoutController
├─ Orchestrator: CheckoutOrchestrator
├─ Service: OrderService
├─ Adapters: PaymentAdapter, InventoryAdapter (HTTP)
└─ Events: publish(OrderConfirmed) → Kafka

Candidate: Refund Flow
├─ Controller: RefundController          ✓ match
├─ Orchestrator: RefundOrchestrator      ✓ match
├─ Service: RefundService                ✓ match
├─ Adapters: PaymentAdapter (HTTP)       ✓ match
└─ Events: publish(RefundProcessed)      ✓ match
→ Consistent pattern

Candidate: Inventory Restock
├─ Entry: @Scheduled job                 ✗ different entry
├─ Orchestrator: RestockOrchestrator     ~ partial
├─ Service: InventoryService             ✓ match
├─ Adapters: (none — direct DB)          ✗ different
└─ Events: publish(StockUpdated)         ✓ match
→ Different pattern (batch, not request-driven)
```

## Inconsistency Severity

| Level | Description | Action |
|---|---|---|
| **Style** | Same structure, different naming | Note, low priority |
| **Variant** | Same layers, different technology | Flag, suggest alignment |
| **Structural** | Different layer chain or responsibilities | Flag with impact analysis |
| **Architectural** | Completely different pattern for same concept | Flag as significant inconsistency |
