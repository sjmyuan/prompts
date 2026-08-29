# Action-Verb Naming Convention

Used by **collect-skill-requirements** (step 1), **create-skill-file** (steps 2 and 6), and **validate-created-skill** (step 3).

## Skill names (kebab-case)
- Must start with an imperative action verb: `edit-svg`, `validate-data`, `generate-diagram`, `review-code`, `create-flowchart`
- NOT noun phrases: `svg-editor`, `data-validator`, `diagram-generator`, `code-reviewer`, `flowchart-creator`

## Capability names (inside `<capabilities>`)
- Must start with an imperative action verb: `<manage-storage>` not `<storage-management>`; `<generate-report>` not `<report-generation>`
- Good: `validate-`, `generate-`, `create-`, `analyze-`, `calculate-`, `collect-`, `transform-`, `review-`
- Bad: `validation`, `generation`, `creation`, `analysis`, `calculation`, `collection`, `transformation`, `review`

## Knowledge subsection names
- Must use **descriptive noun phrases** (`<storage-patterns>`, not `<define-storage>`)
- An action-verb name inside knowledge signals procedural content leaked into knowledge — a structural violation
