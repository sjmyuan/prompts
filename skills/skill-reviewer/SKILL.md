---
name: skill-reviewer
description: Review SKILL.md files for correct structure, section-purpose compliance, and absence of duplication. Evaluates whether knowledge, capabilities, rules, and examples sections each serve their intended purpose. Use when users request feedback or a quality assessment on a copilot skill file.
---

<when-to-use-this-skill>
- User asks to review a skill file (SKILL.md)
- User asks to improve or fix a skill file (SKILL.md)
- User asks whether a SKILL.md is correctly structured
- User asks for feedback on section placement, duplication, or capability format in a skill file
</when-to-use-this-skill>

<knowledge>

<skill-file-section-semantics>
A well-formed copilot skill file uses four sections with distinct, non-overlapping purposes:

| Section | Purpose | What belongs here |
|---|---|---|
| `<knowledge>` | Facts the agent recalls | Reference tables, directory layouts, API signatures, platform constraints, banned practices, selection guides |
| `<capabilities>` | Procedures the agent executes | Ordered step-by-step instructions for *how* to accomplish a task; named with an action verb |
| `<rules>` | Routing triggers | "When [scenario] → use [capability]"; must not repeat what the capability already says |
| `<example-selector>` in `<knowledge>` | Example routing guide | Named file references with one-line scenario descriptions; loaded on demand |

**Common structural violations**:
- Knowledge embedded in capabilities (lookup tables, API lists, constraint bullets inside a capability section)
- Rules that re-state capability content instead of routing to it
- Capabilities written as bullet-point fact lists instead of ordered procedural steps
- Capabilities named as nouns (`<storage-management>`) instead of action verbs (`<manage-storage>`)
- A bare `<examples>` section used instead of an `<example-selector>` entry inside `<knowledge>` (the preferred pattern keeps all lookup material in one place)
- `<examples>` content embedded inline rather than referenced by file path for on-demand loading
</skill-file-section-semantics>

<example-coverage-criteria>
A well-covered examples section spans the skill's key scenarios. Check for these gaps:

| Gap | Severity |
|---|---|
| A named capability has no corresponding example | 🔴 Major — agent has no output model for that workflow |
| Examples cover only simple/happy-path inputs | 🟡 Minor — edge cases are unguided |
| Example count is fewer than distinct capabilities | 🟡 Minor — at least one scenario is unrepresented |
| Example labels reference outdated or renamed capabilities | 🟢 Nit — drift between names |

**Minimum viable coverage**: every distinct capability (or meaningfully different scenario variant) should have at least one linked example.
</example-coverage-criteria>

<example-quality-criteria>
An example file is well-formed when it meets all of the following criteria:

| Criterion | What to check |
|---|---|
| Clear scenario heading | States the skill domain, the trigger condition, and what makes this case distinct from other examples |
| Realistic, non-trivial input | Representative of actual user requests — not a toy or hello-world scenario |
| Output matches capability steps | The structure and content of the output follow the steps of the capability it demonstrates |
| Traceable to a named capability | A reader can identify which capability produced this output |
| No contradictions with the parent skill | The example output does not violate any rule or knowledge entry in the same skill |

**Common example quality violations**:
- Output structure does not match the steps in the corresponding capability (structural drift)
- Scenario is trivially simple for a capability designed to handle complex cases
- Scenario description is missing or vague — the reader cannot tell which trigger condition is being demonstrated
- Example output contradicts a rule or knowledge constraint in the parent skill
- Example was written for an older version of the skill and references renamed or removed capabilities
</example-quality-criteria>

<example-selector>
- Load [examples/skill-file-review.md](examples/skill-file-review.md) for output structure guidance and a complex multi-violation review.
- Load [examples/noun-capabilities-and-inline-examples.md](examples/noun-capabilities-and-inline-examples.md) for a review featuring noun-named capabilities, inline-embedded examples, and a coverage gap finding.
- Load [examples/clean-skill-review.md](examples/clean-skill-review.md) for a near-passing review showing what a well-structured skill looks like with only minor nits.
</example-selector>

</knowledge>

<capabilities>

<review-skill-file>
**Objective**: Evaluate a SKILL.md file for correct section structure, separation of concerns, and absence of duplication.

**Note**: Do not modify the skill file during review. Suggest changes with clear descriptions or patch-style snippets.

**Steps**:
1. Read the full skill file to understand its domain and all sections.
2. For each capability section, verify it describes *how to do something* as ordered steps — flag any that are fact lists, reference tables, or constraint bullets (those belong in `<knowledge>`).
3. For each rule, verify it answers "when scenario X → use capability Y" — flag any rule that re-states content already in a capability (duplication).
4. Check that a `<knowledge>` section exists and contains all reference material (tables, layouts, API signatures, platform constraints) that capabilities currently cite inline.
5. Check capability section names use action verbs; flag noun-named sections.
6. Check that examples are exposed via an `<example-selector>` entry inside `<knowledge>` (preferred) rather than a standalone `<examples>` section. If a bare `<examples>` section exists instead, flag it as 🟡 Minor. Either way, verify that example content is referenced by file path — not embedded inline — and flag inline content as 🔴 Major.
7. Assess example coverage: cross-reference each named capability against the linked examples. Flag capabilities with no corresponding example as 🔴 Major; flag skills where examples cover only a subset of scenarios as 🟡 Minor. Consult **example-coverage-criteria** for the full rubric.
8. Load and review each linked example file:
    a. Verify the file has a clear scenario heading that names the trigger condition and the capability being demonstrated — flag missing or vague descriptions as 🟡 Minor.
    b. Verify the example output structure matches what the capability's steps would produce — flag structural drift as 🔴 Major.
    c. Check the scenario is realistic and non-trivial relative to the capability's complexity — flag toy/hello-world inputs for complex capabilities as 🟡 Minor.
    d. Check the example does not contradict any rule or knowledge entry in the parent skill — flag contradictions as 🔴 Major.
    e. Check that the example references the current capability name; flag stale names that no longer match the skill as 🟢 Nit.
    Consult **example-quality-criteria** for the full rubric.
9. Surface inconsistencies: mixed styles within a section type, two conflicting patterns, or differing levels of procedural detail across capabilities of the same kind. Present both variants with file/line references and ask the user which should be canonical — do not silently pick one.
10. Include a **Positive Highlights** section that acknowledges at least one well-structured aspect of the skill.
11. Include a **Risks & Assumptions** section that states any assumptions made about the intended skill format (e.g., four-section semantics) and notes that no runtime evaluation was performed.
12. Format findings with severity levels (🚫 Blocker, 🔴 Major, 🟡 Minor, 🟢 Nit, ⚠️ Inconsistency) and load **examples/skill-file-review.md** for output structure guidance.
</review-skill-file>

</capabilities>

<rules>
<rule>When the user submits a SKILL.md file for review or asks to improve a skill file, use **review-skill-file**.</rule>
<rule>When two or more conflicting patterns or styles are found within the skill file, use **review-skill-file** and surface them under ⚠️ Inconsistencies.</rule>
</rules>
