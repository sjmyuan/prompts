````markdown
# Example: Skill File Review

**Scenario**: Review of `skills/sql-query-builder/SKILL.md` — a copilot skill that helps an AI agent build, review, and optimize SQL queries.

**Review Focus**: Trigger correctness — whether the frontmatter `description` and `<when-to-use-this-skill>` are consistent and complete.

## Code Review Summary

**Scope**: `skills/sql-query-builder/SKILL.md` — full skill file  
**Focus Areas**: Trigger correctness, description coverage, scenario alignment  
**Overall Assessment**: Trigger correctness failures across multiple scenarios. The `description` covers only one of four activation scenarios, causing the skill to silently fail to load for optimization, review, and dialect-conversion requests.

---

## Findings

### 🔴 Major Issues

#### `description` covers only one of four `<when-to-use-this-skill>` scenarios
- **File**: [SKILL.md](SKILL.md#L1-L4) (frontmatter `description`)
- **Issue**: The frontmatter reads: *"Helps the AI agent construct SQL SELECT, INSERT, UPDATE, and DELETE statements. Use when the user needs to build a SQL query."* The `<when-to-use-this-skill>` section lists four scenarios:
  1. User asks to build or write a SQL query
  2. User asks to review an existing query for correctness or security
  3. User asks to optimize a slow or inefficient query
  4. User asks to convert a query between SQL dialects (e.g., MySQL → PostgreSQL)
  Only scenario 1 ("build a SQL query") is covered by the description's trigger phrase. Scenarios 2–4 have no matching keyword or verb in the description.
- **Impact**: VS Code/Copilot will not load this skill for review, optimization, or dialect-conversion requests. The agent falls back to generic behavior for three of four documented scenarios.
- **Recommendation**: Expand the trigger phrase to cover all scenarios, e.g.: *"Use when the user asks to build, review, optimize, or convert a SQL query."*

#### `<when-to-use-this-skill>` bullet 3 is missing the intent verb
- **File**: [SKILL.md](SKILL.md#L10-L14) (`<when-to-use-this-skill>`)
- **Issue**: Bullet 3 reads: *"User asks about a slow query."* The phrase "asks about" does not state what the user wants done — it could mean explain, optimize, profile, or diagnose. This vagueness prevents the agent from correctly scoping the skill after loading.
- **Recommendation**: Rewrite with an explicit intent verb: *"User asks to optimize or improve the performance of a slow SQL query."*

### 🟡 Minor Issues

#### `description` trigger phrase covers a scenario absent from `<when-to-use-this-skill>`
- **File**: [SKILL.md](SKILL.md#L4) (frontmatter `description`) / [SKILL.md](SKILL.md#L8-L15) (`<when-to-use-this-skill>`)
- **Issue**: The description contains: *"…or when the user wants to understand how a query works."* No bullet in `<when-to-use-this-skill>` covers explain/understand scenarios. The skill is over-triggered for explanation requests, but has no post-load scope check to confirm or reject them.
- **Recommendation**: Either add a corresponding bullet to `<when-to-use-this-skill>` (if explanation is in scope) or remove the phrase from `description` (if it is not).

---

## Positive Highlights
- The `<capabilities>` and `<knowledge>` sections are well-structured — reference tables are in `<knowledge>` and capabilities use ordered steps.
- `<when-to-use-this-skill>` has four distinct scenarios, indicating intentional scope design.

---

## Risks & Assumptions
- Review assumes the frontmatter `description` is the primary signal used by VS Code/Copilot to decide whether to load the skill. If a different mechanism is used, the severity of the under-coverage findings may differ.
- No runtime evaluation was performed — trigger failures are inferred from static analysis of the skill file.

---

## Recommended Next Steps
1. Rewrite the frontmatter `description` trigger phrase to cover all four scenarios. *(Resolves 🔴 Major — under-coverage)*
2. Rewrite bullet 3 in `<when-to-use-this-skill>` to include an explicit intent verb. *(Resolves 🔴 Major — vague scope check)*
3. Decide whether explanation/understand is in scope; add or remove the corresponding phrase from `description`. *(Resolves 🟡 Minor — over-triggering)*
````
