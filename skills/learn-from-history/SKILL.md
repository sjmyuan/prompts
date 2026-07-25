---
name: learn-from-history
description: Extract reusable knowledge, rules, procedures, and implementation recipes from chat sessions, pull requests, git history, Slack/Teams transcripts, and other historical records, then provision them to persistent context. Use when distilling lessons from conversations, extracting step-by-step procedures and how-to knowledge, analyzing PRs for implementation recipes and story gaps, mining git history for patterns, mining communication tool chat history for team knowledge, auditing sessions for preservable insights, or updating skills, agents, or memory from any historical source.
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
- User wants to extract step-by-step procedures or "how-to" knowledge from conversations, PRs, or chat history — the concrete steps the team follows to accomplish recurring tasks
- User provides one or more PRs for similar task types and wants to distill the common implementation recipe (which repos/components to touch, what change pattern to follow)
- User wants to refine and generalize an existing capability by merging it with newly discovered procedural knowledge from historical sources
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
| Extracting a step-by-step procedure from conversation or chat history | Walkthrough of detecting a procedural pattern signal, extracting the ordered steps, and provisioning as a capability | [examples/procedural-discovery.md](examples/procedural-discovery.md) |
| Distilling an implementation recipe from one or more PRs | Walkthrough of detecting an implementation recipe signal across PRs, extracting the repo/component/change-pattern, and abstracting into a generalized capability | [examples/implementation-recipe.md](examples/implementation-recipe.md) |

</context-loading-guide>

<signal-detection-knowledge>
Signal types span multiple source categories. Each has specific triggers and anti-signals — load the full catalog from [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) when scanning for signals.

Quick reference:
- **Interactive** (chat sessions): explicit user feedback, AI self-discovered insight, future-useful information
- **Code-change** (PRs, git history): story-implementation gap, evolutionary pattern, implementation recipe
- **Communication tool** (Slack, Teams, Discord): recurring question, decision record, problem-solution pair, knowledge sharing, escalation pattern, onboarding gap
- **Procedural** (any source): procedural pattern — step-by-step descriptions of how to accomplish a recurring task, including which repos and components to touch and what change pattern to follow
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

2. For chat sessions, load [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) and **scan the conversation** for interactive and procedural signal types:
   - Explicit user feedback (corrections, preferences, "remember this" statements)
   - AI self-discovered insights (reasoning that produced correct knowledge not in context)
   - Future-useful information (hard-won configuration, non-obvious workarounds, undocumented constraints)
   - Procedural pattern (step-by-step descriptions of how to accomplish a task — "first do A, then B, then C")

3. For code-change sources, **delegate to analyze-code-change-history** to produce candidate lessons from the PR/git analysis. This includes both gap-analysis candidates and implementation recipe candidates.

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

**Additional step for implementation recipe detection**:
8. For each PR (even a single one), **extract the change pattern** to detect a potential implementation recipe:
   - **Repo map**: Which repos are touched? If a single task spans multiple repos (e.g., API repo + frontend repo + infra repo), treat each repo's changes as a separate sub-pattern first, then synthesize a cross-repo orchestration.
   - **Per-repo component map**: Within each repo, which files or directories are modified? What's the change sequence?
   - **Cross-repo orchestration**: When multiple repos are involved, what is the dependency order? (e.g., "1) API repo adds endpoint → 2) Frontend repo adds UI → 3) Infra repo updates config")
   - **Generalizability check**: Ask "If someone implemented a similar task next sprint, would they touch these same repos, files, and follow this same order?" If yes, it's a candidate recipe.
   - **Confidence**: Tag as **tentative** for a single instance, **confirmed** when 2+ instances for the same task type follow the same pattern. Even tentative recipes are worth capturing — they get refined as more data arrives.

9. When multiple instances for the same task type are available, **compare across instances** to strengthen the recipe:
   - **What was consistent** across instances vs. **what varied**? (the consistent parts are the recipe; the variants are parameters)
   - **Multi-repo consistency**: Does the cross-repo orchestration hold across instances? Do the same repos always get touched in the same order?
   - Upgrade confidence from tentative to confirmed when the same pattern appears in 2+ instances

10. For each implementation recipe candidate, formulate it at **both levels** when repos are involved:
   - **Repo-level capabilities** (one per repo): What specific files and steps within that repo?
   - **Cross-repo capability** (the orchestration): What is the end-to-end sequence across repos? References the repo-level capabilities as sub-steps.
   - Each level gets its own: **Task type**, **Confidence**, **Steps**, **Parameters**, **Evidence**
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
   - **Multi-step procedure or capability** → the relevant skill file (as a new or updated capability), or project-level persistent notes (as a how-to guide) if no domain skill exists. Procedural patterns and implementation recipes typically become capabilities in skills — they describe "how to do X" following team conventions.
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
   - For capabilities (procedures), use the format: **name** (action-verb phrase), **objective** (one-sentence goal), **ordered steps** (numbered, each starting with an action verb), **parameters** (what varies per instance)
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

<extract-capability>
**Objective**: Detect and extract multi-step procedures from any historical source, format them as actionable capabilities, and prepare them for provisioning. Works on single instances (tentative, lower confidence) as well as multiple instances (confirmed, higher confidence). When a task spans multiple repos, extracts at two levels — per-repo capabilities and a cross-repo orchestration capability — enabling capabilities to improve as more data arrives.

**Steps**:
1. **Identify the procedure**: Scan the source for a sequence of steps that describes how to accomplish a recurring task. Look for:
   - Ordered language: "first", "then", "next", "finally", "after that"
   - Imperative instructions: "you need to", "make sure to", "don't forget to"
   - Checklist-style descriptions: numbered or bulleted steps
   - Conditional branches: "if X, do Y; otherwise do Z"
   - Repo/component references: "touch the auth service", "modify the payment module"
   - For code-change sources: a clear sequence of files touched across one or more repos that suggests a reusable change pattern

2. **Determine the extraction level**: Based on the source, decide whether to extract at one level or multiple:
   - **Single repo**: The task touches one repo → extract one capability for that repo
   - **Multiple repos**: The task spans multiple repos (e.g., API repo + frontend repo + infra repo) → extract at two levels:
     - **Repo-level capabilities**: One per repo, describing the specific change pattern within that repo
     - **Cross-repo capability**: The end-to-end orchestration — which repos in what order, with dependencies between them. References repo-level capabilities as sub-steps.
   - The cross-repo capability is the higher-level abstraction — it tells a newcomer "for this task type, you need to touch these repos in this order, and within each repo you follow this pattern."

3. **Scope the task**: Determine what task this procedure accomplishes:
   - What is the goal? (e.g., "deploy a hotfix to production", "add a new payment method")
   - What triggers this procedure? (e.g., "when a critical bug is found in prod")
   - Who would follow this procedure? (new team member? on-call engineer? any developer?)

4. **Extract the ordered steps**: Write each step as an action starting with an imperative verb:
   - Preserve the original order
   - Remove conversational filler — keep only the actionable part
   - Note any dependencies between steps ("step 3 requires step 2 to complete first")
   - Flag any steps that are conditional ("only if the build passes")
   - For cross-repo capabilities, each step may reference a repo-level capability (e.g., "Step 2: In the frontend repo, apply `<add-bulk-ui>`")

5. **Identify parameters**: Separate what is **constant** (the same every time) from what **varies**:
   - Constants become the procedure steps themselves
   - Variants become parameters — placeholders that differ per instance (e.g., `<branch-name>`, `<service-name>`)
   - For cross-repo capabilities, parameters may span repos (e.g., `<entity>` is used in both API and frontend repos)
   - Document the expected type or format of each parameter

6. **Assess confidence**: Tag the extracted capability with a confidence level:
   - **Tentative**: Derived from a single instance (one conversation, one PR, one multi-repo task). The pattern looks generalizable but hasn't been confirmed by repetition. Still worth capturing — it will be refined by **abstract-capability** when more data arrives.
   - **Confirmed**: Derived from 2+ independent instances showing the same pattern. The recipe is validated by repetition.

7. **Apply capability quality checks**:
   - Is this procedure **reusable**? (would someone follow these same steps more than once?)
   - Is it **non-obvious**? (would a newcomer figure this out without being told?)
   - Is it **complete**? (can someone follow these steps end-to-end without missing context?)
   - Is it **team-specific**? (does it encode this team's conventions vs. generic best practice?)
   - If the procedure is generic/common knowledge, reject it — capabilities should capture team-specific conventions
   - Tentative confidence does NOT cause rejection — it just means the capability should be tagged as tentative and revisited when more data arrives

8. **Format as a capability**: Structure the extracted procedure as:
   - **Capability name**: Action-verb phrase in kebab-case (e.g., `deploy-hotfix`, `add-payment-method`)
   - **Level**: Repo-level (single repo) or Cross-repo (orchestration across repos)
   - **Confidence**: Tentative (1 instance) or Confirmed (2+ instances)
   - **Objective**: One sentence describing the goal
   - **Trigger**: When to apply this capability
   - **Steps**: Numbered list, each starting with an action verb. For cross-repo: reference repo-level capabilities where applicable.
   - **Parameters**: Table of what varies per instance
   - **Source evidence**: Where this procedure was discovered (conversation excerpt, PR links, commit range)

9. **Return the formatted capability** to **determine-provision-target** for target assignment. When returning multi-level capabilities, present the cross-repo capability first (the high-level view), with repo-level capabilities as referenced sub-capabilities.
</extract-capability>

<abstract-capability>
**Objective**: Merge newly discovered procedural knowledge with existing capabilities to produce a more general, refined version. Works at both repo-level and cross-repo level — capabilities at each level can be independently abstracted as more data arrives. This is the learning loop that makes capabilities more abstract and broadly applicable over time.

**Steps**:
1. **Load existing context**: Before proposing changes to a target, read the target file to find any existing capability that covers a related task:
   - Same task type but different parameters? (e.g., existing "deploy service" + new "deploy hotfix")
   - Overlapping steps? (e.g., both mention "run build", "run tests", but differ in later steps)
   - Same repo/component pattern? (e.g., both touch the same set of files in the same order)
   - Same cross-repo orchestration? (e.g., both touch API repo then frontend repo in that order)
   - **Check both levels**: When repos are involved, check for overlaps at the repo level (per-repo patterns) AND at the cross-repo level (orchestration). They may abstract independently — repo-level capabilities can be refined without changing the cross-repo orchestration, and vice versa.

2. **Compare existing vs. new**: For each related existing capability, compare with the new findings:
   - What steps are **identical**? → these are the core, invariant part of the capability
   - What steps are **similar but differ in detail**? → these can be unified with a parameter
   - What steps are **unique to one version**? → these may be conditional branches or variants
   - What does the new finding **add** that the existing capability is missing?
   - What does the existing capability **cover** that the new finding doesn't?
   - **Multi-level comparison**: If both have repo-level and cross-repo capabilities, compare at each level separately. A repo-level capability may abstract cleanly while the cross-repo orchestration stays unchanged.

3. **Identify the abstraction**: Determine the most general version that covers both:
   - Replace concrete values with parameters (e.g., "push to `staging`" → "push to `<environment-branch>`")
   - Merge similar steps (e.g., "SSH into payments-server" + "SSH into auth-server" → "SSH into `<target-server>`")
   - Add conditional steps (e.g., "if hotfix, also create a rollback plan")
   - The abstraction should cover ALL known instances without being so vague it loses usefulness
   - For cross-repo capabilities: if the same repo sequence appears across task types, parameterize what varies within repos while keeping the orchestration fixed

4. **Preserve variant knowledge**: Document when each variant applies:
   - If the procedure differs meaningfully for different contexts, keep the variants as sub-cases
   - Use a parameter table or conditional notes: "For service type X, also do step Y"
   - Don't force unification if the variants serve genuinely different purposes

5. **Validate the abstraction**:
   - Does the abstracted capability still guide a newcomer correctly?
   - Can each original concrete instance be derived from the abstracted version by filling in parameters?
   - Is anything lost in the abstraction? (if yes, preserve it as a note or variant)
   - For multi-level: can a newcomer follow the cross-repo capability and drill into each repo-level capability correctly?

6. **Produce the refined capability**: Format it as in **extract-capability** step 8, plus:
   - **Evolution note**: A brief note showing what was generalized and why
   - **Parameter table**: Each parameter with type, example values, and which variants introduced it

7. **Return the refined capability** to **determine-provision-target** with a note that it replaces (not duplicates) the existing capability. When multiple levels were refined, present the cross-repo capability first, with updated repo-level capabilities as referenced sub-capabilities.
</abstract-capability>

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

<rule>When a candidate lesson describes a sequence of steps to accomplish a task (a procedure or how-to), apply **extract-capability** to format it as a structured capability before passing to **determine-provision-target**.</rule>

<rule>When a candidate capability overlaps with an existing capability already stored in a target (same task type, similar steps, or same repo/component pattern), apply **abstract-capability** to merge them into a refined, more general version before provisioning.</rule>

</rules>
