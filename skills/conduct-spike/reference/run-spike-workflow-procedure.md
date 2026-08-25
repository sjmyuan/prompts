# Run-Spike-Workflow Procedure

Full procedure for the `run-spike-workflow` capability — loaded on demand when a spike investigation starts from scratch. Pause for user confirmation after each capability; skip a pause only if the user requests it.

1. Apply **define-spike-scope**.
2. Do not proceed until the scope is confirmed.
3. Apply **investigate-per-area**, recording each area's **evidence map**.
4. Loop to step 1 when a new investigation direction emerges.
5. Apply **compile-findings-doc**, embedding each area's evidence map inline.
6. Apply **draft-problem-adrs** — evaluating options and drafting each ADR via `draft-adr`, verifying each before saving.
7. Apply **compile-solution-doc** to consolidate ADRs into the solution document.
