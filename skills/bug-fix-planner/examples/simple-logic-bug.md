# Example: Simple Logic Bug Fix

**Scenario**: DataImportedHandler sends incorrect data ID to message publisher

---

## Root Cause Identification

Applies **identify-bug-root-cause**.

**User reports:**
> “The message publisher is receiving the wrong product ID — downstream consumers see a transformed/modified ID in the outgoing event instead of the original source ID.”

**Agent gathers information** — reads `DataImportedHandler.java` and the event publishing tests. Finds: the handler calls `dataTransformer.transform(record)` and then passes `transformedData.getId()` (the transformed ID) to the publisher instead of the original `record.getId()`.

**Agent asks:**
> 1. Should the outgoing message always carry the original source ID, or the transformed ID in some scenarios?
> 2. Are there any existing tests covering the ID field in the published message?

**User responds:**
> Always the original source ID. Existing tests check the message type but not the specific ID field.

**Agent confirms root cause:**
> `DataImportedHandler` passes `transformedData.getId()` to the publisher instead of `record.getId()`. The transformation step changes the ID format, so the downstream consumer receives the wrong identifier. Fix: pass `record.getId()` (the original source ID) when constructing the outgoing message.

*User confirms: ✅*

---

## Bug-Fixing Plan

Applies **plan-bug-fix**.

**Root Cause**: Using transformed ID instead of original ID in the outgoing message

**Bug-Fixing Plan**:

## Steps

- **Step 1**: Validate Baseline (run tests, Spotless, Checkstyle)
- **Step 2**: Write Tests for correct ID handling in DataImportedHandler
- **Step 3**: Confirm Test Failure
- **Step 4**: Fix ID mapping logic in DataImportedHandler
- **Step 5**: Verify Tests Pass
- **Step 6**: Clean Up Unused Code
- **Step 7**: Clean Up Tests
- **Step 8**: Verify Cleanup
- **Step 9**: Validate Quality (mvn spotless:check, Checkstyle)

## Key Characteristics

- **Complexity**: Simple
- **Approach**: Full TDD cycle
- **Focus**: Logic correctness and data mapping
- **Test Coverage**: ID transformation scenarios and edge cases
