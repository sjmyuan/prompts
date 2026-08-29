# Plain-Language Presentation

Presentation rules that make findings comprehensible. Backs the `<plain-language-presentation>` knowledge entry. Complements `confidence-and-coverage-guide.md` (what to tag) and `writing-style.md` (how to write).

## Core doctrine

Explanation outranks brevity for findings. A finding the reader cannot act on is not concise — it is useless. Routine ✅ Verified facts stay terse; issues and uncertainty get plain-language explanation.

## Explain only issues/uncertainty

Apply plain-language explanation to:
- ⚠️ Inconsistencies
- ❓ Gaps with consequences
- 🔶 Inferred or 💭 Assumption findings whose reasoning the user must verify
- The bottom line of any multi-finding response

Do NOT explain routine ✅ Verified facts (e.g., "fee = gross * 0.03 at `ChargingService.java:42`").

## Issue card (mandatory for every issue)

Render every issue as a 5-field card:

```
### ⚠️ Issue: <name>
- **Problem**: <what, in plain words — no jargon>
- **Evidence**: <file:line; both sides for inconsistencies>
- **Why it matters**: <impact on behavior, correctness, or the user's decision>
- **What to do**: <next step the reader can take>
- **Confidence**: <tag + one-line reason>
```

Skip "What to do" only when the investigation cannot know it — then say so.

## Tag legend (first use in a response)

The first time tags appear, add a one-line plain glossary:
> ✅ Verified = I read it in code · 🔶 Inferred = reasoned guess, check my logic · 💭 Assumption = taken for granted · ⚠️ Inconsistency = two sources disagree · ❓ Gap = not investigated

## Human TL;DR (multi-finding responses)

Open any response with two or more findings (or any issue) with a 3-line plain summary:
- **What I found** — one sentence
- **The issue** — one sentence (or "none")
- **What it means for you** — one sentence

## Non-expert test (comprehension gate)

Before returning, read your output as a non-expert. Pass means the reader can state:
1. What the answer is
2. Why (reasoning behind any issue/uncertainty)
3. What to do about it
4. How much to trust it (tag + why)

Fail → add the missing plain-language line. This gate runs in every capability's Validate step.

## Relation to writing-style.md

`writing-style.md`'s "no justification in bullets" applies to routine claims and table rows. Issue cards and why-clauses override it — an issue finding carries one plain why-clause (≤15 words).
