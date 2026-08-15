---
name: review-skill
description: Review SKILL.md files for correct structure, section-purpose compliance, naming conventions, and duplication. Use when reviewing, fixing, improving, or checking trigger correctness of a copilot skill file.
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
Section-purpose table and common structural violations.
Details: [reference/section-semantics.md](reference/section-semantics.md)
</skill-file-section-semantics>

<trigger-correctness>
Criteria for description trigger clarity and `<when-to-use-this-skill>` consistency.
Details: [reference/trigger-correctness.md](reference/trigger-correctness.md)
</trigger-correctness>

<severity-levels>
Severity definitions and Blocker-vs-Major guidance.
Details: [reference/severity-levels.md](reference/severity-levels.md)
</severity-levels>

<size-limits>
Char/line budgets per file type, max-line-length guard, gaming detection, and the measurement script.
Details: [reference/size-limits.md](reference/size-limits.md)
</size-limits>

<size-remediation>
Ordered remediation for over-budget files — redistribute, reduce, escalate — plus anti-patterns to never suggest.
Details: [reference/size-remediation.md](reference/size-remediation.md)
</size-remediation>

<evaluation-process>
Patterns for a skill-defined output-evaluation process, plus severity when absent.
Details: [reference/evaluation-process.md](reference/evaluation-process.md)
</evaluation-process>

<action-verb-naming-convention>
Naming rules for the skill name, capability names, and knowledge subsection names.
Details: [reference/naming-conventions.md](reference/naming-conventions.md)
</action-verb-naming-convention>

<conciseness-check>
Criteria for identifying unnecessary content across SKILL.md, references, and examples.
Details: [reference/conciseness-check.md](reference/conciseness-check.md)
</conciseness-check>

<writing-style>
Prose-quality rules — directive voice, BLUF, hard caps, banned phrases, no narration.
Details: [reference/writing-style.md](reference/writing-style.md)
</writing-style>

<platform-agnostic-writing>
Portability rules — no platform tool names, no concrete context paths, detect-don't-assume.
Details: [reference/platform-agnostic-writing.md](reference/platform-agnostic-writing.md)
</platform-agnostic-writing>

<pipeline-integration-review>
4-point checklist for producer→consumer skill pipelines — handoff, shared schema, awareness, guard clauses.
Details: [reference/pipeline-integration.md](reference/pipeline-integration.md)
</pipeline-integration-review>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Before writing output — load first, every review | Output format | [examples/skill-file-review.md](examples/skill-file-review.md) |
| Noun-named capabilities or inline examples detected | Naming/inline model | [examples/noun-capabilities-and-inline-examples.md](examples/noun-capabilities-and-inline-examples.md) |
| Mostly well-structured skill (few or no major findings) | Near-passing model | [examples/clean-skill-review.md](examples/clean-skill-review.md) |
| Trigger failures dominant | Trigger-failure model | [examples/trigger-correctness-violation.md](examples/trigger-correctness-violation.md) |
| Size/density findings dominant | Size/gaming model | [examples/size-and-line-stuffing-review.md](examples/size-and-line-stuffing-review.md) |
| Writing-style findings dominant | Style model | [examples/writing-style-review.md](examples/writing-style-review.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<review-skill-file>
**Objective**: Evaluate a SKILL.md file for correct section structure, separation of concerns, and absence of duplication.

**Note**: Do not modify the skill file during review; suggest changes as descriptions or patch snippets.

**Steps**:
1. Read the full skill file to understand its domain and all sections — apply **reference/section-semantics.md** for the section-purpose table and violation list.
   a. Verify all expected top-level sections are present: frontmatter YAML, `<when-to-use-this-skill>`, `<knowledge>`, `<capabilities>`; flag any missing as 🔴 Major.
   b. Verify section order: frontmatter → `<when-to-use-this-skill>` → `<knowledge>` → `<capabilities>` → `<rules>` (if present); flag out-of-order as 🟡 Minor.
   c. Measure the file's size — run `scripts/measure_sizes.py` on the skill folder when available, else count lines and estimate chars.
   Apply **reference/size-limits.md** for budgets, line-length, line-stuffing, and gaming detection.
   When both budgets are exceeded, load **reference/size-remediation.md** and recommend fixes (redistribute → reduce → escalate); never suggest merging steps into one sentence (anti-pattern).
2. **Check description quality and trigger consistency** — load **reference/trigger-correctness.md** first:
   a. Verify the frontmatter `description` follows the two-part template (domain summary + trigger phrase) — load **reference/description-template.md**; flag a missing trigger phrase as 🔴 Major.
   b. Score the description using the five-dimension metric — load **reference/description-scoring.md**; report the score (x/10); flag ≤5 as 🔴 Major and 6–8 as 🟡 Minor.
   c. Check the trigger phrase's verbs and scenarios match the `<when-to-use-this-skill>` bullets; flag any term in one absent from the other as 🟡 Minor (under- or over-coverage).
   d. Flag a missing `<when-to-use-this-skill>` as 🔴 Major.
   e. Flag any direct contradiction between `description` scope and `<when-to-use-this-skill>` bullets as 🔴 Major.
3. For each capability, verify it describes *how to do something* as ordered steps — flag fact lists, reference tables, or constraint bullets (those belong in `<knowledge>`).
4. **Check output evaluation process** — Verify each capability includes a validation or checklist step.
   Load **reference/evaluation-process.md** for guidance. Flag no evaluation as 🟡 Minor; no evaluation AND no validation examples as 🔴 Major.
5. **Check conciseness and writing style** — Review SKILL.md, references, and examples for verbose content.
   Load **reference/conciseness-check.md** for severity flags; apply **reference/size-limits.md** budgets to each `reference/` file, and **reference/size-remediation.md** when over budget.
   a. **Check writing style** — Load **reference/writing-style.md**. Verify directive voice, BLUF, hard caps, no banned phrases, no narration. Flag per its severity table.
   b. **Check platform-agnostic writing** — Load **reference/platform-agnostic-writing.md**. Flag platform tool names or concrete context paths in the skill's own prose as 🟡 Minor.
6. For each rule, verify it answers "when scenario X → use capability Y" — flag rules re-stating capability content. If the skill has one capability and no `<rules>` section, do not flag its absence.
7. Check a `<knowledge>` section exists and holds reference material (tables, layouts, APIs, constraints). Flag rubrics embedded in SKILL.md instead of `reference/` files as 🔴 Major.
8. **Check naming conventions** — load **reference/naming-conventions.md** for the full rubric:
   a. Check the frontmatter `name:` follows the action-verb convention (e.g., `edit-svg`, not `svg-editor`); flag noun-phrase names as 🔴 Major.
   b. Check each capability section name uses an action verb; flag noun-named sections as 🔴 Major.
   c. Verify `<knowledge>` subsection names use descriptive noun phrases — an action-verb name (e.g., `<check-constraints>`) signals procedural content leaked into `<knowledge>`; flag as 🟡 Minor.
9. Check on-demand context (examples, rubrics) is exposed via a `<context-loading-guide>` inside `<knowledge>` (preferred), not a standalone `<examples>` section.
   Flag a bare `<examples>` section, a **Scenario | Reference** guide (not condition-first **Load when | Provides | File**), or a bullet-list guide as 🟡 Minor.
   Verify all referenced content is file-linked — not inline — and flag inline content as 🔴 Major.
10. Assess coverage: cross-reference capabilities against linked examples. Flag no-example capabilities as 🔴 Major; subset-only coverage as 🟡 Minor. Load **reference/example-coverage-criteria.md**.
11. Load and review each linked example file:
    a. Verify a clear scenario heading names the trigger condition and demonstrated capability — flag missing or vague as 🟡 Minor.
    b. Verify the example output structure matches what the capability's steps would produce — flag structural drift as 🔴 Major.
    c. Check the scenario is realistic and non-trivial — flag toy/hello-world inputs for complex capabilities as 🟡 Minor.
    d. Check the example does not contradict any rule or knowledge entry in the parent skill — flag contradictions as 🔴 Major.
    e. Check the example references the current capability name; flag stale names as 🟢 Nit.
    f. Apply the **reference/size-limits.md** example budget and max-line-length guard; flag overruns as 🟡 Minor and recommend remediation per **reference/size-remediation.md**.
    Load **reference/example-quality-criteria.md** for the full rubric.
12. Surface inconsistencies: mixed styles within a section type or differing procedural detail. Present both variants and ask the user which is canonical — do not silently pick one.
13. Include a **Positive Highlights** section that acknowledges at least one well-structured aspect of the skill.
14. Include a **Risks & Assumptions** section that states any assumptions made about the intended skill format (e.g., four-section semantics) and notes that no runtime evaluation was performed.
15. Format findings with severity levels (see **reference/severity-levels.md**) and load **examples/skill-file-review.md** for output structure guidance.
16. **Check pipeline integration**: If the skill references another skill, load **reference/pipeline-integration.md** and verify all 4 points. Flag gaps; skip if none referenced.
17. Verify output completeness: every finding has a severity label, **Positive Highlights** and **Risks & Assumptions** sections are present, and all recommendations are actionable (not vague).
</review-skill-file>

</capabilities>

<rules>
<rule>When the user submits a SKILL.md file for review or asks to improve or fix a skill file, use **review-skill-file**.</rule>
<rule>When the user asks whether a skill will trigger or activate correctly, or whether its description matches its scenarios, use **review-skill-file** and focus on step 2.</rule>
</rules>
