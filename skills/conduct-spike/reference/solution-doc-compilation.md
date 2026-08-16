# Solution-Doc Compilation

Full procedure for the `compile-solution-doc` capability — loaded on demand when the spike reaches the solution-doc compilation phase, so the findings-doc procedure is never pulled in. Dispatch briefs: **reference/solution-doc-brief.md**; latest-state rules: **reference/artifact-maintenance-guide.md**.

1. Dispatch solution-doc compilation to `solution-doc-writer` per **multi-agent-orchestration**; brief per **reference/solution-doc-brief.md**.
2. Verify the compiled doc via `question-everything`'s **verify-sub-agent-results**.
3. Save per **spike-artifact-layout** (scope map → `scope.md`, findings → `docs/`, ADRs → `adrs/`, solution doc → `solution.md`); keep at the latest state (see **artifact-maintenance-doctrine**); recompute each area's derived status per **scope-map-status**.
4. Validate: the solution doc mirrors every ADR's chosen solution **grouped by area** (per **scope-map**), cross-references consistent, diagrams match; run the **no-note scan** until clean.
5. Present the bundle: findings = current-state record; ADRs = decision records (review/approve); solution doc = target-state architecture; version-control together.
