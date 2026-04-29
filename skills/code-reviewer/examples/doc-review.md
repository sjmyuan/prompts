````markdown
# Example: Document Review (README)

**Scenario**: Review of `services/payment-service/README.md` for a new microservice being onboarded to the platform.

**Review Focus**: Structure, clarity, completeness, and accuracy for developer onboarding.

## Code Review Summary

**Scope**: `services/payment-service/README.md` — new microservice README
**Focus Areas**: Structure, completeness, accuracy, audience alignment
**Overall Assessment**: Needs work before the service is onboarded — critical setup steps are missing and one command is incorrect.

---

## Findings

### 🔴 Major Issues

#### Missing Prerequisites Section
- **File**: [README.md](README.md)
- **Issue**: No prerequisites section. The README jumps straight to "Getting Started" without listing required tools (Java 21, Docker, AWS CLI, etc.). A developer without those tools will hit cryptic errors before reading a single line of service code.
- **Impact**: Onboarding friction; developers waste time debugging missing tools rather than running the service.
- **Recommendation**: Add a **Prerequisites** section before "Getting Started":
```markdown
## Prerequisites
- Java 21 (install via `sdk use java 21`)
- Docker ≥ 24.0
- AWS CLI v2 configured with the `dev` profile
- Access to the internal package registry (see [confluence/registry-access](…))
```

#### Incorrect `docker-compose` Command
- **File**: [README.md](README.md#L34)
- **Issue**: The "Local Development" section uses `docker-compose up` but the project uses Compose V2 (`docker compose up`). The legacy command fails silently on macOS with Docker Desktop ≥ 4.18.
- **Impact**: Local setup fails on all modern developer machines; the error message is unrelated to the root cause.
- **Recommendation**: Replace every `docker-compose` occurrence with `docker compose` and add a note on the minimum Docker Desktop version required.

---

### 🟡 Minor Issues

#### Environment Variable Table Is Incomplete
- **File**: [README.md](README.md#L52-L65)
- **Issue**: The config reference table lists 8 variables but `application.yaml` declares 12. `PAYMENT_RETRY_MAX_ATTEMPTS`, `PAYMENT_TIMEOUT_MS`, `STRIPE_WEBHOOK_SECRET`, and `DB_POOL_SIZE` are absent.
- **Impact**: Developers miss required configuration and encounter startup failures with no guidance on what is missing.
- **Recommendation**: Audit `application.yaml` and synchronize the README table. Consider generating the table from code comments to prevent future drift.

#### "Deployment" Section Describes the Old Pipeline
- **File**: [README.md](README.md#L80-L95)
- **Issue**: The deployment section references Jenkins pipeline steps, but the project migrated to GitHub Actions in Q3 2025. The Jenkins URL is no longer valid.
- **Impact**: Confusing for anyone following the deployment runbook; could lead to failed or duplicate deployments.
- **Recommendation**: Update to describe the GitHub Actions workflow (`.github/workflows/deploy.yml`) and remove all Jenkins references.

---

### 🟢 Nits / Suggestions

- The "Architecture" diagram (ASCII art on line 22) is helpful but hard to read at scale — consider replacing with a Mermaid diagram for automatic rendering in GitHub.
- Section headings are inconsistently capitalized: "Getting Started" vs "local development" vs "API Reference" — standardize to title case throughout.
- The "Contributing" section is a single line linking to a global `CONTRIBUTING.md` — fine for a shared doc, but verify the link is not broken.

---

## Positive Highlights
- The API reference table (endpoints, methods, descriptions) is well-structured and covers all public routes.
- The troubleshooting section with common errors and fixes is a strong onboarding aid — this kind of section is frequently missing in microservice READMEs.
- Clear separation between "local development" and "integration testing" environments reduces confusion about which setup to follow.

---

## Risks & Assumptions
- Review is based on the README alone; accuracy of commands was cross-checked against `docker-compose.yml` and `application.yaml` but not against actual runtime behavior.
- The environment variable gap may indicate the README is not updated as part of the feature workflow — a process gap, not just a one-time fix.

---

## Recommended Next Steps
1. Add Prerequisites section (required before service onboarding)
2. Fix `docker-compose` → `docker compose` command (required — blocks local setup on modern machines)
3. Complete the environment variable table (required — blocks successful startup)
4. Update Deployment section to reflect the GitHub Actions pipeline (required)
5. Standardize heading capitalization (minor polish)
6. Consider adding a PR checklist item: "Did you update the README?" to prevent future drift

---

## Key Review Characteristics

- **Review Type**: Document review (README)
- **Severity Distribution**: 2 major, 2 minor, 3 nits
- **Primary Concerns**: Missing prerequisites, incorrect commands, incomplete environment variable table, stale deployment instructions
- **Action Required**: Fix major issues before onboarding the service
- **Testing Recommendation**: Have a developer unfamiliar with the service attempt to onboard using only the README and report any friction points
````
