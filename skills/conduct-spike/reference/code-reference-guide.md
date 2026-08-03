# Code Reference Guide

A code reference is the spike's living evidence map: where investigation evidence lives in the code. It exists so findings docs, ADRs, change summaries, and dispatched sub-agents can cite or reuse code evidence **without re-scanning the codebase**.

## Keeping it current

- Compile it during investigation (Phase 2) — before the findings doc, which cites it.
- Update it the moment new evidence is found, during any later work (deep-dive, follow-ups). No round/version tracking — it always reflects the code as it is now. Never rebuilt from scratch.

## Document structure

### 1. Scope
Repos covered, areas covered, last-updated date. A sub-agent reads this first to confirm it is looking at the right map.

### 2. Entry Points
| Area | Entry point (file:line) | Trigger | Purpose |

Controllers, listeners, scheduled jobs, `main` — where each area's flows start. Lets a sub-agent start at the right place instead of searching.

### 3. Key Code Locations
| Area | File:line | Symbol | Role | Why it matters for this spike |

The terrain map. Every row must carry a verifiable `file:line`.

### 4. Call Chains
For each key flow, an ordered numbered trace:
```
1. file:line — method — what happens (1-2 lines)
2. file:line — method — what happens
```
Cross-repo calls annotated `[repo: name]`. Saves sub-agents from re-tracing.

### 5. Evidence Ledger
| Claim / Question | Verdict | Evidence (file:line) | Confidence |

Claims are the spike's questions ("Is there a circuit breaker?"); verdict is the answer; evidence is the exact location; confidence is **verified** / **inferred** / **unverified**. Never present inference as evidence.

### 6. Cross-Area Dependencies
| From area | To area | Coupling (file:line) |

Where one area's code constrains another — feeds the findings doc's cross-area observations.

### 7. Searched-Negatives & Gaps
| Area | Search performed (pattern/query) | Result | Next step |

Dead-end searches recorded so sub-agents don't repeat them; open questions still to investigate.

## Rules

- **Precision**: every location is `file:line`; no vague "in the service layer" entries.
- **Confidence tags**: verified / inferred / unverified — an unverified claim is a gap, not evidence.
- **Searched-negatives are evidence**: a documented "not found" prevents repeated scans.
- **Always current**: updated the moment new evidence is found — no round/version tracking, never rebuilt from scratch.
- **Always passed to sub-agents**: any dispatched brief includes the code reference (or the relevant slice) plus the instruction to skip already-covered code and only dig into marked gaps.
