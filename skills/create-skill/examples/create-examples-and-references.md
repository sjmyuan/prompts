# Example: Add Examples and References to a Drafted Skill

**Scenario**: A SKILL.md is already drafted; the user asks to add example files and extract a large rubric to a reference file. Demonstrates both **create-skill-examples** and **create-skill-references**.

**Applies**: **create-skill-examples**, **create-skill-references**

## Input / Context
Drafted `skills/data-validator/SKILL.md` with 2 capabilities (`<validate-data>`, `<report-errors>`). User asks: "Add examples and reference files."

## Reference Extraction (create-skill-references)
The validation-criteria table is a large rubric — extract to `reference/validation-rubric.md`, then add a `<context-loading-guide>` entry:
`Load when validating data or reporting errors | Validation criteria rubric | reference/validation-rubric.md`

## Example Creation (create-skill-examples)
One example per capability:
- `examples/validate-csv-data.md` → **validate-data** happy path (well-formed CSV)
- `examples/handle-missing-fields.md` → **validate-data** edge case (missing columns)
- `examples/report-error-summary.md` → **report-errors** (error aggregation output)

Each includes a scenario heading, setup paragraph, `Applies **...**`, input, and expected output matching the capability steps. Each is written per **writing-style** and measured per **size-limits** — examples ≤9,000 chars / 150 lines, the reference ≤12,000 / 150.

## Expected Output
```
skills/data-validator/
├── SKILL.md
├── examples/
│   ├── validate-csv-data.md
│   ├── handle-missing-fields.md
│   └── report-error-summary.md
└── reference/
    └── validation-rubric.md
```
