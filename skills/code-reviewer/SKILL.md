---
name: code-reviewer
description: Perform systematic reviews of code and documents across files, folders, diffs, commits, or pull requests. Evaluates correctness, security, performance, maintainability, and structural quality. Provides prioritized, actionable feedback without making changes. Use when users request reviews, feedback, or quality assessments on code or documents.
---

<when-to-use-this-skill>
- User explicitly requests a code review
- User submits files, folders, diffs, commits, or pull requests for review
- User asks for feedback on code quality, security, performance, or maintainability
- User supplies one branch name (diff against current branch) or two branch names (diff between them)
- User asks to review a document (README, design doc, ADR, specification, runbook, etc.) for clarity, completeness, or structure
</when-to-use-this-skill>

<knowledge>

<example-selector>
Load the relevant example file on demand when you need guidance on structuring review output. Only load what is needed to minimize context size.

| Review type | Example file |
|---|---|
| Diff / commit / bug fix | [examples/diff-commit-review.md](examples/diff-commit-review.md) |
| Branch diff (one or two branch names) | [examples/branch-diff-review.md](examples/branch-diff-review.md) |
| Performance optimization | [examples/performance-improvement.md](examples/performance-improvement.md) |
| Document (README, ADR, design doc, spec) | [examples/doc-review.md](examples/doc-review.md) |
</example-selector>

<review-efficiency-knowledge>
Strategies for maximizing review value while respecting time constraints:

- **Prioritize by risk**: Focus on security, correctness, and data integrity first
- **Use context strategically**: Don't read the entire codebase; focus on changed code and immediate dependencies
- **Leverage existing validations**: Note when linters/type-checkers already caught issues
- **Batch similar findings**: Instead of 10 separate naming issues, group them
- **Distinguish patterns from instances**: Flag the pattern once with multiple examples
- **Skip overcrowded areas**: If >5 major issues in one area, flag it as needing a broader refactor
- **Balance depth vs. breadth**: Deep-dive on critical sections, skim lower-risk areas
- **Trust tests**: If comprehensive tests exist and pass, focus the review on test quality
- **Scan for inconsistencies across the whole visible codebase**, not just the diff — look for places where similar problems are solved differently and surface them together
- **Treat all code as suspect**: Existing code may be legacy, copy-pasted, or simply wrong. Never use "it matches the existing code" as a reason to approve something.
</review-efficiency-knowledge>

<defining-severity-levels>
**Severity levels** — apply consistently when categorizing findings:

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
Standard template for all review output:

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

**Formatting guidelines**:
- Use file links with line numbers: `[file.ts](file.ts#L10-L15)`
- Include code snippets when suggesting changes (use diff format for clarity)
- Keep findings concise (2-4 sentences per issue)
- Group related findings together
- Reference symbols/functions by name in backticks: `` `handleSubmit()` ``
- For clean reviews with no findings in a severity tier, omit that section rather than writing "None identified"
</formatting-review-output>

</knowledge>

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
   - For documents: Focus on structure, clarity, completeness, accuracy, and target-audience alignment
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

> **Tip**: For uncommitted (staged/unstaged) changes, load and use the `get_changed_files` deferred tool instead of running git commands — it surfaces the same diff without needing a branch name.
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

<reviewing-document>
**Objective**: Evaluate a document (README, design doc, ADR, specification, runbook, etc.) for clarity, completeness, structure, and accuracy.

**Steps**:
1. Read the full document to understand its purpose, target audience, and scope.
2. Evaluate **structure**: Is there a clear logical flow? Are sections in the expected order for the document type? Are headings consistent in level and phrasing?
3. Evaluate **clarity**: Is the language clear and unambiguous? Are technical terms defined where needed? Are examples provided for complex concepts?
4. Evaluate **completeness**: Are all required sections present (e.g., a README should cover purpose, prerequisites, setup, usage)? Are there unexplained gaps or placeholder text?
5. Evaluate **accuracy**: Do code samples match the described behavior? Are version numbers, commands, and API signatures up to date?
6. Evaluate **audience alignment**: Does the depth and assumed knowledge level match the intended reader? Is jargon appropriate or excessive?
7. Apply **conducting-code-review** dimensions that are relevant to documents: correctness (accuracy), maintainability (single source of truth, no duplication with other docs), and inconsistencies (conflicting statements across sections).
8. Format findings using **formatting-review-output** and load **examples/doc-review.md** for output structure guidance.
</reviewing-document>

</capabilities>

<rules>
<rule>When the user submits files, folders, diffs, or commits for review, first apply **gathering-review-context** to understand scope and intent.</rule>
<rule>When the subject of review is a document (README, ADR, design doc, specification, runbook, etc.), use **reviewing-document**. Focus on structure, clarity, completeness, accuracy, and audience alignment.</rule>
<rule>Apply **conducting-code-review** systematically across all relevant dimensions, focusing on areas most relevant to the change type.</rule>
<rule>Use **defining-severity-levels** criteria consistently when categorizing findings.</rule>
<rule>Format output according to **formatting-review-output** structure for consistency and readability.</rule>
<rule>Apply **review-efficiency-knowledge** strategies to maximize value and minimize review time.</rule>
<rule>When the user supplies branch names for review, first apply **getting-branch-diff** to retrieve the full diff via git CLI before conducting the review. Always review every changed file — never skip any.</rule>
<rule>Do not modify code directly during review. Suggest changes with patch-style snippets or clear descriptions.</rule>
<rule>If critical context is missing and assumptions would compromise review quality, ask the user for clarification before proceeding.</rule>
<rule>Always include at least one positive highlight to encourage good practices.</rule>
<rule>Consult the **example-selector** knowledge table to load the appropriate example file for the review type being performed.</rule>
<rule>**Never assume existing code is correct or represents the intended pattern.** Existing code is often legacy, hastily written, or already known to be problematic. Evaluate it with the same critical eye as new code.</rule>
<rule>When two conflicting patterns, styles, or usages are found anywhere in the reviewed scope, always surface both under **⚠️ Inconsistencies**, present trade-offs neutrally, and explicitly request a decision from the user about which should be authoritative. Do not silently pick one as the standard.</rule>
<rule>When assessing inconsistencies, read enough surrounding context (adjacent files, related modules) to determine whether either pattern is clearly dominant or intentional before reporting — but if genuinely ambiguous, report as an inconsistency requiring a decision.</rule>
</rules>