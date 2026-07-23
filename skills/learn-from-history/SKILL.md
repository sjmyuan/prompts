---
name: learn-from-history
description: Extract reusable knowledge, rules, and capabilities from chat sessions, pull requests, git history, and other historical records, then provision them to persistent context. Use when distilling lessons from conversations, analyzing PRs against user stories, mining git history for patterns, or updating skills, agents, or memory from any historical source.
---

<when-to-use-this-skill>
- User wants to extract and preserve reusable lessons from the current chat session
- User provided explicit feedback during the conversation that should become a permanent rule or knowledge entry
- AI discovered correct patterns, rules, or knowledge not found in existing context that should be saved
- User provides a user story and one or more PRs and wants to extract reusable patterns, constraints, or architectural decisions from the implementation
- User provides git commit history (a range, a branch diff, or specific commits) and wants to identify recurring patterns, convention evolution, or lessons from code changes
- User wants to update an existing skill, agent file, doc, or memory with insights from any historical source
- User wants to check whether a conversation, PR, or code history contains anything worth preserving for future work
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
| User gives explicit feedback that should become a rule | Walkthrough of detecting a user feedback signal, extracting the lesson, and provisioning it | [examples/user-feedback-to-rule.md](examples/user-feedback-to-rule.md) |
| AI independently discovered correct knowledge during the conversation | Walkthrough of detecting an AI-discovered insight, validating it, and provisioning it | [examples/ai-discovered-insight.md](examples/ai-discovered-insight.md) |
| User asks to learn from a session but nothing qualifies | Walkthrough of scanning a session, applying the quality gate, and reporting no lessons found | [examples/nothing-to-learn.md](examples/nothing-to-learn.md) |
| User specifies a target context for the lesson | Walkthrough of user-directed provisioning to a specific skill, agent, or memory file | [examples/user-specified-target.md](examples/user-specified-target.md) |
| User provides a user story and PR(s) to learn from | Walkthrough of comparing story requirements to implementation changes, identifying gaps and extracting reusable knowledge | [examples/pr-story-gap-discovery.md](examples/pr-story-gap-discovery.md) |
| User provides git commit history to learn from | Walkthrough of mining commit history for recurring patterns, convention evolution, and reusable lessons | [examples/git-history-pattern.md](examples/git-history-pattern.md) |

</context-loading-guide>

<signal-detection-knowledge>
Five signal types indicate a potential lesson — three from interactive sources (chat) and two from code-change sources (PRs, git history):

### Interactive Sources (Chat Sessions)

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

### Code-Change Sources (PRs, Git History)

**4. Story-implementation gap** — When comparing a user story to its PR implementation, a meaningful divergence emerges:
- The story assumed a capability that doesn't exist in the codebase and required a workaround
- A non-obvious architectural decision was made during implementation that future similar stories should follow
- The implementation surfaced a constraint (library limitation, performance boundary, API restriction) not mentioned in the story
- A recurring implementation pattern emerged across multiple PRs for the same story type
- The story was implemented differently than described because of a discovered requirement — this is the most valuable signal

**5. Evolutionary pattern** — When scanning git commit history, recurring themes indicate codified knowledge:
- A refactoring pattern appears multiple times across different modules (e.g., "extract X to shared utility")
- Commit messages reveal a convention that evolved over time (e.g., "migrate all X to Y pattern")
- Bug-fix commits cluster around a specific area or pattern (e.g., repeated null-check additions after API calls)
- A sequence of commits tells a story of how a particular problem was solved incrementally, with lessons at each step

### Anti-Signals (do NOT treat these as lessons)

From interactive sources:
- Trivial facts any competent developer would know
- One-off fixes specific to a single line of code
- Information already documented in loaded context
- Session-specific state (e.g., "we're working on file X right now")
- Temporary workarounds that shouldn't be repeated

From code-change sources:
- Trivial diff-only changes (typo fixes, formatting, import reordering)
- A PR that implements the story exactly as described with no surprises or decisions — no gap means no lesson
- Boilerplate additions (new route with standard CRUD, new component matching existing pattern exactly)
- Changes that merely replicate an already-documented pattern elsewhere in the codebase
- Single, isolated commits with no connection to a larger pattern
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

<story-analysis-framework>
When analyzing a user story against PR implementation changes, use this framework to structure the comparison:

| Analysis Lens | What to Look For | Signal Strength |
|---|---|---|
| **Missing capability** | Story assumed a library, API, or pattern that doesn't exist → what was built instead? | High — reusable for similar stories |
| **Architectural decision** | Choice of where code lives, how modules interact, which layer handles what | High — constrains future work |
| **Discovered constraint** | A limit, restriction, or gotcha found only during implementation | High — prevents repeated discovery cost |
| **Story ambiguity resolved** | The story was unclear about X; the implementation settled on Y | Medium — captures tribal knowledge |
| **Unexpected dependency** | The change required touching modules not mentioned in the story | Medium — reveals hidden coupling |
| **Testing approach** | How the change was validated — especially non-obvious test setups | Medium — reusable test patterns |
| **Straightforward implementation** | The change matched the story exactly with no gap | None — no lesson to extract |

The strongest lessons come from the top three rows. Focus analysis there.
</story-analysis-framework>

</knowledge>

<capabilities>

<detect-learning-signals>
**Objective**: Scan the current session or provided historical source for candidate lessons, applying the quality gate to filter out noise.

**Steps**:
1. **Identify the source type**:
   - **Chat session**: The current conversation — scan for interactive signals (types 1–3)
   - **PR + user story**: User provided a story and PR reference(s) — apply **analyze-code-change-history** first, then return here with its candidates
   - **Git history**: User provided commit range or references — apply **analyze-code-change-history** first, then return here with its candidates
   - **Mixed**: User provided multiple sources — process each with the appropriate path, then merge candidates

2. For chat sessions, **scan the conversation** for the three interactive signal types defined in **signal-detection-knowledge**:
   - Explicit user feedback (corrections, preferences, "remember this" statements)
   - AI self-discovered insights (reasoning that produced correct knowledge not in context)
   - Future-useful information (hard-won configuration, non-obvious workarounds, undocumented constraints)

3. For code-change sources, **delegate to analyze-code-change-history** to produce candidate lessons from the PR/git analysis.

4. **Exclude anti-signals** immediately — for each source type, filter out the anti-signals listed in **signal-detection-knowledge**.

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
   - Access to the PR diff(s) — either provided directly, via a PR link, or by running git commands to retrieve the diff
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

4. **Compare story vs implementation** using the **story-analysis-framework**:
   - For each analysis lens (missing capability, architectural decision, discovered constraint, etc.), ask: "Did the implementation reveal something the story didn't capture?"
   - Focus especially on the top three lenses (missing capability, architectural decision, discovered constraint) — these produce the strongest lessons
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

</rules>
