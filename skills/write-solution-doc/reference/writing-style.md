# Concise Writing Style

Applies to all prose in ADRs and solution documents. Tables and diagrams carry the detail; prose states takeaways.

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
| Consequence / risk item | ≤10 words |
| Pros / Cons bullet | 1 claim, no justification |
| Paragraph | ≤3 sentences |
| Sentence | ≤20 words, one clause |

## Atomic bullets
- Each bullet = one claim (fact or verdict), not a sentence with reasoning.
- Reasoning goes in the table or the section takeaway — never inside bullets.

## Tables over prose
- Anything comparative (drivers × options, pros/cons, RAID, RACI) is a table.
- Prose's only job: one line summarizing the table.

## Sentence surgery
- Active voice, subject–verb–object, one clause.
- Banned phrases — delete or rewrite:
  - "It is important to note that…" / "It should be noted that…"
  - "In order to" → "To"
  - "As mentioned above / earlier"
  - "Generally speaking" / "In general"
  - "Please note"
  - "The diagram shows X, Y, Z" (the caption is the summary)
  - "This means that" / "What this means is"
- Never restate what a diagram or table already shows.

## The "So what?" test
- Every sentence must add a new fact or answer "So what?" — otherwise delete it.
- Run this check on the final document before presenting.
