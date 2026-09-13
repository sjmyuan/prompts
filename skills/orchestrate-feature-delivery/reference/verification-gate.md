# Verification Gate

Backs the **verify-cell** capability and the `verified` status in `orchestrate-feature-delivery`. The gate is independent and scoped to what the executor does not provide: **spec compliance** and **trust verification**. Quality review stays with **execute-plan**'s `review-post-execution` — the gate never duplicates it.

## Division of labor

| Layer | Owns | Does not |
|---|---|---|
| **execute-plan** (`review-post-execution`) | Quality review of its own diff (**review-code**); Blocker/Major fix loop | Independent spec compliance; bounded loop; adjudication |
| **verify-cell** (orchestrator) | Independent spec compliance + trust check; bounded fix loop; breaker | Full quality re-review; code changes |

## Handoff contract

No separate files — the gate reuses the feature folder's existing docs (`<feature-folder>` = `deliveries/<epic-name>/<repo>/<feature-name>/`).

| Artifact | Location | Written by | Content |
|---|---|---|---|
| **Brief** | dispatch prompt — seeded from the index per-cell brief + `context.md` | orchestrator | Cell scope, governing ADR ref, solution-doc section, branch, plan location, global constraints |
| **Step record** | `<feature-folder>/plan.md` (or `rework-<date>.md`) | executor | Per-step ✅/❌ status and the commit for each step |
| **Execution handoff** | `<feature-folder>/context.md` → `## Execution` | executor | Return status (`DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`), commit range (`base7..head7`), test evidence, its `review-code` outcome, concerns |
| **Diff** | fetched from git by the reviewer over the recorded `base7..head7` | reviewer | Commit list + stat + full diff; never enters the orchestrator's context |
| **Findings** | dispatch prompt → **planner**; recorded in `rework-<date>.md` | orchestrator → planner | Gate findings handed straight to the planner — not stored in the index |

- Seed the brief from the index per-cell brief plus `context.md` (which already carries the distilled spike context and spike references).
- `context.md` is **planner- and executor-owned** — the orchestrator never writes it; the planner registers the rework in `context.md`.
- The index tracks **status only** — no findings record.
- The executor appends each fix round's handoff to the same `## Execution` section.
- POC cells add `<feature-folder>/evaluation-report.md` (see **produce-poc-report**).

## Gate inputs

Dispatch a **fresh reviewer** agent (**review-code**) with: the cell brief (index scope + spike references), the recorded `base7..head7`, `<feature-folder>/plan.md`, `context.md`, the governing ADR, the solution-doc section, and global constraints. For a POC cell, also pass `<feature-folder>/evaluation-report.md` and its success criteria. The reviewer fetches the diff from git over the recorded range — no diff file. Never the executor instance that produced the work.

## Verdicts

1. **Spec compliance** — Missing / Extra / Misunderstood against the brief and governing ADR.
2. **Trust check** — verify the executor's claimed review outcome and test evidence against the diff. Do not re-run the suite; sample the claimed Blocker/Major fixes.

A full quality re-review is out of scope — `review-post-execution` already ran it.

## Bounded fix loop

| Round | Action |
|---|---|
| Pass | Mark the cell **verified** via **update-delivery-index** |
| Spec gap or Critical/Important | Dispatch the **planner** immediately with the findings — it writes a sibling `rework-<date>.md`; then the **executor**; then a scoped re-review |
| Cap (3 rounds) | Stop and escalate to the user — the cell cannot reach **verified** with an unresolved spec gap |

Never silently discard a finding.

- A fix is a **rework** — planned (**plan-development-task**) then executed (**execute-plan**), never a direct executor edit.
- The cell stays **in-progress** through the rework; the `rework-<date>.md` file is the record, not the index.
- Roll deferred Minors into the epic integration review.

## Epic integration review

When all cells are **done**, run one cross-cell review + integration test pass over the epic. Triage the deferred Minors from each cell's `context.md` `## Execution` handoff; surface residual load-bearing findings to the user. This is the epic-level analog of a whole-branch review — per-cell gates do not cover cross-cell interaction.

## Dispatch discipline

- **Model**: choose the cheapest capable model per dispatch and state it explicitly; escalate a stuck fix round.
- **Wait**: wait in bounded stretches; reconcile live children; chase any that finished silently.
- **No subagents**: a dispatched worker never spawns reviewers or helpers — the orchestrator owns every review seat.

## Checklist

- [ ] `plan.md` (or `rework-<date>.md`) shows every step ✅.
- [ ] `context.md` `## Execution` holds the return status and commit range.
- [ ] Reviewer fetched the diff over the recorded range.
- [ ] Reviewer is a fresh instance, not the executor.
- [ ] Both verdicts present: spec compliance and trust check.
- [ ] Fix loop within 3 rounds; an unresolved finding escalated to the user.
- [ ] Fix findings dispatched to the planner; the `rework-<date>.md` file is the record.
