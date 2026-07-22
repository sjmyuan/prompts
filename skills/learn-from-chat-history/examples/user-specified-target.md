# Example: User-Specified Target

**Applies**: `detect-learning-signals` → `determine-provision-target` (user-directed) → `generate-provision-plan` → `review-and-apply`

**Scenario**: User provides a rule and explicitly says where it should go — in this case, into a specific agent's instructions file.

---

## Input (Conversation Excerpt)

```
User: When I ask this coding assistant to create files, it should always confirm with
      me before writing anything to the src/ directory. Add that to the coding-assistant
      agent instructions.

AI: Got it. I'll note that for the review.

[Later]

User: Now learn from this session.
```

---

## Step 1: detect-learning-signals

**Signal detected**: Explicit user feedback with target specification — user stated a rule ("always confirm before writing to src/") AND specified the target ("coding-assistant agent instructions").

**Signal type**: Explicit user feedback (with target specified)

**Quality gate evaluation**:

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Applies to every file creation in src/ across all future sessions |
| Non-obviousness | ✅ Pass | The default behavior may be to write without confirmation; this is a specific preference |
| Actionability | ✅ Pass | Clear directive: "confirm before creating files in src/" |
| Non-duplication | ✅ Pass | Not in the current coding-assistant agent instructions |
| Specificity | ✅ Pass | Specific: "src/ directory, file creation"; general: applies to all future sessions |

**Verdict**: ACCEPT.

---

## Step 2: determine-provision-target

**User specified target**: "coding-assistant agent instructions"

**Resolve target**: Look for agent files matching "coding-assistant":
- Found: `prompts/copilot-agents/coding-assistant.agent.md`
- Or: `prompts/copilot-agents/coding-assistant.md`

**Validate target**: The file exists. It has a `<rules>` section. The rule belongs there.

**Target confirmed**: `prompts/copilot-agents/coding-assistant.agent.md` → `<rules>` section.

---

## Step 3: generate-provision-plan

| # | Lesson Summary | Signal Type | Target File | Section | Content to Add |
|---|---|---|---|---|---|
| 1 | Confirm with user before creating files in `src/` | User feedback (target specified) | `prompts/copilot-agents/coding-assistant.agent.md` | `<rules>` | `<rule>When creating or modifying files in the `src/` directory, always ask the user for confirmation before writing.</rule>` |

**Rationale**: User explicitly directed this rule to the coding-assistant agent. No classification needed — user intent is clear.

---

## Step 4: review-and-apply

Present to user:

> **Lesson to preserve:**
>
> *Confirm with user before creating files in `src/`.*
>
> **Target** (user-specified): `prompts/copilot-agents/coding-assistant.agent.md` → `<rules>`
>
> **Content to add**:
> ```markdown
> <rule>When creating or modifying files in the `src/` directory, always ask the user for confirmation before writing.</rule>
> ```
>
> Approve / Modify / Reject?

User approves → write to the agent file.
