# Concise Writing Style

Applies to all prose in ADRs and solution documents. Tables and diagrams carry the detail; prose states takeaways. All caps below apply to prose only — diagrams, tables, and code diffs are exempt and carry the full detail.

## Core rule: BLUF (Bottom Line Up Front)
- Open every section with the conclusion in one line, then the why.
- Under each heading, the first line is a **bolded one-line takeaway** (e.g., `**Verdict:** …`, `**Trade-off:** …`).
- Never lead with evidence, background, or analysis.

## Hard caps

| Element | Cap |
|---|---|
| Section opening takeaway | 1 sentence (≤15 words) |
| Context / problem statement | ≤3 sentences |
| Decision justification | 1 sentence |
| Option summary (what it is, strengths, risks) | ≤3 sentences |
| Decision drivers | ≤6 items (one fact each) |
| Consequences | ≤4 items per subsection |
| Consequence / risk item | ≤10 words |
| Pros / Cons bullet | 1 claim, no justification |
| Paragraph | ≤3 sentences |
| Sentence | ≤20 words, one clause |

## Atomic bullets
- Each bullet = one claim (fact or verdict), not a sentence with reasoning.
- Reasoning goes in the table or the section takeaway — never inside bullets.

## Diagrams & tables over prose
- Anything comparative (drivers × options, pros/cons, RAID, RACI) is a table.
- If a diagram or table can carry it, prose must not restate it — the caption or a one-line summary is the only prose allowed.
- Prefer a diagram when it conveys the relationship or flow in less reading time than the prose it replaces; otherwise a single sentence beats a sprawling diagram.
- Prose's only job: one line summarizing the table or diagram.

## Single source of truth
- Every fact appears exactly once in the document; every other mention is a reference, never a restatement.
- Never repeat a fact already given in Context, a table, or a diagram elsewhere in the ADR.

## Sentence surgery
- Active voice, subject–verb–object, one clause.
- Prefer a number to an adjective: "fast" → "2×", "significant" → "3 ms", "large" → "500 users".
- Banned phrases — delete or rewrite:
  - "It is important to note that…" / "It should be noted that…"
  - "In order to" → "To"
  - "As mentioned above / earlier"
  - "Generally speaking" / "In general"
  - "Please note"
  - "The diagram shows X, Y, Z" (the caption is the summary)
  - "This means that" / "What this means is"
- Never restate what a diagram or table already shows.

## The driver-anchored "So what?" test
- Every sentence must move a decision-driver score or add a fact a future reader needs to trust or redo the decision — otherwise delete it.
- Run the delete-by-default pass before presenting: cut ~20% (every sentence that fails the test), then re-add only what is load-bearing.
