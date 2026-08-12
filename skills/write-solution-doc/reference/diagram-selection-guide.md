# Diagram Selection Guide

Backs the `<diagram-selection-guide>` knowledge entry, used by **draw-interaction-diagrams** and **sync-diagrams**.

## Decision Matrix

| Scenario | Recommended Diagram | Rationale |
|---|---|---|
| Runtime message passing between services/components (e.g., API calls, event publishing, request-response chains) | **Sequence Diagram** | Shows participants, message ordering, activation bars, and lifelines — best for temporal interaction flows |
| Business process with decision branches and conditional paths (e.g., order approval workflow, refund eligibility logic, state transitions) | **Flowchart** | Shows decision diamonds, branching paths, and process steps — best for logic and control flow |
| Data pipeline with transformation stages and branching (e.g., ETL steps, data routing rules, enrichment logic) | **Flowchart** | Pipeline stages are process steps; routing rules are decision nodes — naturally fits flowchart syntax |
| Multi-participant orchestration with both runtime calls AND decision logic (e.g., saga orchestration with compensating actions, complex checkout flow) | **Both** — sequence diagram for the happy-path call chain + flowchart for the decision/compensation logic | Use sequence to show who-calls-whom, flowchart to show what-decisions-are-made |
| State machine transitions (e.g., order status lifecycle, user onboarding states) | **Flowchart** (state diagram style) — `stateDiagram-v2` if focus is on states/transitions; `flowchart` if decision logic dominates | States as nodes, transitions as arrows with conditions — choose syntax by whether states or decisions dominate |
| Pure state/status lifecycle with no decision branching (e.g., entity status flow, deployment states) | **State Diagram** (`stateDiagram-v2`) | Cleaner than flowchart for state-centric views — use when the question is "what states exist and what triggers transitions?" |
| Algorithm or processing logic within a single component (e.g., rate limiting algorithm, caching strategy) | **Flowchart** | No cross-component participants — purely internal logic flow |

**Decision rule**: If the primary question is "who talks to whom and in what order?" → use a sequence diagram. If the primary question is "what decisions are made and what paths exist?" → use a flowchart. When both questions matter, produce both diagrams.

## Interop with Existing Diagrams

When receiving diagrams from prior investigation, other tools, or user-provided sources that use different conventions:

- **C4 diagrams**: Accept Mermaid C4 diagrams regardless of element or boundary style; normalize to the native `C4Context` / `C4Container` / `C4Component` syntax (per **reference/mermaid-standards.md**) when embedding in the final document.
- **Sequence diagrams**: Accept both numbered and unnumbered message styles. Preserve existing numbering when present (useful for traceability); add a brief note explaining the numbering scheme.
- **Flowcharts**: Accept Mermaid `flowchart` syntax. Normalize labels and shapes to the **reference/mermaid-standards.md** conventions when embedding.
- **State diagrams**: Accept Mermaid `stateDiagram-v2` syntax.
