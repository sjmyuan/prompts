---
name: learn-from-history
description: Extract reusable knowledge, rules, and procedures from chat sessions, PRs, git history, and team transcripts. Use when distilling lessons, analyzing change history, mining chat, extracting procedures, checking for insights, or refining skills/agents/memory.
---

<when-to-use-this-skill>
- Extract and preserve reusable lessons from the current chat session
- Explicit feedback or AI-discovered patterns should become a permanent rule or knowledge entry
- Learn from a user story with its PR(s), or from git history — extract patterns, constraints, decisions, recipes
- Mine chat history (Slack, Teams, Discord) for team knowledge, decisions, or patterns
- Update a skill, agent file, doc, or memory with historical insights
- Extract step-by-step procedures or implementation recipes, or refine a capability with newly discovered procedural knowledge
</when-to-use-this-skill>

<knowledge>

<core-principle>
Not every interaction yields a lesson worth preserving. A valid lesson applies across future sessions — not a one-off fix or trivial observation. When nothing qualifies, report "nothing worth learning".
</core-principle>

<lesson-type-concepts>
Lessons have two forms, by structure:

| Lesson form | Structure | Provisioned as | Routed through |
|---|---|---|---|
| **Rule / fact** | One-sentence directive or fact | Knowledge section of target | Directly to **provision-lessons** |
| **Procedure (capability)** | Ordered multi-step sequence with parameters and branches | Named capability, per the format template | **extract-and-refine-capability**, then **provision-lessons** |

**Decision rule**: one sentence → rule; ordered steps, parameters, or branches → procedure. When in doubt, default to procedure.
</lesson-type-concepts>

<agent-orchestration>
Sub-agents parallelize analysis; the parent keeps the quality gate, merging, de-duplication, provisioning. Load [reference/agent-orchestration-pattern.md](reference/agent-orchestration-pattern.md) for mapping, detection, prompt templates, merge, fallback.
</agent-orchestration>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Text/code extraction | Playbook | [reference/extraction-playbook.md](reference/extraction-playbook.md) |
| Feedback → rule | Example | [examples/user-feedback-to-rule.md](examples/user-feedback-to-rule.md) |
| AI insight | Example | [examples/ai-discovered-insight.md](examples/ai-discovered-insight.md) |
| Nothing qualifies | Example | [examples/nothing-to-learn.md](examples/nothing-to-learn.md) |
| User-specified target | Example | [examples/user-specified-target.md](examples/user-specified-target.md) |
| Story + PR | Example | [examples/pr-story-gap-discovery.md](examples/pr-story-gap-discovery.md) |
| Git history | Example | [examples/git-history-pattern.md](examples/git-history-pattern.md) |
| Procedure from chat | Example | [examples/procedural-discovery.md](examples/procedural-discovery.md) |
| Recipe from PRs | Example | [examples/implementation-recipe.md](examples/implementation-recipe.md) |
| Multi-source | Example | [examples/multi-agent-orchestration.md](examples/multi-agent-orchestration.md) |
| Capability checks | Checklist | [reference/capability-quality-checklist.md](reference/capability-quality-checklist.md) |
| Formatting a capability | Template | [reference/capability-format-template.md](reference/capability-format-template.md) |

</context-loading-guide>

<signal-types>
Signals span four source categories — interactive (chat), code-change (PRs, git), communication tools (Slack, Teams, Discord), procedural (any source) — plus anti-signals. Load [reference/signal-detection-catalog.md](reference/signal-detection-catalog.md) when scanning.
</signal-types>

<quality-gate>
Every candidate must pass all five dimensions; a single failure rejects it. Load [reference/quality-rubric.md](reference/quality-rubric.md) before scoring.
</quality-gate>

<story-analysis>
Compare a story against its PR with [reference/story-analysis-framework.md](reference/story-analysis-framework.md) — eight lenses; the top four give the strongest lessons.
</story-analysis>

</knowledge>

<capabilities>

<detect-learning-signals>
**Objective**: Master entry point — detect sub-agents, scan sources for candidates, delegate to agents or internal analysis, gate, verify, classify by form, route to provisioning.
**Steps**:
1. **Detect available sub-agents**: scan the platform's agent registry against the source-type → agent mapping (agent-orchestration knowledge). Record matches; if none, use internal capabilities.
2. **Choose execution mode** by source:

| Source type | Execution mode |
|---|---|
| Small chat session | Scan interactively (step 4) |
| PR + story, or git | Code-analysis agent if present, else **analyze-code-changes** |
| Communication transcripts | Text-analysis agent if present, else **analyze-communication-history** |
| Mixed sources | Parallel agents per source if available, else sequential |
| Cross-referenced (story + PR) | One agent with ALL inputs, or internal analysis |

3. **Dispatch to agents**: build each brief per the prompt template in reference/agent-orchestration-pattern.md — source, signal types, structured output, no-file-writes. Dispatch in parallel; collect; merge by de-duplicating and combining complementary findings; tag each candidate with its source.
4. **Scan chat sessions interactively**: load reference/signal-detection-catalog.md; look for feedback, AI insights, future-useful info, described procedures.
5. **Exclude anti-signals**: drop trivial facts, one-off fixes, already-documented info, session state, boilerplate. Lighter pre-filter on agent-produced candidates.
6. **Apply the quality gate**: load reference/quality-rubric.md; score all five dimensions; a single failure rejects.
7. **If no candidates pass**: report "No lessons worth learning from this [source]" and stop — never fabricate lessons.
8. **Verify agent-sourced candidates**: before provisioning, confirm evidence against the primary source; if unconfirmed, re-derive with a NEW same-type agent or reject.
9. **Classify by form**: one-sentence directive or fact → `form: rule`; requires steps, parameters, or branches → `form: procedure` (default when in doubt).
10. **Route by form**: rules → **provision-lessons** directly; procedures → **extract-and-refine-capability** first, then all → **provision-lessons**.
</detect-learning-signals>

<analyze-code-changes>
**Objective**: Analyze PRs (with stories) and git history for reusable patterns, constraints, decisions, and recipes.
**Steps**:
1. **Identify the source type**: PR(s) + story → steps 2–5; git history → steps 6–9. For any PRs, also run step 10.
2. **Gather PR inputs**: story text, story comments, PR diff(s), review comments, additional context.
3. **Parse the user story**: requirements, implicit assumptions, acceptance criteria, scope.
4. **Analyze the PR changes**: file roles, change nature, commit rationale, added/removed lines, tests, review comments.
5. **Compare story vs implementation**: load reference/story-analysis-framework.md; apply its top four lenses (missing capability, architectural decision, discovered constraint, PR discussion); ask "did the implementation reveal something the story missed?" Draft candidates: expected vs actual, gap cause, next-time action.
6. **Gather git inputs**: commit range, messages, diffs.
7. **Scan commit messages for themes**: recurring verbs, repeated paths, related sequences.
8. **Analyze representative diffs** for interesting clusters: applied pattern, one-off vs trend, WHY in messages.
9. **Identify evolutionary patterns**: crystallized conventions, recurring bug fixes, refactoring arcs. Formulate as: pattern, lesson, evidence (commits).
10. **Flag implementation-recipe signals**: if a similar task would follow the same file/repo sequence, flag as recipe (signal #13) with raw evidence — repos, per-repo files, change order, dependency order. Do NOT format here; tag `form: procedure`.
11. **Apply quality pre-filter**: check already-documented, actionable, non-trivial. Return candidates to **detect-learning-signals** with summaries, references, pattern type, form tags, raw evidence, preliminary quality.
</analyze-code-changes>

<analyze-communication-history>
**Objective**: Parse chat transcripts (Slack, Teams, Discord, etc.) for reusable team knowledge, decisions, and patterns.
**Steps**:
1. **Gather inputs**: chat transcript(s), channel/thread context, focus area.
2. **Scan the transcripts**: load reference/signal-detection-catalog.md; look for recurring questions, decisions, problem-solution pairs, knowledge sharing, escalation, onboarding gaps.
3. **Exclude anti-signals**: casual conversation, one-off resolved issues, already-documented info, status updates, operational chatter.
4. **Cluster related signals**: group the same topic across threads — 5 mentions beat 1.
5. **Formulate candidate lessons**: pattern, evidence (transcript excerpts), lesson (what to document, where, for whom).
6. **Return candidates** to **detect-learning-signals** for quality gating.
</analyze-communication-history>

<extract-and-refine-capability>
**Objective**: Transform raw procedural candidates into structured capabilities — described procedures (text path) and implementation recipes (code path) — and refine overlapping capabilities into abstractions.
**Steps**:
1. **Identify the candidate type**: described procedure (signal #12, steps in text) → text path; implementation recipe (signal #13, steps inferred from code changes) → code path. Same-type PRs → process together.
2. **Run the matching path**: load reference/extraction-playbook.md; follow its text-path, code-path, or refine-phase steps.
3. **Return** the formatted capability (or multi-level set, or refined capability) to **detect-learning-signals** for routing.
</extract-and-refine-capability>

<provision-lessons>
**Objective**: Classify lessons by target, produce a reviewable plan, get user approval, and apply changes.
**Steps**:

**Classify phase**:
1. **Detect platform capabilities**: identify available persistent-context mechanisms. Load reference/context-target-catalog.md for target types and suitability.
2. **Classify each lesson**: honor a user-specified target if given; otherwise map per reference/context-target-catalog.md — preference → personal notes; convention → project notes; domain knowledge → skill file; agent behavior → agent file; doc fact → README/ADR; procedure → skill or project notes. Pick the most specific, discoverable target.

**Plan phase**:
3. **Draft the exact content** per target format with source evidence. Table: #, Lesson, Signal Type, Target, Section, Content; include rationale and files needing creation.

**Review phase**:
4. **Present the complete plan** for batch review; per lesson the user chooses Approve, Modify, or Reject. **Do NOT apply any changes until the user explicitly confirms.**

**Apply phase**:
5. **Apply approved lessons**: read the target, insert into the correct section, create files if needed; for skills follow conventions (facts → knowledge, routing → rules, steps → capabilities).
6. **Apply modified lessons**: apply adjustments, re-confirm before writing.
7. **Summarize** what was added and where. If all were rejected or none passed the gate, acknowledge it — do not force a lesson.
</provision-lessons>

</capabilities>

<rules>
<rule>User asks to learn from any source (chat session, PRs+story, git history, communication transcripts) → apply **detect-learning-signals**. It dispatches in parallel when suitable agents exist, or falls back to **analyze-code-changes** / **analyze-communication-history**. The parent controls the quality gate and provisioning.</rule>

<rule>Qualifying lessons → route `form: procedure` candidates through **extract-and-refine-capability**, then all lessons to **provision-lessons**. Never apply changes without explicit user confirmation.</rule>
</rules>
