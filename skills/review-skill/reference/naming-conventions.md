# Action-Verb Naming Conventions

Both the **skill name** and its **capability names** in the skill under review must follow the action-verb naming convention:

**Skill name** (frontmatter `name:` field, kebab-case):
- Must start with an imperative action verb: `edit-svg`, `validate-data`, `generate-diagram`, `review-code`, `create-flowchart`
- NOT noun phrases: `svg-editor`, `data-validator`, `diagram-generator`, `code-reviewer`, `flowchart-creator`
- Example: a skill named `form-validator` should be named `validate-form`

**Capability section names** (inside `<capabilities>`):
- Must start with an imperative action verb: `<manage-storage>`, not `<storage-management>`; `<generate-report>`, not `<report-generation>`
- Good patterns: `validate-`, `generate-`, `create-`, `analyze-`, `calculate-`, `collect-`, `transform-`, `review-`
- Bad patterns: `validation`, `generation`, `creation`, `analysis`, `calculation`, `collection`, `transformation`, `review`

**`<knowledge>` subsection names**:
- Must use **descriptive noun phrases** (`<storage-patterns>`, not `<define-storage>`)
- A subsection named with an action verb inside `<knowledge>` signals that procedural content has leaked into knowledge — this is a structural violation
