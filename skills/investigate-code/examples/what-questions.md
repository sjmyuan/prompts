# Reverse Engineer: What Questions Example

## User Request
"What external systems does this service integrate with?"

## Response Process

### 1. Search Strategy
- Look for adapter classes in infrastructure layer
- Search for configuration properties
- Check for HTTP clients and event publishers
- Review application.yaml for endpoints

### 2. Code Analysis
```java
// Found in infrastructure layer
@Component
public class EventPublisherImpl implements EventPublisher {
    // Publishes to event bus
}

// Configuration in application.yaml
externalApi:
  api:
    url: ${EXTERNAL_API_URL}
```

### 3. Integration Points Identified

**Event Bus Integration**:
- Consumes: Data imported events from data source
- Publishes: Data transformed events
- Technology: Cloud Events standard

**External API Service**:
- Data creation/updates
- Catalog management
- REST API integration

**Monitoring/Observability**:
- OpenTelemetry collector
- Prometheus metrics
- Distributed tracing

### 4. Answer Compilation
This service integrates with:

1. **Data Source System** (Input)
   - Receives data via event bus
   - Consumes DataImported events

2. **External API Service** (Output)
   - Publishes transformed data
   - REST API integration

3. **Event Bus** (Bidirectional)
   - Consumes input events
   - Publishes transformation results

4. **Observability Stack**
   - OpenTelemetry for tracing
   - Prometheus for metrics

**Configuration**: All endpoints configured via environment variables
