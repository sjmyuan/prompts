# Example: Adding a New Message Handler Feature

**Scenario**: Add ability to handle DataUpdated messages and publish transformed data updates to external API service

---

## Requirement Definition

Applies **define-requirement**.

**User request:**
> "We need to handle DataUpdated messages coming in from the message bus and publish the transformed data to our external API service."

**Agent asks clarifying questions:**
> 1. What fields does a `DataUpdated` message contain, and how does the update event differ from `DataImported`?
> 2. Should the transformation logic be the same as for `DataImported`, or does `DataUpdated` require different field mapping?
> 3. Are there existing handler and deserializer patterns we should follow for consistency?
> 4. Should the new handler publish to the same outbound topic as `DataImportedHandler`, or a separate one?

**User responds:**
> Same fields as DataImported. Updates need an additional `lastUpdated` timestamp field in the outgoing message. Yes, follow the existing handler/dispatcher/deserializer layering. Same outbound topic.

**Agent confirms requirement:**
> Add a `DataUpdatedHandler` that consumes `DataUpdated` messages, applies the existing data transformation plus a `lastUpdated` timestamp field, and publishes the result to the outbound topic via `EventPublisherImpl`. Follow the same handler/dispatcher/deserializer architecture as `DataImportedHandler`.

*User confirms: ✅*

---

## Implementation Plan

Applies **plan-implementation**.

**Steps:**
- Step 1: Validate Baseline (run tests, mvn spotless:check, mvn checkstyle:check, mvn compile)
- Step 2: Write Tests for DataUpdatedHandler
- Step 3: Confirm Test Failure
- Step 4: Implement DataUpdatedHandler
- Step 5: Verify Tests Pass
- Step 6: Refactor handler for clarity
- Step 7: Validate Refactoring
- Step 8: Write Tests for dispatcher integration
- Step 9: Confirm Test Failure for integration
- Step 10: Integrate handler with IncomingMessageToHandlerDispatcher
- Step 11: Verify Tests Pass
- Step 12: Write Tests for message deserialization
- Step 13: Confirm Test Failure for deserialization
- Step 14: Implement DataUpdatedDeserializer
- Step 15: Verify Tests Pass
- Step 16: Clean Up unused imports/code
- Step 17: Clean Up Tests
- Step 18: Verify Cleanup
- Step 19: Validate Linting, Formatting and Type Checking (mvn spotless:check, mvn checkstyle:check, mvn compile)

## Key Characteristics

- **Complexity**: Medium - involves handler, dispatcher integration, and message deserialization
- **TDD Approach**: Full cycle for each major component (handler, integration, deserializer)
- **Testing Strategy**: Separate test cycles for handler logic, dispatcher integration, and message parsing
- **Total Steps**: 19 steps with clear separation of concerns
- **Focus**: Message handling, event-driven architecture, clean architecture layers
