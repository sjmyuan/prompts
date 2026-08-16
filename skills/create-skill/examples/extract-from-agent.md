# Example: Extract an Existing Agent Prompt into a Skill

**Scenario**: The user provides an existing agent file (with inline knowledge, capabilities, and rules) and wants it converted to a SKILL.md. Requirements come from reading the source material — not from asking — and the source agent is later simplified to a delegation.

**Applies**: **collect-skill-requirements**, **create-skill-file**

## Input / Context
User provides `claude-agents/adr-writer.md` — a full agent with inline `<knowledge>`, capabilities, and rules — and asks: "Extract this into a skill."

## Source-Material Analysis (collect-skill-requirements step 3)
Read the file and map constructs to skill targets:

| Source construct | Skill target |
|---|---|
| `<knowledge>` subsections | knowledge section (extract large rubrics to `reference/`) |
| Inline capability steps | capabilities with action-verb names |
| `<rules>` | rules (when → capability routing) |

## Expected Output
`skills/<extracted-name>/SKILL.md` with the source content restructured into proper sections, plus a delegation agent file that calls the new skill.

Key moves:
- Rename capabilities to action verbs (e.g., `draft-adr` entries become `<define-problem>`, `<evaluate-options>`, etc.)
- Extract large rubrics (templates, scoring tables) to `reference/` files
- Add a condition-first `<context-loading-guide>`
- Keep the original agent as a thin delegation that applies the skill step by step
