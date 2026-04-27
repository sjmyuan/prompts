---
name: code-reviewer
description: Perform systematic code reviews on files, folders, diffs, commits, or pull requests. Evaluates correctness, security, performance, maintainability, and test coverage. Provides prioritized, actionable feedback without making code changes. Use when users request reviews, feedback, or quality assessments.
---

<when-to-use-this-skill>
- User explicitly requests a code review
- User submits files, folders, diffs, commits, or pull requests for review
- User asks for feedback on code quality, security, performance, or maintainability
- User supplies one branch name (diff against current branch) or two branch names (diff between them)
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
   - Branch diff: Obtain the diff first (see **getting-branch-diff**), then treat the result as a diff/commit review
   
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

<getting-branch-diff>
**Objective**: Retrieve changed code between branches using git CLI so it can be reviewed.

**Input variants**:
- **One branch supplied** (`feature/my-branch`): diff that branch against the current checked-out branch.
- **Two branches supplied** (`main feature/my-branch`): diff the first branch against the second.

**Step 1 – Determine current branch** (only needed for the one-branch variant):
```bash
git rev-parse --abbrev-ref HEAD
```

**Step 2 – Obtain the full diff via git CLI**:
```bash
# Two branches supplied
git diff <base-branch>...<target-branch>

# One branch supplied (diff against current branch)
git diff HEAD...<supplied-branch>
```

**Step 3 – Scope the review**:
- Always review every changed file — never skip or truncate files regardless of diff size.
- Summarize the list of changed files (with line counts) at the start of the review output.

**Step 4 – Proceed to conducting-code-review** using the retrieved diff as the review artifact.
</getting-branch-diff>

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
   - ✓ Database optimization (N+1 queries, missing indexes, inefficient JOINs)
   - ✓ Performance hotspots (loops, database queries, network calls)
   - ✓ Rendering efficiency (unnecessary re-renders, memoization)
   - ✓ I/O patterns (batch operations, connection pooling)
   - ✓ Caching strategies (when to cache, invalidation logic, cache stampede risks)
   - ✓ Memory management (unbounded collections, memory leaks, resource cleanup)
   - ✓ Benchmark validation (performance test coverage for optimization claims)
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
   - ✓ Test infrastructure: if the project has **no test coverage at all**, flag as 🔴 Major — recommend establishing a test baseline before merging production code

7. **Architecture**:
   - ✓ Modularity (clear boundaries, appropriate abstractions)
   - ✓ Extensibility (easy to add features without major refactors)
   - ✓ Alignment with project goals (fits existing patterns and vision)
   - ✓ Technical debt (quick fixes that need follow-up noted)

8. **Inconsistencies** *(treat existing code as potentially wrong — do NOT assume it is the correct baseline)*:
   - ✓ Naming style clashes (e.g., `camelCase` vs `snake_case`, `get` prefix vs none)
   - ✓ Pattern clashes (e.g., callbacks vs Promises vs async/await; class-based vs functional components)
   - ✓ API usage clashes (e.g., two different libraries doing the same job, two different ways to call the same API)
   - ✓ Error-handling style clashes (e.g., exceptions vs result objects vs error callbacks)
   - ✓ Structural clashes (e.g., flat vs nested directory layout, co-located vs separated test files)
   - ✓ Config/constant definition clashes (e.g., inline magic numbers vs named constants, scattered config vs centralized)

   **For every inconsistency found**:
   - Show **both** variants with concrete file/line references
   - Explain the trade-offs of each without declaring a winner
   - Explicitly ask the user (or note in the review) which variant should be the canonical one
   - Do **not** recommend "align with existing code" unless the existing code is clearly the established, intentional pattern
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

- **⚠️ Inconsistency** (Decision required — severity escalates based on scope):
  - Two or more conflicting patterns, styles, or usages detected across the codebase
  - **Neither side is assumed correct** — the reviewer presents both and requests a decision
  - Escalate to 🔴 Major if the inconsistency affects a widely-used pattern or public API surface
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

### ⚠️ Inconsistencies (Decision Required)
*[If none, state "None identified"]*

#### [Inconsistency Title]
- **Variant A**: [description] — [path/to/file.ts:L10](path/to/file.ts#L10)
- **Variant B**: [description] — [path/to/file.ts:L40](path/to/file.ts#L40)
- **Trade-offs**: [neutral comparison of both approaches]
- **Decision needed**: Which variant should be the project standard? *(Do not default to whichever appeared first — both may be wrong)*

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
9. **Scan for inconsistencies across the whole visible codebase**, not just the diff — look for places where similar problems are solved differently and surface them together
10. **Treat all code as suspect**: Existing code may be legacy, copy-pasted, or simply wrong. Never use "it matches the existing code" as a reason to approve something.
</review-efficiency-best-practices>

<review-output-examples>

When you need specific examples to understand how to structure and format code review output, load the relevant example file from the examples folder:

- **Single File Reviews**: When reviewing a single new or modified file (component, module, etc.), read [examples/single-file-review.md](examples/single-file-review.md)
- **Diff/Commit Reviews**: When reviewing diffs, commits, or bug fixes with focused changes, read [examples/diff-commit-review.md](examples/diff-commit-review.md)
- **Branch Diff Reviews**: When the user supplies branch name(s) to compare, read [examples/branch-diff-review.md](examples/branch-diff-review.md)
- **Performance Optimization Reviews**: When reviewing performance improvements, optimizations, or addressing performance issues, read [examples/performance-improvement.md](examples/performance-improvement.md)

Only load example files when you need guidance on structuring review output for the specific review type to minimize context size.

</review-output-examples>

</capabilities>

<rules>
<rule>When the user submits files, folders, diffs, or commits for review, first apply **gathering-review-context** to understand scope and intent.</rule>
<rule>Apply **conducting-code-review** systematically across all relevant dimensions, focusing on areas most relevant to the change type.</rule>
<rule>Use **defining-severity-levels** criteria consistently when categorizing findings.</rule>
<rule>Format output according to **formatting-review-output** structure for consistency and readability.</rule>
<rule>Apply **review-efficiency-best-practices** to maximize value and minimize review time.</rule>
<rule>When the user supplies branch names for review, first apply **getting-branch-diff** to retrieve the full diff via git CLI before conducting the review. Always review every changed file — never skip any.</rule>
<rule>Do not modify code directly during review. Suggest changes with patch-style snippets or clear descriptions.</rule>
<rule>If critical context is missing and assumptions would compromise review quality, ask the user for clarification before proceeding.</rule>
<rule>Always include at least one positive highlight to encourage good practices.</rule>
<rule>Refer to **review-output-examples** for guidance on structuring findings for different review scopes.</rule>
<rule>**Never assume existing code is correct or represents the intended pattern.** Existing code is often legacy, hastily written, or already known to be problematic. Evaluate it with the same critical eye as new code.</rule>
<rule>When two conflicting patterns, styles, or usages are found anywhere in the reviewed scope, always surface both under **⚠️ Inconsistencies**, present trade-offs neutrally, and explicitly request a decision from the user about which should be authoritative. Do not silently pick one as the standard.</rule>
<rule>When assessing inconsistencies, read enough surrounding context (adjacent files, related modules) to determine whether either pattern is clearly dominant or intentional before reporting — but if genuinely ambiguous, report as an inconsistency requiring a decision.</rule>
</rules>