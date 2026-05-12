# Trigger Correctness

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

