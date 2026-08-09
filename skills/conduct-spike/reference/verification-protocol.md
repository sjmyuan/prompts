# Verification Protocol

Use with **verify-the-claims** (dispatch) and **accept-or-requestion** (compare and loop).

## Independence rules

- Always dispatch a NEW agent of the SAME TYPE as the original investigator (e.g., another research agent for a research result, another coding agent for a coding result) — never the original instance. Applies to both **verify-the-claims** and **reinvestigate-with-feedback**.
- The verifier treats the original result as unverified and must answer from primary sources (code, docs, data, logs).
- Never show the verifier a pre-written "expected verdict" — only the claims and the challenges.

## Brief template

```markdown
## Context
<the original result and its key claims>

## Challenges to verify
1. <challenge>: <claim> — <dimension> — <why suspect>

## Task
Verify each challenge against primary sources. Do not assume the original result is correct.
Return a per-challenge verdict:
- **AGREE** — claim holds, with evidence
- **DISAGREE** — claim is wrong, with the corrected claim and evidence
- **UNCERTAIN** — cannot determine from available sources; state what is missing
```

## Comparison rules (accept-or-requestion)

- All material verdicts **AGREE** → accept the result; report agreed claims and residual uncertainty.
- Any material verdict **DISAGREE** or **UNCERTAIN** → apply **reinvestigate-with-feedback** (below), then re-enter **question-the-result** on the new result.
- Round cap: **3 rounds**. At the cap, stop and present both versions (original vs. verified) to the user for a decision — never silently pick one.

## Re-investigation loop (reinvestigate-with-feedback)

- Dispatch a NEW agent of the SAME TYPE as the original investigator — never the original instance.
- The brief carries: the challenged claims, each DISAGREE/UNCERTAIN verdict with evidence, and the corrected understanding.
- The agent redoes the full investigation from scratch and must address every divergence — not rubber-stamp the earlier result.
- The new result is then questioned again and re-verified by another new same-type agent in the next round.

## Traps

- Verifying the whole result instead of per-challenge — a wholesale "looks fine" is not a verdict
- Reusing the original agent instance in **verify-the-claims** or **reinvestigate-with-feedback** — it will defend or anchor on its own output; always dispatch a new agent of the same type
- Sending only the verdict back in **reinvestigate-with-feedback** — the agent needs the verifier's evidence and corrected understanding to redo its investigation
- Treating "same wording" as agreement — compare substance and evidence, not phrasing
- Infinite loops — always honor the round cap
