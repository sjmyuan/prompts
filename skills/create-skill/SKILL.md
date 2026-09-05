---
name: create-skill
description: Author, edit, and validate skill files (SKILL.md) with capabilities, examples, and references that meet reviewer standards. Use when creating, authoring, generating, building, extracting, editing, improving, revising, or validating a skill.
---

<when-to-use-this-skill>
- User asks to create or author a new skill (SKILL.md) from scratch
- User asks to generate examples or references for a skill
- User asks to build a complete skill with capabilities, knowledge, and rules
- User provides existing materials (agent prompts, docs, code) to extract into a skill
- User asks to edit, improve, or revise an existing skill
- User asks to validate a newly created or edited skill before delivery
- Do NOT load for a read-only review — use `review-skill` (its findings feed **edit-skill**)
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

<writing-style>
Created skill prose must use directive voice, BLUF, hard caps, atomic bullets, tables-over-prose, no banned phrases, no meta-narration. Full rules: **../review-skill/reference/writing-style.md**.
</writing-style>
<size-limits>
Budgets are character-based: SKILL.md and each `reference/` ≤12,000 / 150 lines; each `examples/` ≤9,000 / 150 lines; >120-char lines flagged. Measure via **../review-skill/scripts/measure_sizes.py**, else `wc -m`/line count. Full rules: **../review-skill/reference/size-limits.md**.
</size-limits>
<size-remediation>
Fix over-budget files via re-encode → reuse → cut weight → redistribute → reduce → escalate; chars are the only size gate — never merge steps or lines (structural-integrity gate, 🔴 Blocker). Full rules: **../review-skill/reference/size-remediation.md**.
</size-remediation>
<conciseness-check>
Every element must justify its existence — one line = one idea. Cut anything the skill can lose without losing meaning. Full criteria: **../review-skill/reference/conciseness-check.md**.
</conciseness-check>
<evaluation-process>
Each capability must include a validation or checklist step so output is verifiable. Patterns and absence severity: **../review-skill/reference/evaluation-process.md**.
</evaluation-process>
<severity-levels>
Validation findings labeled Blocker 🚫 / Major 🔴 / Minor 🟡 / Nit 🟢 / Inconsistency ⚠️. Table: **../review-skill/reference/severity-levels.md**.
</severity-levels>
<edit-existing-skill>
Editing an existing skill reuses the create-* capabilities in existing-file mode — review-first for open "improve", change-type routing, ripple on rename/remove, validate-after-each. Details: **reference/edit-skill-procedure.md**.
</edit-existing-skill>
<same-name-live-copy-ban>
Never read, compare, or edit a live/loaded skill with the same name in claude/opencode/copilot dirs. The user-provided file(s) are the only source and target — if the user gives no location, ask; never auto-fetch a same-named installed skill.
</same-name-live-copy-ban>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Walking through a greenfield create flow | End-to-end create-skill-file walkthrough | [examples/create-skill-file.md](examples/create-skill-file.md) |
| Extracting an existing agent prompt or doc into a skill | Extraction walkthrough | [examples/extract-from-agent.md](examples/extract-from-agent.md) |
| Adding examples and references to a drafted skill | Examples + references walkthrough | [examples/create-examples-and-references.md](examples/create-examples-and-references.md) |
| Validating a newly created skill before delivery | Validation-report walkthrough | [examples/validate-new-skill.md](examples/validate-new-skill.md) |
| Editing an existing skill (review findings + rename ripple) | Edit walkthrough | [examples/editing-existing-skill.md](examples/editing-existing-skill.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<collect-skill-requirements>
**Objective**: Gather what defines the new skill's purpose, scope, and capabilities.

1. Ask the user targeted questions to understand: **skill name** (kebab-case, imperative verb per **naming-conventions**), **description** (domain + trigger phrase), **when-to-use scenarios** (3–7), **core capabilities** (each named with an imperative action verb), **knowledge requirements** (tables, layouts, constraints), **rules** (when → capability routing), **example scenarios** (≥1 per capability), and **reference needs** (large rubrics to extract).
2. Present a structured summary of the collected information and request confirmation or refinements.
3. If the user provides existing source materials (agent prompts, code, docs), read and analyze them to extract accurate knowledge entries instead of asking from scratch — never fetch a live/loaded skill with the same name (per **same-name-live-copy-ban**).
</collect-skill-requirements>

<create-skill-file>
**Objective**: Generate a complete SKILL.md that meets reviewer quality requirements.

1. Create the directory structure under the user-provided target location (confirmed in **collect-skill-requirements**) with `examples/` and `reference/` subdirectories as needed.
2. Write the frontmatter: `name` in kebab-case with an action verb; `description` per the two-part template — self-score it per **description-quality** (aim ≥ 9).
3. Write `<when-to-use-this-skill>` as 3–7 bullet scenarios whose intent verbs appear in the `description` trigger phrase.
4. Allocate a per-section char budget (when-to-use, knowledge, each capability, rules, guide) totaling ≤ **size-limits**; write each within its cap — prevention beats remediation.
5. Write the knowledge section: put reference data in tables/lists; extract large rubrics to `reference/` files, self-linked from their knowledge subsection and routed inline from the steps that use them.
6. Write each capability with a unique action-verb name and numbered steps; never embed reference tables or constraint bullets inside capabilities.
7. Write rules only when multiple capabilities exist — each answers "When [scenario] → use [capability]".
8. Write all prose per **writing-style** — directive voice, BLUF, hard caps, atomic bullets, no banned phrases, no meta-narration.
9. Write prose per **platform-agnostic-writing** — no platform tool names, no concrete context paths.
10. Validate the draft against **section-semantics** (violations, section order, naming).
11. If the skill is part of a multi-skill pipeline, verify the 4 integration points per **pipeline-integration** from the created files' own self-declared relationships — never fetch sibling skills.
12. Measure the SKILL.md per **size-limits** (script when available, else manual count); if over budget, apply **size-remediation** (lever order + gate) — never merge steps/lines.
13. Write the final content to the user-provided `<target>/SKILL.md` (per **same-name-live-copy-ban**).
</create-skill-file>

<create-skill-examples>
**Objective**: Create or update example files demonstrating each capability.

1. Determine one realistic scenario per capability per **example-standards**.
2. Create one `.md` file per scenario under `examples/`.
3. Include per file: a scenario heading, a setup paragraph, `Applies **[capability-name]**`, the input/context, and the expected output formatted as the capability would produce it.
4. Validate each against **example-standards** before writing.
5. Write example prose per **writing-style** — scenario 1–2 sentences, output as the capability would produce it, no meta-notes inside the output.
6. Measure each example per **size-limits** (≤9,000 chars / 150 lines); if over budget, apply **size-remediation** (trim edge cases, drop low-value examples).
7. Write each example to its file.
</create-skill-examples>

<create-skill-references>
**Objective**: Create or update reference files for large rubrics and detailed criteria.

1. Identify knowledge entries that are large rubrics, scoring matrices, or comprehensive criteria that would bloat SKILL.md.
2. Create a dedicated `.md` file per topic under `reference/` with a clear title, full content, and cross-references to the relevant capability.
3. Write the reference per **writing-style** — title + rubric only, no narrative intro, no restatement of SKILL.md.
4. Measure each reference per **size-limits** (≤12,000 chars / 150 lines); if over budget, apply **size-remediation** (split or condense).
5. Route each reference: self-link it from its knowledge subsection; step-tied files are also routed inline from the step; step-independent files get a `<context-loading-guide>` row.
</create-skill-references>

<validate-created-skill>
**Objective**: Validate the created or edited skill file, examples, and references before delivery.

1. Apply **same-name-live-copy-ban**: validate only the created/user-provided files — never a same-named live copy. Then verify all required sections exist in order: frontmatter, `<when-to-use-this-skill>`, `<knowledge>`, `<capabilities>`, optional `<rules>`.
2. Score the description per **description-quality** (target ≥ 9) and check bidirectional trigger coverage.
3. Check capabilities: action-verb names, ordered steps, no embedded reference data.
4. Check knowledge: material placed correctly, large rubrics extracted, `<context-loading-guide>` condition-first.
5. Check writing style per **writing-style**: directive voice, BLUF, hard caps, no banned phrases, no meta-narration.
6. Check platform-agnostic writing per **platform-agnostic-writing**: no tool names, no concrete context paths.
7. Measure all files per **size-limits**; for over-budget files, apply **size-remediation** (lever order) + structural-integrity gate — line/step-merging fails as 🔴 Blocker.
8. Check conciseness per **conciseness-check**: one line = one idea, nothing fails the "So what?" test.
9. Check examples: coverage of every capability, quality per **example-standards**, traceability, no contradictions.
10. Check rules: route "when → capability" without re-stating capability content.
11. Check each capability has a validation/checklist step per **evaluation-process**; flag absence per its severity.
12. If the skill references another skill or is loaded by sub-agents, verify integration per **pipeline-integration** from the created files' own self-declared relationships only — never fetch other skills.
13. Report results with severity labels per **severity-levels** and fixes; if issues exist, return to the relevant creation capability, fix, and re-validate.
</validate-created-skill>

<edit-skill>
**Objective**: Edit or improve an existing skill's files (SKILL.md, examples, references) by reusing the create-* capabilities in existing-file mode.

1. Apply **same-name-live-copy-ban** — target only the user-provided existing files.
2. Read and inventory the skill: sections, capabilities, knowledge, rules, guide rows, examples, references.
3. Triage per **reference/edit-skill-procedure.md** — an open-ended "improve" runs `review-skill`'s **review-skill-file** (read-only) and applies its findings; a concrete request proceeds directly.
4. Classify each change per the change-type table in **reference/edit-skill-procedure.md** (add, remove, rename, restructure, apply findings, size-reduce).
5. Route each change to **create-skill-file** / **create-skill-examples** / **create-skill-references** in existing-file mode per **reference/edit-skill-procedure.md**.
6. Run the ripple checklist after renames or removals per **reference/edit-skill-procedure.md**.
7. Run **validate-created-skill** after each change; revert on a Blocker 🔴 and redo.
8. Re-measure changed files per **size-limits** and report per **severity-levels**.
</edit-skill>

</capabilities>

<rules>
<rule>When the user requests to create a new skill, use **collect-skill-requirements** to gather name, description, scenarios, capabilities, knowledge, and example needs.</rule>
<rule>After requirements are confirmed, use **create-skill-file** to generate SKILL.md, and **create-skill-examples** plus **create-skill-references** in parallel as needed.</rule>
<rule>When the user provides existing source materials, use **collect-skill-requirements** step 3 to incorporate them into the knowledge section rather than embedding them in capabilities.</rule>
<rule>After creating or editing all files, use **validate-created-skill** before presenting the result.</rule>
<rule>When validation reveals issues, return to the relevant creation capability to fix them, then re-validate.</rule>
<rule>When creating or validating a skill, operate only on the user-provided files per **same-name-live-copy-ban** — never read, compare, or edit a live/loaded skill with the same name.</rule>
<rule>When the user asks to edit, improve, or revise an existing skill, use **edit-skill**; run an open-ended "improve" through `review-skill` first per **reference/edit-skill-procedure.md**.</rule>
<rule>When the user asks for a read-only review of an existing skill file, delegate to the `review-skill` skill instead.</rule>
</rules>
