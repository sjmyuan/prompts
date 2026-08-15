# Sub-Agent Orchestration for Spikes

Dispatch task execution to sub-agents whenever one is available — for Phases 2 (investigate), 2b (compile findings docs), 3 (evaluate solutions), 4 (draft ADRs), and 5 (compile solution doc) — **even when the spike has only a single task**. The primary goal is **preserving the orchestrating agent's context**: running a task directly consumes the orchestrator's context window with file reads, search output, and intermediate reasoning, crowding out the cross-cutting state it must hold (scope, findings, decisions). Parallel speed is a secondary benefit that applies automatically when multiple units are dispatched at once.

| Phase | Agent | Applies skill | Brief template |
|---|---|---|---|
| 2. Investigate | `code-investigator` | `investigate-code` | Investigation brief — [dispatch-briefs.md](dispatch-briefs.md) |
| 2b. Compile findings docs | `solution-doc-writer` | `write-solution-doc` (current-state mode) | Findings-doc brief — [dispatch-briefs.md](dispatch-briefs.md) |
| 3. Evaluate problem solutions | `adr-writer` | `draft-adr` (evaluate chain, interactive) | Evaluation brief — [dispatch-briefs.md](dispatch-briefs.md) |
| 4. Draft problem ADRs | `adr-writer` | `draft-adr` (compile-adr) | ADR-drafting brief — [dispatch-briefs.md](dispatch-briefs.md) |
| 5. Compile solution doc | `solution-doc-writer` | `write-solution-doc` (baseline-input mode) | Solution-doc brief — [dispatch-briefs.md](dispatch-briefs.md) |

Each phase's brief template lives in **reference/dispatch-briefs.md** — prepare the brief from that template, then dispatch to the mapped agent. Every phase is dispatched even for a single task (see below). Evaluation dispatch (Phase 3) runs the interactive `draft-adr` evaluate chain inside the `adr-writer` session — the agent asks the user for drivers, options, and the assumed solution, then returns the result to the orchestrator.

## Why Dispatch Even a Single Task

- **Context preservation (primary)**: the orchestrator keeps its window for synthesis and orchestration; the sub-agent's reading, reasoning, and interactive user dialog (e.g., evaluation) stays in its own context.
- **Speed (secondary)**: multiple units dispatched together run concurrently.
- **Consistency**: one dispatch pattern for all spikes — no separate single-task code path to maintain.

## Dispatching Pattern

1. Identify independent work units (one per investigation area, or one per problem/ADR — batching a whole area's problems into one brief when they share its evidence; including a single unit).
2. For each unit, prepare a focused brief from the phase's template in **reference/dispatch-briefs.md** — context, scope, expected output, and the shared evidence-map input/output rules all live there.
3. Dispatch the briefs — all units concurrently when there are multiple, or the single unit on its own when there is one. Sub-agents operate independently and do not communicate with each other.
4. Collect results from all sub-agents when they complete.
5. Verify each collected result with **verify-sub-agent-results** — the `question-everything` loop with new same-type sub-agents — then synthesize the accepted results into the consolidated format required by the next phase. Review for completeness and consistency across areas, and embed the returned per-area evidence maps into the findings doc(s) (see **reference/findings-document-guide.md**).
6. **Document-compilation briefs** (findings and solution docs) carry the full synthesis context per **reference/dispatch-briefs.md** — the orchestrator still reviews, validates, and presents the returned doc.

## Verifying Returned Results

Every sub-agent result — investigation findings, ADR decisions, and dispatched findings/solution-doc compilations — is questioned via the `question-everything` skill before acceptance (**verify-sub-agent-results**): challenge the result across the six dimensions, verify with a NEW sub-agent of the same type, accept when all challenges AGREE, or re-investigate with another NEW same-type sub-agent when any DISAGREE/UNCERTAIN. Loop until all agree or the 3-round cap; escalate to the user at the cap. The original sub-agent instance is never reused. Dispatched findings/solution-doc compilations synthesize already-verified material, so verification focuses on fidelity to that material rather than a fresh fact-check. Dispatched evaluation results return **provisional assumed solutions** — the orchestrator reviews them for fidelity to the findings doc and cross-area consistency, and the definitive verification lands on the ADR drafted in Phase 4.

## When NOT to Dispatch

- **Phase 1 (define scope)**: stays in the orchestrating agent — it establishes the cross-cutting scope (goal + areas and problems) that every dispatch brief depends on and sets up the spike. All later phases, including evaluation, dispatch whenever a sub-agent is available; evaluation's user dialog runs inside the dispatched sub-agent.
- **No suitable sub-agent available**: fall back to direct execution within the orchestrating agent.
- **Single-task spikes are NOT exempt**: a single area, single ADR, or single document is still dispatched when a sub-agent is available — context preservation is the goal, not parallelism.

## Platform Detection

Before dispatching, detect whether `code-investigator`, `adr-writer`, and `solution-doc-writer` are available on the current platform; fall back to the closest equivalent agent type for each work unit. If no suitable sub-agents are detected, execute directly.
