---
name: doc-maintainer
description: Update project documentation to reflect code changes (bug fixes, refactors, or new features). Provide concise, actionable edits to requirements, architecture, README, and related docs. Use this skill when code changes occur.
---

<when-to-use-this-skill>
Use this skill when:
- Code changes affect public behavior, APIs, developer workflows, or user-facing features
- New features introduce functionality requiring documentation
- Bug fixes change expected behavior or usage patterns
- Refactors modify project structure, file organization, or development setup
- Dependencies, build processes, or deployment procedures are updated
- Documentation is stale, incomplete, or inconsistent with current code
- Tests reveal gaps between documented and actual behavior
- Configuration files (package.json, tsconfig, etc.) are modified in meaningful ways
</when-to-use-this-skill>

<docs>
This skill covers the following documentation types:
- **Requirements** (requirements.md, feature specs)
- **Architecture** (architecture.md, design docs, system diagrams)
- **README** (getting started, setup, project overview)
- **API Documentation** (endpoint specs, function signatures, type definitions)
- **Usage Examples** (code samples, tutorials, demos)
- **Changelog** (release notes, version history)
- **Configuration Guides** (environment setup, build configuration)
- **Troubleshooting** (common issues, debugging guides)
- **Developer Guides** (contributing, coding standards, workflows)
- **Deployment Documentation** (hosting, CI/CD, production setup)
- **Inline Documentation** (JSDoc, code comments for complex logic)
</docs>

<capabilities>

<impact-assessment>
Assess which documentation requires updates based on the change type:

**For Bug Fixes:**
- Update troubleshooting guides if the bug was a common issue
- Revise usage examples if they demonstrated the buggy behavior
- Update changelog with bug fix details
- Check if requirements or specs need correction

**For New Features:**
- Add or update requirements documentation
- Extend architecture docs if new components or patterns are introduced
- Update README with feature overview and setup instructions
- Create or update usage examples demonstrating the feature
- Add API documentation for new interfaces or endpoints
- Update configuration guides if new settings are required
- Document any breaking changes or migration steps

**For Refactors:**
- Update architecture docs if structure or patterns changed
- Revise developer guides if workflows or practices changed
- Update configuration guides if build/dev setup changed
- Refresh inline documentation for refactored code
- Check if examples need updates for new code organization
- Verify README accuracy (file paths, command references)

**For Dependency/Infrastructure Changes:**
- Update README installation and setup sections
- Revise configuration guides
- Update deployment documentation
- Document version compatibility requirements
- Add migration guides for breaking dependency changes
</impact-assessment>

<maintaining-docs>
Follow this systematic approach to update documentation:

1. **Review the Change**
   - Examine modified files, commit messages, and PR descriptions
   - Identify what changed: behavior, API, UX, dependencies, structure
   - Note the user impact and developer impact separately
   - Check test files to understand new behavior validation

2. **Identify Affected Documentation**
   - Use the impact-assessment capability to determine doc scope
   - List specific sections within each document that need updates
   - Prioritize user-facing docs over internal notes
   - Consider both direct and indirect documentation impacts

3. **Make Focused, Accurate Edits**
   - Update only the sections directly affected by the change
   - Avoid broad rewrites unless documentation is fundamentally outdated
   - Ensure technical accuracy by referencing the actual code
   - Use precise terminology consistent with the codebase
   - Maintain the existing tone and style of each document

4. **Add or Update Examples**
   - Provide code snippets showing new usage patterns
   - Include before/after examples for changed APIs
   - Demonstrate edge cases or common pitfalls
   - Ensure examples are runnable and tested (when possible)
   - Use realistic scenarios that match user context

5. **Document Migration Steps**
   - For breaking changes, provide clear step-by-step migration instructions
   - Include code snippets showing the old and new way
   - List all affected code patterns users need to update
   - Explain the rationale for the change
   - Estimate migration effort and provide timelines

6. **Maintain Cross-References**
   - Link related documentation sections
   - Reference source code files and line numbers
   - Point to relevant tests, examples, or config files
   - Cite GitHub issues, PRs, or commit SHAs for traceability
   - Update any broken links or outdated references

7. **Record Design Decisions**
   - Document why certain approaches were chosen
   - Explain trade-offs and alternatives considered
   - Note any constraints or assumptions
   - Preserve context for future maintainers
   - Update architecture decision records (ADRs) if applicable
</maintaining-docs>

<validation-checklist>
Before finalizing documentation updates, verify:

**Accuracy:**
- [ ] All code examples compile/run without errors
- [ ] API signatures match actual implementation
- [ ] Configuration examples use correct syntax
- [ ] File paths and references are correct
- [ ] Version numbers and dates are accurate

**Completeness:**
- [ ] All affected documentation sections identified and updated
- [ ] Breaking changes clearly documented with migration paths
- [ ] New features have usage examples
- [ ] Edge cases and limitations are mentioned
- [ ] Related documentation is cross-referenced

**Clarity:**
- [ ] Documentation is understandable to the target audience
- [ ] Technical jargon is explained or avoided
- [ ] Step-by-step instructions are unambiguous
- [ ] Examples are well-commented and self-explanatory
- [ ] Structure follows a logical flow

**Consistency:**
- [ ] Terminology matches the codebase and existing docs
- [ ] Formatting follows the project's documentation style
- [ ] Tone is consistent with other documentation
- [ ] Examples follow consistent patterns
- [ ] Cross-references use standard linking format

**Maintainability:**
- [ ] Documentation is not overly coupled to implementation details
- [ ] Examples are simple and focused
- [ ] Duplicated information is minimized
- [ ] Version-specific details are clearly marked
- [ ] Documentation location is logical and discoverable
</validation-checklist>

<style-guidelines>
Adapt your writing style to the documentation type:

**Requirements & Specifications:**
- Be precise and unambiguous
- Use "must," "should," "may" consistently (RFC 2119 style)
- Focus on what, not how
- Include acceptance criteria

**Architecture Documentation:**
- Use diagrams where helpful (describe them in text)
- Explain the "why" behind architectural decisions
- Document constraints and trade-offs
- Keep high-level; avoid implementation minutiae

**README:**
- Start with a brief, compelling overview
- Prioritize getting started quickly
- Use bullet points and short paragraphs
- Include badges, screenshots, or demos where relevant

**API Documentation:**
- Document all parameters, return values, and exceptions
- Provide type signatures (TypeScript, JSDoc)
- Include usage examples for each method
- Note deprecations and version compatibility

**Usage Examples:**
- Show realistic, practical scenarios
- Include necessary imports and setup
- Comment complex or non-obvious code
- Demonstrate both common and advanced usage

**Troubleshooting Guides:**
- Use problem-solution format
- Include error messages users actually see
- Provide step-by-step debugging instructions
- Link to related issues or discussions

**Changelog:**
- Group by version, newest first
- Categorize: Added, Changed, Deprecated, Removed, Fixed, Security
- Be concise but specific
- Reference issues/PRs when helpful
</style-guidelines>

<examples>

When you need specific examples to understand how to document different types of code changes, load the relevant example file from the examples folder:

- **Bug Fix Documentation**: When documenting bug fixes and issue resolutions, read [examples/bug-fix-documentation.md](examples/bug-fix-documentation.md)
- **New Feature Documentation**: When documenting new features and capabilities, read [examples/new-feature-documentation.md](examples/new-feature-documentation.md)
- **Refactor Documentation**: When documenting code refactoring and restructuring, read [examples/refactor-documentation.md](examples/refactor-documentation.md)

Only load example files when they are directly relevant to the type of code change being documented to minimize context size.

</examples>

</capabilities>

<rules>

<positive-rules>
**DO:**
- Apply the **impact-assessment** capability first to determine documentation scope based on change type
- Apply the **maintaining-docs** capability systematically for all identified documentation updates
- Apply the **validation-checklist** capability to verify documentation completeness before finishing
- Apply the **style-guidelines** capability to ensure appropriate tone for each doc type
- Update documentation incrementally as code changes occur (don't batch)
- Preserve existing documentation structure and organization unless it's problematic
- Link to specific code files, line numbers, and commits for traceability
- Include practical, runnable examples that users can copy-paste
- Document the "why" behind decisions, not just the "what"
- Keep deprecated documentation with clear warnings rather than deleting it immediately
- Test code examples before including them in documentation
- Consider both developer and end-user audiences when updating docs
</positive-rules>

<negative-rules>
**DON'T:**
- Make documentation updates without reviewing the actual code changes first
- Rewrite entire documents when only specific sections need updates
- Use vague language like "usually," "might," or "should work" in specifications
- Document internal implementation details in user-facing documentation
- Assume users have the same context as developers
- Skip migration guides for breaking changes
- Copy-paste code examples without verifying they work
- Create documentation that will quickly become outdated (e.g., listing all file names)
- Use inconsistent terminology across different documentation files
- Forget to update examples when APIs change
- Leave TODO or placeholder comments in published documentation
- Over-document trivial or self-explanatory code
</negative-rules>

</rules>