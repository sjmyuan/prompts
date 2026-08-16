# ADR-Drafting Brief

Ready-to-fill structured brief for `draft-problem-adrs` → `adr-writer` — loaded on demand when dispatching ADR drafting. Fills the **structured brief shape**; shared evidence-map contract: **reference/dispatch-briefs.md** (**Evidence map in every brief**).

**Announce**: "Dispatching ADR drafting for [N] problem(s) to a sub-agent."

Fill one brief per area (batch the area's problems into one brief when they share its evidence):

## 1. Mission
You are the `adr-writer`. Deliver: one ADR per problem for **[area]**, evaluated and drafted via `draft-adr`.

## 2. Context
- Spike goal: **[goal]**
- Area: **[name]** — **[description]**
- Problems: **[problem list — "How to …?"]**

## 3. Inputs
- The area's findings doc (evidence sections) — cite evidence locations; do not re-read code.

## 4. Tasks
1. Load `draft-adr` and run the full flow — **define-decision-drivers** → **define-considered-options** → **evaluate-options** (apply **detail-options-tech** when tech details are needed) → **compile-adr**.
2. Run the user dialog (drivers, options, chosen option) inside this session.
3. Tag each ADR with its **Area:**.

## 5. Output contract
- One ADR per problem, standalone-readable, citing findings-doc evidence locations (per `draft-adr`'s compile-adr checklist).

## 6. Constraints
- Never hand-edit ADR content outside `draft-adr`.
- Never cite evidence the findings doc does not support.

## 7. Report back
- Flag every constraint / risk / fact an option reveals that the findings doc lacks, so the spike can sync it (per **artifact-maintenance-doctrine**).
