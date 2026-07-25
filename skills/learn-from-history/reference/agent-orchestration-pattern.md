# Agent Orchestration Patterns

Detailed patterns for dispatching analysis tasks to sub-agents, collecting results, and merging findings. Use when orchestrating multiple sub-agents for parallel analysis in the learn-from-history pipeline.

---

## Agent Detection Protocol

Before any analysis, scan the platform's agent registry. The detection mechanism varies by platform:

1. **List available agents**: Query the agent directory or registry for all available sub-agents.
2. **Filter by suitability**: Match each agent's description against the keyword sets below. An agent is suitable if its description contains at least one keyword from the relevant category.
3. **Record capabilities**: For each matching agent, note its name, description, and any tool restrictions (e.g., "read-only", "no file writes").

**Suitability keywords by task type**:

| Task type | Positive keywords (agent is suitable) | Negative keywords (agent is unsuitable) |
|---|---|---|
| Code analysis | "investigate", "review", "analyze code", "explore codebase", "discover patterns", "codebase exploration", "read-only" | "blog", "drawing", "prompt engineer", "skill creator" |
| Communication mining | "analyze text", "mine", "extract knowledge", "research", "chat analysis", "transcript" | (same exclusions) |
| General investigation | "investigate", "explore", "research", "analyze", "discover" | (same exclusions) |

---

## Prompt Templates by Agent Type

### Code Analysis Agent Prompt

Use when dispatching PR(s) + user story or git commit history to a code investigator/reviewer agent.

```
You are analyzing [PR(s) + user story / git commit history] to extract reusable lessons.

SOURCE MATERIAL:
[Full PR diff(s), story text, review comments, commit messages, and any additional context]

YOUR TASK: Scan this material for the following signal types:

**For PR(s) + user story:**
- Story-implementation gaps: Did the implementation reveal something the story didn't capture? Look for workarounds, architectural decisions, discovered constraints, unexpected dependencies.
- PR discussion insights: Do review comments or story threads surface constraints, rationale, or unwritten conventions?
- Implementation recipes: Is there a pattern in which files/repos are touched and in what order? Could a similar task follow this pattern?

**For git commit history:**
- Evolutionary patterns: Do commit messages reveal conventions that crystallized over time? Look for recurring verbs ("fix:", "refactor:", "migrate:"), repeated file paths, and sequences of related commits.
- Bug-fix clusters: Do fixes cluster around a specific area or pattern?

For each finding, produce a structured candidate lesson with:
1. **Summary**: One sentence describing the reusable lesson
2. **Evidence**: Quote or reference the specific source material (commit hash, file path, PR comment excerpt)
3. **Signal type**: Which of the above categories it matches
4. **Preliminary quality self-check**: Is it reusable across multiple future sessions? Is it non-obvious (not common knowledge)? Is it actionable (can be written as a concrete directive)? Does it appear to be undocumented?

Be conservative — flag borderline findings rather than missing them. The parent will apply a formal quality gate later.

CRITICAL: Return only your findings as structured text. Do NOT write to any files, do NOT modify any documents, and do NOT provision any lessons. Your output will be collected and processed by the parent skill.
```

### Communication Mining Agent Prompt

Use when dispatching chat transcripts (Slack, Teams, Discord) to a text analyst agent.

```
You are analyzing chat transcripts from [Slack/Teams/Discord] to extract reusable team knowledge.

SOURCE MATERIAL:
[Full chat transcript(s) with channel/thread context and any known focus areas]

YOUR TASK: Scan these transcripts for the following signal types:

- **Recurring questions**: The same question asked multiple times by different people. Indicates undocumented knowledge.
- **Decision records**: Threads where technical, architectural, or process decisions were reached informally but never formalized as ADRs.
- **Problem-solution pairs**: Someone reports a problem and someone else provides the fix or workaround. Each pair is a potential runbook entry.
- **Knowledge sharing**: Team members proactively sharing tips, tricks, or "TIL" moments.
- **Escalation patterns**: Certain topics consistently routing to the same person — reveals single points of knowledge.
- **Onboarding gaps**: New team members repeatedly asking the same setup, access, or process questions.
- **Procedural patterns**: Step-by-step descriptions of how to accomplish recurring tasks.

**Anti-signals to IGNORE**: Casual conversation, jokes, status updates, one-off resolved issues, operational chatter ("deploy done", "PR merged"), already-documented information, vague complaints without solutions.

For each finding, produce a structured candidate lesson with:
1. **Summary**: One sentence describing the reusable lesson
2. **Evidence**: Quote the transcript excerpt with channel/date context
3. **Signal type**: Which of the above categories it matches
4. **Frequency**: How many times did this pattern appear? (Single mention = weaker; 3+ mentions = stronger)
5. **Preliminary quality self-check**: Is it reusable? Non-obvious? Actionable? Undocumented?

Be conservative — flag borderline findings rather than missing them. The parent will apply a formal quality gate later.

CRITICAL: Return only your findings as structured text. Do NOT write to any files, do NOT modify any documents, and do NOT provision any lessons. Your output will be collected and processed by the parent skill.
```

### General Investigation Agent Prompt

Use when dispatching mixed or complex sources to a general-purpose investigation agent, or when the source type doesn't fit the above templates.

```
You are analyzing [describe source] to extract reusable lessons for a development team.

SOURCE MATERIAL:
[Full source material]

YOUR TASK: Scan this material for patterns, decisions, workarounds, constraints, conventions, or procedural knowledge that would be valuable for future work. Look for anything that:
- Would help someone encountering a similar situation
- Is not common knowledge for a developer with 2+ years in this stack
- Can be expressed as a concrete rule, fact, or step-by-step procedure
- Does not appear to be documented elsewhere in the project

For each finding, produce a structured candidate lesson with:
1. **Summary**: One sentence describing the reusable lesson
2. **Evidence**: Quote or reference the specific source material
3. **Signal type**: Best-fit category (story-implementation gap, evolutionary pattern, decision record, problem-solution pair, procedural pattern, implementation recipe, etc.)
4. **Preliminary quality self-check**: Is it reusable? Non-obvious? Actionable? Undocumented?

Be conservative — flag borderline findings rather than missing them.

CRITICAL: Return only your findings as structured text. Do NOT write to any files, do NOT modify any documents, and do NOT provision any lessons. Your output will be collected and processed by the parent skill.
```

---

## Result Merging and De-duplication

After all agents return, the parent merges results:

### De-duplication Algorithm

1. **Group by lesson essence**: For each pair of candidates (across agents), compute whether they describe the same underlying lesson. Two candidates are duplicates if:
   - They recommend the same action or document the same constraint
   - They reference the same code area, convention, or decision
   - Merging them would not lose information

2. **Merge duplicates**: When duplicates are found:
   - Keep one entry with the strongest evidence (most specific source reference)
   - Combine evidence excerpts from both agents
   - Note in the provision plan: "Discovered independently by [Agent A] and [Agent B]"

3. **Identify complements**: When two candidates describe different aspects of the same underlying issue:
   - Agent A found the pattern, Agent B found the rationale
   - Agent A found the constraint, Agent B found the workaround
   - Merge into a single, richer lesson entry

### Merge Output Format

After merging, produce a consolidated candidate table:

| # | Lesson Summary | Signal Type | Source Agent(s) | Evidence | Quality Pre-Assessment |
|---|---|---|---|---|---|
| 1 | ... | ... | Agent A, Agent B | ... | ... |

---

## Error Handling

| Failure mode | Response |
|---|---|
| Agent invocation fails (timeout, error) | Fall back to internal capability for that source type. Log the failure but don't block other agents. |
| Agent returns empty result | Treat as "no signals found" for that source. Proceed with results from other agents. |
| Agent returns malformed output | Attempt to extract any usable candidate lessons from the raw output. If nothing is salvageable, fall back to internal capability. |
| All agents fail | Fall back entirely to sequential internal analysis. |
| Agent writes to files despite instructions | Revert any unintended changes. Note the violation for future prompt refinement. |
