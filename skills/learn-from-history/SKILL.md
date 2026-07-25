---
name: learn-from-history
description: Extract reusable knowledge, rules, and procedures from chat sessions, PRs, git history, and team transcripts, then provision to persistent context. Use when distilling lessons, analyzing change history, mining chat for tribal knowledge, extracting procedures, checking for reusable insights, or refining skills/agents/memory.
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
**Objective**: Scan the current session or provided historical source for candidate lessons, applying the quality gate to filter out noise.
**Steps**:
1. **Identify the source type**: Chat session → scan for interactive signals. PR + user story or Git history → delegate to **analyze-code-change-history** first. Communication tool history → delegate to **analyze-communication-history** first. Mixed sources → process each path, then merge candidates.

2. For chat sessions, load [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) and **scan the conversation** for interactive and procedural signal types:
   - Explicit user feedback (corrections, preferences, "remember this" statements)
   - AI self-discovered insights (reasoning that produced correct knowledge not in context)
   - Future-useful information (hard-won configuration, non-obvious workarounds, undocumented constraints)
   - Procedural pattern (step-by-step descriptions of how to accomplish a task — "first do A, then B, then C")

3. For code-change sources, **delegate to analyze-code-change-history** to produce candidate lessons from the PR/git analysis. This includes both gap-analysis candidates and implementation recipe candidates.

4. **Exclude anti-signals** immediately — for each source type, filter out the anti-signals listed in the signal detection catalog.

5. For each remaining candidate, **apply the quality gate**. Load [reference/quality-rubric.md](reference/quality-rubric.md) and score all five dimensions: Reusability, Non-obviousness, Actionability, Non-duplication, Specificity.

6. **If no candidates pass**: Report "No lessons worth learning from this [source]" and stop. This is a valid outcome — do not fabricate lessons.

7. **If candidates pass**: Collect them into a provisional list with the evidence (conversation excerpt, story-PR gap, or commit pattern that triggered the signal) and proceed to **determine-provision-target**.
</detect-learning-signals>

<analyze-code-change-history>
**Objective**: Route code-change analysis to the appropriate sub-capability based on source type, apply quality pre-filter, then return candidates to **detect-learning-signals**.
**Steps**:
1. **Identify the source type** and delegate:
   - PR(s) + user story → delegate to **analyze-pr-against-story**
   - Git commit history → delegate to **analyze-git-history**

2. After gap/pattern analysis completes, for any PRs analyzed, delegate to **detect-implementation-recipe** to extract reusable change patterns.

3. **Apply quality pre-filter**: Check if already documented, actionable, and non-trivial (not something a junior dev would already know).

4. **Return candidates** to **detect-learning-signals** with:
   - The candidate lesson summary
   - Source reference (story+PR link or commit range)
   - Which analysis lens or pattern type triggered it
   - A preliminary quality assessment
</analyze-code-change-history>

<analyze-pr-against-story>
**Objective**: Compare a user story's requirements against PR implementation changes to extract candidate reusable knowledge, patterns, and rules.
**Steps**:
1. **Gather inputs**: Confirm you have the user story text, story comments/discussion threads, PR diff(s), PR review comments, and any additional context (design docs, discussion threads).

2. **Parse the user story**: Extract explicit requirements, implicit assumptions, acceptance criteria, and scope boundaries.

3. **Analyze the PR changes**: For each PR, examine files changed and their roles, nature of changes (new abstraction? workaround? data model change?), commit messages for rationale, lines added/removed, test files, and PR review comments — reviewer questions and author replies often surface constraints and unwritten conventions not visible in the diff.

4. Load [reference/story-analysis-framework.md](reference/story-analysis-framework.md) and **compare story vs implementation**: for each analysis lens, ask "Did the implementation reveal something the story didn't capture?" Focus on the top four lenses (missing capability, architectural decision, discovered constraint, PR discussion insight). Draft candidate lessons for each gap found.

5. **Extract candidate lessons**: For each meaningful gap or pattern, formulate it as a candidate:
   - **What was expected** (from the story) vs **what happened** (in the implementation)
   - **Why** the gap existed (missing capability? undiscovered constraint? ambiguous story?)
   - **What to do differently** next time (the actionable lesson)

6. **Return candidates** to **analyze-code-change-history** with the candidate lesson summary, source reference, analysis lens, and preliminary quality assessment.
</analyze-pr-against-story>

<analyze-git-history>
**Objective**: Mine git commit history for recurring patterns, convention evolution, and reusable lessons.
**Steps**:
1. **Gather inputs**: Confirm commit range/references and access to commit messages and diffs.

2. **Scan commit messages for themes**: Look for recurring verbs/patterns ("fix:", "refactor:", "migrate:"), repeated file paths (hotspots), and sequences of related commits.

3. **Analyze representative diffs**: For interesting clusters, identify the applied pattern, whether it's a one-off or trend, and whether commit messages explain the WHY.

4. **Identify evolutionary patterns**: Conventions that crystallized over time, recurring bug categories and their fixes, and refactoring arcs spanning multiple commits.

5. **Extract candidate lessons**: For each pattern, formulate it:
   - **The pattern** (what recurred)
   - **The lesson** (what future work should follow)
   - **Evidence** (the commits that demonstrate the pattern)

6. **Return candidates** to **analyze-code-change-history** with the candidate lesson summary, pattern type, and evidence.
</analyze-git-history>

<detect-implementation-recipe>
**Objective**: Extract reusable implementation recipes from PRs by identifying which repos, components, and change sequences are involved, then generalize into a repeatable pattern.
**Steps**:
1. For each PR, **extract the change pattern**: Map which repos are touched, which files/directories within each repo, and the dependency order across repos. Check generalizability: "Would a similar task next sprint touch these same repos/files in this order?" Tag confidence as **tentative** (single instance) or **confirmed** (2+ instances).

2. When multiple instances exist, **compare across instances**: Identify what was consistent (the recipe) vs. what varied (the parameters). Verify cross-repo orchestration holds across instances. Upgrade confidence when 2+ instances match.

3. For each candidate, formulate at **both levels** when repos are involved: **repo-level** (per-repo files and steps) and **cross-repo** (end-to-end sequence, referencing repo-level capabilities as sub-steps). Each level gets: Task type, Confidence, Steps, Parameters, Evidence.

4. **Return recipe candidates** to **analyze-code-change-history** for quality pre-filtering and forwarding to **detect-learning-signals**.
</detect-implementation-recipe>

<determine-provision-target>
**Objective**: For each qualifying lesson, identify the most appropriate persistent context to receive it.
**Steps**:
1. **Detect platform capabilities**: Identify what persistent context mechanisms are available (personal notes, project notes, skill files, agent files, documentation). Load [reference/context-target-catalog.md](reference/context-target-catalog.md) for guidance on target types and their suitability.

2. If the user **explicitly specified a target** (e.g., "add this to my coding assistant skill"), honor that target. Validate that it exists or can be created, and note this in the plan.

3. If the user did NOT specify a target, **classify each lesson** by its nature and map to the appropriate context target: personal preference → personal notes; project convention → project notes; skill domain knowledge → skill file; agent behavior → agent/instruction file; doc fact → README/ADR/architecture doc; code-change pattern → project notes (project-wide) or skill (domain-specific); procedure/capability → skill file (as capability) or project notes (as how-to); temporary note → session context (rare).

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
1. For each lesson, draft the **exact content** in the format appropriate for the target (see [reference/context-target-catalog.md](reference/context-target-catalog.md)): concise rule or knowledge bullet; for capabilities use name + objective + ordered steps + parameters. Include source evidence.

2. Structure the plan as a table with columns: #, Lesson Summary, Signal Type, Target File, Section, Content to Add.

3. For each entry, include a **rationale** sentence for the target choice.

4. If any target file does not yet exist, note that it will be created.

5. Present the complete plan to the user and proceed to **review-and-apply**.
</generate-provision-plan>

<review-and-apply>
**Objective**: Present the plan for user review, pause for confirmation, then apply approved changes.
**Steps**:
1. Present the plan from **generate-provision-plan** in full.

2. For each lesson, ask the user to **Approve** (proceed), **Modify** (adjust content/target/format), or **Reject** (skip). Present all lessons together for batch review.

3. **Do NOT apply any changes until the user explicitly confirms.**

4. For approved lessons: read the target file, insert content into the correct section, create the file if needed, and follow skill conventions (facts → knowledge, routing → rules, steps → capabilities) when the target is a skill file.

5. For modified lessons: apply the user's adjustments and re-confirm before writing.

6. After all changes are applied, summarize what was added and where.

7. **Important**: If the user rejects all lessons or no lessons passed the quality gate, acknowledge this explicitly — do not force a lesson.
</review-and-apply>

<analyze-communication-history>
**Objective**: Parse chat transcripts from Slack, Teams, Discord, or similar tools to extract reusable team knowledge, decisions, and patterns from people's conversations.
**Steps**:
1. **Gather inputs**: Confirm you have the chat transcript(s), context about channels/threads, and any focus area the user wants to narrow to.

2. Load [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) and **scan the transcripts** for communication tool signals: recurring questions (undocumented knowledge), decision records (unformalized ADRs), problem-solution pairs (tribal knowledge), knowledge sharing (undocumented tips/tricks), escalation patterns (ownership gaps), onboarding gaps (missing setup docs).

3. **Exclude anti-signals**: Filter out casual conversation, one-off resolved issues, already-documented information, status updates, and operational chatter.

4. **Cluster related signals**: If the same topic surfaces across multiple threads or channels, group them — a pattern seen 5 times is a much stronger candidate than a single mention.

5. **Formulate candidate lessons**: For each signal that survives filtering, draft it as:
   - **The pattern** (what recurred or was decided)
   - **Evidence** (excerpts from the transcripts, with thread/channel context)
   - **The lesson** (what should be documented, where, and for whom)

6. **Return candidates** to **detect-learning-signals** for quality gating, with transcript evidence and the signal type that triggered each candidate.
</analyze-communication-history>

<extract-capability>
**Objective**: Detect and extract multi-step procedures from any historical source, format them as actionable capabilities, and prepare them for provisioning. Works on single instances (tentative) as well as multiple instances (confirmed). When a task spans multiple repos, extracts at two levels — per-repo and cross-repo orchestration.
**Steps**:
1. **Identify the procedure**: Scan the source for ordered language ("first", "then", "finally"), imperative instructions, checklist-style steps, conditional branches, or repo/component references. For code-change sources, look for a clear sequence of files touched that suggests a reusable change pattern.

2. **Determine the extraction level**: Single repo → one capability. Multiple repos → extract at two levels: **repo-level** (per-repo change pattern) and **cross-repo** (end-to-end orchestration, referencing repo-level capabilities as sub-steps).

3. **Scope the task**: Identify the goal, trigger condition, and intended audience (newcomer, on-call engineer, any developer).

4. **Extract the ordered steps**: Write each step as an imperative verb, preserving order, removing filler, noting dependencies and conditional branches. Cross-repo steps reference repo-level capabilities where applicable.

5. **Identify parameters**: Separate constants (become steps) from variants (become parameters like `<branch-name>`, `<service-name>`). Cross-repo parameters may span repos. Document expected type/format.

6. **Assess confidence**: **Tentative** (single instance — worth capturing, refined later by **abstract-capability**) or **Confirmed** (2+ independent instances showing the same pattern).

7. **Apply capability quality checks**: Load [reference/capability-quality-checklist.md](reference/capability-quality-checklist.md) and verify each criterion (Reusable, Non-obvious, Complete, Team-specific). Tentative confidence does NOT cause rejection.

8. **Format as a capability**: Load [reference/capability-format-template.md](reference/capability-format-template.md) and structure the extracted procedure using the template fields (name, level, confidence, objective, trigger, steps, parameters, source evidence).

9. **Return the formatted capability** to **determine-provision-target** for target assignment. When returning multi-level capabilities, present the cross-repo capability first (the high-level view), with repo-level capabilities as referenced sub-capabilities.
</extract-capability>

<abstract-capability>
**Objective**: Merge newly discovered procedural knowledge with existing capabilities to produce a more general, refined version. Works at both repo-level and cross-repo level — each can be independently abstracted as more data arrives.
**Steps**:
1. **Load existing context**: Read the target file to find existing capabilities covering related tasks (same task type, overlapping steps, same repo/component pattern, same cross-repo orchestration). When repos are involved, check for overlaps at both repo-level and cross-repo level — they may abstract independently.

2. **Compare existing vs. new**: Identify identical steps (core invariant), similar-but-different steps (unifiable with a parameter), unique steps (conditional branches), what the new finding adds, and what the existing covers that the new doesn't. Compare at each level separately when repos are involved.

3. **Identify the abstraction**: Replace concrete values with parameters, merge similar steps, add conditional steps where variants differ. Cover all known instances without becoming too vague. For cross-repo: parameterize what varies within repos while keeping the orchestration fixed.

4. **Preserve variant knowledge**: Keep meaningful variants as sub-cases with conditional notes ("For service type X, also do step Y"). Don't force unification if variants serve genuinely different purposes.

5. **Validate the abstraction**: Verify the abstracted capability still guides a newcomer correctly, each original instance is derivable by filling parameters, and nothing is lost (preserve as note/variant if so). For multi-level: verify cross-repo → repo-level drill-down works correctly.

6. **Produce the refined capability**: Format it using [reference/capability-format-template.md](reference/capability-format-template.md), plus:
   - **Evolution note**: A brief note showing what was generalized and why
   - **Parameter table**: Each parameter with type, example values, and which variants introduced it

7. **Return the refined capability** to **determine-provision-target** with a note that it replaces (not duplicates) the existing capability. When multiple levels were refined, present the cross-repo capability first, with updated repo-level capabilities as referenced sub-capabilities.
</abstract-capability>

</capabilities>

<rules>

<rule>When the user asks to learn from a chat session, PR(s) with a user story, git commit history, or communication tool transcripts → apply the source-appropriate analysis capability (**detect-learning-signals** for chat, **analyze-code-change-history** for PRs/git, **analyze-communication-history** for transcripts), then feed results into **detect-learning-signals** for quality gating.</rule>

<rule>If **detect-learning-signals** produces qualifying lessons → apply **determine-provision-target**, then **generate-provision-plan**, then **review-and-apply**. Never apply changes without explicit user confirmation.</rule>

<rule>If no lessons pass the quality gate → report "No lessons worth learning from this [source]" and stop. Do not fabricate lessons or proceed to downstream capabilities.</rule>

<rule>If the user specifies a target context explicitly → honor that target in **determine-provision-target** step 2.</rule>

<rule>When a candidate lesson describes a sequence of steps (a procedure/how-to) → apply **extract-capability** before passing to **determine-provision-target**.</rule>

<rule>When a candidate capability overlaps with an existing one → apply **abstract-capability** to merge them before provisioning.</rule>

</rules>
