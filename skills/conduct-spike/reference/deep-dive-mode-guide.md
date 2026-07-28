# Deep-Dive Mode Guide

When a user has previously conducted a spike (formally or informally) and now wants to drill deeper into specific investigation areas, the skill operates in **deep-dive mode**. This is distinct from:

- **Full spike**: Starts from scratch with scope definition; all areas go through the full 5-phase workflow.
- **From existing findings**: The user already has complete findings and just wants to formalize them — investigation is skipped entirely, all areas proceed through evaluate → ADR → solution doc.
- **Revising an ADR**: The evaluation is already done and an ADR exists; only the ADR text needs updating.

## When deep-dive mode applies

Deep-dive mode is for when:

- The user completed a spike but one or more areas had open questions, insufficient depth, or no conclusion reached.
- The user has existing context (scope, partial ADRs, investigation notes) but needs focused re-investigation and evaluation on a subset of areas.
- The goal is to reach a decision on those specific areas, which may produce new ADRs or update existing ones.

## What stays vs. what changes

Areas not selected for deep-dive are left as-is — their existing findings docs, ADRs, and decisions are preserved. The full deep-dive procedure is defined in the **deep-dive-specific-areas** capability and detailed in `reference/deep-dive-procedure.md`.
