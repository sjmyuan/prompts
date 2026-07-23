# Example: User Feedback Becomes a Rule

**Applies**: `detect-learning-signals` → `determine-provision-target` → `generate-provision-plan` → `review-and-apply`

**Scenario**: During a coding session, the user corrects the AI about a project convention. The user wants this preserved so the AI doesn't repeat the mistake.

---

## Input (Conversation Excerpt)

```
User: Can you add error handling to the API route?

AI: Sure, I'll wrap it in a try-catch and return a 500 with the error message.

User: No — in this project we never expose raw error messages in API responses.
      Always return a sanitized "Internal server error" message and log the real error
      with the request ID. Remember this.

AI: Understood. I'll use sanitized messages and log the real error with request ID.
```

Later, user says: "Learn from this session and save what's worth keeping."

---

## Step 1: detect-learning-signals

**Source type**: Chat session

**Signal detected**: Explicit user feedback — the user stated a project-specific rule ("we never expose raw error messages") and explicitly said "Remember this."

**Signal type**: Explicit user feedback

**Quality gate evaluation**:

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Applies to ALL API routes in this project, not just this one |
| Non-obviousness | ✅ Pass | Many projects do expose error messages; this is a specific convention |
| Actionability | ✅ Pass | Can be written as a clear directive |
| Non-duplication | ✅ Pass | Not found in current context (checked project notes, no such rule) |
| Specificity | ✅ Pass | Specific: "sanitized message + log with request ID"; general: applies to all routes |

**Verdict**: ACCEPT — candidate lesson passes all dimensions.

---

## Step 2: determine-provision-target

**Platform detection**: This platform supports project-level persistent notes (workspace conventions).

**Classification**: Project-specific convention → project-level persistent notes.

**Rationale**: This is a codebase-wide rule, not a personal preference (not personal notes). It's not domain-specific knowledge for a particular skill — it's a general project convention. The most appropriate target is project-level notes under a conventions section.

**Target**: Project conventions file (create if not exists), under a new "API Design" section.

---

## Step 3: generate-provision-plan

| # | Lesson Summary | Signal Type | Target File | Section | Content to Add |
|---|---|---|---|---|---|
| 1 | API error responses must use sanitized messages; real errors logged with request ID | User feedback | Project conventions | API Design | "Never expose raw error messages in API responses. Return a sanitized 'Internal server error' message and log the real error with the request ID." |

**Rationale**: This is a project-wide convention, not skill-specific or personal. Project-level notes ensure it's loaded in all sessions within this workspace.

---

## Step 4: review-and-apply

Present to user:

> **Lesson to preserve:**
>
> *API error responses must use sanitized messages; real errors logged with request ID.*
>
> **Target**: Project conventions → API Design section
>
> **Content to add**:
> > Never expose raw error messages in API responses. Return a sanitized 'Internal server error' message and log the real error with the request ID.
>
> Approve / Modify / Reject?

User approves → write to project conventions.
