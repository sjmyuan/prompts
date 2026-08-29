# Example: Plain-Language Findings (Before → After)

## User Request
"Review this change: a bug fix for duplicate product events."

## Before — vague, unactionable

### 🟡 Minor Issues

#### Consider improving the idempotency approach
- **File**: [EventPublisherImpl.java](EventPublisherImpl.java#L28-L30)
- **Issue**: The idempotency implementation could be better.
- **Impact**: Potential issues over time.
- **Recommendation**: Consider a more robust approach.

A finding that names no exact behavior, no specific consequence, and no concrete fix — the developer cannot act on it.

## After — concrete and actionable

> Severity legend: 🚫 Blocker = must fix before merge · 🔴 Major = should fix · 🟡 Minor = nice to fix · 🟢 Nit = polish · ⚠️ Inconsistency = decision required

### 🟡 Minor Issues

#### Unbounded in-memory Set grows forever
- **File**: [EventPublisherImpl.java](EventPublisherImpl.java#L28-L30)
- **Issue**: `publishedMessageIds` is a `HashSet<String>` with no size limit or eviction. In a long-running service, it accumulates every message ID ever published and never shrinks.
- **Impact**: Slow memory growth over the service's lifetime; in a high-throughput deployment the Set can reach hundreds of thousands of entries, raising GC pressure and heap usage until restart.
- **Recommendation**: Use a bounded cache with expiration:
```java
private final Cache<String, Boolean> publishedMessageIds = Caffeine.newBuilder()
  .maximumSize(10_000)
  .expireAfterWrite(Duration.ofHours(1))
  .build();
```

## What changed

| Before | After |
|---|---|
| Vague "could be better" | Names the exact code and behavior (`HashSet`, no eviction) |
| "Potential issues over time" | Specific consequence (unbounded growth → heap/GC pressure) |
| "Consider a more robust approach" | Concrete fix with code snippet |
| No legend | One-line severity legend at first use |
