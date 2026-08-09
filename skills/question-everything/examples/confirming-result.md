# Example: Verification Confirms the Original Result (Accept)

**Scenario**: A coding sub-agent reported that the auth token cache is invalidated on password change, citing `TokenCacheService.java:42`. The result feeds a security audit, so the orchestrating agent runs the skeptic loop before accepting it.

Applies **question-the-result** → **verify-the-claims** → **accept-or-requestion**.

## Input / Context
- **Original sub-agent result**: "Password change invalidates cached tokens — `TokenCacheService.java:42` calls `cache.invalidate(userId)`."
- **Stakes**: security audit; a wrong claim could mask a real token-leak vulnerability.

## Questioning (question-the-result)
1. **Completeness** — Does the claim cover ALL token-issuing paths, or only the one in `TokenCacheService`? What about tokens issued via the refresh flow?
2. **Correctness** — Does the cited line exist and do what is claimed? Is `invalidate(userId)` actually reachable from every password-change path?
3. **Ambiguity** — "invalidates cached tokens" — all token types (access/refresh) or one? Is the cache keyed by `userId` or by token?
4. **Evidence** — Is the call reachable from the password-change controller, or dead code?

Prioritized challenges:
- **C1 (Correctness, high)** — Verify `TokenCacheService.java:42` exists and is reachable from the password-change flow.
- **C2 (Completeness, high)** — Verify whether the refresh-token path also checks the same cache; if not, the claim is incomplete.
- **C3 (Ambiguity, medium)** — Clarify whether invalidation covers both access and refresh tokens.

## Verification (verify-the-claims)
A NEW coding agent (same type as the original, not the original instance) is dispatched with the original claims plus C1–C3, instructed to answer from the codebase only.

## Comparison (accept-or-requestion)
- **C1** — AGREE: `TokenCacheService.java:42` matches; the controller calls it on password change.
- **C2** — AGREE: the refresh path re-validates the same cache key; the claim is complete.
- **C3** — AGREE: invalidation clears both access and refresh entries.

All material verdicts AGREE → **result accepted**. The security audit proceeds with the claim as verified.
