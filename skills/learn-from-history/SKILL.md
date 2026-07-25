---
name: learn-from-history
description: Extract reusable knowledge, rules, and procedures from chat sessions, PRs, git history, and team transcripts, then provision to persistent context. Orchestrates sub-agents for parallel analysis when suitable agents are available. Use when distilling lessons, analyzing change history, mining chat for tribal knowledge, extracting procedures, checking for reusable insights, or refining skills/agents/memory.
---

<when-to-use-this-skill>
- User wants to extract and preserve reusable lessons from the current chat session
- User provided explicit feedback during the conversation that should become a permanent rule or knowledge entry
- AI discovered correct patterns, rules, or knowledge not found in existing context that should be saved
- User provides a user story with PR(s) and wants to extract reusable patterns, constraints, or architectural decisions from the implementation
- User provides git commit history and wants to identify recurring patterns, convention evolution, or lessons from code changes
- User wants to update an existing skill, agent file, doc, or memory with insights from any historical source
- User provides chat history from Slack, Teams, Discord, or similar tools and wants to extract team knowledge, decisions, or problem-solution patterns
- User wants to check whether a conversation, PR, code history, or chat transcript contains anything worth preserving for future work
- User wants to extract step-by-step procedures or "how-to" knowledge — the concrete steps the team follows for recurring tasks
- User provides one or more PRs for similar task types and wants to distill the common implementation recipe
- User wants to refine and generalize an existing capability with newly discovered procedural knowledge
</when-to-use-this-skill>

<knowledge>

<core-principle>
This skill treats lessons seriously. Not every interaction or change yields a lesson worth preserving. A valid lesson must be **general enough to apply across multiple future sessions**, not a one-off fix or trivial observation. When nothing meets the quality bar, the skill explicitly reports "nothing worth learning" — this is a valid and important outcome.
</core-principle>

<agent-orchestration>
When the platform supports sub-agents (specialized agents that can be invoked for subtasks), this skill orchestrates them to parallelize the learning pipeline. The parent skill always retains control of the quality gate, result merging, de-duplication, and provisioning — sub-agents handle only the analysis phase.

**Agent detection**: Before starting analysis, scan the available agent registry. Look for agents whose descriptions indicate code analysis, investigation, review, communication mining, or pattern extraction capabilities. Record each agent's name, description, and any tool restrictions.

**Task-to-agent mapping**:

| Source type | Agent type needed | Agent description keywords | Fallback capability |
|---|---|---|---|
| PR(s) + user story | Code investigator / reviewer | "investigate", "review", "analyze code", "explore codebase", "discover patterns" | analyze-code-changes |
| Git commit history | Code investigator / explorer | "investigate", "explore", "analyze history", "discover patterns", "codebase exploration" | analyze-code-changes |
| Communication transcripts | Text analyst / researcher | "analyze text", "mine", "extract knowledge", "research", "chat analysis" | analyze-communication-history |
| Mixed / complex sources | Multiple agents (parallel) | Above keywords, distributed across agents | Sequential internal analysis |

**Parallelization strategy**: When multiple independent source types are present (e.g., PRs + git history + chat transcripts), dispatch each to a different agent simultaneously. Agents are stateless and independent — they can run in parallel without coordination. The parent collects all results after all agents complete.

**Agent prompt structure**: For each dispatched agent, construct a prompt that:
1. States the source type and what signal types to look for (reference the signal detection catalog's categories: story-implementation gaps, evolutionary patterns, recurring questions, decision records, problem-solution pairs, procedural patterns, implementation recipes)
2. Provides the full source material (PR diff, commit range, transcript, etc.)
3. Asks for structured output: a list of candidate lessons, each with a summary, evidence excerpt from the source, the signal type it matches, and a preliminary quality self-assessment (reusable? non-obvious? actionable? not already documented elsewhere?)
4. Instructs the agent to be conservative — flag borderline candidates rather than missing them; the parent applies the formal quality gate later
5. Explicitly instructs: "Return only findings as structured text. Do NOT write to any files, do NOT modify any documents, and do NOT provision any lessons."

**Result collection and merging**: After all agents return:
1. Collect all candidate lessons into a single pool
2. De-duplicate across agent results — the same lesson discovered from different sources should be merged, not duplicated
3. Merge complementary findings — one agent may find the pattern, another may find the rationale or a different angle on the same underlying lesson
4. Tag each candidate with its source agent for traceability in the provision plan

**Fallback**: If no suitable agents are detected, or if agent invocation fails (timeout, error, empty result), fall back to the internal capabilities (analyze-code-changes, analyze-communication-history) running sequentially. The quality gate, capability extraction, and provisioning steps are identical in both paths — only the analysis phase differs.

**When NOT to use agents**: 
- Single, small source (one short chat session) — agent dispatch overhead exceeds benefit; scan interactively
- Sources that require tight cross-referencing (e.g., comparing a story against its PR requires seeing both together) — use a single agent that receives all inputs, or fall back to internal analysis
- User explicitly requests sequential, step-by-step processing with visibility into each step
</agent-orchestration>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Evaluating whether a candidate lesson is worth preserving | 5-dimension quality rubric with scoring criteria and rejection thresholds | [reference/quality-rubric.md](reference/quality-rubric.md) |
| Determining which context target fits a lesson | Catalog of context targets with suitability criteria and format requirements | [reference/context-target-catalog.md](reference/context-target-catalog.md) |
| Scanning a chat session or historical source for learning signals | Complete catalog of signal types with triggers, examples, and anti-signals | [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) |
| Comparing a user story against its PR implementation | Analysis lens framework with comparison dimensions and signal-strength ratings | [reference/story-analysis-framework.md](reference/story-analysis-framework.md) |
| User gives explicit feedback that should become a rule | Walkthrough: detecting user feedback → extracting lesson → provisioning | [examples/user-feedback-to-rule.md](examples/user-feedback-to-rule.md) |
| AI independently discovered correct knowledge during the conversation | Walkthrough: detecting AI-discovered insight → validating → provisioning | [examples/ai-discovered-insight.md](examples/ai-discovered-insight.md) |
| User asks to learn from a session but nothing qualifies | Walkthrough: scanning session → applying quality gate → reporting no lessons | [examples/nothing-to-learn.md](examples/nothing-to-learn.md) |
| User specifies a target context for the lesson | Walkthrough of user-directed provisioning to a specific target | [examples/user-specified-target.md](examples/user-specified-target.md) |
| User provides a user story and PR(s) to learn from | Walkthrough: comparing story vs implementation → identifying gaps → extracting knowledge | [examples/pr-story-gap-discovery.md](examples/pr-story-gap-discovery.md) |
| User provides git commit history to learn from | Walkthrough: mining commit history for patterns, convention evolution, and lessons | [examples/git-history-pattern.md](examples/git-history-pattern.md) |
| Extracting a step-by-step procedure from conversation or chat history | Walkthrough: detecting procedural signal → extracting steps → provisioning as capability | [examples/procedural-discovery.md](examples/procedural-discovery.md) |
| Distilling an implementation recipe from one or more PRs | Walkthrough: detecting recipe signal → extracting pattern → abstracting into capability | [examples/implementation-recipe.md](examples/implementation-recipe.md) |
| Applying quality checks to an extracted capability | 4-dimension checklist with rejection rules and confidence guidance | [reference/capability-quality-checklist.md](reference/capability-quality-checklist.md) |
| Formatting an extracted or abstracted capability for provisioning | Structured template with required fields and refined-capability extensions | [reference/capability-format-template.md](reference/capability-format-template.md) |
| Orchestrating multiple sub-agents for parallel analysis | Prompt templates per agent type, result format spec, merging/de-duplication algorithms, error handling | [reference/agent-orchestration-pattern.md](reference/agent-orchestration-pattern.md) |

</context-loading-guide>

<signal-types>
Signal types span multiple source categories. Each has specific triggers and anti-signals — load the full catalog from [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) when scanning for signals.

Quick reference:
- **Interactive** (chat): explicit user feedback, AI self-discovered insight, future-useful information
- **Code-change** (PRs, git): story-implementation gap, evolutionary pattern, implementation recipe
- **Communication tool** (Slack, Teams, Discord): recurring question, decision record, problem-solution pair, knowledge sharing, escalation pattern, onboarding gap
- **Procedural** (any source): step-by-step descriptions of recurring tasks, including repos/components to touch and change patterns
- **Anti-signals**: trivial facts, one-off fixes, already-documented info, session state, boilerplate changes, casual chat, resolved-once issues
</signal-types>

<quality-gate>
Every candidate lesson must pass all five dimensions in the quality rubric. Load [reference/quality-rubric.md](reference/quality-rubric.md) for the full rubric with scoring criteria, rejection rules, and decision matrix. A single failure rejects the candidate.
</quality-gate>

<story-analysis>
When comparing a user story against PR implementation changes, load [reference/story-analysis-framework.md](reference/story-analysis-framework.md) for the full comparison framework with eight analysis lenses, signal strength ratings, and guidance on which rows produce the strongest lessons.
</story-analysis>

</knowledge>

<capabilities>

<detect-learning-signals>
**Objective**: Master entry point — detect sub-agents, scan any historical source for candidate lessons, delegate to agents or internal analysis, apply the quality gate, and route qualifying lessons to provisioning.
**Steps**:
0. **Detect available sub-agents**: Scan the platform's agent registry for agents suitable for analysis tasks. Look for agents whose descriptions match the keywords in the task-to-agent mapping table (see agent-orchestration knowledge). Record available agent names and their capabilities. If no suitable agents are found, proceed with internal capabilities only.

1. **Identify the source type and choose execution mode**:
   - **Single, small chat session** → proceed to step 3 (scan interactively — agent overhead not justified for small sessions)
   - **PR(s) + user story** → if a suitable code investigator/reviewer agent was detected in step 0, dispatch to it (see step 2); otherwise delegate to **analyze-code-changes**
   - **Git commit history** → if a suitable code investigator/explorer agent was detected, dispatch to it; otherwise delegate to **analyze-code-changes**
   - **Communication tool transcripts** → if a suitable text analyst/researcher agent was detected, dispatch to it; otherwise delegate to **analyze-communication-history**
   - **Mixed sources (multiple independent source types)** → dispatch each source type to a different agent in parallel if available; otherwise process each path sequentially with internal capabilities
   - **Sources requiring cross-referencing** (e.g., story + its PR) → dispatch to a single agent with ALL inputs, or fall back to internal analysis

2. **Dispatch to agents** (when agents are available): For each agent to invoke, load [reference/agent-orchestration-pattern.md](reference/agent-orchestration-pattern.md) and construct a prompt following the prompt template for that agent type. Include: the source material, signal types to look for, structured output requirements, and the instruction to NOT write files. Dispatch all independent agents in parallel. Wait for all agents to complete, then collect results. Merge by de-duplicating across agent outputs and combining complementary findings. Tag each candidate with its source agent. Proceed to step 4.

3. For chat sessions without agent dispatch, load [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) and **scan the conversation** for signal types: explicit user feedback, AI self-discovered insights, future-useful information, and procedural patterns (step-by-step task descriptions).

4. **Exclude anti-signals** immediately — filter out trivial facts, one-off fixes, already-documented info, session state, boilerplate changes. For agent-produced candidates, apply a lighter pre-filter since agents were already instructed to be conservative.

5. For each remaining candidate, **apply the quality gate**. Load [reference/quality-rubric.md](reference/quality-rubric.md) and score all five dimensions: Reusability, Non-obviousness, Actionability, Non-duplication, Specificity.

6. **If no candidates pass**: Report "No lessons worth learning from this [source]" and stop. This is a valid outcome — do not fabricate lessons.

7. **If candidates pass**: Collect them with evidence and source attribution (agent name or internal analysis). For procedural candidates, route through **extract-and-refine-capability** first. Then pass all to **provision-lessons**.
</detect-learning-signals>

<analyze-code-changes>
**Objective**: Analyze PRs (with user stories) and git commit history for reusable patterns, constraints, architectural decisions, and implementation recipes.
**Steps**:
1. **Identify the source type**: PR(s) + user story → steps 2–5. Git commit history → steps 6–9. For any PRs analyzed, also run step 10 (implementation recipe).

2. **Gather PR inputs**: Confirm you have the user story text, story comments, PR diff(s), PR review comments, and any additional context.

3. **Parse the user story**: Extract explicit requirements, implicit assumptions, acceptance criteria, and scope boundaries.

4. **Analyze the PR changes**: Examine files changed and their roles, nature of changes (new abstraction? workaround? data model change?), commit messages for rationale, lines added/removed, test files, and PR review comments — reviewer questions and author replies often surface constraints and unwritten conventions.

5. **Compare story vs implementation**: Load [reference/story-analysis-framework.md](reference/story-analysis-framework.md) and for each analysis lens, ask "Did the implementation reveal something the story didn't capture?" Focus on the top four lenses (missing capability, architectural decision, discovered constraint, PR discussion insight). Draft candidate lessons for each gap: what was expected vs. what happened, why the gap existed, and what to do differently next time.

6. **Gather git inputs**: Confirm commit range/references and access to commit messages and diffs.

7. **Scan commit messages for themes**: Look for recurring verbs/patterns ("fix:", "refactor:", "migrate:"), repeated file paths (hotspots), and sequences of related commits.

8. **Analyze representative diffs**: For interesting clusters, identify the applied pattern, whether it's a one-off or trend, and whether commit messages explain the WHY.

9. **Identify evolutionary patterns**: Conventions that crystallized over time, recurring bug categories and their fixes, and refactoring arcs spanning multiple commits. Formulate each as: the pattern, the lesson, and the evidence (commits).

10. **Extract implementation recipes**: For each PR, map which repos/files are touched and the dependency order. Check generalizability: "Would a similar task follow this same pattern?" Tag confidence as **tentative** (single instance) or **confirmed** (2+ instances). When multiple instances exist, compare across them to identify the invariant recipe vs. parameters. Formulate at both **repo-level** and **cross-repo** levels.

11. **Apply quality pre-filter**: Check if already documented, actionable, and non-trivial. Return all candidates to **detect-learning-signals** with summaries, source references, analysis lens/pattern type, and preliminary quality assessment.
</analyze-code-changes>

<analyze-communication-history>
**Objective**: Parse chat transcripts from Slack, Teams, Discord, or similar tools to extract reusable team knowledge, decisions, and patterns.
**Steps**:
1. **Gather inputs**: Confirm you have the chat transcript(s), context about channels/threads, and any focus area.

2. Load [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) and **scan the transcripts** for communication tool signals: recurring questions (undocumented knowledge), decision records (unformalized ADRs), problem-solution pairs (tribal knowledge), knowledge sharing (undocumented tips/tricks), escalation patterns (ownership gaps), onboarding gaps (missing setup docs).

3. **Exclude anti-signals**: Filter out casual conversation, one-off resolved issues, already-documented information, status updates, and operational chatter.

4. **Cluster related signals**: Group the same topic across multiple threads — a pattern seen 5 times is stronger than a single mention.

5. **Formulate candidate lessons**: For each surviving signal, draft the pattern (what recurred/was decided), evidence (transcript excerpts with context), and the lesson (what to document, where, and for whom).

6. **Return candidates** to **detect-learning-signals** for quality gating, with transcript evidence and signal type.
</analyze-communication-history>

<extract-and-refine-capability>
**Objective**: Extract multi-step procedures from any source and optionally refine them by merging with existing capabilities. Handles both net-new extraction and abstraction of overlapping capabilities.
**Steps**:

**Extract phase** (always run):
1. **Identify the procedure**: Scan for ordered language, imperative instructions, checklist-style steps, conditional branches, or repo/component references. For code-change sources, look for a clear sequence of files touched.

2. **Determine the extraction level**: Single repo → one capability. Multiple repos → extract at two levels: **repo-level** (per-repo change pattern) and **cross-repo** (end-to-end orchestration, referencing repo-level capabilities as sub-steps).

3. **Scope the task**: Identify the goal, trigger condition, and intended audience.

4. **Extract the ordered steps**: Write each step as an imperative verb, preserving order, removing filler, noting dependencies and conditional branches.

5. **Identify parameters**: Separate constants (become steps) from variants (become parameters). Document expected type/format.

6. **Assess confidence**: **Tentative** (single instance) or **Confirmed** (2+ independent instances).

7. **Apply quality checks**: Load [reference/capability-quality-checklist.md](reference/capability-quality-checklist.md) and verify Reusable, Non-obvious, Complete, Team-specific. Tentative confidence does NOT cause rejection.

8. **Format as a capability**: Load [reference/capability-format-template.md](reference/capability-format-template.md) and structure using the template fields.

**Refine phase** (run only when an overlapping capability exists in the target):
9. **Load existing context**: Read the target file to find existing capabilities covering related tasks. Check for overlaps at both repo-level and cross-repo level.

10. **Compare existing vs. new**: Identify identical steps (core invariant), similar-but-different steps (unifiable with parameters), unique steps (conditional branches). Compare at each level separately.

11. **Identify the abstraction**: Replace concrete values with parameters, merge similar steps, add conditional branches. Cover all known instances without becoming too vague.

12. **Preserve variant knowledge**: Keep meaningful variants as sub-cases. Don't force unification if variants serve genuinely different purposes.

13. **Validate the abstraction**: Verify each original instance is derivable by filling parameters, and nothing is lost.

14. **Produce the refined capability**: Format using the template, plus an evolution note and parameter table. Mark as replacing (not duplicating) the existing capability.

**Return** the formatted capability (or multi-level capabilities) to **detect-learning-signals** for routing to **provision-lessons**.
</extract-and-refine-capability>

<provision-lessons>
**Objective**: Classify qualifying lessons by target, generate a reviewable plan, get user approval, and apply changes.
**Steps**:

**Classify phase**:
1. **Detect platform capabilities**: Identify available persistent context mechanisms. Load [reference/context-target-catalog.md](reference/context-target-catalog.md) for target types and suitability.

2. If the user **explicitly specified a target**, honor it. Otherwise, **classify each lesson** by nature: personal preference → personal notes; project convention → project notes; skill domain knowledge → skill file; agent behavior → agent/instruction file; doc fact → README/ADR/architecture doc; code-change pattern → project notes (project-wide) or skill (domain-specific); procedure/capability → skill file (as capability) or project notes (as how-to); temporary note → session context (rare). Choose the **most specific and discoverable** target when multiple fit.

**Plan phase**:
3. For each lesson, draft the **exact content** in the format appropriate for the target (see context-target-catalog). Include source evidence. Structure as a table: #, Lesson Summary, Signal Type, Target File, Section, Content to Add. Include a rationale for each target choice. Note any files that need creation.

**Review phase**:
4. Present the complete plan. For each lesson, ask the user to **Approve** (proceed), **Modify** (adjust), or **Reject** (skip). Present all lessons together for batch review. **Do NOT apply any changes until the user explicitly confirms.**

**Apply phase**:
5. For approved lessons: read the target file, insert content into the correct section, create the file if needed, and follow skill conventions (facts → knowledge, routing → rules, steps → capabilities) when the target is a skill file.

6. For modified lessons: apply the user's adjustments and re-confirm before writing.

7. After all changes are applied, summarize what was added and where. If the user rejects all lessons or none passed the quality gate, acknowledge this explicitly — do not force a lesson.
</provision-lessons>

</capabilities>

<rules>

<rule>When the user asks to learn from any source (chat session, PRs+story, git history, communication transcripts) → apply **detect-learning-signals** as the master entry point. It will detect available sub-agents, dispatch analysis tasks in parallel when suitable agents exist, or fall back to internal **analyze-code-changes** / **analyze-communication-history** capabilities. The parent always controls the quality gate and provisioning.</rule>

<rule>When suitable sub-agents are detected and the source is large or multi-type → prefer agent dispatch over internal analysis. Agents enable parallel execution and specialized analysis. Fall back to internal capabilities only when no suitable agents exist or dispatch fails.</rule>

<rule>When **detect-learning-signals** produces qualifying lessons → if any candidate is procedural, route through **extract-and-refine-capability** first. Then pass all lessons to **provision-lessons**. Never apply changes without explicit user confirmation.</rule>

<rule>If no lessons pass the quality gate → report "No lessons worth learning from this [source]" and stop. Do not fabricate lessons.</rule>

</rules>
