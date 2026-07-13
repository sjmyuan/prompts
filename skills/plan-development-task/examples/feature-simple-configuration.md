# Example: Simple Feature — Configurable Retry Settings

**Scenario**: Add configurable retry settings for Azure Service Bus message publishing.

---

## Change Classification

Applies **classify-change-type**.

**User request:**
> "We need to add configurable retry settings for our Azure Service Bus message publishing — max retry count and retry delay."

**Agent classifies** — keywords: "add", "configurable" → **Feature** (new configuration capability).

*User confirms classification: ✅*

---

## Feature Scope Definition

Applies **define-feature-scope**.

**Agent asks clarifying questions:**
> 1. What are the defaults for max retry count and retry delay?
> 2. Should the retry settings apply globally or per message type?
> 3. Are there existing configuration patterns in the project we should follow?

**User responds:**
> Defaults: 3 retries, 100 ms delay. Global (one setting for all message types). Yes, follow the existing `azure.servicebus` config prefix pattern.

**Agent confirms requirement:**
> Add `azure.servicebus.retry.max-retries` (default: 3) and `azure.servicebus.retry.delay-ms` (default: 100) to `application.yaml`. Add a `RetryConfig` configuration class. Update `EventPublisherImpl` to use these settings instead of hardcoded values.

*User confirms: ✅*

---

## Implementation Plan

Applies **plan-feature-implementation**.

**TDD Approach**: Streamlined — simple configuration changes with minimal logic; test loading, defaults, and application of settings

**Steps:**
- Step 1: Validate Baseline (run tests, linting, type-checking)
- Step 2: Write Tests for retry configuration properties
- Step 3: Confirm Test Failure
- Step 4: Add retry properties to application.yaml and configuration class
- Step 5: Update EventPublisherImpl to use retry configuration
- Step 6: Verify Tests Pass
- Step 7: Validate Linting, Formatting and Type Checking

## Key Characteristics

- **Complexity**: Low — simple configuration property with minimal logic changes
- **TDD Approach**: Streamlined — consolidated test and implementation steps
- **Testing Strategy**: Configuration loading, default values, and application of settings
- **Total Steps**: 7
- **Rationale**: Simple configuration additions don't require extensive refactoring or cleanup cycles
