# Fan-Out Guide: Signals, Splits, Briefs, Merge

Used by **fan-out-tasks** steps 1–9 and the self-linked knowledge pointers.

## Signals to fan out (all should hold)

| Signal | Meaning |
|---|---|
| Separable targets | ≥2 distinct modules, packages, entry points, repos, or candidate lists |
| Independent answers | Findings in one area do not change another's conclusion |
| Similar work | Same capability + same reporting doctrine across areas ("cover area X") |
| Enough effort | Serial run would sweep many locations; parallel reads beat one long pass |

Anti-signals (run directly):

- Serial dependency — one area's scope depends on another's findings
- Single small lookup, or a tightly coupled slice with bleeding boundaries
- Shared-write target — clones would edit the same files or state; fan-out is read-only / report-producing
- Platform cannot spawn same-type sub-agents

## Split heuristics

1. Cut along the strongest seams: repository → module/package → entry point → file cluster.
2. Make one area per seam; put boundaries where code touches least to minimize overlap.
3. Map each area to a sub-question whose answers compose to the original question.
4. Prefer 2–4 areas; more raises overlap and merge cost.

## Coverage sanity check (before dispatch)

- Every part of the original task is claimed by ≥1 area (no holes).
- No two areas claim the same target (no double-reads).
- Fix failures by re-partitioning; if that fails, run serially. Never guess; never ask.

## Brief invariants (host authors inline, per area)

1. Scope boundary — what is in and what is explicitly out.
2. Sub-question phrased from the original task.
3. Return contract echoing the host's reporting doctrine: findings with file:line, searched-negatives, confidence tags when the host uses them; keep it short — reports land in the host's context.
4. Self-containment — the brief carries every fact the clone needs; clones inherit no host history and see no other clone.
5. Leaf instruction — do not fan out further.

## Merge rules

- Merge short reports; re-read code only to spot-check a shared boundary, a conflict, or a sampled claim.
- Deduplicate — one underlying claim from two areas → report once, note both locations.
- Reconcile shared boundaries — a file claimed by two areas → read it once to settle.
- Surface conflicts — contradicting reports → present both with locations as an inconsistency; never average or hide.
- Spot-check at least one claim per area against primary sources — clones can err systematically, not only at shared boundaries.
- End with a coverage summary — areas covered, per-area returns, unresolved conflicts, searched-negatives.

## Platform dispatch detection

- Check whether the host may spawn same-type sub-agents on this platform.
- Available → dispatch all clones **in one response** — multiple dispatches in a single turn run in parallel; one per turn runs sequentially.
- Unavailable → run the same split serially (chunked) instead of abandoning the plan.

## Model routing

Pick the cheapest capable model per clone and state it explicitly — an omitted model inherits the host's session model, often the most expensive.

- Same work, but area complexity can differ: cheap for mechanical lookups, standard for multi-file tracing, capable for subtle reasoning.
- Clones are the same agent type; model choice is still per clone.

## Waiting on clones

- Never poll with short timeouts; never sit in one silent, open-ended wait.
- While local work remains (drafting briefs, preparing the merge), keep working — reports arrive on their own.
- When idle, wait in bounded stretches (five to ten minutes where the platform allows).
- Between stretches, reconcile live clones: list them and chase any that finished without reporting.

## Depth guard

- Clones are leaf tasks. Every brief forbids re-fan-out; dispatch is one level deep only.

## Common mistakes

| Mistake | Fix |
|---|---|
| "Fan out the whole thing" — no split | Cut along the strongest seams into 2–4 disjoint areas (Split heuristics). |
| Overlapping areas | One target per area; re-partition, or run serially. |
| Brief assumes host context | Make the brief self-contained — clones inherit no history. |
| One clone dispatched per turn | Put all dispatches in one response to run them in parallel. |
| Merging without a spot-check | Spot-check one claim per area against primary sources. |
| Hiding a contradiction | Present both reports as an inconsistency; never average. |
| Fanning out mutating work | Fan-out is read-only; run shared-write work directly. |
