---
name: skill-reviewer
description: Review SKILL.md files for correct structure, section-purpose compliance, and absence of duplication. Evaluates whether knowledge, capabilities, rules, and examples sections each serve their intended purpose. Use when users request feedback, a quality assessment, or want to improve, fix, or ensure a copilot skill file triggers correctly.
---

<when-to-use-this-skill>
- User asks to review a skill file (SKILL.md)
- User asks to improve or fix a skill file (SKILL.md)
- User asks whether a SKILL.md is correctly structured
- User asks for feedback on section placement, duplication, or capability format in a skill file
- User asks whether a skill will trigger or activate correctly
</when-to-use-this-skill>

<knowledge>

<skill-file-section-semantics>
A well-formed copilot skill file uses these sections with distinct, non-overlapping purposes:

| Section | Purpose | What belongs here |
|---|---|---|
| Frontmatter `description:` | Skill-load decision | Plain-language summary used by VS Code/Copilot to decide whether to load this skill; must cover **all** activation scenarios |
| `<when-to-use-this-skill>` | Post-load scope check | Bullet list of user-facing scenarios that confirm this skill applies; must align with the frontmatter `description` |
| `<knowledge>` | Facts the agent recalls | Reference tables, directory layouts, API signatures, platform constraints, banned practices, selection guides; large rubrics extracted to `reference/` files and loaded on demand |
| `<capabilities>` | Procedures the agent executes | Ordered step-by-step instructions for *how* to accomplish a task; named with an action verb |
| `<rules>` | Internal routing triggers | "When [scenario] → use [capability]"; must not repeat what the capability already says; **may be omitted in single-capability skills** |
| `<context-loading-guide>` in `<knowledge>` | On-demand context router | Condition-first table (`Load when` \| `Provides` \| `File`) that states the exact condition under which each file (examples, references, rubrics) should be loaded; loaded on demand |

**Common structural violations**:
- Knowledge embedded in capabilities (lookup tables, API lists, constraint bullets inside a capability section)
- Rules that re-state capability content instead of routing to it
- Capabilities written as bullet-point fact lists instead of ordered procedural steps
- Capabilities named as nouns (`<storage-management>`) instead of action verbs (`<manage-storage>`)
- A bare `<examples>` section used instead of a `<context-loading-guide>` entry inside `<knowledge>` (the preferred pattern consolidates all on-demand context — examples, references, rubrics — in one place)
- `<context-loading-guide>` written as a bullet list, or as a two-column **Scenario | Reference** table — the first column must be a decision condition ("Load when…"), not a content description
- `<context-loading-guide>` first column describes *what the file contains* instead of *when to load it* — forces the agent to infer the loading condition, leading to missed or wrong loads
- `<examples>` content embedded inline rather than referenced by file path for on-demand loading
- Large reference rubrics embedded inline in SKILL.md instead of extracted to `reference/` files
</skill-file-section-semantics>

<trigger-correctness>
A skill fires correctly only when its external trigger (frontmatter `description`) and internal trigger (`<when-to-use-this-skill>`) are consistent and complete.

| Part | Location | Role |
|---|---|---|
| Frontmatter `description:` | YAML header | Used by VS Code/Copilot to decide whether to load this skill; must cover **all** scenarios in `<when-to-use-this-skill>` |
| `<when-to-use-this-skill>` | Top-level section | Granular bullet list read by the agent after the skill is loaded; confirms correct activation |

**Description trigger clarity criteria**:
- The `description` must explicitly state *when* the skill should be loaded — typically expressed as a "Use when…" or "Use for…" phrase at the end
- The `description` must include the primary intent verbs (e.g., review / fix / create / improve) that match the `<when-to-use-this-skill>` bullets
- The trigger phrase in `description` must cover **all** scenarios listed in `<when-to-use-this-skill>` (no under-coverage)
- The trigger phrase in `description` must not cover scenarios **absent** from `<when-to-use-this-skill>` (no over-triggering)

**Common trigger violations**:
- `description` has no explicit trigger phrase ("Use when…" clause missing) → VS Code/Copilot has no reliable signal to load the skill
- `description` covers only a subset of `<when-to-use-this-skill>` scenarios → skill silently fails to activate for uncovered scenarios
- `description` is so broad it fires for unrelated requests → skill is over-triggered
- `<when-to-use-this-skill>` entries are too vague (e.g., "User asks about X") without specifying the intent verb (review / fix / create / improve)
- `<when-to-use-this-skill>` is absent — the agent has no post-load scope check
- A scenario listed in `<when-to-use-this-skill>` has no corresponding keyword or verb phrase in `description`
- Trigger language in `description` contradicts or differs from `<when-to-use-this-skill>` scope (e.g., `description` says "fix" but `<when-to-use-this-skill>` only lists review scenarios)
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

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Before writing review output — load first, every review | Canonical output format, severity label usage, multi-violation structure | [examples/skill-file-review.md](examples/skill-file-review.md) |
| You detect noun-named capabilities or inline-embedded examples | Output model for naming and inline-content findings | [examples/noun-capabilities-and-inline-examples.md](examples/noun-capabilities-and-inline-examples.md) |
| The skill appears mostly well-structured (few or no major findings) | Output model for a near-passing review | [examples/clean-skill-review.md](examples/clean-skill-review.md) |
| Executing step 8 (example coverage assessment) | Coverage gap criteria and severity table | [reference/example-coverage-criteria.md](reference/example-coverage-criteria.md) |
| Executing step 9 (individual example file review) | Quality criteria checklist for example files | [reference/example-quality-criteria.md](reference/example-quality-criteria.md) |

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
2. **Check description trigger clarity and consistency**:
   a. Verify the frontmatter `description` contains an explicit trigger phrase (e.g., "Use when…" or "Use for…") that states when the skill should be loaded — flag a missing trigger phrase as 🔴 Major.
   b. Check that the intent verbs and key scenarios in the trigger phrase match the bullets in `<when-to-use-this-skill>` (bidirectional): flag any `<when-to-use-this-skill>` scenario whose keyword or intent verb is absent from `description` as 🟡 Minor (under-coverage); flag any trigger scenario in `description` absent from `<when-to-use-this-skill>` as 🟡 Minor (over-triggering or undocumented scope).
   c. If `<when-to-use-this-skill>` is missing entirely, flag as 🔴 Major.
   d. Flag any direct contradiction between the scope described in `description` and the bullets in `<when-to-use-this-skill>` as 🔴 Major.
   Consult **trigger-correctness** in `<knowledge>` for the full rubric.
3. For each capability section, verify it describes *how to do something* as ordered steps — flag any that are fact lists, reference tables, or constraint bullets (those belong in `<knowledge>`).
4. For each rule, verify it answers "when scenario X → use capability Y" — flag any rule that re-states content already in a capability (duplication). If the skill has only one capability and no `<rules>` section, do not flag its absence.
5. Check that a `<knowledge>` section exists and contains all reference material (tables, layouts, API signatures, platform constraints) that capabilities currently cite inline. Also check that large reference rubrics are not embedded directly in SKILL.md — they should be in `reference/` files loaded on demand; flag inline rubrics as 🔴 Major.
6. Check capability section names use action verbs; flag noun-named sections. Also verify that `<knowledge>` subsection names use descriptive noun phrases — a subsection named with an action verb (e.g., `<check-constraints>`) signals that procedural content has leaked into `<knowledge>`.
7. Check that on-demand context (examples, reference rubrics) is exposed via a `<context-loading-guide>` entry inside `<knowledge>` (preferred) rather than a standalone `<examples>` section. If a bare `<examples>` section exists instead, flag it as 🟡 Minor. If a `<context-loading-guide>` exists but uses a description-first **Scenario | Reference** format instead of a condition-first **Load when | Provides | File** format, flag it as 🟡 Minor — the first column must state the decision condition, not describe the file's content. If the guide is written as a bullet list, flag it as 🟡 Minor. Either way, verify that all referenced content is linked by file path — not embedded inline — and flag inline content as 🔴 Major.
8. Assess example coverage: cross-reference each named capability against the linked examples. Flag capabilities with no corresponding example as 🔴 Major; flag skills where examples cover only a subset of scenarios as 🟡 Minor. Load **reference/example-coverage-criteria.md** for the full rubric.
9. Load and review each linked example file:
    a. Verify the file has a clear scenario heading that names the trigger condition and the capability being demonstrated — flag missing or vague descriptions as 🟡 Minor.
    b. Verify the example output structure matches what the capability's steps would produce — flag structural drift as 🔴 Major.
    c. Check the scenario is realistic and non-trivial relative to the capability's complexity — flag toy/hello-world inputs for complex capabilities as 🟡 Minor.
    d. Check the example does not contradict any rule or knowledge entry in the parent skill — flag contradictions as 🔴 Major.
    e. Check that the example references the current capability name; flag stale names that no longer match the skill as 🟢 Nit.
    Load **reference/example-quality-criteria.md** for the full rubric.
10. Surface inconsistencies: mixed styles within a section type, two conflicting patterns, or differing levels of procedural detail across capabilities of the same kind. Present both variants with file/line references and ask the user which should be canonical — do not silently pick one.
11. Include a **Positive Highlights** section that acknowledges at least one well-structured aspect of the skill.
12. Include a **Risks & Assumptions** section that states any assumptions made about the intended skill format (e.g., four-section semantics) and notes that no runtime evaluation was performed.
13. Format findings with severity levels (🚫 Blocker, 🔴 Major, 🟡 Minor, 🟢 Nit, ⚠️ Inconsistency) and load **examples/skill-file-review.md** for output structure guidance.
</review-skill-file>

</capabilities>

<rules>
<rule>When the user submits a SKILL.md file for review or asks to improve or fix a skill file, use **review-skill-file**.</rule>
<rule>When the user asks whether a skill will trigger or activate correctly, or whether its description matches its scenarios, use **review-skill-file** and focus on step 2 (trigger correctness).</rule>
</rules>
