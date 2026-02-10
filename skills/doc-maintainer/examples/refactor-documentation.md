# Example: Refactor Documentation

**Scenario**: Extracted message handling logic into MessageHandlerRegistry from IncomingMessageToHandlerDispatcher

**Change Type**: Refactor

**Documentation Updates**:

## 1. docs/architecture.md

```markdown
### Message Handling Architecture

**MessageHandlerRegistry**: Centralized handler registration and lookup
- Location: `application/registry/MessageHandlerRegistry.java`
- Responsibilities: Handler registration, message type routing, handler lifecycle
- Pattern: Registry pattern with Spring dependency injection
- Used by: IncomingMessageToHandlerDispatcher, MessageProcessor

**Migration from inline Map**:
The handler mapping was extracted from IncomingMessageToHandlerDispatcher into a dedicated registry component to improve:
- Testability of handler registration logic
- Extensibility for dynamic handler registration
- Separation of concerns (routing vs. dispatching)
```

## 2. Developer Guide (docs/documentation.md)

```markdown
## Adding New Message Handlers

To add a new message handler:

1. Create handler class implementing `IncomingMessageHandler<T>`:
```java
@Service
public class MyMessageHandler implements IncomingMessageHandler<MyMessage> {
  @Override
  public void handle(MyMessage message) {
    // processing logic
  }
}
```

2. Register in MessageHandlerRegistry (auto-registered via Spring):
```java
@Configuration
public class HandlerConfiguration {
  @Bean
  public MessageHandlerRegistry registry(List<IncomingMessageHandler<?>> handlers) {
    return new MessageHandlerRegistry(handlers);
  }
}
```

The registry automatically discovers and registers all Spring-managed handlers.
```

## 3. Inline Documentation

Added comprehensive JavaDoc to `MessageHandlerRegistry.java` explaining registration mechanism and lookup strategy.

---

## Key Documentation Characteristics

- **Change Type**: Refactor
- **Documentation Scope**: Architecture, Developer Guide, JavaDoc
- **Primary Focus**: Code organization, extensibility patterns, developer workflow
- **Impact Level**: Medium (affects how developers add new handlers)
