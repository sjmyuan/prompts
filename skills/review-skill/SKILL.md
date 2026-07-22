---
name: review-skill
description: Review SKILL.md files for correct structure, section-purpose compliance, naming convention adherence, and absence of duplication. Evaluates whether knowledge, capabilities, rules, and examples sections each serve their intended purpose and whether names follow action-verb conventions. Use when users request feedback, a quality assessment, or want to improve, fix, or ensure a copilot skill file triggers correctly.
---

<when-to-use-this-skill>
- User asks to review a skill file (SKILL.md)
- User asks to improve or fix a skill file (SKILL.md)
- User asks whether a SKILL.md is correctly structured
- User asks for feedback on section placement, duplication, or capability format in a skill file
- User asks whether a skill will trigger or activate correctly
- User asks whether a skill's name or capability names follow naming conventions
</when-to-use-this-skill>

<knowledge>

<skill-file-section-semantics>
Section-purpose table and common structural violations. Load **reference/section-semantics.md** for the full rubric.
</skill-file-section-semantics>

<trigger-correctness>
Criteria for description trigger clarity and `<when-to-use-this-skill>` consistency. Load **reference/trigger-correctness.md** for the full rubric.
</trigger-correctness>

<severity-levels>

| Level | Symbol | When to use |
|---|---|---|
| Blocker | 🚫 | The skill cannot be used in production as-is — it will fail to load, never activate, or produce incorrect output in all or most realistic scenarios |
| Major | 🔴 | A structural violation or coverage gap that causes the agent to behave incorrectly for at least one realistic scenario |
| Minor | 🟡 | A pattern deviation that reduces quality or maintainability but does not break the skill for the common case |
| Nit | 🟢 | Cosmetic or trivial issue — naming consistency, minor wording, style alignment |
| Inconsistency | ⚠️ | Two conflicting patterns that cannot be auto-resolved; present both variants and ask the user to decide |

**Blocker vs. Major**: Use 🚫 Blocker when the agent cannot complete the task at all in the normal case (e.g., no capability defined, frontmatter missing entirely, `<when-to-use-this-skill>` absent so the skill never self-confirms activation). Use 🔴 Major for violations that break the skill only in specific — but realistic — scenarios.

</severity-levels>

<skill-size-limit>
The SKILL.md under review should not exceed **150 lines** to keep context size manageable during review. Flag the file size as:

- **≤150 lines** — No flag (acceptable).
- **151–300 lines** — 🟡 Minor (excessive length; consider extracting more content to `reference/` files).
- **>300 lines** — 🔴 Major (must be refactored before a meaningful review; extract large rubrics and examples to `reference/` files).
</skill-size-limit>

<evaluation-process>
A well-structured skill should define an evaluation process to assess the quality of its own output. Look for:

- A dedicated validation or checklist step within a capability that lists criteria for verifying output correctness.
- A separate capability focused on evaluating or self-reviewing the skill's output.
- A reference file containing a quality checklist that the capability instructs the agent to load and apply.
- Explicit success criteria or pass/fail checks defined in the capability steps.

Common patterns:
- "Verify that [output] meets [criteria]" as a step.
- "Load **reference/quality-checklist.md** and apply each criterion".
- A dedicated `<validate-output>` capability with ordered validation steps.

Flag the absence of any evaluation mechanism as follows:
- No evaluation step in any capability → 🟡 Minor (output reliability depends entirely on agent discretion).
- No evaluation step AND no examples demonstrating output validation → 🔴 Major (no way to verify output correctness).
</evaluation-process>

<action-verb-naming-convention>
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
</action-verb-naming-convention>

<conciseness-check>
Criteria for identifying unnecessary content across SKILL.md, reference files, and example files. Load **reference/conciseness-check.md** for the full rubric.
</conciseness-check>

<platform-agnostic-writing>
Skills should be portable across AI platforms. Avoid platform-specific references:

- **No platform-specific tool names**: Replace tool names like `vscode_askQuestions` or `run_in_terminal` with generic action descriptions — e.g., "ask the user for confirmation" or "run the command"
- **No concrete context paths**: Describe persistent context targets by their type (personal persistent notes, project-level persistent notes, session-scoped context) rather than by concrete file paths like `/memories/` or `/memories/repo/`
- **Detect, don't assume**: When a capability needs to interact with platform features (context stores, tools, file structures), first detect what the platform supports, then map accordingly

Flag violations as:
- 🟡 Minor — A single platform-specific reference that doesn't break the skill
- 🔴 Major — Multiple platform-specific references that would prevent the skill from working on another platform
</platform-agnostic-writing>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Evaluating section structure, naming, or on-demand context placement (steps 1, 3–8) | Section-purpose table and common structural violations | [reference/section-semantics.md](reference/section-semantics.md) |
| Checking trigger clarity and description-to-when-to-use coverage (step 2) | Trigger-correctness criteria, trigger phrase rules, and common violations | [reference/trigger-correctness.md](reference/trigger-correctness.md) |
| Writing or evaluating the `description` field (step 2a) | Two-part description template with example | [reference/description-template.md](reference/description-template.md) |
| Scoring description quality (step 2b) | Five-dimension scoring rubric with pass/fail thresholds | [reference/description-scoring.md](reference/description-scoring.md) |
| Before writing review output — load first, every review | Canonical output format, severity label usage, multi-violation structure | [examples/skill-file-review.md](examples/skill-file-review.md) |
| You detect noun-named capabilities or inline-embedded examples | Output model for naming and inline-content findings | [examples/noun-capabilities-and-inline-examples.md](examples/noun-capabilities-and-inline-examples.md) |
| The skill appears mostly well-structured (few or no major findings) | Output model for a near-passing review | [examples/clean-skill-review.md](examples/clean-skill-review.md) |
| Trigger-correctness failures are the primary or dominant finding | Output model for a review focused on description/when-to-use mismatches | [examples/trigger-correctness-violation.md](examples/trigger-correctness-violation.md) |
| Executing step 10 (example coverage assessment) | Coverage gap criteria and severity table | [reference/example-coverage-criteria.md](reference/example-coverage-criteria.md) |
| Executing step 11 (individual example file review) | Quality criteria checklist for example files | [reference/example-quality-criteria.md](reference/example-quality-criteria.md) |
| Checking naming conventions for skill name and capability names (step 8) | Action-verb naming convention rules for skill name, capability names, and knowledge subsection names | See `<action-verb-naming-convention>` in `<knowledge>` |
| Checking file size and line count (step 1c) | Size limit thresholds (150/300 lines) and severity guidance | See `<skill-size-limit>` in `<knowledge>` |
| Checking for output evaluation process (step 4) | Evaluation process patterns, common checklist patterns, and severity guidance | See `<evaluation-process>` in `<knowledge>` |
| Checking conciseness across all files (step 5) | Unnecessary-content patterns per file type and severity guidance | [reference/conciseness-check.md](reference/conciseness-check.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<review-skill-file>
**Objective**: Evaluate a SKILL.md file for correct section structure, separation of concerns, and absence of duplication.

**Note**: Do not modify the skill file during review. Suggest changes with clear descriptions or patch-style snippets.

**Steps**:
1. Read the full skill file to understand its domain and all sections.
   a. Verify all expected top-level sections are present: frontmatter YAML, `<when-to-use-this-skill>`, `<knowledge>`, and `<capabilities>`; flag any missing required section as 🔴 Major.
   b. Verify sections appear in the correct order: frontmatter → `<when-to-use-this-skill>` → `<knowledge>` → `<capabilities>` → `<rules>` (if present); flag out-of-order sections as 🟡 Minor.
   c. Count the total lines of the SKILL.md file. If it exceeds 150 lines, flag as 🟡 Minor (excessive length consumes context during review — consider extracting content to `reference/` files). If it exceeds 300 lines, flag as 🔴 Major (file must be refactored before meaningful review).
2. **Check description quality and trigger consistency** — load **reference/trigger-correctness.md** first:
   a. Verify the frontmatter `description` follows the two-part template (domain summary + trigger phrase) — load **reference/description-template.md**; flag a missing trigger phrase as 🔴 Major.
   b. Score the description using the five-dimension quality metric — load **reference/description-scoring.md**; report the score (x/10) and flag a score ≤5 as 🔴 Major; flag a score of 6–8 as 🟡 Minor.
   c. Check that the intent verbs and key scenarios in the trigger phrase match the bullets in `<when-to-use-this-skill>` (bidirectional): flag any `<when-to-use-this-skill>` scenario whose keyword or intent verb is absent from `description` as 🟡 Minor (under-coverage); flag any trigger scenario in `description` absent from `<when-to-use-this-skill>` as 🟡 Minor (over-triggering or undocumented scope).
   d. If `<when-to-use-this-skill>` is missing entirely, flag as 🔴 Major.
   e. Flag any direct contradiction between the scope described in `description` and the bullets in `<when-to-use-this-skill>` as 🔴 Major.
3. For each capability section, verify it describes *how to do something* as ordered steps — flag any that are fact lists, reference tables, or constraint bullets (those belong in `<knowledge>`).
4. **Check for output evaluation process** — For each capability, verify it includes a validation or checklist step that evaluates the quality of the skill's output. Load `<evaluation-process>` in `<knowledge>` for guidance. If no capability contains any form of output evaluation, flag as 🟡 Minor. If the skill also lacks examples demonstrating output validation, flag as 🔴 Major.
5. **Check conciseness across all files** — Review SKILL.md, all reference files, and all example files for unnecessary or verbose content. Load `<conciseness-check>` in `<knowledge>` for guidance. Flag violations as:
    - 🟢 Nit for a single verbose file.
    - 🟡 Minor for systematic verbosity across multiple files.
    - 🔴 Major if the skill could be cut by >30% without losing meaning.
6. For each rule, verify it answers "when scenario X → use capability Y" — flag any rule that re-states content already in a capability (duplication). If the skill has only one capability and no `<rules>` section, do not flag its absence.
7. Check that a `<knowledge>` section exists and contains all reference material (tables, layouts, API signatures, platform constraints) that capabilities currently cite inline. Also check that large reference rubrics are not embedded directly in SKILL.md — they should be in `reference/` files loaded on demand; flag inline rubrics as 🔴 Major.
8. **Check naming conventions** — load `<action-verb-naming-convention>` in `<knowledge>` for the full rubric:
   a. Check the skill's frontmatter `name:` field follows the action-verb naming convention (imperative verb + noun in kebab-case, e.g., `edit-svg`, `validate-data`); flag noun-phrase names (e.g., `svg-editor`, `data-validator`) as 🔴 Major.
   b. Check each capability section name uses an action verb; flag noun-named sections as 🔴 Major.
   c. Verify that `<knowledge>` subsection names use descriptive noun phrases — a subsection named with an action verb (e.g., `<check-constraints>`) signals that procedural content has leaked into `<knowledge>`; flag as 🟡 Minor.
9. Check that on-demand context (examples, reference rubrics) is exposed via a `<context-loading-guide>` entry inside `<knowledge>` (preferred) rather than a standalone `<examples>` section. If a bare `<examples>` section exists instead, flag it as 🟡 Minor. If a `<context-loading-guide>` exists but uses a description-first **Scenario | Reference** format instead of a condition-first **Load when | Provides | File** format, flag it as 🟡 Minor — the first column must state the decision condition, not describe the file's content. If the guide is written as a bullet list, flag it as 🟡 Minor. Either way, verify that all referenced content is linked by file path — not embedded inline — and flag inline content as 🔴 Major.
10. Assess example coverage: cross-reference each named capability against the linked examples. Flag capabilities with no corresponding example as 🔴 Major; flag skills where examples cover only a subset of scenarios as 🟡 Minor. Load **reference/example-coverage-criteria.md** for the full rubric.
11. Load and review each linked example file:
    a. Verify the file has a clear scenario heading that names the trigger condition and the capability being demonstrated — flag missing or vague descriptions as 🟡 Minor.
    b. Verify the example output structure matches what the capability's steps would produce — flag structural drift as 🔴 Major.
    c. Check the scenario is realistic and non-trivial relative to the capability's complexity — flag toy/hello-world inputs for complex capabilities as 🟡 Minor.
    d. Check the example does not contradict any rule or knowledge entry in the parent skill — flag contradictions as 🔴 Major.
    e. Check that the example references the current capability name; flag stale names that no longer match the skill as 🟢 Nit.
    Load **reference/example-quality-criteria.md** for the full rubric.
12. Surface inconsistencies: mixed styles within a section type, two conflicting patterns, or differing levels of procedural detail across capabilities of the same kind. Present both variants with file/line references and ask the user which should be canonical — do not silently pick one.
13. Include a **Positive Highlights** section that acknowledges at least one well-structured aspect of the skill.
14. Include a **Risks & Assumptions** section that states any assumptions made about the intended skill format (e.g., four-section semantics) and notes that no runtime evaluation was performed.
15. Format findings with severity levels (🚫 Blocker, 🔴 Major, 🟡 Minor, 🟢 Nit, ⚠️ Inconsistency) and load **examples/skill-file-review.md** for output structure guidance.
16. Verify output completeness: every finding has a severity label, **Positive Highlights** and **Risks & Assumptions** sections are present, and all recommendations are actionable (not vague).
</review-skill-file>

</capabilities>

<rules>
<rule>When the user submits a SKILL.md file for review or asks to improve or fix a skill file, use **review-skill-file**.</rule>
<rule>When the user asks whether a skill will trigger or activate correctly, or whether its description matches its scenarios, use **review-skill-file** and focus on step 2 (trigger correctness).</rule>
</rules>
