# Multi-Agent Orchestration for Spikes

Spikes with multiple investigation areas benefit from parallel execution. The orchestrating agent (running this skill) can dispatch independent work units to specialized sub-agents that operate concurrently:

| Phase | Parallelizable? | Mechanism |
|---|---|---|
| 2. Investigate | Yes — each area is independent | Dispatch each investigation area to a code-exploration sub-agent with a focused investigation brief |
| 4. Draft ADRs | Yes — each ADR is independent | Dispatch each area's evaluation results to a sub-agent with instructions to load `draft-adr` and produce a complete ADR |

## Dispatching Pattern

1. Identify independent work units (one per investigation area).
2. For each unit, prepare a focused brief with the area's context, scope, and expected output format.
3. Dispatch all briefs to sub-agents concurrently. Sub-agents operate independently and do not communicate with each other.
4. Collect results from all sub-agents when they complete.
5. Synthesize the collected results into the consolidated format required by the next phase. Review for completeness and consistency across areas.

## When NOT to Parallelize

- Single-area spikes: direct execution is simpler and has less coordination overhead.
- Phases 1 (define scope), 3 (evaluate solutions), and 5 (compile solution doc): these involve user interaction or cross-area synthesis that cannot be parallelized.
- When suitable sub-agents are not available on the current platform: fall back to sequential execution within the orchestrating agent.

## Platform Detection

Before dispatching, detect what code-exploration and skill-execution agents are available on the current platform. Use the most appropriate agent type for each work unit. If no suitable sub-agents are detected, execute sequentially.
