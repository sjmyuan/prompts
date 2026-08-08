# Orchestration Guide

Rules for **orchestrate-delivery**, **resume-delivery**, and **update-delivery-index** in `orchestrate-feature-delivery`.

## Agent dispatch

- **Always delegate — never do the work yourself.** The orchestrator only dispatches and tracks. Every delivery task maps to a dedicated agent:

| Task | Delegated agent | Applies | Result |
|---|---|---|---|
| Spike a rework | **spike-conductor** | **conduct-spike** | focused findings / ADR / solution-doc updates + change summary |
| Plan a cell | **coding-assistant** | **plan-development-task** | `plan.md` + `context.md` |
| Execute a cell | **coding-assistant** | **execute-plan** | code changes + commits |
| Update solution doc | **solution-doc-writer** | **write-solution-doc** | revised sections, rewrite in place |
| Update ADR | **adr-writer** | **draft-adr** | revised ADR, rewrite in place |

- **One cell per agent.** Planning agents apply **plan-development-task** and write `{location}/{repo}/{feature}/plan.md` + `context.md`. Execution agents apply **execute-plan** and run the plan.
- **Artifact updates are delegated too.** When a plan or execution surfaces changes to the spike's solution doc or ADRs, dispatch a **solution-doc-writer** / **adr-writer** agent for the update — never edit those artifacts from the orchestrator.
- **Full context in every brief.** Each agent brief carries the cell's scope brief plus its **spike references** (paths to the relevant change-summary items, ADR files, and solution-doc section). Agents load these on demand — do not inline entire solution docs into the brief.
- **Persist references to context.md.** Planning agents record the spike references in `context.md`, so execution and resume agents have durable distilled context and can load referenced artifacts when needed.
- Dispatch agents **in parallel** across cells, subject to:
  - **Wave gating**: only dispatch cells whose dependency cells are **done** (merged).
  - **No conflict in parallel**: never run two cells that touch the same repo with a conflict edge at the same time — serialize them.
  - **Capacity**: match the number of parallel agents to what the platform supports; ask the user when unsure.
- Use the platform's agent/sub-agent mechanism — detect what is available (e.g., coding-assistant agents) and dispatch accordingly.
- **Branches**: one branch per repo per cell, named to match the **repo's branch convention** (detect from existing branches / git config / team docs, or ask the user — never assume a prefix); recorded in the delivery index and included in the agent brief; execution agents create the branch during their Prepare Environment step and commit small-step locally (see **branch-and-push-conventions**).
- **Push gating**: never push a branch or open a PR automatically — after a cell's work is complete and ready to integrate, ask the user for confirmation first.

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

## Post-implementation rework

When an issue is found after a cell is **done** (implemented/merged):

1. **Focused spike**: dispatch the **spike-conductor** agent (conduct-spike), scoped narrowly to the affected decision — usually the feature's governing ADR. Do not re-open the whole epic.
2. **Delegate artifact updates**: ADR changes → **adr-writer** (draft-adr); solution-doc changes → **solution-doc-writer** (write-solution-doc); change summary recomputed via conduct-spike.
3. **Update the index**: record the rework — spike's ADR focus, new change-summary items, rework wave/feature, appended plan location.
4. **Append the plan**: dispatch **plan-development-task** (coding-assistant) to append a `## Rework <date>` section to the feature's existing `plan.md` — implemented steps are never modified.
5. **Execute the appended plan**: dispatch **execute-plan** (coding-assistant) to run only the new rework steps.
6. Update the index; ask the user before pushing / opening a PR.
