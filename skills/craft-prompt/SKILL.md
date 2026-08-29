---
name: craft-prompt
description: Craft and refine prompts and agent files for copilot, claude, or opencode by applying the SKR framework. Use when creating, refining, or improving a prompt, agent, or persona definition.
---

<when-to-use-this-skill>
- User asks to create a new prompt from scratch
- User asks to refine or improve an existing prompt
- User asks to create an agent file for copilot, claude, or opencode
- User asks to create an agent file that delegates to referenced skills
- User asks to refine an existing agent file to remove duplication
- Do NOT load for general writing or coding — use the domain agent instead
</when-to-use-this-skill>

<knowledge>

<skr-framework>
The SKR framework structures prompts into three sections: knowledge (facts), skills (procedures), rules (routing).

| Section | Purpose |
|---|---|
| Knowledge | Background facts, examples, and context the AI needs |
| Skills | Named reusable capabilities with step-by-step instructions |
| Rules | Decision criteria: "When [condition], apply **skill-name** to [purpose]." |
</skr-framework>

<skr-prompt-template>
The canonical SKR prompt opens with a role statement, then knowledge, skills, and rules sections. Full template and fill rules: **reference/skr-prompt-template.md**.
</skr-prompt-template>

<agent-file-formats>
Copilot, Claude, and opencode agent files share a SKR body but differ in frontmatter fields, file suffix, and tool declarations. Per-platform frontmatter and tool schemas: **reference/agent-file-formats.md**.
</agent-file-formats>

<agent-file-frontmatter>
Agent files start with YAML frontmatter; the required fields vary by platform. `description` is always required; `name`, `tools`, `mode`, and `permission` are platform-specific.
</agent-file-frontmatter>

<agent-file-best-practices>
Agent files that delegate to referenced skills contain only wrapper-layer content.

| Layer | Contains |
|---|---|
| Agent wrapper | Agent scope, tool restrictions, delegation rules, behavior constraints |
| Referenced skill | Domain knowledge, procedural capability steps, domain routing rules |
</agent-file-best-practices>

<agent-file-rules-vs-capabilities>
Rules route "when to act"; capabilities define "how to act". Never conflate them. Patterns: **reference/rules-vs-capabilities.md**.
</agent-file-rules-vs-capabilities>
<prompt-writing-style>
Generated prompts and agent files use directive voice, BLUF, hard caps, atomic bullets, and the SKR section conventions. Full style rules and wrapper pattern: **reference/prompt-writing-style.md**.
</prompt-writing-style>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Filling the final prompt structure | SKR template with placeholder guidance | [reference/skr-prompt-template.md](reference/skr-prompt-template.md) |
| Writing frontmatter for a target platform | Copilot/claude/opencode frontmatter and tool schemas | [reference/agent-file-formats.md](reference/agent-file-formats.md) |
| Deciding whether content is a rule or a capability | Violation and correct patterns | [reference/rules-vs-capabilities.md](reference/rules-vs-capabilities.md) |
| Writing the prompt or agent-file body | Style rules, hard caps, banned phrases, wrapper pattern | [reference/prompt-writing-style.md](reference/prompt-writing-style.md) |
| Creating a prompt from scratch | Walkthrough of collect, identify, define, assemble | [examples/create-prompt-from-scratch.md](examples/create-prompt-from-scratch.md) |
| Refining an existing prompt | Walkthrough of gap analysis and refill | [examples/refine-existing-prompt.md](examples/refine-existing-prompt.md) |
| Crafting an agent file for a platform | Walkthrough of platform detection and wrapper assembly | [examples/craft-agent-file.md](examples/craft-agent-file.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<collect-prompt-knowledge>
**Objective**: Gather what the prompt's AI needs to know.
1. Ask targeted questions about the prompt's purpose, target audience, and desired outcomes.
2. Identify the background facts, domain constraints, examples, and context to encode.
3. Summarize the collected knowledge; present it for confirmation.
4. Verify the summary covers purpose, audience, and outcomes.
</collect-prompt-knowledge>

<identify-prompt-skills>
**Objective**: Define the named capabilities the prompt's AI persona needs.
1. Derive the tasks the persona must perform from the confirmed knowledge.
2. Define each task as a skill with a clear name and step-by-step instructions.
3. Present the skills for confirmation and refinement.
4. Verify each skill has a name and concrete steps.
</identify-prompt-skills>

<define-prompt-rules>
**Objective**: Establish when each skill applies.
1. State each rule as "When [condition], apply **skill-name** to [purpose]."
2. Present the rules for confirmation.
3. Verify every defined skill is referenced by at least one rule.
</define-prompt-rules>

<assemble-prompt>
**Objective**: Deliver the final prompt in the canonical SKR format.
1. Fill the SKR template from **reference/skr-prompt-template.md** with the confirmed sections.
2. Write a role statement defining the AI's persona and task.
3. Write each section per **reference/prompt-writing-style.md** — directive voice, atomic bullets, no banned phrases.
4. Present the complete prompt in a fenced markdown code block.
5. Ask which section needs adjustment.
6. Verify the output matches the template structure and the style rules.
</assemble-prompt>

<refine-prompt>
**Objective**: Improve an existing prompt by closing its gaps.
1. Analyze the prompt for gaps: missing role, vague knowledge, undefined skills, or absent rules.
2. Identify the weak or absent sections; explain what is missing.
3. Apply **collect-prompt-knowledge**, **identify-prompt-skills**, and **define-prompt-rules** to fill the gaps.
4. Reassemble the refined prompt with **assemble-prompt**.
5. Verify each gap is filled and no new gaps are introduced.
</refine-prompt>

<craft-agent-file>
**Objective**: Produce a platform-ready agent file that delegates to skills without duplication.
1. Detect the target platform: copilot, claude, or opencode; ask if unspecified.
2. Load the platform's frontmatter and tool schema from **reference/agent-file-formats.md**.
3. Match tools to the agent's tasks per the platform schema.
4. Read each referenced skill file first to learn what it covers.
5. Assemble the frontmatter per the platform format.
6. Write the body with agent scope, delegation rules, and behavior constraints only, following the wrapper pattern from **reference/prompt-writing-style.md**.
7. Never duplicate the referenced skill's content.
8. Present the agent file in a fenced markdown code block.
9. Ask which section needs adjustment.
10. Verify the file matches the platform's frontmatter, follows the style rules, and contains no duplicated skill content.
</craft-agent-file>

</capabilities>

<rules>
<rule>When the user asks for a new prompt from scratch, use **collect-prompt-knowledge**.</rule>
<rule>When the user provides an existing prompt to improve, use **refine-prompt**.</rule>
<rule>After knowledge is confirmed, use **identify-prompt-skills**.</rule>
<rule>After skills are confirmed, use **define-prompt-rules**.</rule>
<rule>After rules are confirmed, use **assemble-prompt**.</rule>
<rule>When the user asks for an agent file for copilot, claude, or opencode, use **craft-agent-file** with the matching format from **reference/agent-file-formats.md**.</rule>
<rule>When the user asks for an agent file with skill references, first use **collect-prompt-knowledge**, **identify-prompt-skills**, and **define-prompt-rules**, then **craft-agent-file**.</rule>
<rule>When refining an agent file that delegates to a skill, read the skill first and strip duplication from the wrapper.</rule>
</rules>
