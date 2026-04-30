# Reverse Engineer: When Questions Example

## User Request
"When does the session token get refreshed in this application?"

## Response Process

### 1. Question Classification
- Question type: **When** — focus on timing, lifecycle events, and trigger conditions
- Scope: session/authentication lifecycle within the application

### 2. Search Strategy
- Semantic search for "token refresh", "session expiry", "token renewal"
- Grep for refresh-related method names: `refreshToken`, `renewSession`, `onTokenExpiry`
- Inspect lifecycle hooks, interceptors, and middleware files

### 3. Search Results

```
src/
├── infrastructure/auth/
│   ├── TokenRefreshInterceptor.java   ← HTTP interceptor checking expiry
│   └── AuthTokenService.java          ← refresh logic implementation
├── application/
│   └── security/SessionManager.java   ← session lifecycle orchestration
└── domain/auth/AccessToken.java       ← token expiry model
```

### 4. Trigger Conditions Found

```java
// TokenRefreshInterceptor.java — fires on every outgoing HTTP request
public boolean preHandle(HttpServletRequest request, ...) {
    AccessToken token = sessionManager.getCurrentToken();
    if (token.isExpiringSoon()) {          // within 5-minute threshold
        authTokenService.refresh(token);
    }
    return true;
}

// AccessToken.java — defines "expiring soon"
public boolean isExpiringSoon() {
    return Instant.now().isAfter(expiresAt.minus(5, ChronoUnit.MINUTES));
}
```

### 5. Initialization Sequence

```
Application startup
  → SessionManager.initialize()          (loads stored token from secure storage)

User login
  → AuthTokenService.issue()             (issues new token, sets expiresAt = now + 60 min)

Every outgoing HTTP request
  → TokenRefreshInterceptor.preHandle()  (checks isExpiringSoon)
      └─ if within 5-min window → AuthTokenService.refresh()
                                          (issues new token, resets expiresAt)

User logout
  → SessionManager.invalidate()          (clears token from memory and storage)

Token refresh failure (network error)
  → SessionManager.invalidate()          (forces re-login)
```

### 6. Answer

The session token is refreshed at **three moments**:

1. **On every outgoing HTTP request** — `TokenRefreshInterceptor` checks whether the token expires within the next 5 minutes; if so, `AuthTokenService.refresh()` is called transparently before the request proceeds. See [TokenRefreshInterceptor.java](src/infrastructure/auth/TokenRefreshInterceptor.java#L18-L28).

2. **Never proactively in the background** — there is no scheduled job or timer. Refresh is purely request-driven.

3. **Forced re-login on refresh failure** — if the refresh call fails (expired refresh token, network error), `SessionManager.invalidate()` clears the session and the user is redirected to the login screen. See [SessionManager.java](src/application/security/SessionManager.java#L45-L52).

**Key timing detail**: The 5-minute pre-expiry window is defined in [`AccessToken.isExpiringSoon()`](src/domain/auth/AccessToken.java#L31) and can be adjusted there. The access token itself has a 60-minute TTL set in [`AuthTokenService.issue()`](src/infrastructure/auth/AuthTokenService.java#L22).
