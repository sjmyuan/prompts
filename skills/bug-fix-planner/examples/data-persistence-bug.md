# Example: Data Persistence Bug Fix

**Scenario**: Event messages lost when Azure Service Bus connection is interrupted

---

## Root Cause Identification

Applies **identify-bug-root-cause**.

**User reports:**
> "We're seeing message loss when the Azure Service Bus connection drops intermittently. Some events get published but others just disappear with no error logged."

**Agent gathers information** — reads `EventPublisherImpl.java`, `ServiceBusConfiguration.java`, and their tests. Finds: `ServiceBusSenderClient` is created with no `AmqpRetryOptions`; the `sendMessage()` call in `EventPublisherImpl` has no `try/catch`; the test suite has no connection-failure scenarios.

**Agent asks clarifying questions:**
> 1. Is message loss happening on all connection drops or only prolonged outages (>5 s)?
> 2. Are there dead-letter queue entries, or are messages silently discarded?
> 3. Is the retry policy expected to be at the SDK level or the application level?

**User responds:**
> Both short and long outages trigger it. No dead-letter entries — they're silently dropped. We expected SDK-level retries.

**Agent confirms root cause:**
> The `ServiceBusSenderClient` is constructed without an `AmqpRetryOptions` policy, so any transient connection error throws immediately and the message is lost. The `sendMessage()` call in `EventPublisherImpl` has no `try/catch`, so the exception propagates silently. Two issues: (1) add retry options to `ServiceBusConfiguration`, (2) add error handling in `EventPublisherImpl`.

*User confirms: ✅*

---

**Bug-Fixing Plan**:

## Steps

- **Step 1**: Validate Baseline
- **Step 2**: Write Focused Tests for EventPublisherImpl retry handling
- **Step 3**: Confirm Test Failure for EventPublisherImpl
- **Step 4**: Fix Code for EventPublisherImpl to add retry logic
- **Step 5**: Verify Fix for EventPublisherImpl
- **Step 6**: Clean Up Unused Code for EventPublisherImpl
- **Step 7**: Clean Up Tests for EventPublisherImpl
- **Step 8**: Verify Cleanup for EventPublisherImpl
- **Step 9**: Validate Spotless and Checkstyle for EventPublisherImpl
- **Step 10**: Write Focused Tests for ServiceBusConfiguration
- **Step 11**: Confirm Test Failure for ServiceBusConfiguration
- **Step 12**: Fix Code for ServiceBusConfiguration to enable retry policy
- **Step 13**: Verify Fix for ServiceBusConfiguration
- **Step 14**: Clean Up Unused Code for ServiceBusConfiguration
- **Step 15**: Clean Up Tests for ServiceBusConfiguration
- **Step 16**: Verify Cleanup for ServiceBusConfiguration
- **Step 17**: Validate Spotless and Checkstyle for ServiceBusConfiguration
- **Step 18**: Validate Quality

## Key Characteristics

- **Complexity**: Complex (multiple files, async messaging, retry handling)
- **Approach**: Full TDD cycle for each affected file
- **Focus**: Message persistence, connection resilience, retry strategy
- **Test Coverage**: Connection failure scenarios, retry logic, error handling
