# Problem Decomposition Rubric for Spikes

This rubric helps determine whether a spike problem is properly decomposed into investigation areas. Use it during `define-spike-scope` to validate and refine the breakdown.

## Decomposition Heuristics

When breaking down a spike problem into investigation areas, apply these heuristics:

| Heuristic | Description | Example |
|---|---|---|
| **Decision independence** | Can this area be decided without knowing the outcome of other areas? | "Database choice" vs. "API framework choice" |
| **Layer separation** | Different architectural layers often form natural boundaries | "Storage layer", "API layer", "Frontend rendering" |
| **Risk isolation** | High-uncertainty areas deserve their own investigation | "Migration strategy for legacy data" |
| **Team/owner boundaries** | Areas owned by different teams may need separate ADRs | "Auth service changes" vs. "Payment service changes" |
| **Technology domains** | Different tech stacks or domains split naturally | "Mobile client" vs. "Backend services" vs. "Infrastructure" |

Target 2–5 investigation areas. Fewer than 2 means the problem may not need a spike; more than 5 suggests the scope may be too broad and should be narrowed.

## Decomposition Quality Criteria

| Criterion | Good | Needs Work | Bad |
|---|---|---|---|
| **Decision independence** | Each area can be decided independently; no area's outcome depends on another's | Some areas have partial dependency but can proceed with assumptions | Areas are tightly coupled; one decision forces another |
| **Scope granularity** | Each area addresses one clear decision (e.g., "Which database?") | Area bundles 2 related decisions (e.g., "Database + caching strategy") | Area is a grab-bag of unrelated decisions |
| **Investigate-ability** | Current implementation for this area can be meaningfully explored | Partial codebase exists but is poorly documented | No code exists yet (greenfield); investigation would be theoretical |
| **Actionability** | Clear what a good outcome looks like; ADR will have concrete options | Outcome is fuzzy but directionally clear | No one knows what "done" looks like for this area |
| **Boundary clarity** | Clear which code/modules/teams fall inside vs. outside this area | Some grey areas at the edges | Completely unclear what's in scope |

## Decomposition Patterns

### By Architectural Layer
Best for: Full-stack problems spanning multiple tiers.
```
Area 1: Data storage layer (database choice, schema, migration)
Area 2: API/service layer (framework, endpoints, auth)
Area 3: Frontend layer (rendering strategy, state management)
Area 4: Infrastructure layer (deployment, CI/CD, monitoring)
```

### By Risk Profile
Best for: Problems where uncertainty is concentrated in specific areas.
```
Area 1: High-risk core (the novel/untested part — spike this deepest)
Area 2: Integration surface (how new solution connects to existing systems)
Area 3: Migration path (how to transition from current to target state)
```

### By Team Ownership
Best for: Cross-team initiatives.
```
Area 1: Team A's domain (e.g., "Auth service changes")
Area 2: Team B's domain (e.g., "Payment gateway integration")
Area 3: Shared/infra domain (e.g., "API gateway configuration")
```

### By Technology Domain
Best for: Problems touching multiple technology stacks.
```
Area 1: Mobile client (iOS/Android)
Area 2: Web frontend (React)
Area 3: Backend services (Java/Spring)
Area 4: Data pipeline (Kafka/Spark)
```

## Edge Cases

### Single Area Spike
If the problem truly has only one decision to make (e.g., "Should we migrate from MySQL to PostgreSQL?"), a single-area spike is valid. The workflow still produces one ADR + one solution doc, but the solution doc will be simpler.

### Too Many Areas (>5)
If decomposition yields more than 5 areas, the spike scope is likely too broad. Options:
1. **Narrow the spike goal**: Focus on the highest-uncertainty areas first; defer others to a follow-up spike.
2. **Merge related areas**: Combine areas that share decision drivers and options.
3. **Split into multiple spikes**: Run separate spikes for truly independent problem domains.

### Greenfield (No Existing Code)
If there is no existing implementation to investigate, the `investigate-per-area` phase shifts to:
- Researching industry approaches and open-source solutions
- Studying similar systems in the organization
- Prototyping proof-of-concepts instead of tracing code
