# Example: New Feature Documentation

**Scenario**: Added support for data category transformation with CategoryTransformer service

**Change Type**: New Feature

---

## Change Review and Documentation Impact

Applies **maintain-docs** (steps 1–2).

**Agent reviews the change** — reads new files and PR description:
> New `CategoryTransformer` service added to the application layer. Consumes `CategoryMappingRepository` for mapping rules from `application.yaml`. Called from `DataImportedHandler` to transform source categories into external API categories.

**Agent identifies affected documentation** (consults **impact-lookup** for new feature):
> - **README.md**: Add feature summary under "Features".
> - **docs/architecture.md**: Add the new service component and its data flow.
> - **docs/data.md**: Document the category mapping configuration structure.
> - **Usage examples**: Show how the service is wired into the handler.

---

## Documentation Updates

## 1. README.md

Added section under "Features":

```markdown
### Data Category Transformation

The service now supports transforming data categories from source format to external API category structure, with support for hierarchical category mapping.
```

## 2. docs/architecture.md

```markdown
### Category Transformation

**Pattern**: Strategy pattern with CategoryTransformer service
**Components**: 
- `CategoryTransformer`: Main transformation service in application layer
- `CategoryMappingRepository`: Interface for category mapping persistence
- `CategoryMappingRepositoryImpl`: Database implementation

**Data Flow**:
1. DataImportedHandler receives message with category data
2. CategoryTransformer applies mapping rules from configuration
3. Transformed categories included in OutgoingMessage
```

## 3. docs/data.md

```markdown
## Category Mapping Structure

Categories are mapped using hierarchical rules defined in `application.yaml`:

```yaml
category-mapping:
  source-categories:
    "hardware-tools": "api-tools"
    "safety-equipment": "api-safety"
```

## 4. Usage Example (in docs/README.md)

```java
@Service
public class DataImportedHandler {
  private final CategoryTransformer categoryTransformer;
  
  public void handle(IncomingMessage.DataImported message) {
    List<Category> categories = categoryTransformer.transform(message.categories());
    // ... use transformed categories
  }
}
```

---

## Key Documentation Characteristics

- **Change Type**: New Feature
- **Documentation Scope**: README, Architecture, Data Model, Code Examples
- **Primary Focus**: Feature overview, architecture explanation, configuration guide
- **Impact Level**: Major (new system-wide capability)
