---
name: learn-from-history
description: Extract reusable knowledge, rules, and procedures from chat sessions, PRs, git history, and team transcripts. Use when distilling lessons, analyzing change history, mining chat, extracting procedures, checking for insights, or refining skills/agents/memory.
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

<lesson-type-concepts>
A **lesson** is any reusable insight extracted from a historical source. Lessons come in two forms, distinguished by their **structure**, not how they were discovered:

| Lesson form | Structure | Examples | Provisioned as | Routed through |
|---|---|---|---|---|
| **Rule / Knowledge fact** | A single, standalone directive or piece of information — can be stated in one sentence | "Always null-check API responses with `?.` and `??`", "The rate limiter has a 10KB body limit", "Extract utilities to `src/shared/` when used in 3+ places" | Knowledge section of the target (skill, project notes, agent file, etc.) | Directly to **provision-lessons** |
| **Procedure (capability)** | An ordered, multi-step sequence of actions for accomplishing a recurring task | "How to deploy a hotfix" (6 steps), "How to add a bulk operation" (8 steps with parameters), "How to onboard a new service" (5 steps) | Named capability in the target (skill or project notes), formatted per the capability format template | Through **extract-and-refine-capability** before **provision-lessons** |

A **pattern** is a recurring observation across historical sources — it describes the **discovery mechanism**, not the lesson form. Patterns can yield either rules or procedures:
- An **evolutionary pattern** in git history (signal #5) may yield rules ("always use `date-fns-tz`") or procedures
- A **described procedure** in chat (signal #12) yields a procedure
- An **implementation recipe** in PRs (signal #13) yields a procedure

**Key decision rule**: If a candidate can be fully expressed as a single sentence directive or fact → it's a rule/knowledge fact (provision directly). If it requires ordered steps, parameters, conditional branches, or a sequence of actions → it's a procedure (route through extract-and-refine-capability).
</lesson-type-concepts>

<agent-orchestration>
When the platform supports sub-agents, this skill orchestrates them to parallelize the learning pipeline. The parent skill retains control of the quality gate, result merging, de-duplication, and provisioning. Load [reference/agent-orchestration-pattern.md](reference/agent-orchestration-pattern.md) for the full task-to-agent mapping table, agent detection protocol, prompt templates, parallelization strategy, result merging algorithm, fallback guidance, and anti-patterns for agent use.
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
| Extracting a step-by-step procedure from conversation or chat history | Walkthrough: detecting a described procedure (signal #12) → extracting steps → provisioning as capability | [examples/procedural-discovery.md](examples/procedural-discovery.md) |
| Distilling an implementation recipe from one or more PRs | Walkthrough: detecting a recipe signal (signal #13) → extracting change sequence → abstracting into capability | [examples/implementation-recipe.md](examples/implementation-recipe.md) |
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
- **Procedural** (any source): described procedures (step-by-step task instructions in text) and implementation recipes (change sequences inferred from PRs) — both yield multi-step capabilities, not single rules
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
**Objective**: Master entry point — detect sub-agents, scan any historical source for candidate lessons, delegate to agents or internal analysis, apply the quality gate, classify each lesson by form (rule vs. procedure), route accordingly, and pass all to provisioning.
**Steps**:
1. **Detect available sub-agents**: Scan the platform's agent registry for agents suitable for analysis tasks. Look for agents whose descriptions match the keywords in the task-to-agent mapping table (see agent-orchestration knowledge). Record available agent names and their capabilities. If no suitable agents are found, proceed with internal capabilities only.

2. **Identify the source type and choose execution mode**:
   - **Single, small chat session** → proceed to step 4 (scan interactively — agent overhead not justified for small sessions)
   - **PR(s) + user story** → if a suitable code investigator/reviewer agent was detected in step 1, dispatch to it (see step 3); otherwise delegate to **analyze-code-changes**
   - **Git commit history** → if a suitable code investigator/explorer agent was detected, dispatch to it; otherwise delegate to **analyze-code-changes**
   - **Communication tool transcripts** → if a suitable text analyst/researcher agent was detected, dispatch to it; otherwise delegate to **analyze-communication-history**
   - **Mixed sources (multiple independent source types)** → dispatch each source type to a different agent in parallel if available; otherwise process each path sequentially with internal capabilities
   - **Sources requiring cross-referencing** (e.g., story + its PR) → dispatch to a single agent with ALL inputs, or fall back to internal analysis

3. **Dispatch to agents** (when agents are available): For each agent to invoke, load [reference/agent-orchestration-pattern.md](reference/agent-orchestration-pattern.md) and construct a prompt following the prompt template for that agent type. Include: the source material, signal types to look for, structured output requirements, and the instruction to NOT write files. Dispatch all independent agents in parallel. Wait for all agents to complete, then collect results. Merge by de-duplicating across agent outputs and combining complementary findings. Tag each candidate with its source agent. Proceed to step 5.

4. For chat sessions without agent dispatch, load [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) and **scan the conversation** for signal types: explicit user feedback, AI self-discovered insights, future-useful information, and described procedures (step-by-step task descriptions — signal #12).

5. **Exclude anti-signals** immediately — filter out trivial facts, one-off fixes, already-documented info, session state, boilerplate changes. For agent-produced candidates, apply a lighter pre-filter since agents were already instructed to be conservative.

6. For each remaining candidate, **apply the quality gate**. Load [reference/quality-rubric.md](reference/quality-rubric.md) and score all five dimensions: Reusability, Non-obviousness, Actionability, Non-duplication, Specificity.

7. **If no candidates pass**: Report "No lessons worth learning from this [source]" and stop. This is a valid outcome — do not fabricate lessons.

8. **Classify each qualifying candidate by lesson form** (see lesson-type-concepts in knowledge). Ask: "Can this lesson be fully expressed as a single sentence directive or fact, or does it require ordered steps, parameters, conditional branches, or a sequence of actions?"
   - **Rule / Knowledge fact** (single statement) → tag as `form: rule` and hold for direct provisioning
   - **Procedure / Capability** (multi-step) → tag as `form: procedure` and route through **extract-and-refine-capability** before provisioning
   - **When in doubt**, default to `form: procedure` — it's safer to structure something as steps and later simplify than to lose procedural structure

9. **Route by form**:
   - For `form: rule` candidates: collect with evidence and source attribution, pass directly to **provision-lessons**
   - For `form: procedure` candidates: first pass through **extract-and-refine-capability** to produce formatted capabilities, then pass the resulting capabilities (now in structured form) along with any `form: rule` candidates to **provision-lessons**

10. Collect **all** processed candidates (rules + formatted capabilities) with evidence, source attribution, and form tags. Pass the complete set to **provision-lessons**.
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

10. **Flag implementation recipe signals**: For each PR, ask "Would a similar task follow the same sequence of files and changes?" If yes, flag this as an implementation recipe candidate (signal #13). Gather the raw evidence — the list of repos touched, files changed per repo, change order, and dependency order between repos. Do NOT extract or format the recipe here — that is the job of **extract-and-refine-capability**. Tag each flagged recipe with `form: procedure` and attach the raw evidence (repo map, file list, change sequence).

11. **Apply quality pre-filter**: Check if already documented, actionable, and non-trivial. Return all candidates to **detect-learning-signals** with summaries, source references, analysis lens/pattern type, form tags, raw evidence (for recipes), and preliminary quality assessment.
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
**Objective**: Transform raw procedural candidates into structured capabilities, handling two distinct source types: described procedures (text-described steps from chat/transcripts) and implementation recipes (change sequences inferred from PRs). Also refine existing capabilities by merging overlapping ones into parameterized abstractions.
**Steps**:

**Determine source type** (always run first):
1. **Identify what kind of procedural candidate this is**:
   - **Described procedure** (signal #12): Someone described steps in words — chat message, Slack thread, document. The steps are explicit in the text. → follow steps 2–8 (extract phase, text path)
   - **Implementation recipe** (signal #13): The procedure is inferred from code changes across PRs. The steps are implicit in the file/change sequence and repo map. → follow steps 9–16 (extract phase, code path)
   - When multiple PRs exist for the same task type, process them together — the code path handles multi-instance comparison natively.

**Extract phase — Text path** (described procedures from chat, transcripts, documents):
2. **Identify the procedure in the text**: Scan for ordered language (first/then/next/finally), imperative instructions (you need to/make sure to/always), checklist-style formatting (numbered/bulleted lists), conditional branches (if this is a hotfix, also…), and tool/script invocations.

3. **Scope the task**: Identify the goal (what does this accomplish?), the trigger condition (when would someone do this?), and the intended audience.

4. **Extract the ordered steps**: Write each step as an imperative verb phrase, preserve order, remove filler, note dependencies between steps and conditional branches.

5. **Identify parameters**: Separate constants (team conventions that become steps) from variants (values that change per instance — become parameters). Document expected type/format for each parameter.

6. **Assess confidence**: **Tentative** (single description from one source) or **Confirmed** (described independently 2+ times, or explicitly stated as "the standard way").

7. **Apply quality checks**: Load [reference/capability-quality-checklist.md](reference/capability-quality-checklist.md) and verify Reusable, Non-obvious, Complete, Team-specific. Tentative confidence does NOT cause rejection.

8. **Format as a capability**: Load [reference/capability-format-template.md](reference/capability-format-template.md) and structure using the template fields. Skip to step 17 (refine phase check).

**Extract phase — Code path** (implementation recipes from PRs):
9. **Gather the raw evidence**: The candidate should already have attached: repo map (which repos were touched), per-repo file list and change order, and dependency order between repos. If this evidence is missing, go back to the source PR(s) and collect it.

10. **Map the change sequence per repo**: For each repo touched, list the files modified/created in order. Identify the logical phases within each repo (e.g., "API endpoint → DB helper → tests").

11. **Map the cross-repo orchestration** (if multiple repos): Identify which repo must be worked on first and the dependency order. Note any deploy ordering constraints.

12. **Check generalizability**: "Would a similar task follow this same sequence of repos, files, and change types?" If the task is domain-specific (e.g., bulk operations) but the structural pattern generalizes (e.g., "API endpoint → middleware → UI → tests"), capture both.

13. **Determine the extraction level**:
    - Single repo → one repo-level capability
    - Multiple repos → extract at two levels: **repo-level** (per-repo change pattern) and **cross-repo** (end-to-end orchestration, referencing repo-level capabilities as sub-steps)

14. **Assess confidence and compare instances** (when multiple PRs exist):
    - **Tentative** (1 PR) — the recipe is a hypothesis; tag accordingly
    - **Confirmed** (2+ PRs for same task type) — compare across instances, compute hit rate per step, identify which steps are always present vs. conditional

15. **Apply quality checks**: Load [reference/capability-quality-checklist.md](reference/capability-quality-checklist.md) and verify Reusable, Non-obvious, Complete, Team-specific. For cross-repo capabilities, also verify that dependencies between repos are clear. Tentative confidence does NOT cause rejection.

16. **Format as a capability** (or set of capabilities for multi-repo): Load [reference/capability-format-template.md](reference/capability-format-template.md) and structure using the template fields. For multi-repo: produce one capability per repo plus one cross-repo orchestration capability.

**Refine phase** (run only when an overlapping capability exists in the target):
17. **Load existing context**: Read the target file to find existing capabilities covering related tasks. Check for overlaps at both repo-level and cross-repo level.

18. **Compare existing vs. new**: Identify identical steps (core invariant), similar-but-different steps (unifiable with parameters), unique steps (conditional branches). Compare at each level separately.

19. **Identify the abstraction**: Replace concrete values with parameters, merge similar steps, add conditional branches. Cover all known instances without becoming too vague.

20. **Preserve variant knowledge**: Keep meaningful variants as sub-cases with their concrete parameter values. Don't force unification if variants serve genuinely different purposes.

21. **Validate the abstraction**: Verify each original instance is derivable by filling parameters, and nothing is lost.

22. **Produce the refined capability**: Format using the template, plus an evolution note and parameter table showing each parameter with values for all known variants. Mark as replacing (not duplicating) the existing capability.

**Return** the formatted capability (or multi-level capabilities for multi-repo recipes, or refined capability for abstractions) to **detect-learning-signals** for routing to **provision-lessons**.
</extract-and-refine-capability>

<provision-lessons>
**Objective**: Classify qualifying lessons by target, generate a reviewable plan, get user approval, and apply changes.
**Steps**:

**Classify phase**:
1. **Detect platform capabilities**: Identify available persistent context mechanisms. Load [reference/context-target-catalog.md](reference/context-target-catalog.md) for target types and suitability.

2. If the user **explicitly specified a target**, honor it. Otherwise, **classify each lesson** by nature and form:
   - **`form: rule` candidates** (single facts/directives): personal preference → personal notes; project convention → project notes; skill domain knowledge → skill file; agent behavior → agent/instruction file; doc fact → README/ADR/architecture doc; temporary note → session context (rare)
   - **`form: procedure` candidates** (formatted capabilities): project-specific how-to → project notes (as a named capability); domain-specific procedure → skill file (as a named capability); cross-cutting operational procedure → project notes (as a named capability)
   Choose the **most specific and discoverable** target when multiple fit.

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

<rule>When **detect-learning-signals** produces qualifying lessons → route `form: procedure` candidates through **extract-and-refine-capability** first to produce formatted capabilities. Then pass all lessons (rules + formatted capabilities) to **provision-lessons**. Never apply changes without explicit user confirmation.</rule>

<rule>If no lessons pass the quality gate → report "No lessons worth learning from this [source]" and stop. Do not fabricate lessons.</rule>

</rules>
