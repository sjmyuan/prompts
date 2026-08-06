# Orchestration Guide

Rules for **orchestrate-delivery**, **resume-delivery**, and **update-delivery-index** in `orchestrate-feature-delivery`.

## Agent dispatch

- **One cell per agent.** Planning agents apply **plan-development-task** and write `{location}/{repo}/{feature}/plan.md` + `context.md`. Execution agents apply **execute-plan** and run the plan.
- **Full context in every brief.** Each agent brief carries the cell's scope brief plus its **spike references** (paths to the relevant change-summary items, ADR files, and solution-doc section). Agents load these on demand — do not inline entire solution docs into the brief.
- **Persist references to context.md.** Planning agents record the spike references in `context.md`, so execution and resume agents have durable distilled context and can load referenced artifacts when needed.
- Dispatch agents **in parallel** across cells, subject to:
  - **Wave gating**: only dispatch cells whose dependency cells are **done** (merged).
  - **No conflict in parallel**: never run two cells that touch the same repo with a conflict edge at the same time — serialize them.
  - **Capacity**: match the number of parallel agents to what the platform supports; ask the user when unsure.
- Use the platform's agent/sub-agent mechanism — detect what is available (e.g., coding-assistant agents) and dispatch accordingly.

## Orchestration loop

1. Load the index, or create it via decompose → map → order → produce.
2. Assess state (per-cell status + wave gating).
3. Select ready cells: unplanned → plan; planned → execute; skip done; note blocked.
4. Dispatch parallel agents for the ready cells.
5. Collect results; apply **update-delivery-index**.
6. Re-assess and repeat until all cells are done or the user pauses.

## Status updates

- After every agent result, update the cell status; when a PR merges, mark its cell **done** and re-check downstream cells for wave-readiness.
- Never let conversation text be the source of truth — the delivery index is.

## Resume

- On resume, load the index: completed waves are skipped; in-progress cells resume from the last step in `plan.md`; failed cells are re-planned or retried with the user; blocked cells wait for their blocker.
- Report what is resumed vs skipped before dispatching.

## Failure handling

| State | Meaning | Recovery |
|---|---|---|
| **failed** | agent hit an error (record reason) | ask the user: re-plan (plan-development-task) or retry |
| **blocked** | waiting on an unmerged dependency or a user decision (record blocker) | do not dispatch until the blocker clears |
| **in-progress** | agent was interrupted mid-execution | resume from the last completed step in `plan.md` |
