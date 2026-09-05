# Sub-Agent Orchestration for Spikes

Dispatch task execution to sub-agents — for investigation, findings-doc compilation, ADR drafting (including option evaluation via `draft-adr`), and solution-doc compilation — **even when the spike has only a single task**. A sub-agent is always available; the primary goal is **preserving the orchestrating agent's context**: running a task in the orchestrator consumes its context window with file reads, search output, and intermediate reasoning, crowding out the cross-cutting state it must hold (scope, findings, decisions). Parallel speed is a secondary benefit that applies automatically when multiple units are dispatched at once.

| Capability | Agent | Applies skill | Brief template |
|---|---|---|---|
| Investigate | `code-investigator` | `investigate-code` | Investigation brief — [investigation-brief.md](investigation-brief.md) |
| Compile findings docs | `solution-doc-writer` | `write-solution-doc` (current-state mode) | Findings-doc brief — [findings-doc-brief.md](findings-doc-brief.md) |
| Draft problem ADRs (evaluate + draft) | `adr-writer` | `draft-adr` (full flow) | ADR-drafting brief — [adr-drafting-brief.md](adr-drafting-brief.md) |
| Compile solution doc | `solution-doc-writer` | `write-solution-doc` (baseline-input mode) | Solution-doc brief — [solution-doc-brief.md](solution-doc-brief.md) |

Each capability's brief template lives in its own reference file (see the table above) — prepare the brief from it, then dispatch to the mapped agent. Every capability is dispatched even for a single task (see below). ADR drafting runs the full `draft-adr` flow — decision drivers → options → evaluation → compile-adr — inside the `adr-writer` session; the agent asks the user for drivers, options, and the chosen option, then returns the ADR.

## Why Dispatch Even a Single Task

- **Context preservation (primary)**: the orchestrator keeps its window for synthesis and orchestration; the sub-agent's reading, reasoning, and interactive user dialog (e.g., ADR evaluation) stays in its own context.
- **Speed (secondary)**: multiple units dispatched together run concurrently.
- **Consistency**: one dispatch pattern for all spikes — no separate single-task code path to maintain.

## Dispatching Pattern

1. Identify independent work units (one per investigation area, or one per problem/ADR — batching a whole area's problems into one brief when they share its evidence; including a single unit).
2. For each unit, fill the capability's ready-to-fill brief (see the table above) per the **structured brief shape** — substitute the `[bracketed]` fields; the shared evidence-map input/output contract lives in **reference/dispatch-briefs.md**.
3. Dispatch the briefs — all units concurrently when there are multiple, or the single unit on its own when there is one. Sub-agents operate independently and do not communicate with each other.
4. Collect results from all sub-agents when they complete.
5. Verify each collected result via `question-everything`'s **verify-sub-agent-results** — dispatch NEW same-type sub-agents per the verification protocol. Review the accepted results for completeness and consistency across areas, then hand each area's verified evidence map to `compile-findings-doc`, which embeds it into its own `docs/findings-<area>.md` (see **reference/findings-document-guide.md**).
6. **Document-compilation briefs** (findings and solution docs) carry the full synthesis context per **reference/findings-doc-brief.md** / **reference/solution-doc-brief.md** — the orchestrator still reviews, validates, and presents the returned doc.

## Verifying Returned Results

Every sub-agent result — investigation findings, ADR decisions, and dispatched findings/solution-doc compilations — is verified before acceptance via `question-everything`'s **verify-sub-agent-results**: challenge the result across the six dimensions, dispatch a NEW same-type sub-agent to verify each challenge against primary sources, accept when all material challenges AGREE, or re-investigate with another NEW same-type sub-agent when any DISAGREE/UNCERTAIN. Loop until all agree or the 3-round cap; escalate to the user at the cap. The original sub-agent instance is never reused. Dispatched findings/solution-doc compilations synthesize already-verified material, so verification focuses on fidelity to that material rather than a fresh fact-check. Full loop: `question-everything`'s **reference/verification-protocol.md**.

## When NOT to Dispatch

- **Scope definition**: stays in the orchestrating agent — it establishes the cross-cutting scope (goal + areas and problems) that every dispatch brief depends on and sets up the spike. All later steps dispatch to a sub-agent; the ADR-drafting user dialog (drivers, options, evaluation) runs inside the dispatched sub-agent.
- **Single-task spikes are NOT exempt**: a single area, single ADR, or single document is still dispatched — context preservation is the goal, not parallelism.

## Platform Detection

Before dispatching, detect whether `code-investigator`, `adr-writer`, and `solution-doc-writer` are available on the current platform; map each work unit to the closest equivalent agent type.
