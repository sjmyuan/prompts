# Example: Complex Data Transformation Logic

**Use Case**: When implementing sophisticated transformation rules or complex business logic that requires rigorous testing and validation.

**Scenario**: Implement multi-locale data attribute transformation with fallback logic and validation

---

## Requirement Definition

Applies **define-requirement**.

**User request:**
> "We need to transform product attribute values so that each attribute is returned in the user's preferred locale, with a fallback to the default locale if the translation is missing, and with validation to reject invalid locale codes."

**Agent asks clarifying questions:**
> 1. What format are locale codes in — BCP 47 (`en-US`) or ISO 639-1 (`en`)?
> 2. What constitutes a "missing" translation — null value, empty string, or both?
> 3. Is the fallback always to a single default locale, or a priority chain (e.g., `fr-CA` → `fr` → `en`)?
> 4. What happens if the fallback locale also has no translation — return null or throw?
> 5. Are attribute values always strings, or can they be numeric/boolean?

**User responds:**
> BCP 47. Both null and empty string count as missing. Two-level chain: regional → base language → configured default. Return null if all levels miss. Values are always strings.

**Agent confirms requirement:**
> The `LocaleAttributeTransformer` must: (1) accept an attribute map keyed by locale, (2) resolve the value by trying the exact locale, then the base language, then the configured default, (3) treat null and empty string as absent, (4) reject malformed BCP 47 codes with a validation error, (5) return null if no match is found at any level. The `FallbackLocaleResolver` encapsulates the priority chain so it can be unit-tested independently.

*User confirms: ✅*

---

## Implementation Plan (Full TDD - Complex logic requires rigorous testing)

**Consolidation rationale**: `LocaleAttributeTransformer` and `FallbackLocaleResolver` form a single cohesive unit — the transformer delegates entirely to the resolver and they share test fixtures. Consolidating them into one TDD cycle reduces the total step count from 32 to 22 without sacrificing coverage.

**Steps:**
- Step 1: Validate Baseline
- Step 2-11: Full TDD cycle for LocaleAttributeTransformer + FallbackLocaleResolver (consolidated — tightly coupled components, shared test fixtures)
  - Step 2: Write Tests for LocaleAttributeTransformer and FallbackLocaleResolver
  - Step 3: Confirm Test Failure
  - Step 4: Implement core transformation algorithm (LocaleAttributeTransformer)
  - Step 5: Implement fallback resolution logic (FallbackLocaleResolver)
  - Step 6: Verify Tests Pass
  - Step 7: Refactor transformer and resolver for clarity
  - Step 8: Validate Refactoring
  - Step 9: Clean Up unused code and tests
  - Step 10: Verify Cleanup
  - Step 11: Validate Linting, Formatting and Type Checking
- Step 12-20: Full TDD cycle for integration with DataImportedHandler
  - Step 12: Write Tests for handler integration
  - Step 13: Confirm Test Failure
  - Step 14: Integrate transformation logic with handler
  - Step 15: Verify Tests Pass
  - Step 16: Refactor handler integration
  - Step 17: Validate Refactoring
  - Step 18: Clean Up unused code and tests
  - Step 19: Verify Cleanup
  - Step 20: Validate Linting, Formatting and Type Checking
- Step 21: Final Validation (run all tests, lint, and type-check: mvn spotless:check, mvn checkstyle:check, mvn compile)

## Key Characteristics

- **Complexity**: High - sophisticated algorithm with locale fallback, validation, and multiple integration points
- **TDD Approach**: Full cycle for each major component
- **Testing Strategy**: Comprehensive coverage of:
  - Multiple locale scenarios and fallback chains
  - Edge cases (missing attributes, invalid locales, empty data)
  - Boundary conditions (max attribute length, special characters)
  - Integration scenarios with message handling
- **Total Steps**: 21 steps — two components consolidated into one TDD cycle because they share context; handler integration kept as a separate cycle
- **Separation**: Clear phases for transformer layer (core + resolver) and handler integration
- **Focus**: Data transformation correctness, locale handling, error resilience

## When to Use This Pattern

Use this full TDD approach when:
- Implementing complex algorithms or business logic with multiple decision points
- Working with critical features that impact data integrity or business rules
- The feature involves multiple services and integration points
- Edge cases and error handling are crucial for correctness
- The logic will be difficult to debug if not properly tested upfront
- Requirements involve complex validation rules or multi-step transformations
