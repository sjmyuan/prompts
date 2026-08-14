# Current-State Mode

The solution-doc format has two input modes beyond the default target-state compile: documenting what exists today (as-is), and evolving that baseline into the target state (to-be). Backs the `<current-state-mode>` knowledge entry.

## Current-state mode (as-is / findings documents)

Produce the same 9-section structure, diagrams, and formatting, but describing the **current state** rather than the target:

- Label every diagram "current state" — C4, sequence, and flowchart views reflect what exists today, not the plan.
- Replace the **RAID Analysis** and **RACI Matrix** sections with **Constraints & Pain Points** and **Raw Data & Metrics** from the current-state evidence.
- Keep sections that do not apply (e.g., target-state-only API contracts) marked `[Skipped]` unless they describe existing contracts.
- The result is a baseline that can be evolved directly into a target-state document.

## Baseline-input mode (evolve as-is → to-be)

When compiling a target-state document from a current-state baseline (e.g., spike findings docs):

- Start from the current-state document and **evolve each section** as-is → to-be — do not redraw from scratch.
- Diagrams show the **target architecture**, not current state: update C4 topology, interaction flows, and API/event contracts to the chosen solution.
- Add what the target introduces (new contracts, RAID analysis, RACI matrix); replace the baseline's Constraints & Pain Points / Raw Data & Metrics with RAID and RACI.
- The target document stays decision-only — current-state detail lives in the baseline it evolved from.

## Where this mode comes from

Used by the `conduct-spike` skill: findings documents are compiled in **current-state mode**, and the solution document is compiled in **baseline-input mode** seeded with the findings baseline. `conduct-spike` seeds the compile; this skill owns the format rules.
