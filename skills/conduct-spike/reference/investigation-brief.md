# Investigation Brief

Ready-to-fill structured brief for `investigate-per-area` → `code-investigator` — loaded on demand when dispatching an area's investigation. Fills the **structured brief shape**; carries the shared evidence-map contract: **reference/dispatch-briefs.md** (**Evidence map in every brief**).

**Announce**: "Dispatching investigation of [N] area(s) to a sub-agent."

Fill one brief per area:

## 1. Mission
You are the `code-investigator`. Deliver: current-state findings plus a per-area evidence map for **[area]**.

## 2. Context
- Spike goal: **[goal]**
- Area: **[name]** — **[description]**
- Mode: **brownfield** (trace code) | **greenfield** (research approaches + POC; see **greenfield-scenarios**)

## 3. Inputs
- **[existing findings doc / evidence map path]** — start from its **Verified** claims; dig only **Gap** / **Inconsistency** / **Inferred** / **Assumption** claims. First pass (no doc yet): build the map from scratch.

## 4. Tasks
1. Apply `investigate-code` to the area — **[entry points / open questions]**.
2. Trace call chains to `file:line` precision.
3. Record an evidence-ledger verdict per claim (**Verified** / **Inferred** / **Assumption** / **Inconsistency** / **Gap**).
4. Record searched-negatives so downstream agents do not re-scan.

## 5. Output contract
- Narrative findings: current state, constraints, gaps (per `investigate-code` report format).
- Evidence map: entry points, key `file:line` locations, call chains, evidence ledger, searched-negatives (per **reference/findings-document-guide.md**).

## 6. Constraints
- Never modify code or artifacts — return findings only.
- Never re-verify a claim the findings doc marks **Verified**.
- Never assert a fact without a `file:line` or a recorded searched-negative.

## 7. Report back
- Flag every **Gap** / **Inconsistency** the findings doc does not already record.
- Flag anything that contradicts another area, for cross-area synthesis.
