---
name: learn-from-history
description: Extract reusable knowledge, rules, and capabilities from chat sessions, pull requests, git history, Slack/Teams transcripts, and other historical records, then provision them to persistent context. Use when distilling lessons from conversations, analyzing PRs against user stories, mining git history for patterns, mining communication tool chat history for team knowledge, auditing sessions for preservable insights, or updating skills, agents, or memory from any historical source.
---

<when-to-use-this-skill>
- User wants to extract and preserve reusable lessons from the current chat session
- User provided explicit feedback during the conversation that should become a permanent rule or knowledge entry
- AI discovered correct patterns, rules, or knowledge not found in existing context that should be saved
- User provides a user story and one or more PRs and wants to extract reusable patterns, constraints, or architectural decisions from the implementation
- User provides git commit history (a range, a branch diff, or specific commits) and wants to identify recurring patterns, convention evolution, or lessons from code changes
- User wants to update an existing skill, agent file, doc, or memory with insights from any historical source
- User provides chat history from Slack, Teams, Discord, or other communication tools and wants to extract team knowledge, recurring questions, decisions, or problem-solution patterns from people's conversations
- User wants to check whether a conversation, PR, code history, or communication tool transcript contains anything worth preserving for future work
</when-to-use-this-skill>

<knowledge>

<core-principle>
This skill treats lessons seriously. Not every interaction or change yields a lesson worth preserving. A valid lesson must be **general enough to apply across multiple future sessions**, not a one-off fix or trivial observation. When nothing meets the quality bar, the skill explicitly reports "nothing worth learning" — this is a valid and important outcome.
</core-principle>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Evaluating whether a candidate lesson is worth preserving | 5-dimension quality rubric (Reusability, Non-obviousness, Actionability, Non-duplication, Specificity) with scoring criteria and rejection thresholds | [reference/quality-rubric.md](reference/quality-rubric.md) |
| Determining which context target fits a lesson | Catalog of context targets (skills, agents, docs, memory scopes) with suitability criteria, format requirements, and examples for each | [reference/context-target-catalog.md](reference/context-target-catalog.md) |
| Scanning a chat session or historical source for learning signals | Complete catalog of five signal types (interactive and code-change) with triggers, examples, and anti-signals for each | [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) |
| Comparing a user story against its PR implementation | Analysis lens framework with seven comparison dimensions, signal-strength ratings, and guidance on which rows produce the strongest lessons | [reference/story-analysis-framework.md](reference/story-analysis-framework.md) |
| User gives explicit feedback that should become a rule | Walkthrough of detecting a user feedback signal, extracting the lesson, and provisioning it | [examples/user-feedback-to-rule.md](examples/user-feedback-to-rule.md) |
| AI independently discovered correct knowledge during the conversation | Walkthrough of detecting an AI-discovered insight, validating it, and provisioning it | [examples/ai-discovered-insight.md](examples/ai-discovered-insight.md) |
| User asks to learn from a session but nothing qualifies | Walkthrough of scanning a session, applying the quality gate, and reporting no lessons found | [examples/nothing-to-learn.md](examples/nothing-to-learn.md) |
| User specifies a target context for the lesson | Walkthrough of user-directed provisioning to a specific skill, agent, or memory file | [examples/user-specified-target.md](examples/user-specified-target.md) |
| User provides a user story and PR(s) to learn from | Walkthrough of comparing story requirements to implementation changes, identifying gaps and extracting reusable knowledge | [examples/pr-story-gap-discovery.md](examples/pr-story-gap-discovery.md) |
| User provides git commit history to learn from | Walkthrough of mining commit history for recurring patterns, convention evolution, and reusable lessons | [examples/git-history-pattern.md](examples/git-history-pattern.md) |

</context-loading-guide>

<signal-detection-knowledge>
Five signal types indicate potential lessons: three from interactive sources (chat sessions) and two from code-change sources (PRs, git history). Each has specific triggers and anti-signals — load the full catalog from [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) when scanning for signals.

Quick reference:
- **Interactive**: explicit user feedback, AI self-discovered insight, future-useful information
- **Code-change**: story-implementation gap, evolutionary pattern
- **Communication tool**: recurring question, decision record, problem-solution pair, knowledge sharing, escalation pattern, onboarding gap
- **Anti-signals**: trivial facts, one-off fixes, already-documented info, session state, boilerplate changes, casual chat, resolved-once issues
</signal-detection-knowledge>

<quality-gate>
Every candidate lesson must pass all five dimensions in the quality rubric. Load [reference/quality-rubric.md](reference/quality-rubric.md) for the full rubric with scoring criteria, rejection rules, and decision matrix. A single failure rejects the candidate.
</quality-gate>

<story-analysis>
When comparing a user story against PR implementation changes, load [reference/story-analysis-framework.md](reference/story-analysis-framework.md) for the full comparison framework with eight analysis lenses (including PR discussion insights), signal strength ratings, and guidance on which rows produce the strongest lessons.
</story-analysis>

</knowledge>

<capabilities>

<detect-learning-signals>
**Objective**: Scan the current session or provided historical source for candidate lessons, applying the quality gate to filter out noise.

**Steps**:
1. **Identify the source type**:
   - **Chat session**: The current conversation — scan for interactive signals (types 1–3)
   - **PR + user story**: User provided a story and PR reference(s) — apply **analyze-code-change-history** first, then return here with its candidates
   - **Git history**: User provided commit range or references — apply **analyze-code-change-history** first, then return here with its candidates
   - **Communication tool history**: User provided chat transcripts from Slack, Teams, Discord, etc. — apply **analyze-communication-history** to extract candidate lessons, then return here for quality gating
   - **Mixed**: User provided multiple sources — process each with the appropriate path, then merge candidates

2. For chat sessions, load [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) and **scan the conversation** for the three interactive signal types:
   - Explicit user feedback (corrections, preferences, "remember this" statements)
   - AI self-discovered insights (reasoning that produced correct knowledge not in context)
   - Future-useful information (hard-won configuration, non-obvious workarounds, undocumented constraints)

3. For code-change sources, **delegate to analyze-code-change-history** to produce candidate lessons from the PR/git analysis.

4. **Exclude anti-signals** immediately — for each source type, filter out the anti-signals listed in the signal detection catalog.

5. For each remaining candidate, **apply the quality gate**. Load [reference/quality-rubric.md](reference/quality-rubric.md) and score each dimension:
   - Reusability — Would this apply across multiple future sessions?
   - Non-obviousness — Would a competent practitioner already know this?
   - Actionability — Can it be expressed as a concrete rule/fact/step?
   - Non-duplication — Is it absent from all current context?
   - Specificity — Is it specific enough to be useful AND general enough to be reusable?

6. **If no candidates pass**: Report "No lessons worth learning from this [source]" and stop. This is a valid outcome — do not fabricate lessons.

7. **If candidates pass**: Collect them into a provisional list with the evidence (conversation excerpt, story-PR gap, or commit pattern that triggered the signal) and proceed to **determine-provision-target**.
</detect-learning-signals>

<analyze-code-change-history>
**Objective**: Analyze PR(s) against a user story, or analyze git commit history, to extract candidate reusable knowledge, patterns, and rules.

**Steps** for PR + user story analysis:
1. **Gather inputs**: Confirm you have:
   - The user story text (requirements, acceptance criteria, context)
   - Story comments and discussion threads — clarifications, scope decisions, or assumptions surfaced after the story was written
   - Access to the PR diff(s) — either provided directly, via a PR link, or by running git commands to retrieve the diff
   - PR review comments and discussion threads — reviewer questions, author replies, and design discussions that capture rationale not visible in the diff
   - Any additional context the user provides about the story (design docs, discussion threads)

2. **Parse the user story**: Extract from the story:
   - The explicit requirements (what the story says must be done)
   - Implicit assumptions (what the story assumes already exists)
   - Acceptance criteria (how success is measured)
   - Scope boundaries (what the story explicitly excludes)

3. **Analyze the PR changes**: For each PR, examine:
   - Files changed and their roles in the codebase (new module? modification to existing? config change?)
   - The nature of changes (new abstraction? workaround? plumbing? data model change?)
   - Commit messages — these often contain rationale not visible in the diff alone
   - Lines added vs removed — large deletions may indicate a refactoring or simplification
   - Test files — how was the change validated?
   - **PR review comments and story comment threads** — reviewer questions ("why not X?") and author replies often surface constraints, architectural reasoning, and unwritten conventions that the diff alone can't reveal

4. Load [reference/story-analysis-framework.md](reference/story-analysis-framework.md) and **compare story vs implementation** using the framework:
   - For each analysis lens (missing capability, architectural decision, discovered constraint, etc.), ask: "Did the implementation reveal something the story didn't capture?"
   - Focus especially on the top four lenses (missing capability, architectural decision, discovered constraint, PR discussion insight) — these produce the strongest lessons
   - For each gap found, draft a candidate lesson: "When implementing stories like [type], be aware that [gap/constraint/decision]"

5. **Extract candidate lessons**: For each meaningful gap or pattern, formulate it as a candidate:
   - **What was expected** (from the story) vs **what happened** (in the implementation)
   - **Why** the gap existed (missing capability? undiscovered constraint? ambiguous story?)
   - **What to do differently** next time (the actionable lesson)

**Steps** for git history analysis:
1. **Gather inputs**: Confirm you have:
   - The commit range or references (e.g., `main..feature-branch`, last N commits, specific commit hashes)
   - Access to commit messages and diffs — retrieved via git commands

2. **Scan commit messages for themes**: Look for:
   - Recurring verbs or patterns (e.g., "fix:", "refactor:", "extract:", "migrate:")
   - Repeated file paths across commits — hotspots that indicate frequently-changing areas
   - Sequences of related commits (e.g., 3 commits iterating on the same function)

3. **Analyze representative diffs**: For interesting commit clusters, read the actual changes:
   - What pattern was applied? (e.g., extract to helper, add validation layer, introduce interface)
   - Was this a one-off or part of a trend?
   - Does the commit message explain the WHY?

4. **Identify evolutionary patterns**:
   - Conventions that crystallized over time (e.g., "all API calls now go through a client factory")
   - Recurring bug categories and their fixes (e.g., "multiple commits fix missing null checks on API responses")
   - Refactoring arcs (e.g., "gradual migration from class components to hooks over 15 commits")

5. **Extract candidate lessons**: For each pattern, formulate it:
   - **The pattern** (what recurred)
   - **The lesson** (what future work should follow)
   - **Evidence** (the commits that demonstrate the pattern)

**Steps** for both paths:
6. **Apply quality pre-filter**: Before returning to **detect-learning-signals**, do a quick pre-screen:
   - Is this already documented? (quick check against known context)
   - Is it actionable? (can you write it as a directive?)
   - Is it non-trivial? (would a junior dev on this team already know it?)

7. **Return candidates** to **detect-learning-signals** with:
   - The candidate lesson summary
   - Source reference (story+PR link or commit range)
   - Which analysis lens or pattern type triggered it
   - A preliminary quality assessment
</analyze-code-change-history>

<determine-provision-target>
**Objective**: For each qualifying lesson, identify the most appropriate persistent context to receive it.

**Steps**:
1. **Detect platform capabilities**: Identify what persistent context mechanisms are available (personal notes, project notes, skill files, agent files, documentation). Load [reference/context-target-catalog.md](reference/context-target-catalog.md) for guidance on target types and their suitability.

2. If the user **explicitly specified a target** (e.g., "add this to my coding assistant skill"), honor that target. Validate that it exists or can be created, and note this in the plan.

3. If the user did NOT specify a target, **classify each lesson** by its nature. Detect what persistent context mechanisms the current platform supports, then map accordingly:
   - **Personal preference / workflow rule** → personal persistent notes or preferences store
   - **Project-specific convention or command** → project-level persistent notes or configuration
   - **Domain knowledge for a skill** → the relevant skill definition file (e.g., `skills/*/SKILL.md`)
   - **Agent behavior rule** → the relevant agent or instruction file
   - **Project documentation fact** → relevant project documentation (README, ADR, architecture doc)
   - **Code-change-derived pattern** → project-level persistent notes (if project-wide) or relevant skill (if domain-specific). PR-derived lessons are typically project-scoped; classify based on whether the pattern would apply outside this project.
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
   - Include the source evidence (conversation excerpt, story-PR gap, or commit pattern)

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

<analyze-communication-history>
**Objective**: Parse chat transcripts from Slack, Teams, Discord, or similar tools to extract reusable team knowledge, decisions, and patterns from people's conversations.

**Steps**:
1. **Gather inputs**: Confirm you have:
   - The chat transcript(s) — exported from Slack, Teams, Discord, or copy-pasted threads
   - Context about the channels or threads (e.g., "#backend channel, last 30 days", "design discussion thread about auth")
   - Any focus area the user wants to narrow to (e.g., "just look for deployment-related knowledge")

2. Load [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) and **scan the transcripts** for communication tool signal types:

   **Recurring question pattern** (High signal):
   - The same question appears multiple times from different people
   - Answers converge on the same solution each time — this is undocumented knowledge
   - Ask: "What question keeps getting asked that should have a documented answer?"

   **Decision record** (High signal):
   - A thread where a technical or process decision was reached ("let's go with X approach")
   - The decision was never formalized in an ADR, doc, or convention file
   - Ask: "What decision was made here that future team members won't know about?"

   **Problem-solution pair** (High signal):
   - Someone reports an issue, someone else provides a fix or workaround
   - The solution is non-obvious or relies on tribal knowledge
   - Ask: "Would someone hit this same problem next month and have to rediscover the fix?"

   **Knowledge sharing** (Medium signal):
   - A team member shares a tip, trick, or "TIL" that isn't documented elsewhere
   - A non-obvious workaround or best practice is described
   - Ask: "Is this insight documented anywhere? If not, it's a candidate."

   **Escalation pattern** (Medium signal):
   - Certain topics or questions always get routed to the same person
   - Reveals who-knows-what — useful for onboarding and bus-factor reduction
   - Ask: "Is there a 'goto person' pattern that should be captured as ownership docs?"

   **Onboarding gap** (Medium signal):
   - New team members consistently ask the same setup, access, or process questions
   - Indicates missing or stale onboarding documentation
   - Ask: "What are new people always confused about?"

3. **Exclude anti-signals** — filter out:
   - Casual conversation, jokes, social chat
   - One-off issues that were resolved and never recurred
   - Information already documented in existing context
   - Status updates, standup notes, meeting scheduling
   - Purely operational chatter ("deploy is done", "PR merged")

4. **Cluster related signals**: If the same topic surfaces across multiple threads or channels, group them — a pattern seen 5 times is a much stronger candidate than a single mention.

5. **Formulate candidate lessons**: For each signal that survives filtering, draft it as:
   - **The pattern** (what recurred or was decided)
   - **Evidence** (excerpts from the transcripts, with thread/channel context)
   - **The lesson** (what should be documented, where, and for whom)

6. **Return candidates** to **detect-learning-signals** for quality gating, with transcript evidence and the signal type that triggered each candidate.
</analyze-communication-history>

</capabilities>

<rules>

<rule>When the user asks to learn from a chat session, extract lessons, or preserve insights, first apply **detect-learning-signals** to scan the session and filter candidates through the quality gate.</rule>

<rule>When the user provides a user story with PR(s) or asks to learn from PR/change history, apply **analyze-code-change-history** to extract candidate lessons from the code changes, then feed results into **detect-learning-signals** for quality gating.</rule>

<rule>When the user provides git commit history (a range, branch diff, or specific commits) and asks to learn from it, apply **analyze-code-change-history** to extract candidate patterns, then feed results into **detect-learning-signals** for quality gating.</rule>

<rule>If **detect-learning-signals** produces one or more qualifying lessons (from any source), apply **determine-provision-target** to identify where each lesson belongs.</rule>

<rule>After targets are determined, apply **generate-provision-plan** to produce the reviewable plan.</rule>

<rule>After the plan is generated, apply **review-and-apply** to present for user approval. Never apply changes without explicit user confirmation.</rule>

<rule>If no lessons pass the quality gate in **detect-learning-signals**, report "No lessons worth learning from this [source]" and stop. Do not proceed to downstream capabilities.</rule>

<rule>If the user specifies a target context explicitly (e.g., "add this to skill X"), honor that target in **determine-provision-target** step 2.</rule>

<rule>When the user provides chat history from Slack, Teams, Discord, or other communication tools and wants to extract team knowledge, apply **analyze-communication-history** to parse the transcripts and extract candidate lessons, then feed results into **detect-learning-signals** for quality gating.</rule>

</rules>
