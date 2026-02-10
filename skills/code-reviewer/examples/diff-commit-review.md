````markdown
# Example: Diff/Commit Review (Bug Fix)

**Scenario**: Review of a bug fix commit for issue #234 - duplicate product events published to Azure Service Bus

**Review Focus**: Correctness, regression prevention, event handling

## Code Review Summary

**Scope**: Fix for issue #234 - duplicate product events being published
**Focus**: Correctness, idempotency, regression prevention
**Overall Assessment**: Requires test coverage before merge

---

## Findings

### 🔴 Major Issues

#### Missing Test for Bug Fix
- **File**: Tests missing for [EventPublisherImpl.java](EventPublisherImpl.java#L68-L75)
- **Issue**: No test verifying idempotency check prevents duplicate event publishing. The bug fix adds a Set to track published message IDs, but there's no regression test.
- **Impact**: Risk of regression in future refactors without test coverage
- **Recommendation**: Add test case in `EventPublisherImplTest`:
```java
@Test
void shouldNotPublishDuplicateEventsWithSameMessageId() {
  // Arrange
  String messageId = "test-message-123";
  OutgoingMessage message1 = createTestMessage(messageId);
  OutgoingMessage message2 = createTestMessage(messageId);
  
  // Act
  eventPublisher.publish(message1);
  eventPublisher.publish(message2);
  
  // Assert
  verify(serviceBusSender, times(1)).sendMessage(any());
}
```

#### Potential Memory Leak with Unbounded Set
- **File**: [EventPublisherImpl.java](EventPublisherImpl.java#L28-L30)
- **Issue**: Using `HashSet<String>` to track published message IDs without any cleanup or size limit. In a long-running service, this Set will grow indefinitely.
- **Impact**: Memory leak over time as the Set accumulates all message IDs ever published
- **Recommendation**: Use bounded cache with expiration:
```java
private final Cache<String, Boolean> publishedMessageIds = Caffeine.newBuilder()
  .maximumSize(10_000)
  .expireAfterWrite(Duration.ofHours(1))
  .build();
```

### 🟡 Minor Issues

#### Missing Logger Statement for Duplicate Detection
- **File**: [EventPublisherImpl.java](EventPublisherImpl.java#L71-L73)
- **Issue**: Silent return when duplicate is detected, no logging for observability
- **Impact**: Difficult to debug or monitor duplicate event scenarios in production
- **Recommendation**: Add log statement:
```java
if (publishedMessageIds.contains(messageId)) {
  log.warn("Duplicate event detected, skipping publication: messageId={}", messageId);
  return;
}
```

---

## Positive Highlights
- Root cause correctly identified - missing idempotency check
- Clean, minimal change that directly addresses the issue
- Good use of Set data structure for O(1) lookup performance

---

## Risks & Assumptions
- Assumes message IDs are unique and reliably provided
- Memory leak risk if not addressed (see major issue)
- No consideration for distributed scenarios (multiple service instances)

---

## Recommended Next Steps
1. Add regression test (required before merge)
2. Fix memory leak with bounded cache (required for production)
3. Add logging for duplicate detection (recommended for observability)
4. Consider if distributed idempotency is needed (e.g., Redis-based deduplication for multi-instance deployments)

---

## Key Review Characteristics

- **Review Type**: Diff/commit (bug fix)
- **Severity Distribution**: 2 major, 1 minor
- **Primary Concerns**: Test coverage, memory management, and observability
- **Action Required**: Must add test and fix memory leak before merge
- **Testing Recommendation**: Test both single-instance and high-volume scenarios

````
