# Example: Configuration Bug Fix

**Scenario**: Application fails to start in production because a required environment variable for the database connection pool size is missing, causing the server to fall back to the default of 1 and time out under load

---

## Root Cause Identification

Applies **identify-bug-root-cause**.

**User reports:**
> “The production deployment is timing out under moderate load. Locally it’s fine. We noticed the pool size looks wrong in the logs.”

**Agent gathers information** — reads `DatabaseConfig.java`, `application-production.yml`, and deployment manifests. Finds: `DB_POOL_SIZE` is read via `${DB_POOL_SIZE:1}` — a Spring default of `1` silently takes effect when the variable is absent. The production deployment manifests do not declare `DB_POOL_SIZE`.

**Agent asks:**
> 1. Was `DB_POOL_SIZE` ever set in the production environment, or was it always missing?
> 2. What is the expected pool size for production — is there a documented value?

**User responds:**
> It was never set; the team assumed the app would error if it was missing. Expected size is 20.

**Agent confirms root cause:**
> `DB_POOL_SIZE` is not declared in the production deployment configuration. The Spring placeholder default of `1` silently applies, causing connection starvation under any real load. Two fixes: (1) add the variable to the production config with the correct value, (2) replace the silent default with a fail-fast startup check so missing config is caught immediately.

*User confirms: ✅*

---

## Bug-Fixing Plan (Adapted TDD — Validate with Build/Run)

Applies **plan-bug-fix**.

**Root Cause**: `DB_POOL_SIZE` environment variable is not declared in the production deployment configuration; the application reads it at startup but has no validated default and no startup error

## Steps

- **Step 1**: Validate Baseline (run existing tests, linting, type-checking)
- **Step 2**: Add startup validation test — verify app throws a descriptive error when `DB_POOL_SIZE` is missing or non-numeric
- **Step 3**: Confirm Test Failure
- **Step 4**: Fix Code — add required variable declaration to `config/production.env.example` and add a validated startup check that throws on missing/invalid value
- **Step 5**: Verify Fix — re-run tests; start app locally with and without the variable to confirm the error message is clear
- **Step 6**: Clean Up Unused Code — remove any silent fallback that allowed the bad default to go undetected
- **Step 7**: Clean Up Tests — remove tests that asserted the old silent-fallback behavior
- **Step 8**: Verify Cleanup
- **Step 9**: Validate Linting, Formatting and Type Checking

## Key Characteristics

- **Complexity**: Simple (single configuration entry point)
- **Approach**: Adapted TDD — validate with build/run rather than unit tests; startup validation test replaces the standard test-first cycle
- **Focus**: Configuration completeness and fail-fast startup behavior
- **Rationale for Adaptation**: Configuration bugs are confirmed by running the application with and without the variable; a targeted startup validation test provides coverage without requiring a full integration environment
