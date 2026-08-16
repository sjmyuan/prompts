---
name: create-skill
description: Generate complete copilot skill files (SKILL.md) with capabilities, examples, and references that meet reviewer standards. Use when creating, authoring, generating, building, extracting, or validating a new skill.
---

<when-to-use-this-skill>
- User asks to create a new copilot skill (SKILL.md)
- User asks to author a new skill file from scratch
- User asks to generate examples or references for a skill
- User asks to build a complete skill with capabilities, knowledge, and rules
- User provides existing materials (agent prompts, docs, code) to extract into a skill
- User asks to validate a newly created skill before delivery
- Do NOT load for reviewing an existing skill file — use `review-skill` instead
</when-to-use-this-skill>

<knowledge>

<skill-file-sections>
A well-formed SKILL.md uses distinct, non-overlapping sections: frontmatter `description` (load decision), `<when-to-use-this-skill>` (scope check), `<knowledge>` (facts), `<capabilities>` (procedures), `<rules>` (routing), and a `<context-loading-guide>` inside knowledge. Section table, structural violations, and directory layout: **reference/section-semantics.md**.
</skill-file-sections>

<description-quality>
The `description` follows a two-part template — domain summary plus a "Use when…" trigger phrase listing intent verbs — and is scored on five dimensions. Template, scoring rubric, and trigger-correctness rules: **reference/description-quality.md**.
</description-quality>

<naming-conventions>
Skill names and capability names start with an imperative action verb; knowledge subsection names use descriptive noun phrases. Full rubric: **reference/naming-conventions.md**.
</naming-conventions>

<example-standards>
Every capability needs a linked example; each example must have a scenario heading, realistic input, output matching the capability's steps, and no contradictions. Full criteria: **reference/example-standards.md**.
</example-standards>

<platform-agnostic-writing>
Created skills must avoid platform-specific tool names, use abstract context descriptions, and detect-don't-assume. Full rules: **reference/platform-agnostic-writing.md**.
</platform-agnostic-writing>

<pipeline-integration>
A skill in a multi-skill pipeline must satisfy 4 integration points: handoff mechanism, shared schema, bidirectional awareness, guard clauses. Full checklist: **reference/pipeline-integration.md**.
</pipeline-integration>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Writing or scoring the `description`, or checking trigger coverage | Description template, scoring rubric, trigger rules | [reference/description-quality.md](reference/description-quality.md) |
| Naming a skill, capability, or knowledge subsection | Action-verb naming rubric | [reference/naming-conventions.md](reference/naming-conventions.md) |
| Checking section purpose, order, or structural violations | Section table, violation list, directory layout | [reference/section-semantics.md](reference/section-semantics.md) |
| Creating or validating example files | Example coverage + quality criteria | [reference/example-standards.md](reference/example-standards.md) |
| Writing skill prose for portability | Platform-agnostic rules | [reference/platform-agnostic-writing.md](reference/platform-agnostic-writing.md) |
| Creating a skill that feeds another skill or is loaded by sub-agents | 4-point integration checklist | [reference/pipeline-integration.md](reference/pipeline-integration.md) |
| Walking through a greenfield create flow | End-to-end create-skill-file walkthrough | [examples/create-skill-file.md](examples/create-skill-file.md) |
| Extracting an existing agent prompt or doc into a skill | Extraction walkthrough | [examples/extract-from-agent.md](examples/extract-from-agent.md) |
| Adding examples and references to a drafted skill | Examples + references walkthrough | [examples/create-examples-and-references.md](examples/create-examples-and-references.md) |
| Validating a newly created skill before delivery | Validation-report walkthrough | [examples/validate-new-skill.md](examples/validate-new-skill.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<collect-skill-requirements>
**Objective**: Gather what defines the new skill's purpose, scope, and capabilities.

1. Ask the user targeted questions to understand: **skill name** (kebab-case, imperative verb per **naming-conventions**), **description** (domain + trigger phrase), **when-to-use scenarios** (3–7), **core capabilities** (each named with an imperative action verb), **knowledge requirements** (tables, layouts, constraints), **rules** (when → capability routing), **example scenarios** (≥1 per capability), and **reference needs** (large rubrics to extract).
2. Present a structured summary of the collected information and request confirmation or refinements.
3. If the user provides existing source materials (agent prompts, code, docs), read and analyze them to extract accurate knowledge entries instead of asking from scratch.
</collect-skill-requirements>

<create-skill-file>
**Objective**: Generate a complete SKILL.md that meets reviewer quality requirements.

1. Create the directory structure `skills/<skill-name>/` with `examples/` and `reference/` subdirectories as needed.
2. Write the frontmatter: `name` in kebab-case with an action verb; `description` per the two-part template — self-score it per **description-quality** (aim ≥ 9).
3. Write `<when-to-use-this-skill>` as 3–7 bullet scenarios whose intent verbs appear in the `description` trigger phrase.
4. Write the knowledge section: put reference data in tables/lists; extract large rubrics to `reference/` files exposed via a condition-first `<context-loading-guide>`.
5. Write each capability with a unique action-verb name and numbered steps; never embed reference tables or constraint bullets inside capabilities.
6. Write rules only when multiple capabilities exist — each answers "When [scenario] → use [capability]".
7. Validate the draft against **section-semantics** (violations, section order, naming).
8. If the skill is part of a multi-skill pipeline, verify the 4 integration points per **pipeline-integration**.
9. Write the final content to `skills/<skill-name>/SKILL.md`.
</create-skill-file>

<create-skill-examples>
**Objective**: Create example files demonstrating each capability.

1. Determine one realistic scenario per capability per **example-standards**.
2. Create one `.md` file per scenario under `examples/`.
3. Include per file: a scenario heading, a setup paragraph, `Applies **[capability-name]**`, the input/context, and the expected output formatted as the capability would produce it.
4. Validate each against **example-standards** before writing.
5. Write each example to its file.
</create-skill-examples>

<create-skill-references>
**Objective**: Create reference files for large rubrics and detailed criteria.

1. Identify knowledge entries that are large rubrics, scoring matrices, or comprehensive criteria that would bloat SKILL.md.
2. Create a dedicated `.md` file per topic under `reference/` with a clear title, full content, and cross-references to the relevant capability.
3. Add a condition-first `<context-loading-guide>` entry pointing to each new reference file.
</create-skill-references>

<validate-created-skill>
**Objective**: Validate the created skill file, examples, and references before delivery.

1. Verify all required sections exist in order: frontmatter, `<when-to-use-this-skill>`, `<knowledge>`, `<capabilities>`, optional `<rules>`.
2. Score the description per **description-quality** (target ≥ 9) and check bidirectional trigger coverage.
3. Check capabilities: action-verb names, ordered steps, no embedded reference data.
4. Check knowledge: material placed correctly, large rubrics extracted, `<context-loading-guide>` condition-first.
5. Check examples: coverage of every capability, quality per **example-standards**, traceability, no contradictions.
6. Check rules: route "when → capability" without re-stating capability content.
7. Report results with any issues and suggested fixes; if issues exist, return to the relevant creation capability, fix, and re-validate.
</validate-created-skill>

</capabilities>

<rules>
<rule>When the user requests to create a new skill, use **collect-skill-requirements** to gather name, description, scenarios, capabilities, knowledge, and example needs.</rule>
<rule>After requirements are confirmed, use **create-skill-file** to generate SKILL.md, and **create-skill-examples** plus **create-skill-references** in parallel as needed.</rule>
<rule>When the user provides existing source materials, use **collect-skill-requirements** step 3 to incorporate them into the knowledge section rather than embedding them in capabilities.</rule>
<rule>After creating all files, use **validate-created-skill** before presenting the result.</rule>
<rule>When validation reveals issues, return to the relevant creation capability to fix them, then re-validate.</rule>
<rule>When the user asks to review an existing skill file, do not use this skill — delegate to the `review-skill` skill instead.</rule>
</rules>
