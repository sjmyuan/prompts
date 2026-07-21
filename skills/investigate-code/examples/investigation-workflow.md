# Example: Typical Code Investigation

## User Request
"How does the data transformation process work in the `data-import-service`?"

---

## Step 1 — Clarify & Investigate

Applies investigate-codebase.

The question is broad — agent asks: "Which service specifically, and are you asking about the full pipeline or a specific step?" User clarifies: "The `data-import-service`, full pipeline from event arrival to publishing."

**Entry point discovery** — grepping for listeners and handlers:

```
infrastructure/eventlistener/
├── DataImportedListener.java              ← entry point: consumes events
└── IncomingMessageToHandlerDispatcher.java ← routes by message type
application/service/
└── DataImportedHandler.java               ← orchestrates transformation
domain/service/
└── DataTransformer.java                   ← core field-mapping logic
infrastructure/externaladapter/
└── EventPublisherImpl.java                ← exit point: publishes results
```

**Control flow**: `DataImportedListener` → `IncomingMessageToHandlerDispatcher` → `DataImportedHandler` → `DataTransformer` → `EventPublisherImpl`

**Data flow**: Raw JSON → `DataImported` event → `DataRecord` → `ExternalApiData` (transformed) → outbound topic

**Architectural pattern**: Clean Architecture — infrastructure layer consumes/publishes, application layer orchestrates, domain layer owns transformation logic.

---

## Step 2 — Present Findings

The `data-import-service` transforms data through a four-layer pipeline:

1. **Event arrival** — [`DataImportedListener.java`](infrastructure/eventlistener/DataImportedListener.java) consumes messages and deserializes them into `DataImported` domain events.
2. **Routing** — [`IncomingMessageToHandlerDispatcher.java`](infrastructure/eventlistener/IncomingMessageToHandlerDispatcher.java) inspects the event type and routes to `DataImportedHandler`.
3. **Orchestration** — [`DataImportedHandler.java`](application/service/DataImportedHandler.java) calls `DataTransformer.transform()` to convert `DataRecord` into `ExternalApiData`.
4. **Core transformation** — [`DataTransformer.java`](domain/service/DataTransformer.java) contains all field-mapping: ID normalization, category mapping, price calculation.
5. **Publishing** — [`EventPublisherImpl.java`](infrastructure/externaladapter/EventPublisherImpl.java) serializes `ExternalApiData` and sends to the outbound topic.

**Design rationale**: Clean Architecture boundary means `DataTransformer` has no knowledge of message formats — all serialization lives in infrastructure. This makes transformation logic independently testable.

**Next steps**: For individual field-mapping rules, investigate `DataTransformer.transform()` directly. For error handling, check `DataImportedHandler` for retry/dead-letter routing.

---

## Variation: "Why" Questions

When the user asks "why" (e.g., "Why does the service use event-driven architecture instead of REST?"), the same investigate-codebase capability applies, but the synthesis step emphasizes design rationale:

- Search architecture docs, ADRs, and inline comments for design intent
- Look for evidence of trade-offs (e.g., eventual consistency documented in `docs/architecture.md`)
- Present: direct answer → supporting evidence from code/docs → acknowledged trade-offs

## Variation: "Where" Questions

For "where" questions (e.g., "Where is data validation implemented?"), investigate-codebase focuses on file-level location:

- Search for validation-related classes and annotations
- Present as layered map: Domain layer (`DataRecord.validate()`) → Application layer (`DataImportedHandler`) → Infrastructure layer (`DataValidator`)
- Include pattern observation (e.g., "Following Clean Architecture, core validation lives in domain")

## Variation: "When" Questions

For "when" questions (e.g., "When does the token get refreshed?"), focus on timing and trigger conditions:

- Search for lifecycle hooks, interceptors, timers
- Present as initialization/timing sequence with trigger conditions
- Include concrete timing details (e.g., "5-minute pre-expiry window in `AccessToken.isExpiringSoon()`")
