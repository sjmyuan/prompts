# Solution Document Modularity Guide

Large solution documents become unwieldy for both humans and AI. When AI fetches context, loading a monolithic 50-page document wastes tokens and attention on irrelevant sections. This guide defines when and how to split a solution document into modular, independently-loadable pieces.

## Why modularity matters

- **Efficient AI context loading**: The agent can load only the section relevant to the current task (e.g., just the API contract for a specific service, not the entire infrastructure section).
- **Independent updateability**: When one service's API contract changes, only its extracted document needs updating — not the entire solution doc.
- **Parallel review**: Different reviewers can focus on different sections concurrently.

## When to split

Apply these heuristics during `compile-solution-doc` after producing the initial solution document:

| Signal | Action |
|---|---|
| Solution doc exceeds ~3000 words or 5+ major sections | Assess for modularity |
| A section is self-contained and references no other sections for core understanding | Candidate for extraction |
| A section would be useful as a standalone reference during implementation (e.g., API contracts, infrastructure topology) | Strong candidate for extraction |
| Two sections are developed or reviewed by different teams | Split along team boundaries |
| A section contains detailed listings (endpoints, schemas, config values) that are mostly reference material | Extract to keep main doc narrative-focused |

## When NOT to split

- **Single-service or simple solutions**: A single document is clearer.
- **Highly cross-referencing sections**: If extracting a section would require the reader to constantly jump back to the main doc, keep it inline.
- **Narrative-dependent sections**: If a section's meaning depends on reading the preceding section in sequence, keep them together.

## Splitting patterns

### Pattern 1: By service (recommended for multi-service architectures)

```
solution-overview.md           # Hub: C4 System/Container diagrams, decisions summary, RAID, RACI
├── service-a-contract.md      # API contracts, sequence diagrams for Service A
├── service-b-contract.md      # API contracts, sequence diagrams for Service B
├── infrastructure-topology.md # Deployment diagram, CI/CD, monitoring
└── data-architecture.md       # Database schemas, data flow, migration plan
```

The hub document contains cross-references like:
> **Service A API Contracts**: See [service-a-contract.md](./service-a-contract.md) for the full OpenAPI spec, sequence diagrams, and error handling strategy.

### Pattern 2: By architectural layer

```
solution-overview.md           # Hub: decisions summary, RAID, RACI
├── api-layer.md               # API Gateway config, endpoint routing, auth
├── service-layer.md           # Service contracts, inter-service communication
├── data-layer.md              # Database topology, schemas, caching strategy
└── infrastructure-layer.md    # Deployment, scaling, monitoring
```

### Pattern 3: By decision area (mirrors ADR structure)

```
solution-overview.md           # Hub: C4 diagrams, cross-cutting concerns, RAID, RACI
├── area-1-service-boundaries.md
├── area-2-communication.md
├── area-3-database-strategy.md
└── area-4-migration-plan.md
```

## Cross-reference format

In the hub document, replace each extracted section with a concise summary (2–4 sentences) followed by a link:

```markdown
### Service A: Wallet Payment Service

Wallet Payment Service handles all wallet-based payment flows — initiation, authorization, settlement, and refunds. It communicates with the Bank Transfer Service via async Kafka events for settlement and exposes a REST API for payment status queries.

> **Full specification**: [wallet-payment-service-contract.md](./wallet-payment-service-contract.md) — OpenAPI spec, sequence diagrams, error handling, and database schema.
```

Each extracted document must include a back-reference to the hub so it can be understood when loaded independently:

```markdown
# Wallet Payment Service — API Contracts

> **Parent document**: [solution-overview.md](./solution-overview.md) — system-level architecture, decisions, RAID, and RACI. This document details the Wallet Payment Service contract and should be read alongside the overview.

## Service Context
[Brief recap of what this service does and its role in the system — enough to stand alone.]
```

## Validation checklist

After modularizing, verify:

- [ ] Each extracted document can be understood without reading the hub (has enough context).
- [ ] Each extracted document has a back-reference to the hub.
- [ ] The hub summarizes each extracted section in 2–4 sentences.
- [ ] No critical information exists only in an extracted doc — the hub's summary captures the decision-relevant points.
- [ ] Cross-references use relative paths that work in the target repository.
- [ ] The total context needed for any single review task fits in one document + hub (no need to load all extracted docs).
