# Sub-Agent Orchestration for Spikes

Dispatch task execution to sub-agents whenever one is available — for Phases 2 (investigate) and 4 (draft ADRs) — **even when the spike has only a single task**. The primary goal is **preserving the orchestrating agent's context**: running a task directly consumes the orchestrator's context window with file reads, search output, and intermediate reasoning, crowding out the cross-cutting state it must hold (scope, code reference, findings, decisions). Parallel speed is a secondary benefit that applies automatically when multiple units are dispatched at once.

| Phase | Dispatchable? | Mechanism |
|---|---|---|
| 2. Investigate | Yes — each area, even a single one | Dispatch each investigation area to a code-exploration sub-agent with a focused investigation brief |
| 4. Draft ADRs | Yes — each ADR, even a single one | Dispatch each area's evaluation results to a sub-agent with instructions to load `draft-adr` and produce a complete ADR |

## Why Dispatch Even a Single Task

- **Context preservation (primary)**: the orchestrator keeps its window for synthesis and user interaction; the sub-agent's reading and reasoning stays in its own context.
- **Speed (secondary)**: multiple units dispatched together run concurrently.
- **Consistency**: one dispatch pattern for all spikes — no separate single-task code path to maintain.

## Dispatching Pattern

1. Identify independent work units (one per investigation area or ADR — including a single unit).
2. For each unit, prepare a focused brief with the unit's context, scope, and expected output format.
3. **Include the code reference in every brief**: pass the existing code reference (or the relevant slice) so the sub-agent starts from verified `file:line` locations instead of scanning from scratch. Instruct it to treat verified claims as settled and only dig into marked gaps and searched-negatives.
4. **Require a code reference back**: every investigation brief asks the sub-agent to return a per-area code reference (entry points, key code locations with file:line, call chains, evidence verdicts, searched-negatives) alongside its narrative findings.
5. Dispatch the briefs — all units concurrently when there are multiple, or the single unit on its own when there is one. Sub-agents operate independently and do not communicate with each other.
6. Collect results from all sub-agents when they complete.
7. Synthesize the collected results into the consolidated format required by the next phase. Review for completeness and consistency across areas, and merge the returned per-area code references into the consolidated code reference (see **reference/code-reference-guide.md**).

## Code Reference in Sub-Agent Briefs

The code reference is the input/output contract between the orchestrator and sub-agents:

- **Input**: every brief carries the code reference (or its area slice). Sub-agents start from entry points, follow existing call chains, and treat the evidence ledger's **verified** claims as settled — they verify only `inferred`/`unverified` claims or marked gaps.
- **Output**: every investigation brief returns a per-area code reference slice so the orchestrator can grow the consolidated document (see **compile-code-reference**).
- **Searched-negatives travel with the map**: a documented "not found" tells the next sub-agent not to repeat the scan.
- **ADR-drafting briefs** include the area's code reference so ADRs can cite evidence locations without re-reading code.
- **First pass is the seed**: when no code reference exists yet, briefs omit the input but still require the output — the first investigation builds the map.

## When NOT to Dispatch

- **Phases 1 (define scope), 3 (evaluate solutions), and 5 (compile solution doc)**: these involve user interaction or cross-area synthesis that must stay in the orchestrating agent.
- **No suitable sub-agent available**: fall back to direct execution within the orchestrating agent.
- **Single-task spikes are NOT exempt**: a single area or single ADR is still dispatched when a sub-agent is available — context preservation is the goal, not parallelism.

## Platform Detection

Before dispatching, detect what code-exploration and skill-execution agents are available on the current platform. Use the most appropriate agent type for each work unit. If no suitable sub-agents are detected, execute directly.
