# Example: Complex Feature — Multi-Locale Data Attribute Transformation

**Scenario**: Implement multi-locale product attribute value transformation with fallback logic and locale validation.

---

## Change Classification

Applies **classify-change-type**.

**User request:**
> "We need to transform product attribute values so that each attribute is returned in the user's preferred locale, with a fallback to the default locale if the translation is missing, and with validation to reject invalid locale codes."

**Agent classifies** — keywords: "need to transform", "implement", "add" → **Feature** (new behavior).

*User confirms classification: ✅*

---

## Feature Scope Definition

Applies **define-feature-scope**.

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

## Implementation Plan

Applies **plan-feature-implementation**.

**TDD Approach**: Full TDD cycle for each major component — complex business logic requires rigorous testing

**Consolidation rationale**: `LocaleAttributeTransformer` and `FallbackLocaleResolver` form a single cohesive unit — the transformer delegates entirely to the resolver and they share test fixtures. Consolidating them into one TDD cycle reduces the total step count.

**Steps:**
- Step 1: Validate Baseline (run tests, linting, type-checking)
- Step 2-11: Full TDD cycle for LocaleAttributeTransformer + FallbackLocaleResolver (consolidated)
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
- Step 12-20: Full TDD cycle for handler integration
  - Step 12: Write Tests for handler integration
  - Step 13: Confirm Test Failure
  - Step 14: Integrate transformation logic with handler
  - Step 15: Verify Tests Pass
  - Step 16: Refactor handler integration
  - Step 17: Validate Refactoring
  - Step 18: Clean Up unused code and tests
  - Step 19: Verify Cleanup
  - Step 20: Validate Linting, Formatting and Type Checking
- Step 21: Final Validation (run all tests, lint, and type-check)

## Key Characteristics

- **Complexity**: High — sophisticated algorithm with locale fallback, validation, and multiple integration points
- **TDD Approach**: Full cycle for each major component
- **Testing Strategy**: Multi-locale scenarios, fallback chains, edge cases (missing attributes, invalid locales, empty data)
- **Total Steps**: 21 (consolidated from 32)
- **Separation**: Transformer layer (core + resolver) and handler integration as separate cycles
