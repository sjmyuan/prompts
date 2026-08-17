# Plan Executor: Handling Failed Steps Example

**Scenario**: A bug-fix plan hits a compilation error mid-execution; the executor marks the step ❌, analyzes the root cause, applies a recovery fix within scope, and retries. Demonstrates **track-plan**, **execute-step**, and **handle-errors**.

**Applies**: **track-plan**, **execute-step**, **handle-errors**

## User Request
"Implement the bug fix plan we created for the null pointer exception in data transformation"

## Plan to Execute
1. Add null checks in DataImportedHandler
2. Update unit tests
3. Add integration test
4. Update error handling documentation

## Initial Plan Status
**Status**: Step 1 ⏳ · Step 2 ⏳ · Step 3 ⏳ · Step 4 ⏳

---

### Step 1: Add Null Checks 🔄 → ✅

**Objective**: Add defensive null checks to prevent null pointer exceptions
**Files**: Modifying `application/service/DataImportedHandler.java`
**Implementation**:
```java
public void handle(DataImported event) {
    if (event == null || event.getRecord() == null) {
        throw new InvalidDataEventException("Data event cannot be null");
    }
    if (event.getRecord().getId() == null) {
        throw new InvalidDataException("Data record ID is required");
    }
    transformAndPublish(event.getRecord());
}
```
**Validation**: Handler compiles and includes null checks
**Status**: ✅ Completed · Steps 2–4 ⏳

---

### Step 2: Update Unit Tests 🔄 → ❌

**Objective**: Add unit tests to verify null check behavior
**Files**: Modifying `application/service/DataImportedHandlerTest.java`
**Implementation** (attempted):
```java
@Test
void shouldThrowExceptionForNullData() {
    DataImported event = new DataImported(null);
    assertThrows(InvalidDataEventException.class, () -> handler.handle(event));
}
```

**Error Encountered**:
```
[ERROR] DataImportedHandlerTest.java:[45,20] cannot find symbol
  symbol:   class InvalidDataEventException
```

**Status**: ❌ Failed — missing exception class · Step 1 ✅ · Steps 3–4 ⏳

---

**Analysis**: `InvalidDataEventException` doesn't exist yet; the tests need it to compile.

**Recovery** — per **handle-errors** step 4, applying **check-scope-boundary** first: the plan has no boundary block, so the fallback boundary (plan steps/files) governs; adding the missing exception is a required dependency of Step 2's tests and touches no out-of-scope file, so the fix proceeds and is recorded as a clarifying note.

**Files**: Creating `domain/exceptions/InvalidDataEventException.java`
```java
public class InvalidDataEventException extends RuntimeException {
    public InvalidDataEventException(String message) { super(message); }
}
```

**Retry Step 2** — add the import and re-run:
```java
import com.example.application.domain.exceptions.InvalidDataEventException;
```
**Validation**: All tests compiling and passing ✓
**Status**: ✅ Completed (after recovery) · Step 1 ✅ · Steps 3–4 ⏳

---

### Step 3: Add Integration Test 🔄 → ✅

**Objective**: Create end-to-end test for null data handling
**Files**: Creating `presentation/DataTransformationIntegrationTest.java`
**Implementation**:
```java
@SpringBootTest
@AutoConfigureMockMvc
class DataTransformationIntegrationTest {
    @Test
    void shouldRejectNullDataEvent() throws Exception {
        mockMvc.perform(post("/api/transform")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"record\": null}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Data event cannot be null"));
    }
}
```
**Validation**: Integration test passing ✓
**Status**: ✅ Completed · Steps 1–2 ✅ · Step 4 ⏳

---

### Step 4: Update Documentation 🔄 → ✅

**Objective**: Document the new error handling behavior
**Files**: Modifying `docs/operations.md`
**Implementation**: added an `## Error Handling` section — when `InvalidDataEventException` is thrown (null event, missing record ID, null required fields) and the resolution.
**Validation**: Documentation is clear and accurate
**Status**: ✅ Completed

---

## Final Plan Status
**Status**: Step 1 ✅ · Step 2 ✅ (recovered) · Step 3 ✅ · Step 4 ✅

## Completion Summary
✅ All 4 steps completed successfully. Step 2 failed ❌ (missing exception class), root cause analyzed, recovery fix applied within scope, step retried ✅.

**Files Changed**:
- Created: 2 (`InvalidDataEventException.java`, `DataTransformationIntegrationTest.java`)
- Modified: 2 (`DataImportedHandler.java`, `operations.md`)
- Total: 4

The plan file and context file are kept as a permanent record.
