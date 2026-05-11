---
name: code-reviewer
description: Perform systematic reviews of code and documents across files, folders, diffs, commits, pull requests, or branch comparisons. Evaluates correctness, security, performance, maintainability, and structural quality. Provides prioritized, actionable feedback without making changes. Use when users request reviews, feedback, or quality assessments on code or documents.
---

<when-to-use-this-skill>
- User explicitly requests a code review
- User submits files, folders, diffs, commits, or pull requests for review
- User asks for feedback on code quality, security, performance, or maintainability
- User supplies one branch name (diff against current branch) or two branch names (diff between them)
- User asks to review a document (README, design doc, ADR, specification, runbook, etc.) for clarity, completeness, or structure
</when-to-use-this-skill>

<knowledge>

<review-dimensions-reference>
See [reference/review-dimensions.md](reference/review-dimensions.md) for the full 8-dimension checklist (Correctness, Maintainability, Performance, Security, APIs, Tests, Architecture, Inconsistencies). Load before applying **conducting-code-review**.
</review-dimensions-reference>

<context-loading-guide>
Load on demand to minimize context size. **gathering-review-context** is demonstrated as the lead-in step in all four example files — load any one for output structure guidance on that capability.

| Load when | Provides | File |
|---|---|---|
| About to review a diff, commit, or bug fix | Output structure example for diff/commit reviews | [examples/diff-commit-review.md](examples/diff-commit-review.md) |
| User supplies one or two branch names for comparison | Output structure example for branch diff reviews | [examples/branch-diff-review.md](examples/branch-diff-review.md) |
| Reviewing a performance optimization or slow-code change | Output structure example for performance-focused reviews | [examples/performance-improvement.md](examples/performance-improvement.md) |
| Reviewing a document (README, ADR, design doc, specification, runbook) | Output structure example for document reviews | [examples/doc-review.md](examples/doc-review.md) |
</context-loading-guide>

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
See [reference/severity-levels.md](reference/severity-levels.md) for the full severity rubric (🚫 Blocker, 🔴 Major, 🟡 Minor, 🟢 Nit, ⚠️ Inconsistency) with criteria for each level. Load before categorizing review findings.
</defining-severity-levels>

<formatting-review-output>
See [reference/review-output-format.md](reference/review-output-format.md) for the standard review output template (Summary, Findings by severity, Positive Highlights, Risks & Assumptions, Next Steps) and formatting guidelines. Load before presenting review findings.
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

**Steps**:
1. Consult **review-dimensions-reference** knowledge and apply each of the 8 dimensions to the reviewed code. For each dimension, evaluate all relevant ✓ checklist items and note any violations.
2. For each violation found, assign a severity level using **defining-severity-levels** knowledge and prepare a concise finding.
3. For dimension 8 (Inconsistencies): capture every conflicting pattern with both variants and concrete file/line references; note trade-offs and flag for a user decision — do not silently pick one.
4. Format all findings using the **formatting-review-output** knowledge template.
5. Load the appropriate example from the **context-loading-guide** table for output structure guidance.
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
<rule>When the user submits files, folders, diffs, or commits for review, first apply **gathering-review-context**, then **conducting-code-review**.</rule>
<rule>When the user supplies one or two branch names for comparison, first apply **getting-branch-diff** to retrieve the diff, then apply **conducting-code-review**.</rule>
<rule>When the subject of review is a document (README, ADR, design doc, specification, runbook, etc.), use **reviewing-document** instead of **conducting-code-review**.</rule>
</rules>
<rule>Apply **review-efficiency-knowledge** strategies to maximize value and minimize review time.</rule>
<rule>When the user supplies branch names for review, first apply **getting-branch-diff** to retrieve the full diff via git CLI before conducting the review. Always review every changed file — never skip any.</rule>
<rule>Do not modify code directly during review. Suggest changes with patch-style snippets or clear descriptions.</rule>
<rule>If critical context is missing and assumptions would compromise review quality, ask the user for clarification before proceeding.</rule>
<rule>Always include at least one positive highlight to encourage good practices.</rule>
<rule>Consult the **context-loading-guide** knowledge table to load the appropriate example file for the review type being performed.</rule>
<rule>**Never assume existing code is correct or represents the intended pattern.** Existing code is often legacy, hastily written, or already known to be problematic. Evaluate it with the same critical eye as new code.</rule>
<rule>When two conflicting patterns, styles, or usages are found anywhere in the reviewed scope, always surface both under **⚠️ Inconsistencies**, present trade-offs neutrally, and explicitly request a decision from the user about which should be authoritative. Do not silently pick one as the standard.</rule>
<rule>When assessing inconsistencies, read enough surrounding context (adjacent files, related modules) to determine whether either pattern is clearly dominant or intentional before reporting — but if genuinely ambiguous, report as an inconsistency requiring a decision.</rule>
</rules>