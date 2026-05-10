````markdown
# Example: Skill File Review

**Scenario**: Review of `skills/commit-message-writer/SKILL.md` — a copilot skill that guides an AI agent to produce consistent, well-formed git commit messages.

**Review Focus**: Full structural review — section semantics, capability naming, rules, and example coverage.

## Code Review Summary

**Scope**: `skills/commit-message-writer/SKILL.md` — full skill file  
**Focus Areas**: Section purpose compliance, duplication, naming, example coverage  
**Overall Assessment**: Well-structured. All sections serve their intended purpose with no major violations. One minor issue and two nits noted.

---

## Findings

### � Minor Issues

#### Examples exposed via standalone `<examples>` section instead of `<context-loading-guide>` inside `<knowledge>`
- **File**: [SKILL.md](SKILL.md#L58-L64)
- **Issue**: The skill uses a top-level `<examples>` section rather than a `<context-loading-guide>` entry nested inside `<knowledge>`. The preferred pattern consolidates all on-demand context — examples, references, rubrics — in one place so the agent always knows where to look.
- **Recommendation**: Move the examples list into a `<context-loading-guide>` block inside the `<knowledge>` section. The file references can stay exactly as-is; only the placement and tag name change.

---

### �🟢 Nits / Suggestions

#### `<knowledge>` entry for commit type prefixes could include a "when in doubt" fallback
- **File**: [SKILL.md](SKILL.md#L12-L28)
- **Issue**: The prefix reference table (feat, fix, chore, docs, refactor, test, ci) does not indicate what to use when a change spans multiple types.
- **Recommendation**: Add a single note: *"When a commit spans multiple types, prefer the type with the highest user impact (feat > fix > refactor > chore)."* This prevents the agent from stalling on ambiguous inputs.

#### Rule for breaking changes could link to the capability more explicitly
- **File**: [SKILL.md](SKILL.md#L55-L57)
- **Issue**: The rule reads *"Always include a BREAKING CHANGE footer for API removals"*. This is a valid routing trigger but doesn't reference the capability (`<write-commit-message>`) by name.
- **Recommendation**: Rewrite as: *"When the diff contains a removed or renamed public API, use **write-commit-message** and include a `BREAKING CHANGE:` footer as described in step 4."*

---

## Positive Highlights
- `<knowledge>` cleanly holds the prefix table, 72-character line-wrap rule, and footer format — none of this is duplicated in the capability body. Exemplary separation of concerns.
- `<write-commit-message>` uses numbered steps throughout and is named with a clear action verb. The steps are sequential and unambiguous.
- Rules correctly use "scenario → capability" routing. None re-state capability content.
- Example coverage is complete: three files covering a simple bug fix, a multi-file feature, and a breaking-change migration span the main scenario variants.
- `<when-to-use-this-skill>` is tight and correctly scoped.

---

## Risks & Assumptions
- Review assumes the four-section semantics (knowledge / capabilities / rules) with on-demand context exposed via `<context-loading-guide>` inside `<knowledge>`. If the intended skill format differs, findings may not apply.

---

## Recommended Next Steps
1. Move the `<examples>` section into `<knowledge>` as a `<context-loading-guide>` entry. *(Resolves 🟡 minor)*
2. Add a "when in doubt" fallback note to the prefix table. *(Resolves 🟢 nit)*
3. Rewrite the breaking-change rule to explicitly name the capability. *(Resolves 🟢 nit)*

One minor structural fix required; otherwise ready for production use.
````
