# Signal Detection Catalog

Five signal types indicate a potential lesson — three from interactive sources (chat) and two from code-change sources (PRs, git history).

## Interactive Sources (Chat Sessions)

### 1. Explicit user feedback
The user states a preference, rule, or correction:
- "Remember this for next time…"
- "Actually, the correct way is…"
- "From now on, always use X instead of Y…"
- "This is the pattern we follow…"
- User corrects the AI and the AI acknowledges the correction

### 2. AI self-discovered insight
The AI independently arrives at correct knowledge not in current context:
- AI reasons through a problem and discovers a correct approach that contradicts or extends existing context
- AI identifies a gap in knowledge and fills it through inference or external lookup
- AI synthesizes multiple pieces of information into a new, reusable rule
- The insight was NOT already in the loaded skills, agent files, memory, or docs

### 3. Future-useful information
Information surfaced that would benefit future sessions:
- A non-obvious workaround for a known limitation
- A project-specific convention discovered through trial and error
- A configuration detail that took significant effort to determine
- A dependency or compatibility constraint that isn't documented elsewhere

## Code-Change Sources (PRs, Git History)

### 4. Story-implementation gap
When comparing a user story to its PR implementation, a meaningful divergence emerges:
- The story assumed a capability that doesn't exist in the codebase and required a workaround
- A non-obvious architectural decision was made during implementation that future similar stories should follow
- The implementation surfaced a constraint (library limitation, performance boundary, API restriction) not mentioned in the story
- A recurring implementation pattern emerged across multiple PRs for the same story type
- The story was implemented differently than described because of a discovered requirement — this is the most valuable signal

**PR and story comments as a gap-discovery source**: Review discussions and story comment threads are rich signals that the code diff alone misses:
- A reviewer asks "why didn't you use X approach?" and the author replies with a constraint that isn't documented anywhere
- Story comments clarify scope or assumptions that weren't in the original story text — these clarifications themselves are reusable knowledge
- A long discussion thread on a specific design choice often contains the WHY behind an architectural decision
- Reviewers consistently flag the same kind of issue across multiple PRs — this is an unwritten convention ready to be codified
- "LGTM but next time do Y" comments surface forward-looking conventions

### 5. Evolutionary pattern
When scanning git commit history, recurring themes indicate codified knowledge:
- A refactoring pattern appears multiple times across different modules (e.g., "extract X to shared utility")
- Commit messages reveal a convention that evolved over time (e.g., "migrate all X to Y pattern")
- Bug-fix commits cluster around a specific area or pattern (e.g., repeated null-check additions after API calls)
- A sequence of commits tells a story of how a particular problem was solved incrementally, with lessons at each step

## Communication Tool Sources (Slack, Teams, Discord, etc.)

Chat transcripts from communication tools contain tribal knowledge that often never makes it into formal documentation. These signals are distinct from interactive chat-session signals (which involve the AI) — here the AI is an observer mining people's conversations.

### 6. Recurring question pattern
The same question asked multiple times by different people across channels or over time:
- A specific error message or failure mode keeps appearing in #support or #backend
- Multiple people ask "how do I set up X?" or "what's the process for Y?"
- Answers converge on the same solution each time — this is a candidate for documentation or automation
- **Signal strength**: High — indicates a documentation gap causing repeated interruption

### 7. Decision record
A thread where a technical, architectural, or process decision was reached informally:
- A Slack thread that ends with "ok let's go with option B then" but no ADR was written
- Design decisions made in DMs or channel discussions that affect future work
- Scope or requirement decisions made in chat that never reached the story/ticket
- **Signal strength**: High — decisions without records create confusion and inconsistency later

### 8. Problem-solution pair
Someone reports a problem and someone else provides the fix or workaround:
- A thread like "I'm getting error X when deploying" → "oh, you need to set env var Y first"
- Non-obvious troubleshooting steps that rely on a specific person's knowledge
- Workarounds for known limitations that aren't documented in the codebase or runbooks
- **Signal strength**: High — each pair is a potential runbook entry or FAQ item

### 9. Knowledge sharing
A team member proactively shares a tip, trick, or "TIL":
- "PSA: you can use command X to debug Y" in a channel
- A better approach to a common task shared by an experienced team member
- Links to external resources with context about how they apply to this project
- **Signal strength**: Medium — useful but may already be known by some team members

### 10. Escalation pattern
Certain topics or questions consistently route to the same person:
- "@alice can you help with the database migration?" appears across many threads
- Reveals single points of knowledge — useful for bus-factor awareness and onboarding
- Indicates areas where knowledge transfer or documentation is needed
- **Signal strength**: Medium — more about who-knows-what than what-to-do

### 11. Onboarding gap
New team members consistently ask the same setup, access, or process questions:
- "How do I get access to the staging environment?"
- "Which repo has the API definitions?"
- "Who do I talk to about X?"
- **Signal strength**: Medium — indicates stale or missing onboarding docs

## Anti-Signals (do NOT treat these as lessons)

### From interactive sources:
- Trivial facts any competent developer would know
- One-off fixes specific to a single line of code
- Information already documented in loaded context
- Session-specific state (e.g., "we're working on file X right now")
- Temporary workarounds that shouldn't be repeated

### From code-change sources:
- Trivial diff-only changes (typo fixes, formatting, import reordering)
- A PR that implements the story exactly as described with no surprises or decisions — no gap means no lesson
- Boilerplate additions (new route with standard CRUD, new component matching existing pattern exactly)
- Changes that merely replicate an already-documented pattern elsewhere in the codebase
- Single, isolated commits with no connection to a larger pattern

### From communication tool sources:
- Casual conversation, jokes, social chat, emoji reactions
- One-off issues resolved once and never seen again
- Status updates, standup notes, meeting scheduling chatter
- Purely operational messages ("deploy done", "PR merged", "build passed")
- Information already captured in existing documentation, runbooks, or ADRs
- Vague complaints without a concrete solution or action
- Personal discussions unrelated to project work
