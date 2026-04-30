# Reverse Engineer: Why Questions Example

## User Request
"Why does the service use event-driven architecture instead of REST API for data imports?"

---

## Step 1 — Define Question (Broad/Ambiguous Path)

Applies **define-question**.

This question is broad — "the service" could refer to several services in the repo, and "event-driven vs REST" may relate to performance, coupling, history, or a specific trade-off. The full clarification steps apply.

**Agent asks:**
> 1. Which service are you asking about — `data-import-service`, `catalog-sync-service`, or another?
> 2. Are you looking for the original design rationale (why it was built this way) or a current trade-off assessment (is this still the right approach)?
> 3. Is there a specific concern motivating the question (e.g., latency, debugging difficulty, coupling)?

**User responds:**
> The `data-import-service`. Original design rationale — we're writing up the ADR. No specific concern.

**Agent confirms scope:**
> Investigate why `data-import-service` uses event-driven integration for data imports rather than synchronous REST calls, focusing on the original design rationale. Will examine architecture docs, ADR files, event listener implementation, and any comments indicating design intent.

*User confirms: ✅ — proceed with investigation.*

---

## Step 2 — Investigate Codebase

Applies **investigate-codebase**.

**Architecture documentation** — reads `docs/architecture.md`:
> "Asynchronous processing for large data catalogs; loose coupling between data source and external API via event-driven integration."

**ADR search** — no dedicated ADR file found; design rationale is embedded in inline comments and the architecture doc.

**Code structure analysis**:
```
infrastructure/
├── eventlistener/
│   ├── DataImportedListener.java   ← Kafka consumer
│   └── CloudEventFactory.java
└── externaladapter/
    └── EventPublisherImpl.java     ← outbound publisher
```

**Key implementation evidence**:
```java
@KafkaListener(topics = "data.imported")
public void onDataImported(String message) {
    // Async processing — no blocking calls
    // SDK-level retry handled by AmqpRetryOptions
}
```

**Trade-offs documented in comments and architecture doc**:
- Eventual consistency accepted for data synchronization use cases
- Added operational complexity (dead-letter queue, retry config) traded against system resilience

---

## Step 3 — Present Answer

Applies **present-answer**.

`data-import-service` uses event-driven architecture because the original design prioritized scalability and resilience — large catalog imports would time out under REST, and any transient failure would lose data with no recovery path.

**Five supporting reasons from the architecture doc and implementation**:
1. **Asynchronous processing** — catalog imports can contain thousands of records; async consumers prevent gateway timeouts. Evidence: `@KafkaListener` in [`DataImportedListener.java`](infrastructure/eventlistener/DataImportedListener.java).
2. **Scalability** — Kafka consumer group members scale independently; REST would require vertical scaling of the import endpoint.
3. **Loose coupling** — the data source publishes events without knowing about the external API consumer; [`EventPublisherImpl.java`](infrastructure/externaladapter/EventPublisherImpl.java) is the only integration point.
4. **Resilience** — SDK-level retry means transient failures are handled automatically; no data loss on connection drops.
5. **Message persistence** — the broker retains unprocessed messages; a consumer restart picks up where it left off without requiring a re-import.

**Trade-off acknowledged**: Eventual consistency — records do not appear in the external API immediately after import. This was an accepted trade-off for data synchronization, documented in [`docs/architecture.md`](docs/architecture.md).

**Next steps**: To assess whether event-driven is still the right approach, compare message lag metrics against current consistency requirements. To understand the retry configuration specifically, investigate `ServiceBusConfiguration.java`.
