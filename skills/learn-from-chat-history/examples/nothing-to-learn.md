# Example: Nothing Worth Learning

**Applies**: `detect-learning-signals` (terminates early when quality gate rejects all candidates)

**Scenario**: User asks the AI to learn from a session. The conversation was a routine bug fix with no reusable insights. The quality gate rejects every candidate.

---

## Input (Conversation Excerpt)

```
User: The login page has a typo — it says "pasword" instead of "password".

AI: Found it on line 47 of login.tsx. I'll fix it.

User: Thanks. Also, can you add a test for the email validation function?

AI: Sure. The function is in utils/validation.ts. I'll add a test case for it.

User: Great. Now, learn from this session and save what's worth keeping.
```

---

## Step 1: detect-learning-signals

**Scan for signals**:
- No explicit user feedback with rules/preferences (user didn't say "remember this" or "always do X")
- No AI self-discovered insights (the typo was user-reported; the test was straightforward)
- No future-useful information (typo fixes are one-off; adding a test for an existing function is routine)

**Anti-signals identified**:
- "Fix typo on line 47" — one-off fix, specific to one line → REJECT (Reusability)
- "Add test for email validation" — routine task, any developer would know to do this → REJECT (Non-obviousness)
- "The typo was in login.tsx" — session-specific state → REJECT (Reusability)

**Quality gate**: All candidates rejected at Reusability or Non-obviousness stage.

---

## Output

> **No lessons worth learning from this session.**

The conversation covered routine bug fixes and standard development tasks. No reusable knowledge, non-obvious insights, or generalizable rules were identified. The quality gate rejected all candidates — this is expected and correct.

If you believe I missed something worth preserving, let me know specifically what you'd like to capture.
