# Fan-Out Guide: Signals, Splits, Briefs, Merge

Used by **fan-out-tasks** steps 1–8 and the self-linked knowledge pointers.

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
3. Return contract echoing the host's reporting doctrine: findings with file:line, searched-negatives, confidence tags when the host uses them.
4. Leaf instruction — do not fan out further.

## Merge rules

- Merge short reports; re-read code only to spot-check a shared boundary or a conflict.
- Deduplicate — one underlying claim from two areas → report once, note both locations.
- Reconcile shared boundaries — a file claimed by two areas → read it once to settle.
- Surface conflicts — contradicting reports → present both with locations as an inconsistency; never average or hide.
- End with a coverage summary — areas covered, per-area returns, unresolved conflicts, searched-negatives.

## Platform dispatch detection

- Check whether the host may spawn same-type sub-agents on this platform.
- Available → dispatch clones concurrently.
- Unavailable → run the same split serially (chunked) instead of abandoning the plan.

## Depth guard

- Clones are leaf tasks. Every brief forbids re-fan-out; dispatch is one level deep only.
