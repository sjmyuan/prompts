---
name: doc-maintainer
description: Synchronize documentation with code changes across README, architecture docs, API docs, and requirements. Assesses documentation impact and provides focused updates, migration guides, and examples. Use after implementing bug fixes, features, or refactors that affect documented behavior, APIs, or workflows, or when documentation is stale, inconsistent, or missing, or when tests reveal discrepancies between documented and actual behavior, or when configuration files affecting developer setup are modified.
---

<when-to-use-this-skill>
- Code changes affect public behavior, APIs, developer workflows, or user-facing features
- New features introduce functionality requiring documentation
- Bug fixes change expected behavior or usage patterns
- Refactors modify project structure, file organization, or development setup
- Dependencies, build processes, or deployment procedures are updated
- Documentation is stale, incomplete, or inconsistent with current code
- Tests reveal gaps between documented and actual behavior
- Configuration files (package.json, tsconfig, etc.) are modified in meaningful ways
</when-to-use-this-skill>

<knowledge>

<documentation-types>
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
</documentation-types>

<impact-lookup>
See [reference/impact-lookup.md](reference/impact-lookup.md) for the full lookup table: which documentation types to update for bug fixes, new features, refactors, and dependency/infrastructure changes. Load before step 2 of **maintain-docs**.
</impact-lookup>

<doc-validation-criteria>
See [reference/doc-validation-criteria.md](reference/doc-validation-criteria.md) for the full validation checklist: Accuracy, Completeness, Clarity, Consistency, and Maintainability (25 items). Load before running step 8 of **maintain-docs**.
</doc-validation-criteria>

<writing-style-reference>
See [reference/writing-style-guide.md](reference/writing-style-guide.md) for per-documentation-type style rules (Requirements, Architecture, README, API docs, Usage Examples, Troubleshooting, Changelog). Load on demand when updating a document type.
</writing-style-reference>

<context-loading-guide>
Load only the example directly relevant to the current change type to minimize context size.

| Load when | Provides | File |
|---|---|---|
| Documenting a bug fix or issue resolution | Full workflow example: assess impact + update docs for a bug fix | [examples/bug-fix-documentation.md](examples/bug-fix-documentation.md) |
| Documenting a new feature | Full workflow example: assess impact + update docs for new functionality | [examples/new-feature-documentation.md](examples/new-feature-documentation.md) |
| Documenting a refactor or structural change | Full workflow example: assess impact + update docs for a refactor | [examples/refactor-documentation.md](examples/refactor-documentation.md) |
| Documenting dependency or infrastructure changes | Full workflow example: assess impact + update docs for dependency/infra changes | [examples/dependency-infrastructure-documentation.md](examples/dependency-infrastructure-documentation.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<maintain-docs>
Follow this systematic approach to update documentation:

1. **Review the Change**
   - Examine modified files, commit messages, and PR descriptions
   - Identify what changed: behavior, API, UX, dependencies, structure
   - Note the user impact and developer impact separately
   - Check test files to understand new behavior validation

2. **Identify Affected Documentation**
   - Consult **impact-lookup** knowledge to determine which documentation types require updates
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

8. **Validate Before Finalizing**
   - Run through **doc-validation-criteria** knowledge to verify accuracy, completeness, clarity, consistency, and maintainability
</maintain-docs>

</capabilities>

<rules>

<rule> When code changes or documentation gaps are provided, apply **maintain-docs**. </rule>

</rules>

