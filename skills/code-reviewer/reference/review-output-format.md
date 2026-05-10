# Review Output Format

Standard template for all review output:

```
## Code Review Summary

**Scope**: [Brief description of what was reviewed]
**Focus Areas**: [e.g., correctness, security, performance]
**Overall Assessment**: [Brief evaluation - e.g., "Ready to merge with minor changes" or "Requires blockers to be addressed"]

---

## Findings

### 🚫 Blockers (Must Fix)

#### [Finding Title]
- **File**: [path/to/file.ts:L10-L15](path/to/file.ts#L10-L15)
- **Issue**: [Clear description of what's wrong and why it matters]
- **Impact**: [Specific consequence if not fixed]
- **Recommendation**: [Concrete fix with code snippet if helpful]

### 🔴 Major Issues

### 🟡 Minor Issues

### 🟢 Nits / Suggestions

### ⚠️ Inconsistencies (Decision Required)

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
