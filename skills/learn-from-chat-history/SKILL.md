---
name: learn-from-chat-history
description: Extract reusable knowledge, rules, and capabilities from chat sessions and provision them to persistent context. Use when distilling lessons, capturing feedback, preserving AI-discovered insights, or updating skills, agents, or memory.
---

<when-to-use-this-skill>
- User wants to extract and preserve reusable lessons from the current chat session
- User provided explicit feedback during the conversation that should become a permanent rule or knowledge entry
- AI discovered correct patterns, rules, or knowledge not found in existing context that should be saved
- User wants to update an existing skill, agent file, doc, or memory with insights from the conversation
- User wants to check if a conversation contains anything worth preserving for future sessions
</when-to-use-this-skill>

<knowledge>

<core-principle>
This skill treats lessons seriously. Not every interaction yields a lesson worth preserving. A valid lesson must be **general enough to apply across multiple future sessions**, not a one-off fix or trivial observation. When nothing meets the quality bar, the skill explicitly reports "nothing worth learning" — this is a valid and important outcome.
</core-principle>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Evaluating whether a candidate lesson is worth preserving | 5-dimension quality rubric (Reusability, Non-obviousness, Actionability, Non-duplication, Specificity) with scoring criteria and rejection thresholds | [reference/quality-rubric.md](reference/quality-rubric.md) |
| Determining which context target fits a lesson | Catalog of context targets (skills, agents, docs, memory scopes) with suitability criteria, format requirements, and examples for each | [reference/context-target-catalog.md](reference/context-target-catalog.md) |
| User gives explicit feedback that should become a rule | Walkthrough of detecting a user feedback signal, extracting the lesson, and provisioning it | [examples/user-feedback-to-rule.md](examples/user-feedback-to-rule.md) |
| AI independently discovered correct knowledge during the conversation | Walkthrough of detecting an AI-discovered insight, validating it, and provisioning it | [examples/ai-discovered-insight.md](examples/ai-discovered-insight.md) |
| User asks to learn from a session but nothing qualifies | Walkthrough of scanning a session, applying the quality gate, and reporting no lessons found | [examples/nothing-to-learn.md](examples/nothing-to-learn.md) |
| User specifies a target context for the lesson | Walkthrough of user-directed provisioning to a specific skill, agent, or memory file | [examples/user-specified-target.md](examples/user-specified-target.md) |

</context-loading-guide>

<signal-detection-knowledge>
Three signal types indicate a potential lesson:

**1. Explicit user feedback** — The user states a preference, rule, or correction:
- "Remember this for next time…"
- "Actually, the correct way is…"
- "From now on, always use X instead of Y…"
- "This is the pattern we follow…"
- User corrects the AI and the AI acknowledges the correction

**2. AI self-discovered insight** — The AI independently arrives at correct knowledge not in current context:
- AI reasons through a problem and discovers a correct approach that contradicts or extends existing context
- AI identifies a gap in knowledge and fills it through inference or external lookup
- AI synthesizes multiple pieces of information into a new, reusable rule
- The insight was NOT already in the loaded skills, agent files, memory, or docs

**3. Future-useful information** — Information surfaced that would benefit future sessions:
- A non-obvious workaround for a known limitation
- A project-specific convention discovered through trial and error
- A configuration detail that took significant effort to determine
- A dependency or compatibility constraint that isn't documented elsewhere

**Anti-signals** (do NOT treat these as lessons):
- Trivial facts any competent developer would know
- One-off fixes specific to a single line of code
- Information already documented in loaded context
- Session-specific state (e.g., "we're working on file X right now")
- Temporary workarounds that shouldn't be repeated
</signal-detection-knowledge>

<quality-gate-summary>
Every candidate lesson must pass a 5-dimension quality evaluation. Load [reference/quality-rubric.md](reference/quality-rubric.md) for the full rubric. Summary:

| Dimension | Reject if… |
|---|---|
| **Reusability** | Applies to only one specific scenario; won't generalize |
| **Non-obviousness** | Any competent practitioner would already know this |
| **Actionability** | Cannot be expressed as a concrete rule, fact, or step |
| **Non-duplication** | Already exists in current context (skills, memory, docs) |
| **Specificity** | Too vague to be useful OR too specific to be reusable |

A lesson must pass ALL five dimensions. If any dimension fails, reject the candidate lesson.
</quality-gate-summary>

</knowledge>

<capabilities>

<detect-learning-signals>
**Objective**: Scan the current chat session for candidate lessons, applying the quality gate to filter out noise.

**Steps**:
1. **Scan the conversation** for the three signal types defined in **signal-detection-knowledge**:
   - Explicit user feedback (corrections, preferences, "remember this" statements)
   - AI self-discovered insights (reasoning that produced correct knowledge not in context)
   - Future-useful information (hard-won configuration, non-obvious workarounds, undocumented constraints)

2. **Exclude anti-signals** immediately — trivial facts, one-off fixes, already-documented info, session state, temporary workarounds.

3. For each remaining candidate, **apply the quality gate**. Load [reference/quality-rubric.md](reference/quality-rubric.md) and score each dimension:
   - Reusability — Would this apply across multiple future sessions?
   - Non-obviousness — Would a competent practitioner already know this?
   - Actionability — Can it be expressed as a concrete rule/fact/step?
   - Non-duplication — Is it absent from all current context?
   - Specificity — Is it specific enough to be useful AND general enough to be reusable?

4. **If no candidates pass**: Report "No lessons worth learning from this session" and stop. This is a valid outcome — do not fabricate lessons.

5. **If candidates pass**: Collect them into a provisional list with the evidence (the conversation excerpt that triggered the signal) and proceed to **determine-provision-target**.
</detect-learning-signals>

<determine-provision-target>
**Objective**: For each qualifying lesson, identify the most appropriate persistent context to receive it.

**Steps**:
1. **Detect platform capabilities**: Identify what persistent context mechanisms are available (personal notes, project notes, skill files, agent files, documentation). Load [reference/context-target-catalog.md](reference/context-target-catalog.md) for guidance on target types and their suitability.

2. If the user **explicitly specified a target** (e.g., "add this to my coding assistant skill"), honor that target. Validate that it exists or can be created, and note this in the plan.

3. If the user did NOT specify a target, **classify each lesson** by its nature. Detect what persistent context mechanisms the current platform supports, then map accordingly:
   - **Personal preference / workflow rule** → personal persistent notes or preferences store (e.g., user-level configuration, global rules file)
   - **Project-specific convention or command** → project-level persistent notes or configuration (e.g., workspace rules, project conventions file)
   - **Domain knowledge for a skill** → the relevant skill definition file (e.g., `skills/*/SKILL.md`)
   - **Agent behavior rule** → the relevant agent or instruction file (e.g., `.agent.md`, `.instructions.md`, system prompt)
   - **Project documentation fact** → relevant project documentation (README, ADR, architecture doc)
   - **Task-specific temporary note** → session-scoped context (rare; prefer persistent targets)

4. For each classification, determine:
   - The **exact file path** to update
   - The **section** within that file where the lesson belongs
   - The **format** the lesson should take (rule, knowledge entry, capability step, etc.)

5. If a lesson could fit multiple targets, choose the **most specific and discoverable** one (e.g., a skill is more discoverable than personal notes; project-level notes are more scoped than personal notes).

6. Collect all target assignments and proceed to **generate-provision-plan**.
</determine-provision-target>

<generate-provision-plan>
**Objective**: Produce a concrete, reviewable plan showing exactly what will be added and where.

**Steps**:
1. For each lesson, draft the **exact content** to be added to the target context:
   - Write it in the format appropriate for the target (see [reference/context-target-catalog.md](reference/context-target-catalog.md) for format requirements)
   - Keep it concise — a few sentences for a rule, a bullet for a knowledge entry
   - Include the source evidence (conversation excerpt that triggered the signal)

2. Structure the plan as a clear table:

   | # | Lesson Summary | Signal Type | Target File | Section | Content to Add |
   |---|---------------|-------------|-------------|---------|----------------|
   | 1 | … | … | … | … | … |

3. For each entry, include a **rationale** sentence explaining why this target was chosen over alternatives.

4. If any target file does not yet exist, note that it will be created.

5. Present the complete plan to the user and proceed to **review-and-apply**.
</generate-provision-plan>

<review-and-apply>
**Objective**: Present the plan for user review, pause for confirmation, then apply approved changes.

**Steps**:
1. Present the plan from **generate-provision-plan** in full.

2. For each lesson, ask the user to:
   - **Approve** — proceed with the change
   - **Modify** — adjust the content, target, or format
   - **Reject** — skip this lesson entirely

3. **Do NOT apply any changes until the user explicitly confirms**. For multiple lessons, present them together and ask the user to approve, modify, or reject each one individually.

4. For approved lessons:
   - Read the target file to understand current structure
   - Insert the content into the correct section
   - If the target file doesn't exist, create it with proper structure
   - If the target is a skill file, ensure the content follows skill conventions (facts and references in the knowledge section, routing triggers in the rules section, procedural steps in the capabilities section)

5. For modified lessons:
   - Apply the user's adjustments to the content
   - Re-confirm before writing

6. After all changes are applied, summarize what was added and where.

7. **Important**: If the user rejects all lessons or no lessons passed the quality gate, acknowledge this explicitly — do not force a lesson.
</review-and-apply>

</capabilities>

<rules>

<rule>When the user asks to learn from a chat session, extract lessons, or preserve insights, first apply **detect-learning-signals** to scan the session and filter candidates through the quality gate.</rule>

<rule>If **detect-learning-signals** produces one or more qualifying lessons, apply **determine-provision-target** to identify where each lesson belongs.</rule>

<rule>After targets are determined, apply **generate-provision-plan** to produce the reviewable plan.</rule>

<rule>After the plan is generated, apply **review-and-apply** to present for user approval. Never apply changes without explicit user confirmation.</rule>

<rule>If no lessons pass the quality gate in **detect-learning-signals**, report "No lessons worth learning from this session" and stop. Do not proceed to downstream capabilities.</rule>

<rule>If the user specifies a target context explicitly (e.g., "add this to skill X"), honor that target in **determine-provision-target** step 2.</rule>

</rules>
