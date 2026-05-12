# Skill File Section Semantics

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
