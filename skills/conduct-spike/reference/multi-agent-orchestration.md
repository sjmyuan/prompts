# Multi-Agent Orchestration for Spikes

Spikes with multiple investigation areas benefit from parallel execution. The orchestrating agent (running this skill) can dispatch independent work units to specialized sub-agents that operate concurrently:

| Phase | Parallelizable? | Mechanism |
|---|---|---|
| 2. Investigate | Yes — each area is independent | Dispatch each investigation area to a code-exploration sub-agent with a focused investigation brief |
| 4. Draft ADRs | Yes — each ADR is independent | Dispatch each area's evaluation results to a sub-agent with instructions to load `draft-adr` and produce a complete ADR |

## Dispatching Pattern

1. Identify independent work units (one per investigation area).
2. For each unit, prepare a focused brief with the area's context, scope, and expected output format.
3. **Include the code reference in every brief**: pass the existing code reference (or the relevant slice) so the sub-agent starts from verified `file:line` locations instead of scanning from scratch. Instruct it to treat verified claims as settled and only dig into marked gaps and searched-negatives.
4. **Require a code reference back**: every investigation brief asks the sub-agent to return a per-area code reference (entry points, key code locations with file:line, call chains, evidence verdicts, searched-negatives) alongside its narrative findings.
5. Dispatch all briefs to sub-agents concurrently. Sub-agents operate independently and do not communicate with each other.
6. Collect results from all sub-agents when they complete.
7. Synthesize the collected results into the consolidated format required by the next phase. Review for completeness and consistency across areas, and merge the returned per-area code references into the consolidated code reference (see **reference/code-reference-guide.md**).

## Code Reference in Sub-Agent Briefs

The code reference is the input/output contract between the orchestrator and sub-agents:

- **Input**: every brief carries the code reference (or its area slice). Sub-agents start from entry points, follow existing call chains, and treat the evidence ledger's **verified** claims as settled — they verify only `inferred`/`unverified` claims or marked gaps.
- **Output**: every investigation brief returns a per-area code reference slice so the orchestrator can grow the consolidated document (see **compile-code-reference**).
- **Searched-negatives travel with the map**: a documented "not found" tells the next sub-agent not to repeat the scan.
- **ADR-drafting briefs** include the area's code reference so ADRs can cite evidence locations without re-reading code.
- **First pass is the seed**: when no code reference exists yet, briefs omit the input but still require the output — the first investigation builds the map.

## When NOT to Parallelize

- Single-area spikes: direct execution is simpler and has less coordination overhead.
- Phases 1 (define scope), 3 (evaluate solutions), and 5 (compile solution doc): these involve user interaction or cross-area synthesis that cannot be parallelized.
- When suitable sub-agents are not available on the current platform: fall back to sequential execution within the orchestrating agent.

## Platform Detection

Before dispatching, detect what code-exploration and skill-execution agents are available on the current platform. Use the most appropriate agent type for each work unit. If no suitable sub-agents are detected, execute sequentially.
