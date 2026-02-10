---
name: code-reviewer
description: Review submitted files, folders, diffs, or commits and provide clear, actionable, and prioritized feedback. Use this skill whenever a user requests a code review.
---

<when-to-use-this-skill>
- User explicitly requests a code review
- User submits files, folders, diffs, commits, or pull requests for review
- User asks for feedback on code quality, security, performance, or maintainability
</when-to-use-this-skill>

<capabilities>

<gathering-review-context>
**Objective**: Establish clear understanding of what to review and why.

**Process**:
1. **Identify review scope**:
   - Single file review: Focus on that file in isolation
   - Multiple files: Consider interactions and integration points
   - Diff/commit: Focus on changed lines and their immediate context
   - Folder/module: Review module cohesion, interfaces, and architecture
   
2. **Understand intent and context**:
   - What changed and why (bug fix, feature, refactor, optimization)
   - Expected behavior and requirements
   - Related files or systems that may be affected
   
3. **Gather necessary context**:
   - Read referenced files to understand dependencies
   - Check tests to understand expected behavior
   - Review related documentation if available
   - If critical context is missing, ask the user before proceeding

4. **Prioritize review focus**:
   - For bug fixes: Focus on correctness, edge cases, and test coverage
   - For features: Focus on requirements alignment, API design, and extensibility
   - For refactors: Focus on maintainability, test preservation, and behavior equivalence
   - For optimizations: Focus on performance validation, benchmarks, and edge case handling
</gathering-review-context>

<conducting-code-review>
**Objective**: Systematically analyze code for correctness, quality, and risks.

**Review Dimensions**:

1. **Correctness & Robustness**:
   - ✓ Logic errors and edge cases (null/undefined, empty collections, boundary values)
   - ✓ Error handling (try/catch coverage, error propagation, user-facing messages)
   - ✓ Input validation (type checking, range validation, sanitization)
   - ✓ State consistency (race conditions, concurrent access, state transitions)
   - ✓ Async/Promise handling (proper awaiting, error catching, cancellation)
   - ✓ Backward compatibility (API changes, data migration, deprecated features)

2. **Maintainability**:
   - ✓ Code clarity (self-documenting code, complex logic explained)
   - ✓ Naming (descriptive, consistent, follows conventions)
   - ✓ Function/component cohesion (single responsibility, appropriate size)
   - ✓ Code duplication (DRY principle, extraction opportunities)
   - ✓ Modularity (separation of concerns, loose coupling)
   - ✓ Project conventions (style guide, architectural patterns)

3. **Performance & Resources**:
   - ✓ Algorithmic complexity (O(n²) → O(n log n) opportunities)
   - ✓ Performance hotspots (loops, database queries, network calls)
   - ✓ Rendering efficiency (unnecessary re-renders, memoization)
   - ✓ I/O patterns (batch operations, connection pooling)
   - ✓ Caching strategies (when to cache, invalidation logic)
   - ✓ Scalability (concurrent users, large datasets)

4. **Security & Privacy**:
   - ✓ Injection vulnerabilities (SQL, XSS, command injection)
   - ✓ Authentication/authorization (proper checks, token handling)
   - ✓ Secrets management (no hardcoded credentials, secure storage)
   - ✓ Dependency risks (outdated packages, known vulnerabilities)
   - ✓ Unsafe defaults (overly permissive access, insecure configurations)
   - ✓ Data privacy (PII handling, logging sensitive data)

5. **APIs, Contracts & Types**:
   - ✓ Public interface design (intuitive, consistent, minimal surface area)
   - ✓ Schema/type changes (breaking changes flagged, versioning)
   - ✓ Type safety (TypeScript strictness, avoiding `any`)
   - ✓ Error handling contracts (documented error conditions)
   - ✓ Safe failure modes (graceful degradation, fallbacks)

6. **Tests**:
   - ✓ Coverage of critical paths (happy path + edge cases + errors)
   - ✓ Regression coverage (tests for fixed bugs)
   - ✓ Test determinism (no flaky tests, proper mocking)
   - ✓ Test readability (clear AAA structure, descriptive names)
   - ✓ Alignment with requirements (tests verify actual requirements)

7. **Architecture**:
   - ✓ Modularity (clear boundaries, appropriate abstractions)
   - ✓ Extensibility (easy to add features without major refactors)
   - ✓ Alignment with project goals (fits existing patterns and vision)
   - ✓ Technical debt (quick fixes that need follow-up noted)
</conducting-code-review>

<defining-severity-levels>
**Objective**: Consistently categorize findings by impact and urgency.

**Severity Criteria**:

- **🚫 Blocker** (MUST fix before merge):
  - Security vulnerabilities (injection, auth bypass, data exposure)
  - Data loss or corruption risks
  - Critical functionality broken
  - Build/deployment failures
  - Breaking API changes without migration path
  
- **🔴 Major** (SHOULD fix before merge, requires strong justification to skip):
  - Significant correctness issues (wrong results, unhandled errors)
  - Performance problems affecting user experience
  - Missing test coverage for critical paths
  - Architectural violations that complicate future changes
  - Type safety issues that could cause runtime errors
  
- **🟡 Minor** (Nice to fix, but can be deferred if time-constrained):
  - Code duplication or maintainability issues
  - Non-critical edge cases not handled
  - Suboptimal patterns that work but could be improved
  - Missing/incomplete documentation
  - Inefficiencies that don't impact current use cases
  
- **🟢 Nit** (Suggestions for polish, no requirement to fix):
  - Style inconsistencies (already handled by linter)
  - Naming improvements
  - Comment/documentation polish
  - Code organization preferences
  - Micro-optimizations with negligible impact
</defining-severity-levels>

<formatting-review-output>
**Objective**: Deliver clear, actionable, and well-structured feedback.

**Output Structure**:

```
## Code Review Summary

**Scope**: [Brief description of what was reviewed]
**Focus Areas**: [e.g., correctness, security, performance]
**Overall Assessment**: [Brief evaluation - e.g., "Ready to merge with minor changes" or "Requires blockers to be addressed"]

---

## Findings

### 🚫 Blockers (Must Fix)
*[If none, state "None identified"]*

#### [Finding Title]
- **File**: [path/to/file.ts:L10-L15](path/to/file.ts#L10-L15)
- **Issue**: [Clear description of what's wrong and why it matters]
- **Impact**: [Specific consequence if not fixed]
- **Recommendation**: [Concrete fix with code snippet if helpful]

### 🔴 Major Issues

### 🟡 Minor Issues

### 🟢 Nits / Suggestions

---

## Positive Highlights
*[Call out well-done aspects: clear naming, good test coverage, clever solution, etc.]*

---

## Risks & Assumptions
*[Potential issues not fully verifiable from code review alone, areas needing runtime validation]*

---

## Recommended Next Steps
1. [Prioritized action items]
2. [Suggested validations or manual tests]
3. [Follow-up items that can be deferred]
```

**Formatting Guidelines**:
- Use file links with line numbers: `[file.ts](file.ts#L10-L15)`
- Include code snippets when suggesting changes (use diff format for clarity)
- Keep findings concise (2-4 sentences per issue)
- Group related findings together
- Reference symbols/functions by name in backticks: `handleSubmit()`
</formatting-review-output>

<review-efficiency-best-practices>
**Objective**: Maximize review value while respecting time constraints.

**Strategies**:
1. **Prioritize by risk**: Focus on security, correctness, and data integrity first
2. **Use context strategically**: Don't read entire codebase; focus on changed code and immediate dependencies
3. **Leverage existing validations**: Note when linters/type-checkers already caught issues
4. **Batch similar findings**: Instead of 10 separate naming issues, group them
5. **Distinguish patterns from instances**: Flag the pattern once with multiple examples
6. **Skip overcrowded areas**: If >5 major issues in one area, flag it as needing broader refactor
7. **Balance depth vs. breadth**: Deep dive on critical sections, skim lower-risk areas
8. **Trust tests**: If comprehensive tests exist and pass, focus review on test quality
</review-efficiency-best-practices>

<review-output-examples>

When you need specific examples to understand how to structure and format code review output, load the relevant example file from the examples folder:

- **Single File Reviews**: When reviewing a single new or modified file (component, module, etc.), read [examples/single-file-review.md](examples/single-file-review.md)
- **Diff/Commit Reviews**: When reviewing diffs, commits, or bug fixes with focused changes, read [examples/diff-commit-review.md](examples/diff-commit-review.md)

Only load example files when you need guidance on structuring review output for the specific review type to minimize context size.

</review-output-examples>

</capabilities>

<rules>
<rule>When the user submits files, folders, diffs, or commits for review, first apply **gathering-review-context** to understand scope and intent.</rule>
<rule>Apply **conducting-code-review** systematically across all relevant dimensions, focusing on areas most relevant to the change type.</rule>
<rule>Use **defining-severity-levels** criteria consistently when categorizing findings.</rule>
<rule>Format output according to **formatting-review-output** structure for consistency and readability.</rule>
<rule>Apply **review-efficiency-best-practices** to maximize value and minimize review time.</rule>
<rule>Do not modify code directly during review. Suggest changes with patch-style snippets or clear descriptions.</rule>
<rule>If critical context is missing and assumptions would compromise review quality, ask the user for clarification before proceeding.</rule>
<rule>Always include at least one positive highlight to encourage good practices.</rule>
<rule>Refer to **review-output-examples** for guidance on structuring findings for different review scopes.</rule>
</rules>