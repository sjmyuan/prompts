# Example: Raising Challenges on a Returned Result

**Scenario**: A sub-agent reported that the auth token cache is invalidated on password change, citing `TokenCacheService.java:42`. The result will be consumed downstream, so the agent applies the skeptic's questioning — nothing is verified yet; the challenges are handed to the orchestrator.

Applies **question-the-result**.

## Input / Context
- **Returned result**: "Password change invalidates cached tokens — `TokenCacheService.java:42` calls `cache.invalidate(userId)`."
- **Stakes**: security audit; a wrong claim could mask a real token-leak vulnerability.

## Questioning (question-the-result)
1. **Completeness** — Does the claim cover ALL token-issuing paths, or only the one in `TokenCacheService`? What about tokens issued via the refresh flow?
2. **Correctness** — Does the cited line exist and do what is claimed? Is `invalidate(userId)` reachable from every password-change path?
3. **Ambiguity** — "invalidates cached tokens" — all token types (access/refresh) or one? Is the cache keyed by `userId` or by token?
4. **Evidence** — Is the call reachable from the password-change controller, or dead code?

## Output — prioritized challenges (raised, not yet verified)
- **C1 (Correctness, high)** — Verify `TokenCacheService.java:42` exists and is reachable from the password-change flow.
- **C2 (Completeness, high)** — Verify whether the refresh-token path also checks the same cache; if not, the claim is incomplete.
- **C3 (Ambiguity, medium)** — Clarify whether invalidation covers both access and refresh tokens.
