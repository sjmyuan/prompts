# Run-Spike-Workflow Procedure

Full procedure for the `run-spike-workflow` capability — loaded on demand when a spike investigation starts from scratch. Pause for user confirmation after each capability; skip a pause only if the user requests it. Run the write-boundary check after every write capability per **reference/write-boundary-guide.md**; stop and report on any out-of-folder change.

1. Apply **define-spike-scope**.
2. Do not proceed until the scope is confirmed.
3. Apply **investigate-per-area**, recording each area's **evidence map**.
4. Loop to step 1 when a new investigation direction emerges.
5. Apply **compile-findings-doc**, embedding each area's evidence map inline; run the write-boundary check.
6. Apply **draft-problem-adrs** — evaluating options and drafting each ADR via `draft-adr`, verifying each before saving; run the write-boundary check.
7. Apply **compile-solution-doc** to consolidate ADRs into the solution document; run the write-boundary check.
8. Run the **final consistency review** — cross-check findings → ADRs → solution doc and cross-area constraints; confirm each `done` problem has its ADR and each area's decisions are mirrored in the solution doc; surface inconsistencies before concluding.
9. Record any implementation need as an out-of-scope note in `scope.md` / `solution.md`; never implement — the user runs `orchestrate-feature-delivery`.
