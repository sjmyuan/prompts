# Reverse Engineer: How Questions Example

## User Request
"How does the data transformation process work in this service?"

## Response Process

### 1. Entry Point Discovery
- Search for main controller or event listener classes
- Found: `DataImportedListener` handles incoming data events
- Entry point: Message consumption from event bus

### 2. Flow Analysis
```
DataImportedListener
  ↓
IncomingMessageToHandlerDispatcher
  ↓
DataImportedHandler (Application Service)
  ↓
Data Transformation Logic
  ↓
ExternalApiDataPort (Output Port)
  ↓
EventPublisher (Infrastructure)
```

### 3. Key Components Identified
- **Event Listener**: Receives data imported events from data source
- **Handler Dispatcher**: Routes messages to appropriate handlers
- **Domain Service**: `DataImportedHandler` orchestrates the transformation
- **Output Adapter**: Publishes transformed data to external API
- **Event Publisher**: Sends events to external systems

### 4. Data Flow
1. Data source event arrives via message bus
2. Deserialized into `DataImported` domain event
3. Handler validates and transforms data
4. Transformed data published to external API
5. Success/failure event emitted

### 5. Answer Compilation
The data transformation follows Clean Architecture:
- Events are consumed by infrastructure layer
- Dispatched to application layer handlers
- Domain logic processes transformation
- Results published via output ports
- Event-driven architecture ensures loose coupling

**Key Files**:
- Event handling: `DataImportedListener.java`
- Orchestration: `DataImportedHandler.java`
- Publishing: `EventPublisherImpl.java`
