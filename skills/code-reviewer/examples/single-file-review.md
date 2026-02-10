````markdown
# Example: Single File Review (Feature Addition)

**Scenario**: Review of a new `DataAttributeTransformer.java` service class for transforming data source attributes

**Review Focus**: Correctness, Clean Architecture compliance, maintainability, Java best practices

## Code Review Summary

**Scope**: New `DataAttributeTransformer.java` service class
**Focus**: Correctness, Clean Architecture compliance, maintainability, null-safety
**Overall Assessment**: Ready to merge after fixing 1 major and 1 minor issue

---

## Findings

### 🔴 Major Issues

#### Missing Input Validation and Null Checks
- **File**: [DataAttributeTransformer.java](DataAttributeTransformer.java#L42-L48)
- **Issue**: No null check on `IncomingMessage.DataImported` parameter before accessing nested fields. Direct access to `record.getMetadata().getFirst()` will throw NPE if list is empty.
- **Impact**: NullPointerException at runtime if null message or empty metadata list is passed
- **Recommendation**: Add validation with Optional handling:
```java
public OutgoingDataAttributes transform(IncomingMessage.DataImported record) {
  Objects.requireNonNull(record, "Data record cannot be null");
  
  Optional<MetadataInfo> metadata = Optional.ofNullable(record.getMetadata())
    .filter(list -> !list.isEmpty())
    .map(List::getFirst);
    
  if (metadata.isEmpty()) {
    throw new IllegalArgumentException("Data record must have at least one metadata entry");
  }
  // processing logic
}
```

### 🟡 Minor Issues

#### Hardcoded Default Locale
- **File**: [DataAttributeTransformer.java](DataAttributeTransformer.java#L55-L60)
- **Issue**: Default locale "en-US" hardcoded in service rather than from configuration
- **Impact**: Changing default locale requires code changes and redeployment
- **Recommendation**: Move to `application.yaml` and inject via `@Value("${data.default.locale}")` annotation

#### Missing JavaDoc for Public Method
- **File**: [DataAttributeTransformer.java](DataAttributeTransformer.java#L42)
- **Issue**: Public `transform()` method lacks JavaDoc documentation
- **Impact**: Reduces code maintainability and IDE documentation tooltips
- **Recommendation**: Add comprehensive JavaDoc:
```java
/**
 * Transforms data source attributes into external API format.
 *
 * @param record the incoming data record from data source
 * @return transformed data attributes
 * @throws IllegalArgumentException if record is null or has no metadata
 */
public OutgoingDataAttributes transform(IncomingMessage.DataImported record) {
```

---

## Positive Highlights
- Clear separation of concerns following Clean Architecture hexagonal pattern
- Proper use of Spring dependency injection with constructor injection
- Appropriate use of Java records for immutable DTOs
- Clean method naming that clearly conveys intent

---

## Risks & Assumptions
- Assumes all records will have metadata - may need fallback logic for records without metadata
- No validation of attribute value formats (e.g., ID format, value ranges)

---

## Recommended Next Steps
1. Fix input validation and null safety (blocker for production readiness)
2. Externalize default locale configuration (recommended)
3. Add JavaDoc documentation (recommended)
4. Consider adding unit tests for edge cases (empty lists, null fields)

---

## Key Review Characteristics

- **Review Type**: Single file (new service)
- **Severity Distribution**: 1 major, 2 minor
- **Primary Concerns**: Null-safety, input validation, and configuration management
- **Action Required**: Must fix major issue before merge
- **Testing Recommendation**: Ensure comprehensive test coverage for null/empty scenarios

````
