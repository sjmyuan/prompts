# Investigate-Per-Area Procedure

Full procedure for the `investigate-per-area` capability — loaded on demand when area investigation begins. Dispatch pattern: **reference/multi-agent-orchestration.md**; investigation brief: **reference/investigation-brief.md**.

1. Dispatch each area's investigation to `code-investigator` per **multi-agent-orchestration**.
2. Brief each investigation per **reference/investigation-brief.md**.
3. Verify each area's result via `question-everything`'s **verify-sub-agent-results**.
4. Ask: "Is the investigation complete, or continue in a new direction?"
5. Loop to scope when a new direction is chosen.
6. Hand off to **compile-findings-doc** with the evidence maps.
