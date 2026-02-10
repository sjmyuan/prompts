# Reverse Engineer: Why Questions Example

## User Request
"Why does the service use event-driven architecture instead of REST API for data imports?"

## Response Process

### 1. Architecture Analysis
- Review system architecture documentation
- Analyze event listener implementation
- Check for API endpoints
- Review ADR (Architecture Decision Records) if available

### 2. Documentation Review
```markdown
# From docs/architecture.md
- Asynchronous processing for large data catalogs
- Loose coupling between data source and external API
- Event-driven integration pattern
```

### 3. Code Structure Analysis
```
infrastructure/
├── eventlistener/
│   ├── DataImportedListener.java  <- Event consumer
│   └── CloudEventFactory.java
└── externaladapter/
    └── EventPublisherImpl.java  <- Event publisher
```

### 4. Benefits Identified

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

### 5. Trade-offs Considered
- **Eventual consistency** vs **immediate consistency**
- **Complexity** vs **Scalability**
- **Debugging difficulty** vs **System resilience**

### 6. Answer Compilation
The service uses event-driven architecture for several key reasons:

1. **Asynchronous Processing**: Data imports can be large batches; async processing prevents timeouts
2. **Scalability**: Can scale consumers independently based on load
3. **Loose Coupling**: Data source and external API systems are decoupled
4. **Resilience**: Built-in retry, error handling, and message persistence
5. **Performance**: Non-blocking operations allow higher throughput

The trade-off is eventual consistency, but for data synchronization, this is acceptable as records don't need immediate real-time updates.

**Decision documented in**: `docs/architecture.md`
