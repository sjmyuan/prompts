# Verification Protocol

Use with **verify-sub-agent-results** (the verification loop).

## Independence rules

- Always dispatch a NEW agent of the SAME TYPE as the original investigator (e.g., another research agent for a research result, another coding agent for a coding result) — never the original instance. Applies to both the verification dispatch and the re-investigation dispatch.
- The verifier treats the original result as unverified and must answer from primary sources (code, docs, data, logs).
- Never show the verifier a pre-written "expected verdict" — only the claims and the challenges.
- If no same-type sub-agent is available, verify directly against primary sources in the current session.

## Brief template

```markdown
## Context
<the original result and its key claims>

## Challenges to verify
1. <challenge>: <claim> — <dimension> — <why suspect>

## Task
Verify each challenge against primary sources. Do not assume the original result is correct.
Read-only task — do not write or modify any files.
Return a per-challenge verdict, each citing its primary source (file:line, doc, or log):
- **AGREE** — claim holds, with the supporting source
- **DISAGREE** — claim is wrong, with the corrected claim and its source
- **UNCERTAIN** — cannot determine from available sources; state what is missing
```

## Comparison rules

- All material verdicts **AGREE** → accept the result; report agreed claims and residual uncertainty.
- Any material verdict **DISAGREE** or **UNCERTAIN** → dispatch a new same-type agent to redo the investigation (below), then re-enter **question-the-result** on the new result.
- Round cap: **3 rounds**. At the cap, stop and present both versions (original vs. verified) to the user for a decision — never silently pick one.
- Dispatch verification only for material (high/medium-priority) challenges; low-priority ones are noted, not verified.

## Re-investigation loop

- Dispatch a NEW agent of the SAME TYPE as the original investigator — never the original instance.
- The brief carries: the challenged claims, each DISAGREE/UNCERTAIN verdict with its cited source and evidence, and the corrected understanding.
- The agent redoes the full investigation from scratch and must address every divergence — not rubber-stamp the earlier result.
- The new result is then questioned again and re-verified by another new same-type agent in the next round.

## Traps

- Verifying the whole result instead of per-challenge — a wholesale "looks fine" is not a verdict
- Reusing the original agent instance in verification or re-investigation — it will defend or anchor on its own output; always dispatch a new agent of the same type
- Sending only the verdict back in re-investigation — the agent needs the verifier's evidence and corrected understanding to redo its investigation
- Treating "same wording" as agreement — compare substance and evidence, not phrasing
- Verifying low-priority challenges — dispatch only material (high/medium) challenges; low-priority ones are noted, not verified
- Accepting verdicts without a cited source — each AGREE/DISAGREE must name the primary source that supports it
- Infinite loops — always honor the round cap
