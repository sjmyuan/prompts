# Reverse Engineer: How Questions Example

## User Request
"How does the data transformation process work in this service?"

---

## Step 1 — Define Question (Broad/Ambiguous Path)

Applies **define-question**.

This question is broad — "this service" could refer to multiple services in the repository, and "data transformation process" could mean the domain logic, the serialization pipeline, the infrastructure layer, or all of the above. The full clarification steps apply.

**Agent asks:**
> 1. Which service are you asking about — `data-import-service`, `catalog-sync-service`, or another?
> 2. Are you asking about the full end-to-end pipeline (event arrival to publishing) or a specific step such as field mapping or format conversion?
> 3. Is there a specific component or file you’ve already looked at that you want to start from?

**User responds:**
> The `data-import-service`. The full pipeline — event arrival to the outgoing message. No specific starting point.

**Agent confirms scope:**
> Investigate how `data-import-service` transforms incoming data events into outgoing messages — from the event listener entry point through domain logic to the event publisher. Focus on control flow and key transformation steps.

*User confirms: ✅ — proceed with investigation.*

---

## Step 2 — Investigate Codebase

Applies **investigate-codebase**.

**Entry point discovery** — semantic search for event listeners and handler classes:
```
infrastructure/
├── eventlistener/
│   ├── DataImportedListener.java              ← entry point: consumes events from message bus
│   └── IncomingMessageToHandlerDispatcher.java ← routes by message type
└── externaladapter/
    └── EventPublisherImpl.java                ← exit point: publishes transformed events
application/
└── service/
    └── DataImportedHandler.java               ← orchestrates transformation
domain/
├── model/
│   ├── DataRecord.java
│   └── ExternalApiData.java
└── service/
    └── DataTransformer.java                   ← core field-mapping logic
```

**Control flow trace**:
`DataImportedListener` → `IncomingMessageToHandlerDispatcher` → `DataImportedHandler` → `DataTransformer` → `EventPublisherImpl`

**Data flow**:
1. `DataImportedListener` receives a raw JSON payload from the message bus and deserializes it into a `DataImported` event.
2. `IncomingMessageToHandlerDispatcher` inspects the event type and routes to `DataImportedHandler`.
3. `DataImportedHandler` calls `DataTransformer.transform(record)` to map `DataRecord` fields to `ExternalApiData`.
4. The transformed `ExternalApiData` is passed to `EventPublisherImpl.publishDataTransformed()`, which serializes and sends it to the outbound topic.

**Architectural pattern**: Clean Architecture — infrastructure layer consumes and publishes; application layer orchestrates; domain layer owns transformation logic.

---

## Step 3 — Present Answer

Applies **present-answer**.

The `data-import-service` transforms data through a four-layer pipeline: event consumption → dispatch → domain transformation → publishing.

**Pipeline walkthrough**:
1. **Event arrival** — [`DataImportedListener.java`](infrastructure/eventlistener/DataImportedListener.java) consumes messages from the message bus and deserializes them into `DataImported` domain events.
2. **Routing** — [`IncomingMessageToHandlerDispatcher.java`](infrastructure/eventlistener/IncomingMessageToHandlerDispatcher.java) inspects the event type and routes to the appropriate handler.
3. **Orchestration** — [`DataImportedHandler.java`](application/service/DataImportedHandler.java) calls `DataTransformer.transform()` to convert the incoming `DataRecord` into `ExternalApiData`, then passes the result to the publisher.
4. **Core transformation** — [`DataTransformer.java`](domain/service/DataTransformer.java) contains all field-mapping logic: ID normalization, category mapping, price calculation, and localization.
5. **Publishing** — [`EventPublisherImpl.java`](infrastructure/externaladapter/EventPublisherImpl.java) serializes `ExternalApiData` and sends it to the outbound topic.

**Design rationale**: The Clean Architecture boundary means `DataTransformer` has no knowledge of message formats or external APIs — all serialization concerns live in the infrastructure layer. This makes transformation logic independently testable without a message broker.

**Next steps**: To understand individual field-mapping rules, investigate `DataTransformer.transform()` directly. To understand error handling during transformation, check `DataImportedHandler` for try/catch blocks and dead-letter routing.
