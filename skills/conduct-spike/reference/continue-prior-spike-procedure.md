# Continue-Prior-Spike Procedure

Full procedure for the `continue-prior-spike` capability — loaded on demand when a prior spike is resumed. Continuation mode: **continuation-mode**; statuses: **reference/scope-map-guide.md**.

1. Load the prior spike's artifacts — scope summary, findings docs, ADRs, solution doc; ask the user to share or summarize them when any are unavailable.
2. Confirm the continuation scope against `scope.md`; read statuses to surface open problems (`investigating`/`deciding` per **scope-map-status**).
3. Confirm which areas and problems to add, adjust, or remove; map each delta to its affected ADR(s) and solution section.
4. Validate changed problems are independently decidable and unchanged decisions are preserved; update the scope map.
5. Run the standard workflow in revise-in-place mode per **continuation-mode**: apply **investigate-per-area** (seeded with existing evidence maps), **compile-findings-doc**, **draft-problem-adrs**, then **sync-update-artifacts**.
6. Update `scope.md` statuses as each step completes.
7. Run the **final consistency review** — cross-check findings → ADRs → solution doc and cross-area constraints; surface inconsistencies before concluding.
8. Ask whether to continue with another round or conclude.
