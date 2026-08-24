# Concise Writing Style

Applies to all prose in the delivery index (`deliveries/<epic-name>/index.md`). Tables carry the detail; prose states takeaways.

## Core rule: BLUF (Bottom Line Up Front)
- The **Summary** line states the epic state in one line.
- Every section opens with the conclusion in one line, then the why.
- Never narrate the orchestration process ("I dispatched…", "Agent X reported…") — record state and facts only.

## Hard caps

| Element | Cap |
|---|---|
| Summary line | 1 line |
| Feature description | 1 sentence |
| Bullet | 1 claim, no justification |
| Cell status note | 1 line (status + reason) |
| Sentence | ≤20 words, one clause |

## Atomic bullets
- Each bullet = one claim (fact or verdict), not reasoning.
- Reasoning goes in the table or the section takeaway — never inside bullets.

## Tables over prose
- Anything comparative (features, waves, cell statuses, dependencies) is a table.
- Prose's only job: one line summarizing the table.

## Rewrite transforms (apply via rewrite-concise)
Move-then-shorten: if a fact belongs in a table (status, wave, dependency, PR), move it there first, then shorten what remains. Facts outrank brevity — never drop a fact to hit a cap; a 20-word sentence is fine if it is the shortest faithful form.

| Wordy | Concise |
|---|---|
| F2 is contract-first, consumes F1, and cannot merge until F1 merges | bullet claim + dependency-table row |
| I dispatched agent X to plan F1 (process narration) | Status: planned — agent X |
| Each and every / in the event that / in the near future | Each / if / soon |
| Might possibly / somewhat / in general | delete (hedges) |
| Sentence >20 words | split at the second clause |

## Banned phrases
- "It is important to note that…" / "It should be noted that…"
- "In order to" → "To"
- "As mentioned above / earlier"
- "Please note" / "Generally speaking"
- Process narration: "I dispatched", "Agent X reported", "This means that"

## The "So what?" test
- Every sentence must add a new fact or answer "So what?" — otherwise delete it.
- Run this check during **rewrite-concise**, before confirming.
