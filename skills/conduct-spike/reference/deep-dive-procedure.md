# Deep-Dive Procedure

Full detailed procedure for the **deep-dive-specific-areas** capability. This is triggered when a user wants to continue a previous spike by digging deeper into specific unresolved areas.

## Step 1: Gather existing context

Ask the user to share the context from the previous spike. This may include:

- The original spike goal and investigation area list.
- Existing ADRs (draft or final) for any areas.
- Investigation notes, diagrams, or findings from the previous session.
- A solution document if one was already produced.
- If the user doesn't have these readily available, ask them to describe what was covered and what was decided.

## Step 2: Confirm the deep-dive scope

- Ask: "Which specific area(s) from the previous spike do you want to dig deeper into?"
- For each selected area, clarify: "What question remains unanswered? What uncertainty do you need to resolve?"
- Confirm which areas are **not** being revisited — those areas' decisions stand as-is.
- Validate: ensure the selected areas are still independently decidable and that the deep-dive scope is narrow enough to produce a conclusion.

## Step 3: Investigate deeper (per selected area)

- For each selected area, announce: "Deep-diving into area: [area name] — [specific unresolved question]."
- Load and apply the `investigate-code` skill (or adapt for greenfield per the greenfield-scenarios guidance), but with a **targeted, narrow focus**:
  - Scope investigation strictly to what's needed to answer the unresolved question.
  - Don't re-investigate what was already confirmed — reference existing findings and only fill gaps.
  - If the previous investigation was shallow, deepen it: trace deeper call paths, profile performance, prototype a critical path, research alternative technologies more thoroughly.
- Compile the new findings, noting what's new vs. what was already known from the previous spike. If the deep-dive reveals facts that contradict or refine previous findings, incorporate the corrections directly into the findings document.

## Step 4: Update the findings document(s) (per selected area)

- Load the existing findings document(s) from the previous spike.
- For each deep-dived area, update its findings document with the new investigation results, applying any corrections directly to the affected sections. If the area has its own findings doc, update that file. If using a consolidated doc, update the relevant section.
- Clearly mark what's new vs. what was previously known.
- Present the updated findings document(s) and ask the user to confirm before proceeding.

## Step 5: Evaluate solutions (per selected area)

- Present the deepened investigation findings (now reflected in the updated findings document).
- Apply the evaluate-solutions-per-area capability for each deep-dived area, leveraging the brainstorm prompts in `reference/solution-brainstorming-prompts.md`.
- If options were already considered in the previous spike, bring them forward — ask if any should be re-evaluated in light of new findings or if new options have emerged.
- Confirm the assumed solution for each area.

## Step 6: Update or produce ADRs (per selected area)

- If an ADR already exists for the area: load it, update the investigation findings, re-evaluate the options if needed, and revise the chosen option and consequences accordingly. Preserve the ADR's existing structure and metadata.
- If no ADR exists yet for the area: apply the draft-area-adrs capability to produce a new ADR.
- Ensure each ADR references the relevant findings document(s) for evidence.
- Keep the ADR clean: it contains only the revised decision (problem, drivers, options, chosen option, consequences). No logs or raw investigation data — any corrected facts live in the findings document.

## Step 7: Optionally update the solution document

- Ask: "Do the new or updated ADRs change the overall system-level view?"
- If yes, apply the compile-solution-doc capability to refresh the solution document, incorporating the updated ADR decisions.
- If no, note that the existing solution document remains valid. The new/updated ADRs supplement it.
- Keep the refreshed solution document clean: update only the affected target-state sections (diagrams, contracts, RAID, RACI). No logs, no change notes, no investigation history — those stay in the findings document.

## Step 8: Present the deep-dive results

- Summary of what was investigated deeper and what changed.
- The updated findings document(s) (or updated sections).
- The new or updated ADRs.
- The updated solution document (if applicable).
- Remind the user: "Other areas from the previous spike were not revisited. If those areas also need deeper investigation, we can deep-dive into them next."

## Step 9: Suggest spike directions for the next round

After presenting the deep-dive results, apply **suggest-spike-directions** to present direction candidates for the next spike round. Generate 3 go-deeper and 3 go-broader candidates grounded in what the deep-dive uncovered:

- **Go-deeper candidates**: Anchor to specific unresolved details surfaced by the deep-dive (e.g., "we decided on settlement extraction but didn't design the Kafka topic schema — should we spike that now?").
- **Go-broader candidates**: Anchor to adjacent concerns the deep-dive touched but didn't investigate (e.g., "settlement is now a critical dependency — should we spike its resilience requirements?").

Following the direction menu format in **suggest-spike-directions**, present the candidates and ask the user whether to pursue any direction or conclude the deep-dive. If the user selects a direction, treat it as a new spike scope and apply **define-spike-scope**.
