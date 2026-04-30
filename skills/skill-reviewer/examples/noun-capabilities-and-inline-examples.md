````markdown
# Example: Skill File Review

**Scenario**: Review of `skills/form-validator/SKILL.md` — a copilot skill that guides an AI agent through form validation for a React web app.

**Review Focus**: Skill structure correctness, with particular attention to capability naming, example format, and example coverage.

## Code Review Summary

**Scope**: `skills/form-validator/SKILL.md` — full skill file  
**Focus Areas**: Capability naming conventions, examples section format, example coverage  
**Overall Assessment**: Core knowledge and rules are solid, but capability names are nouns rather than verbs, examples are embedded inline instead of referenced, and one capability has no example at all.

---

## Findings

### 🔴 Major Issues

#### Capabilities named as nouns instead of action verbs
- **File**: [SKILL.md](SKILL.md#L30-L95)
- **Issue**: All three capability sections use noun phrases: `<field-validation>`, `<error-display>`, `<async-validation>`. Capability names should describe *what the agent does*, not what the concept is.
- **Impact**: The agent cannot distinguish "a thing I know about" (knowledge) from "a procedure I execute" (capability). Noun-named sections are routinely treated as reference entries, reducing procedural compliance.
- **Recommendation**: Rename to action-verb phrases that describe the agent's task:
  - `<field-validation>` → `<validate-field>`
  - `<error-display>` → `<render-validation-errors>`
  - `<async-validation>` → `<run-async-validation>`

#### `<async-validation>` capability has no corresponding example
- **File**: [SKILL.md](SKILL.md#L80-L95)
- **Issue**: The `<examples>` section links two files — `examples/field-validation.md` and `examples/error-display.md` — but nothing covers the async validation flow. This is the most complex capability in the skill (race conditions, debounce logic, loading states) and is the one most in need of a concrete output model.
- **Impact**: The agent has no template to follow for async scenarios; outputs will be inconsistent or incorrect.
- **Recommendation**: Add `examples/async-validation.md` and link it from the `<examples>` section.

### 🟡 Minor Issues

#### Examples are embedded inline rather than referenced by file path
- **File**: [SKILL.md](SKILL.md#L100-L145)
- **Issue**: The `<examples>` section contains the full input/output content of both examples inline, rather than loading them on demand via file references. This inflates the skill context even when the examples are not relevant.
- **Impact**: Every activation of this skill loads ~300 tokens of example content regardless of the actual task, increasing noise and cost.
- **Recommendation**: Extract each example to a separate file and replace the inline content with a file path reference, e.g.:
  ```
  - [examples/field-validation.md](examples/field-validation.md) — synchronous single-field validation
  - [examples/error-display.md](examples/error-display.md) — rendering grouped error messages
  ```

### 🟢 Nits / Suggestions

#### `<knowledge>` section is well-structured
- Contains the validation rule reference table, HTML5 constraint API list, and accessibility requirements. Nothing is duplicated in the capabilities. Good.

#### `<when-to-use-this-skill>` correctly limits scope
- Three clear trigger phrases, no ambiguity. No change needed.

---

## Positive Highlights
- The `<knowledge>` section cleanly separates reference material (validation rules, API surface, a11y constraints) from procedural content.
- Rules correctly use "When [scenario] → use [capability]" routing without repeating capability content.
- The skill domain is well-scoped: it does not try to cover form layout, state management, or submission logic.

---

## Recommended Next Steps
1. Rename all three capability sections to action-verb phrases. *(Resolves 🔴 naming)*
2. Create `examples/async-validation.md` and link it from `<examples>`. *(Resolves 🔴 coverage gap)*
3. Extract inline example content to separate files; replace with file-path references. *(Resolves 🟡 inline examples)*
````
