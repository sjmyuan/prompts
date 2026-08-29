# Confidence & Coverage Guide

Presentation format for reporting findings honestly: what is certain, what is not, and what was missed. Backs the `<present-findings-with-confidence>` capability and the `<finding-confidence-model>` knowledge entry. Plain-language presentation (issue cards, tag legend, TL;DR, non-expert test) lives in **plain-language-presentation.md**.

## The Five Categories

| Tag | Meaning | When to use |
|---|---|---|
| ✅ Verified | Directly read in source, file:line confirmed | You opened the file and read the line |
| 🔶 Inferred | Reasoned from evidence, not directly confirmed | e.g., "no config file found, so the default serializer is assumed" |
| 💭 Assumption | Taken for granted without direct evidence | e.g., "sibling packages follow the same pattern" |
| ⚠️ Inconsistency | Contradiction between two sources of truth | code vs code, code vs docs, code vs config |
| ❓ Gap | Searched but not found, or not investigated | unread branches, unscanned repos, coverage limits |

## Confidence & Coverage Block Format

Close every investigation with a compact block:

```
### Confidence & Coverage
- ✅ Verified: ...
- 🔶 Inferred: ...
- 💭 Assumptions: ...
- ❓ Gaps: ...
- ⚠️ Inconsistencies: ...
```

## Phrasing Examples

- **Verified**: "`ChargingService` computes `fee = gross * 0.03` — Verified, `ChargingService.java:42`"
- **Inferred**: "🔶 Inferred — no config file found; Kafka default serializer assumed"
- **Assumption**: "💭 Assumption — 'the fee' is a single concept; a second `fee` exists in the payout branch (see Inconsistency)"
- **Gap**: "❓ Gap — only the charging branch was traced; the refund branch was not investigated"
- **Inconsistency**: "⚠️ Inconsistency — `README.md` states 5 retries, but `EmailAdapter.java:40` retries 3 times"

## Rules of Thumb

- A stated gap is a finding; a hidden gap is a partial truth. Never present "what I found" without "what I did not find".
- Inferred and Assumption findings must state *why*, so the user can verify the reasoning; render them as issue cards when consequential (per plain-language-presentation.md).
- Inconsistencies must locate both sides; classify severity per `reference/pattern-discovery-strategies.md`.
- When a gap is later closed, re-run the affected investigation step and update the profile.
