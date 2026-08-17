# Plan Executor: Multi-File Implementation Example

**Scenario**: A 7-step plan spans domain model, handler, adapter, publisher, and configuration layers; execution tracks status across multiple files and architectural layers. Demonstrates **track-plan** and **execute-step**.

**Applies**: **track-plan**, **execute-step**

## User Request
"Execute the plan to add data category transformation feature"

## Plan to Execute
1. Create domain model for Category
2. Add category transformation logic to handler
3. Create category adapter for external API
4. Update event publisher to include category data
5. Add configuration for category mapping
6. Write unit tests for all components
7. Write integration test

## Initial Plan Status
**Status**: Steps 1–7 ⏳

---

### Step 1: Create Domain Model 🔄 → ✅

**Objective**: Create domain model class for Category with validation
**Files**: Creating `domain/model/Category.java`
**Implementation**:
```java
public class Category {
    private final String id;
    private final String name;
    private final String parentId;
    public Category(String id, String name, String parentId) {
        validateCategory(id, name);
        this.id = id; this.name = name; this.parentId = parentId;
    }
    private void validateCategory(String id, String name) { /* both required */ }
    // getters
}
```
**Validation**: Class compiles with validation logic
**Status**: ✅ Completed · Steps 2–7 ⏳

---

### Step 2: Add Category Transformation Logic ✅

**Objective**: Integrate category transformation into the handler
**Files**: Modifying `application/service/DataImportedHandler.java`
**Implementation**: `handle()` maps `record.getCategoryIds()` via `categoryTransformer.transformCategories(...)` and builds `ExternalApiData` with `categories(...)`.
**Validation**: Handler compiles and integrates category transformation
**Status**: ✅ Completed · Steps 3–7 ⏳

---

### Step 3: Create Category Adapter ✅

**Objective**: Create adapter to fetch category data from external API
**Files**: Creating `infrastructure/adapter/CategoryAdapterImpl.java`
**Implementation**:
```java
@Component
public class CategoryAdapterImpl implements CategoryAdapter {
    @Override
    public List<Category> fetchCategories(List<String> categoryIds) {
        ResponseEntity<CategoryResponse> response = restTemplate.getForEntity(
            url + "?where=id in (\"" + String.join("\",\"", categoryIds) + "\")",
            CategoryResponse.class);
        return response.getBody().getResults().stream()
            .map(this::toDomainCategory).collect(Collectors.toList());
    }
}
```
**Validation**: Adapter compiles and correctly maps API responses
**Status**: ✅ Completed · Steps 4–7 ⏳

---

### Step 4: Update Event Publisher ✅

**Objective**: Add category data to published events
**Files**: Modifying `infrastructure/externaladapter/EventPublisherImpl.java`
**Implementation**: `publishDataTransformed` maps `data.getCategories()` to category IDs in the published event.
**Validation**: Event publisher includes category data in events
**Status**: ✅ Completed · Steps 5–7 ⏳

---

### Step 5: Add Configuration ✅

**Objective**: Add configuration properties for category mapping
**Files**: Modifying `resources/application.yaml`; Creating `infrastructure/config/CategoryMappingConfig.java`
**Implementation**: `category.mapping.{enabled, default-locale, fetch-hierarchy}` YAML + `@ConfigurationProperties` class.
**Validation**: Configuration loads successfully on application startup
**Status**: ✅ Completed · Steps 6–7 ⏳

---

### Step 6: Write Unit Tests ✅

**Objective**: Create comprehensive unit tests for all new components
**Files**: Creating `application/service/CategoryTransformerTest.java`, `infrastructure/adapter/CategoryAdapterImplTest.java`
**Implementation**: transformer happy-path + empty-list cases; adapter response-mapping tests.
**Validation**: All unit tests passing (24 tests) ✓
**Status**: ✅ Completed · Step 7 ⏳

---

### Step 7: Write Integration Test ✅

**Objective**: Create end-to-end integration test for category transformation
**Files**: Creating `presentation/CategoryTransformationIntegrationTest.java`
**Implementation**:
```java
@SpringBootTest
@AutoConfigureMockMvc
class CategoryTransformationIntegrationTest {
    @Test
    void shouldTransformDataWithCategories() throws Exception {
        mockMvc.perform(post("/api/transform")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    { "id": "TEST-001", "name": "Test Data Record",
                      "categoryIds": ["cat1", "cat2"] }"""))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.categories.length()").value(2));
    }
}
```
**Validation**: Integration test passing ✓
**Status**: ✅ Completed

---

## Final Plan Status
**Status**: Steps 1–7 ✅

## Completion Summary
✅ All 7 steps completed successfully.

**Files Changed**:
- Created: 5 · Modified: 3 · Total: 8
- Lines added: ~350 · Test coverage: 95% · All 25 tests passing

The plan file and context file are kept as a permanent record.
