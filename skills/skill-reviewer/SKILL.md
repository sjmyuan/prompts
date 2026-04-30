---
name: skill-reviewer
description: Review SKILL.md files for correct structure, section-purpose compliance, and absence of duplication. Evaluates whether knowledge, capabilities, rules, and examples sections each serve their intended purpose. Use when users request feedback or a quality assessment on a copilot skill file.
---

<when-to-use-this-skill>
- User asks to review a skill file (SKILL.md)
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
| `<examples>` | Concrete output models | Realistic input/output pairs; loaded on demand, not inline |

**Common structural violations**:
- Knowledge embedded in capabilities (lookup tables, API lists, constraint bullets inside a capability section)
- Rules that re-state capability content instead of routing to it
- Capabilities written as bullet-point fact lists instead of ordered procedural steps
- Capabilities named as nouns (`<storage-management>`) instead of action verbs (`<manage-storage>`)
- `<examples>` loaded eagerly instead of referenced by name for on-demand loading
</skill-file-section-semantics>

<example-selector>
Load [examples/skill-file-review.md](examples/skill-file-review.md) for output structure guidance when formatting the review.
</example-selector>

</knowledge>

<capabilities>

<review-skill-file>
**Objective**: Evaluate a SKILL.md file for correct section structure, separation of concerns, and absence of duplication.

**Steps**:
1. Read the full skill file to understand its domain and all sections.
2. For each capability section, verify it describes *how to do something* as ordered steps — flag any that are fact lists, reference tables, or constraint bullets (those belong in `<knowledge>`).
3. For each rule, verify it answers "when scenario X → use capability Y" — flag any rule that re-states content already in a capability (duplication).
4. Check that a `<knowledge>` section exists and contains all reference material (tables, layouts, API signatures, platform constraints) that capabilities currently cite inline.
5. Check capability section names use action verbs; flag noun-named sections.
6. Check `<examples>` entries are referenced by file path for on-demand loading, not embedded inline.
7. Surface inconsistencies: mixed styles within a section type, two conflicting patterns, or differing levels of procedural detail across capabilities of the same kind. Present both variants with file/line references and ask the user which should be canonical — do not silently pick one.
8. Format findings with severity levels (🚫 Blocker, 🔴 Major, 🟡 Minor, 🟢 Nit, ⚠️ Inconsistency) and load **examples/skill-file-review.md** for output structure guidance.
</review-skill-file>

</capabilities>

<rules>
<rule>When the user submits a SKILL.md file for review, use **review-skill-file**. Evaluate section placement, duplication between rules and capabilities, and whether capabilities are procedural steps rather than fact lists. Consult **skill-file-section-semantics** for the criteria.</rule>
<rule>Do not modify the skill file directly during review. Suggest changes with clear descriptions or patch-style snippets.</rule>
<rule>Always include at least one positive highlight to acknowledge well-structured parts of the skill.</rule>
<rule>When two conflicting patterns or styles are found within the skill file, surface both under ⚠️ Inconsistencies, present trade-offs neutrally, and explicitly request a decision from the user.</rule>
</rules>
