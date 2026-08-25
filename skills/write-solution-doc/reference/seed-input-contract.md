# Seed Input Contract

Backs the `<current-state-mode>` knowledge entry for the embedded (sub-agent) use case: `conduct-spike` dispatches the `solution-doc-writer` agent to compile findings docs (current-state mode) and solution docs (baseline-input mode). Defines what a seeding brief must provide, the guard clause, and what the agent returns.

## Input schema (what a seeding brief must provide)

A brief embedding this skill MUST include:

| Field | Required | Notes |
|---|---|---|
| Mode | Yes | `current-state` (as-is findings) or `baseline-input` (target-state from a baseline) |
| Seed content | Yes | Existing findings docs, diagrams, or the solution decision being documented |
| Scope boundary | Yes | Sections to compile vs. skip; out-of-scope spike context |
| Language | No | Default: brief language; else detect from user input |

Without a mode and seed content, the skill cannot determine which sections to produce — do not begin the sequence.

## Guard clause

- Embedded mode: do NOT re-gather or re-question what the brief already seeded — incorporate it directly per the pre-existing-content rule.
- No seed content and no mode provided: STOP and request the seed before running `clarify-business-context`.
- Standalone sessions (no brief): the full questioning sequence applies normally.

## Return contract (what the agent returns to the orchestrator)

Return to the orchestrator:

1. **Compiled documents** — final solution document (or findings doc in current-state mode) at the agreed artifact path.
2. **Mode confirmation** — which mode was used and which baseline (if any) was evolved.
3. **Skipped sections** — sections marked `[Skipped]` and why.
4. **Open decisions** — items needing user or orchestrator input before the document is final.

The orchestrator (`conduct-spike`) validates structure and presentation; this skill owns the format rules.
