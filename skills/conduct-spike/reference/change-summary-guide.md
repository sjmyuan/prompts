# Change Summary Guide

A change summary bridges the gap between architectural decisions (ADRs, solution doc) and implementation. It translates the delta between current state (findings docs) and target state (solution doc) into concrete, actionable change items grouped by area or service.

## Purpose

- Gives stakeholders a clear view of implementation scope before committing resources.
- Provides a traceable link from each ADR decision to the code that must change.
- Helps identify cross-cutting concerns (e.g., a shared library change affects multiple services).
- Serves as input to project planning and effort estimation — but is NOT a detailed implementation plan or task breakdown.

## When to produce

Produce the change summary after the solution document is finalized. It is an optional artifact — ask the user whether they want it. Skip when:
- The spike is purely exploratory and no implementation is planned yet.
- The solution is trivial (single service, few changes).
- The user explicitly declines.

## Relationship to other artifacts

| Artifact | Role in change summary |
|---|---|
| Findings documents | Define the baseline — what exists today. Changes are derived by diffing against this. |
| ADRs | Each ADR's chosen option drives a cluster of changes. Cite the ADR number for each change cluster. |
| Solution document | Defines the target state. The change summary lists what must happen to get there. |

## Change categories

Group each change into one of these categories for consistent structure:

| Category | Description | Example |
|---|---|---|
| **New** | Code, services, or modules that must be created from scratch | New `WalletPaymentService` microservice |
| **Modified** | Existing code that must be changed | Refactor `PaymentOrchestrator` to delegate to new services |
| **Retired** | Code to deprecate, delete, or archive | Remove `BankTransferService` from monolith after extraction |
| **Configuration** | Environment variables, feature flags, CI/CD, infrastructure-as-code | Add Kafka topic definitions to Terraform |
| **Data** | Schema changes, migrations, data transforms | Split `transactions` table; create per-service databases |
| **Dependency** | New libraries, frameworks, or external services to adopt | Add Kafka client library; provision Kafka cluster |
| **Test** | New or updated test suites needed | Integration tests for inter-service async communication |

## Format

```markdown
# Change Summary: [Spike Goal]

## Area: [Area Name] (ADR-00X)

### New
- **[Service/Module Name]**: [Brief description of what to create and why.]
  - Scope: [estimated files/packages — or "needs code access to estimate"]
  - Depends on: [ADR refs, other change clusters]

### Modified
- **[Existing Code Path]**: [What changes and why.]
  - Scope: [estimated files/packages]
  - Risks: [any notable risk]

### Retired
- **[Code to remove]**: [When and how to retire it.]

### Configuration
- **[Config change]**: [What env/infra/config changes are needed.]

### Data
- **[Data change]**: [Schema migration, data transform needed.]

### Dependency
- **[New dependency]**: [Library, framework, or service to adopt.]

### Test
- **[Test need]**: [What new or updated tests are required.]

---

## Cross-Cutting Concerns

[Changes that span multiple areas — shared library updates, infrastructure provisioning, etc.]

## Notes

- [Any caveats, assumptions, or open questions about the change scope.]
```

## Code access

The quality of the change summary depends on whether the current codebase is accessible:

- **With code access**: Trace the code paths identified in findings documents. Estimate scope concretely (files, packages, LOC ranges). Identify specific classes/functions to modify.
- **Without code access**: Describe changes at the architectural level based on findings and solution docs. Mark scope estimates as unverified. Note where code access would improve accuracy.

Always be transparent with the user about whether scope estimates are code-verified or architectural approximations.

## Keeping it current

The change summary is **never final**: it derives from the delta between findings (baseline) and the solution doc (target). Whenever either changes — new evidence, findings correction, ADR decision change, deep-dive — recompute the affected clusters via **sync-update-artifacts** (see `artifact-sync-guide.md`) so the summary always reflects the current artifacts.
