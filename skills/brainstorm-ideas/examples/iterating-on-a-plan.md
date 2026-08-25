# Example: Iterating on a Code-Review Plan

**Scenario**: Process topic — a focused round 1 improves a clear idea, then **iterate-session** deepens one direction. Shows **adaptive-pacing**, **iterate-session**, and the upgraded plan output.

**Applies**: **facilitate-session**, **iterate-session**
**Phases**: **clarify-idea**, **identify-goals**, **explore-challenges**, **generate-ideas**, **evaluate-ideas**, **challenge-ideas**, **refine-idea**, **compile-actionable-plan**

## Input / Context
User request: "My team's code reviews take days. The problem is clear — waiting and nitpicking — but I don't know the fix."

## Round 1 — focused mode
Facilitator: "The idea is clear, so I'll run focused mode — only the gaps, one checkpoint."

### clarify-idea (extract, don't re-ask)
Facilitator: "Captured: reviews take days because of waiting and nitpicking. What would faster mean in practice?"
User: "A non-trivial PR reviewed within one working day."

**Confirmed idea**: Get non-trivial PRs reviewed within one working day by cutting waiting and nitpicking.

### identify-goals
Facilitator: "What would success look like?"
User: "Median review time under 24 hours, and reviewers stop leaving nitpick comments."

**Confirmed goals**: median review under 24h; fewer nitpick comments.

### explore-challenges
Facilitator: "What could stop this — for example, reviewers being busy or PRs too big?"
User: "Reviewers are on other work, and PRs get too large before review."

**Confirmed challenges**: reviewer availability; oversized PRs.

### generate-ideas (focused set)
Facilitator: "Four candidates, quick pass:"

```
Faster Reviews
├── Inversion — smaller PRs
│   └── Enforce PR size limits
├── Combination — scheduled review slots
│   └── Shared review calendar
├── Elimination — no full re-review
│   └── One-pass approval, fix later
└── Analogy — like a queue
    └── Reviewer rotation queue
```

User: "PR size limits and the rotation queue feel strongest."

### evaluate + challenge (merged checkpoint)
Facilitator: "Scoring and stress-testing in one pass since these are few:"

| Idea | Value | Feasibility | Scope | Challenge result |
|---|---|---|---|---|
| PR size limits | High | High | Fits | Allow exceptions for big refactors |
| Reviewer rotation | High | High | Fits | One reviewer per PR, less context — acceptable |
| Review calendar | Medium | Medium | Fits | Dropped — coordination overhead |
| One-pass + fix later | Medium | Low | Fits | Dropped — quality risk |

**Refined idea**: Speed up reviews with PR size limits and a reviewer rotation queue.

### compile-actionable-plan (round 1)
Facilitator: "Here is the round-1 plan:"

## Refined Idea
Speed up code reviews with PR size limits and a reviewer rotation queue.

## Delta
Moved from "days of waiting" to two concrete levers: smaller PRs and assigned reviewers.

## Goals
- Median review time under 24 hours
- Reviewer nitpick comments near zero

## Challenges & Solutions
| Challenge | Solution |
|---|---|
| Reviewer availability | Rotation queue assigns a reviewer up front |
| Oversized PRs | PR size limits, exceptions for large refactors |

## Decisions & Deferred
- **Chose:** PR size limits; reviewer rotation queue
- **Dropped:** review calendar; one-pass + fix later
- **Open:** enforcing size limits without blocking big refactors

## Key Components
- PR size limit rule
- Reviewer rotation queue

## Next Steps
1. Define the PR size limit (depends on: team norms)
2. Set up the rotation queue
3. Pilot on one team and measure median review time

Facilitator: "Round 1 done. Want to go further — deepen a direction, combine, or pivot?"

## Round 2 — iterate-session
User: "Deepen the rotation queue — how should the rotation actually work?"

### Re-apply generate-ideas (deepen one direction)
Facilitator: "Three sub-ideas for the rotation:"

```
Rotation Queue
├── By expertise
│   └── Route to the owner of the touched area
├── By availability
│   └── Pick from reviewers free today
└── By fairness
    └── Round-robin across the team
```

User: "Expertise routing, with a round-robin fallback so nobody is skipped."

### Re-apply refine-idea
Facilitator: "So the queue routes by expertise first, falls back to round-robin. Does that hold against the availability challenge?"
User: "Yes — the fallback keeps it fair and unblocked."

**Refined addition**: rotation routes by expertise, falling back to round-robin.

### Update the plan
Facilitator: "Round-2 plan, updated with the queue decision (unchanged sections elided):"

## Refined Idea
Speed up code reviews with PR size limits and a rotation queue that routes by expertise with a round-robin fallback.

## Delta
Round 1 added the two levers; round 2 made the queue concrete.

## Goals
Unchanged: median review under 24h; nitpick comments near zero.

## Decisions & Deferred
- **Chose:** PR size limits; expertise-first rotation queue
- **Dropped:** review calendar; one-pass + fix later
- **Open:** size-limit enforcement mechanics

## Next Steps
1. Define the PR size limit (depends on: team norms)
2. Map reviewers to expertise areas
3. Build the queue: expertise match, then round-robin fallback
4. Pilot on one team and measure median review time

Facilitator: "Round 2 captured. Anything else to deepen, or is this the plan we lock in?"
