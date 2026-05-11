# Example: Refactor Documentation

**Scenario**: Extracted message handling logic into MessageHandlerRegistry from IncomingMessageToHandlerDispatcher

**Change Type**: Refactor

---

## Change Review and Documentation Impact

Applies **maintain-docs** (steps 1–2).

**Agent reviews the change** — reads refactored files and PR description:
> `IncomingMessageToHandlerDispatcher` previously held an inline `Map<MessageType, Handler>`. A new `MessageHandlerRegistry` bean was extracted to own handler registration and lookup. The dispatcher now delegates to the registry. No external behavior change.

**Agent identifies affected documentation** (consults **impact-lookup** for refactor):
> - **docs/architecture.md**: Update to show the new `MessageHandlerRegistry` component and its relationship to the dispatcher.
> - **Developer Guide**: Update the "adding new message handlers" walkthrough to reference the registry.
> - **Inline JavaDoc**: Document the registry's registration mechanism and the reason for the extraction.
> README and user-facing docs unaffected — no observable behavior change.

---

## Documentation Updates

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
