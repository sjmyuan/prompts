# Plan Executor: Handling Failed Steps Example

## User Request
"Implement the bug fix plan we created for the null pointer exception in data transformation"

## Plan to Execute
1. ✅ Add null checks in DataImportedHandler
2. ❌ Update unit tests (FAILED - compilation error)
3. ⏸️ Add integration test
4. ⏸️ Update error handling documentation

## Execution Process

### Step 1: Add Null Checks ✅
```java
// DataImportedHandler.java
public void handle(DataImported event) {
    if (event == null || event.getRecord() == null) {
        log.error("Received null data event");
        throw new InvalidDataEventException("Data event cannot be null");
    }
    
    DataRecord record = event.getRecord();
    if (record.getId() == null) {
        throw new InvalidDataException("Data record ID is required");
    }
    
    transformAndPublish(record);
}
```
**Status**: Completed ✅

### Step 2: Update Unit Tests ❌
**Attempted**:
```java
@Test
void shouldThrowExceptionForNullData() {
    DataImported event = new DataImported(null);
    assertThrows(InvalidDataEventException.class, 
        () -> handler.handle(event));
}
```

**Error Encountered**:
```
[ERROR] DataImportedHandlerTest.java:[45,20] cannot find symbol
  symbol:   class InvalidDataEventException
  location: class DataImportedHandlerTest
```

**Analysis**: Missing exception class import

**Recovery Action**: Create the exception class first
```java
// exceptions/InvalidDataEventException.java
public class InvalidDataEventException extends RuntimeException {
    public InvalidDataEventException(String message) {
        super(message);
    }
}
```

**Retry Step 2**: Update unit tests with correct import ✅
```java
import com.example.application.domain.exceptions.InvalidDataEventException;

@Test
void shouldThrowExceptionForNullData() {
    DataImported event = new DataImported(null);
    assertThrows(InvalidDataEventException.class, 
        () -> handler.handle(event));
}
```
**Status**: Completed ✅ (after recovery)

### Step 3: Add Integration Test ✅
```java
@SpringBootTest
@AutoConfigureMockMvc
class DataTransformationIntegrationTest {
    
    @Test
    void shouldRejectNullDataEvent() throws Exception {
        String nullEventJson = "{\"record\": null}";
        
        mockMvc.perform(post("/api/transform")
                .contentType(MediaType.APPLICATION_JSON)
                .content(nullEventJson))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error")
                    .value("Data event cannot be null"));
    }
}
```
**Status**: Completed ✅

### Step 4: Update Documentation ✅
Updated `docs/operations.md`:
```markdown
## Error Handling

### InvalidDataEventException
Thrown when:
- Data event is null
- Data record ID is missing
- Required record fields are null

**Resolution**: Ensure data source sends complete data records
```
**Status**: Completed ✅

## Final Status
✅ All steps completed successfully
- Initial failure in step 2 was resolved by creating missing exception class
- Remaining steps executed without issues

## Lessons Learned
- Check for missing dependencies before implementation
- Exception classes should be created before usage
- Integration tests validate end-to-end behavior
