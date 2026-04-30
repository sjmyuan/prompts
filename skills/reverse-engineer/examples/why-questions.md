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

## Step 2 — Investigate Codebase & Present Answer

Applies **investigate-codebase** then **present-answer**.

### Architecture Analysis
- Review system architecture documentation
- Analyze event listener implementation
- Check for API endpoints
- Review ADR (Architecture Decision Records) if available

### Documentation Review
```markdown
# From docs/architecture.md
- Asynchronous processing for large data catalogs
- Loose coupling between data source and external API
- Event-driven integration pattern
```

### Code Structure Analysis
```
infrastructure/
├── eventlistener/
│   ├── DataImportedListener.java  <- Event consumer
│   └── CloudEventFactory.java
└── externaladapter/
    └── EventPublisherImpl.java  <- Event publisher
```

### Benefits Identified

**From Implementation**:
```java
@KafkaListener(topics = "data.imported")
public void onDataImported(String message) {
    // Async processing
    // No blocking calls
    // Automatic retry handling
}
```

**Advantages**:
1. **Scalability**: Can process thousands of records asynchronously
2. **Resilience**: Message queue provides retry and error handling
3. **Loose Coupling**: Data source doesn't need to know about external API
4. **Performance**: Non-blocking operations
5. **Reliability**: Message persistence ensures no data loss

### Trade-offs Considered
- **Eventual consistency** vs **immediate consistency**
- **Complexity** vs **Scalability**
- **Debugging difficulty** vs **System resilience**

### Answer Compilation
The service uses event-driven architecture for several key reasons:

1. **Asynchronous Processing**: Data imports can be large batches; async processing prevents timeouts
2. **Scalability**: Can scale consumers independently based on load
3. **Loose Coupling**: Data source and external API systems are decoupled
4. **Resilience**: Built-in retry, error handling, and message persistence
5. **Performance**: Non-blocking operations allow higher throughput

The trade-off is eventual consistency, but for data synchronization, this is acceptable as records don't need immediate real-time updates.

**Decision documented in**: `docs/architecture.md`
