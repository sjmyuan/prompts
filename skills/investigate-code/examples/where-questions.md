# Reverse Engineer: Where Questions Example

## User Request
"Where is the data validation logic implemented?"

## Response Process

### 1. Search Strategy
- Look for validation-related classes
- Search for @Valid annotations
- Check domain model for validation rules
- Look in application service layer

### 2. Initial Search
```bash
# Search for validation keywords
grep -r "validation|validate|@Valid" --include="*.java"
```

### 3. Results Analysis
```
src/main/java/com/example/application/
├── application/
│   └── service/
│       └── DataImportedHandler.java  <- Validation orchestration
├── domain/
│   └── model/
│       └── DataRecord.java  <- Domain validation rules
└── infrastructure/
    └── validation/
        └── DataValidator.java  <- Validation implementation
```

### 4. Code Review
```java
// DataImportedHandler.java
public void handle(DataImported event) {
    validateRecordData(event.getRecord());
    transformRecord(event.getRecord());
}

// DataRecord.java (Domain Model)
public class DataRecord {
    @NotNull
    private String id;
    
    @NotEmpty
    private String name;
    
    // Domain validation
    public void validate() {
        if (id == null || id.isBlank()) {
            throw new InvalidDataException("ID required");
        }
    }
}
```

### 5. Answer Compilation
Data validation is implemented in multiple layers:

1. **Domain Layer** (`domain/model/DataRecord.java`)
   - Business rule validation
   - Invariant enforcement
   - Self-validation methods

2. **Application Layer** (`application/service/DataImportedHandler.java`)
   - Orchestrates validation flow
   - Coordinates with validators

3. **Infrastructure Layer** (`infrastructure/validation/`)
   - Technical validation
   - Format/schema validation

**Pattern**: Following Clean Architecture, core business validation lives in the domain layer, while technical validation is in infrastructure.
