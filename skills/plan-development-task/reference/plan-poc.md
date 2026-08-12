# plan-poc

1. **Prepare Environment (Prerequisites)**: apply **plan-prerequisites** — a **POC branch** per the repo's branch convention, clean tree, deps installed, baseline green; stop and raise if not ready.
2. Load the ADR and the option's **tech details** (draft-adr's **detail-options-tech**): target-state diagrams + code change profile (file:line, current code, proposed diff, how-to).
3. Clarify with the user: the option under proof, the **success criteria** (measurable, tied to the ADR's decision drivers), and the standalone feature slice that demonstrates it end-to-end.
4. **Define Scope Boundary**: the option's target area is **In scope**; other options, other ADRs, and unrelated modules are **Out of scope**; ratify with the user.
5. Break the slice into independently testable functionalities; order by dependencies; consolidate per plan-feature-implementation step 5.
6. Load **reference/tdd-approach-selection.md**; choose the TDD variant per functionality and document the rationale.
7. Create the plan (starting with the ratified `## Scope Boundary` block): TDD steps per functionality (Write Focused Tests → Confirm Failure → Implement Minimal Code → Verify → Refactor → Validate → Clean Up → Verify Cleanup → Quality Gate).
8. Add a final **evaluation step**: how evidence is measured/collected against each success criterion (benchmark, complexity diff, integration check) — this is what the decision gate judges.
9. Mark the plan `type: poc`; keep step count ≤ 25.
10. **Validate Plan Quality** against **reference/plan-quality-checklist.md**; revise failures before presenting.
11. Summarize to the user; persist via **export-plan** (success criteria + evaluation method into `context.md`).
