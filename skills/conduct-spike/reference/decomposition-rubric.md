# Problem Decomposition Rubric for Spikes

This rubric helps determine whether a spike problem is properly decomposed. A spike decomposes into **areas** (shared-subject groupings) and each area into **problems** ("How to …?" decisions). Each problem produces one ADR. Areas define the evidence/findings boundary; problems define the decidable units. Use it during `define-spike-scope` to validate and refine the breakdown, then record it in `scope.md`.

## Two-level structure

```
Area: Data storage
├── Problem: How to pick the database engine? → adr-database-01-…
└── Problem: How to migrate the schema?      → adr-database-02-…
Area: API layer
└── Problem: How to expose the API contract? → adr-api-01-…
```

- A problem belongs to exactly one area; a problem that "spans" areas signals mis-grouping.
- An area exists because it holds problems — no empty areas.
- Areas keep `findings-<area>.md` (the evidence home); problems each get one ADR.

## Area heuristics (groupings)

When grouping the spike problem into investigation areas, apply:

| Heuristic | Description | Example |
|---|---|---|
| **Layer separation** | Different architectural layers form natural area boundaries | "Storage layer", "API layer", "Frontend rendering" |
| **Risk isolation** | High-uncertainty subjects deserve their own area | "Migration strategy for legacy data" |
| **Team/owner boundaries** | Areas owned by different teams split naturally | "Auth service changes" vs. "Payment service changes" |
| **Technology domains** | Different tech stacks or domains split naturally | "Mobile client" vs. "Backend services" vs. "Infrastructure" |

Target 2–5 areas. Fewer than 2 means the problem may not need a spike; more than 5 suggests the scope may be too broad and should be narrowed.

## Problem heuristics (decision units)

Within each area, enumerate the "How to …?" decisions:

| Heuristic | Description | Example |
|---|---|---|
| **Decision independence** | Each problem is decidable without knowing another's outcome | "How to pick the DB engine?" vs. "How to migrate the schema?" |
| **One ADR per problem** | Each problem maps to exactly one ADR | "How to expose the API?" → one ADR |
| **Shared evidence** | Problems in one area share its subject/evidence map | DB-engine choice and schema migration both need the DB topology |

Target 1–3 problems per area; more than ~8 total problems → narrow the spike goal, merge problems, or split into follow-up spikes.

## Decomposition Quality Criteria

| Criterion | Good | Needs Work | Bad |
|---|---|---|---|
| **Area cohesion** | Each area is one shared subject; its problems belong together | Some problems are loosely related to the area | Area is a grab-bag of unrelated problems |
| **Problem granularity** | Each problem is one clear "How to …" decision | A problem bundles 2 related decisions | Problem is a grab-bag of unrelated decisions |
| **Decision independence** | Each problem can be decided independently | Some problems have partial dependency but proceed with assumptions | Problems tightly coupled; one decision forces another |
| **Investigate-ability** | The area's code can be meaningfully explored | Partial codebase exists but is poorly documented | No code exists yet (greenfield); investigation would be theoretical |
| **Actionability** | Clear what a good outcome looks like; each ADR has concrete options | Outcome is fuzzy but directionally clear | No one knows what "done" looks like for this area |
| **Boundary clarity** | Clear which code/modules/teams fall inside vs. outside each area | Some grey areas at the edges | Completely unclear what's in scope |

## Decomposition Patterns

### By Architectural Layer
Best for: Full-stack problems spanning multiple tiers.
```
Area: Data storage layer
├── How to choose the database engine?
└── How to migrate the schema safely?
Area: API/service layer
└── How to expose the service contract?
Area: Frontend layer
└── How to manage client state?
Area: Infrastructure layer
└── How to handle deployment and monitoring?
```

### By Risk Profile
Best for: Problems where uncertainty is concentrated in specific areas.
```
Area: High-risk core (the novel/untested part — spike this deepest)
└── How to prove the novel part works at the required scale?
Area: Integration surface (how the new solution connects to existing systems)
└── How to connect without breaking current behavior?
Area: Migration path (how to transition from current to target state)
└── How to migrate with zero downtime?
```

### By Team Ownership
Best for: Cross-team initiatives.
```
Area: Team A's domain (e.g., "Auth service changes") └── How to …?
Area: Team B's domain (e.g., "Payment gateway integration") └── How to …?
Area: Shared/infra domain (e.g., "API gateway configuration") └── How to …?
```

### By Technology Domain
Best for: Problems touching multiple technology stacks.
```
Area: Mobile client (iOS/Android) └── How to …?
Area: Web frontend (React)       └── How to …?
Area: Backend services (Java/Spring) └── How to …?
Area: Data pipeline (Kafka/Spark)    └── How to …?
```

## Edge Cases

### Single-Area Spike
If the problem truly has one subject (e.g., "Should we migrate from MySQL to PostgreSQL?"), a single-area spike is valid. It still holds one or more problems: one subject, one problem → one ADR; one subject, two problems → two ADRs (e.g., engine choice + schema migration). The workflow produces the same artifacts — findings doc + ADR(s) + solution doc — just simpler.

### Too Many Areas (>5) or Too Many Problems (>~8)
The spike scope is likely too broad. Options:
1. **Narrow the spike goal**: Focus on the highest-uncertainty areas/problems first; defer others to a follow-up spike.
2. **Merge**: Combine areas that share evidence; merge problems that share decision drivers.
3. **Split into multiple spikes**: Run separate spikes for truly independent problem domains.

### Greenfield (No Existing Code)
If there is no existing implementation to investigate, each area's `investigate-per-area` shifts to:
- Researching industry approaches and open-source solutions
- Studying similar systems in the organization
- Prototyping proof-of-concepts instead of tracing code
