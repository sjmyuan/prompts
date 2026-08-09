---
name: question-everything
description: Question agent-reported information like a skeptic across completeness, correctness, and ambiguity, then verify independently before accepting. Use when questioning, challenging, verifying, or validating information returned by an agent or sub-agent.
---

<when-to-use-this-skill>
- User asks to question or challenge a result returned by an agent or sub-agent
- User wants a returned result verified before it is acted upon or committed
- User asks the agent to act as a skeptic toward a result or claim
- A result will be consumed downstream (decision, commit, merge, release) and being wrong is costly
- Two agents or sub-agents return conflicting results and a resolution is needed
- User asks to validate the correctness, completeness, or clarity of a returned result
</when-to-use-this-skill>

<knowledge>

<skeptic-mindset>
Treat every returned result as an unverified claim. The default stance is suspicion, not trust — trust is earned through questioning and independent verification. Never accept a result merely because it is confident, detailed, or produced by a capable-looking agent.
</skeptic-mindset>

<questioning-dimensions>
Question results across six dimensions: **Completeness** (missing paths/cases), **Correctness** (accuracy vs. primary sources), **Ambiguity** (vague wording), **Consistency** (self-contradiction), **Evidence** (claims backed by sources), **Assumptions** (silent premises). Load [reference/questioning-dimensions.md](reference/questioning-dimensions.md) for the full rubric with concrete questions per dimension.
</questioning-dimensions>

<verification-principles>
- **Independence**: verify with a NEW agent of the same type as the original investigator — never the original instance
- **Primary sources**: the verifier answers from code, docs, data, or logs, not by re-stating the original
- **Traceability**: every verdict maps to one challenge; never verify the result wholesale
</verification-principles>

<loop-control>
Accept when the verifier agrees with the original. When it diverges, dispatch a new agent of the same type as the original to redo the investigation with the updated information, then question the new result again. Cap the loop at 3 rounds, then stop and present both versions to the user. See [reference/verification-protocol.md](reference/verification-protocol.md) for comparison and escalation rules.
</loop-control>

<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| About to generate challenges on a returned result | Full dimension rubric with concrete questions per dimension | [reference/questioning-dimensions.md](reference/questioning-dimensions.md) |
| About to dispatch an independent verification agent | Brief template, dispatch rules, comparison and loop-control rules | [reference/verification-protocol.md](reference/verification-protocol.md) |
| A verification confirms the original result | End-to-end example of questioning → verification → acceptance | [examples/confirming-result.md](examples/confirming-result.md) |
| A verification contradicts the original result | End-to-end example of divergence → new round → convergence | [examples/contradicting-result.md](examples/contradicting-result.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<question-the-result>
**Objective**: Apply a skeptic's lens to a returned result and produce concrete, prioritized challenges.

1. Load [reference/questioning-dimensions.md](reference/questioning-dimensions.md) via the **context-loading-guide**.
2. Restate the result's key claims so each challenge targets one specific claim, never the result as a whole.
3. Probe each claim against the six dimensions using the rubric's questions.
4. Formulate each challenge as: the claim questioned, the dimension, why it is suspect, and what a satisfactory answer looks like.
5. Prioritize by impact — what breaks if the claim is wrong, and how plausible the error is.
6. Output the ordered challenge list; if no challenge survives, state that the result passes initial questioning.
</question-the-result>

<verify-the-claims>
**Objective**: Dispatch a new agent of the same type as the original investigator to verify the challenges against primary sources.

1. Load [reference/verification-protocol.md](reference/verification-protocol.md) via the **context-loading-guide**.
2. Detect the original agent's type (e.g., research agent, coding agent) and dispatch a NEW agent of the same type — never the original instance.
3. Compose the verification brief: the original result's claims, each challenge, the verification scope, and the required per-challenge verdict format.
4. Instruct the verifier to answer from primary sources only and to treat the original result as unverified.
5. Collect the verdicts, keeping each one traceable to its challenge.
</verify-the-claims>

<accept-or-requestion>
**Objective**: Compare verification verdicts with the original result, then accept or start a new round.

1. Load the comparison and loop-control rules in [reference/verification-protocol.md](reference/verification-protocol.md).
2. For each challenge, compare the verifier's verdict (AGREE / DISAGREE / UNCERTAIN) with the original claim.
3. If every material verdict is AGREE → accept the result; report the agreed claims and residual uncertainty.
4. If any material verdict is DISAGREE or UNCERTAIN → apply **reinvestigate-with-feedback** to have a NEW agent of the same type redo the investigation with the updated information; the loop then re-enters **question-the-result**.
5. If rounds reach the cap (3) without convergence → stop and present both versions to the user; never silently pick one.
</accept-or-requestion>

<reinvestigate-with-feedback>
**Objective**: Have a new agent of the same type as the original producer redo the investigation with the updated information.

1. Collect the divergence: the challenged claims, the verifier's DISAGREE/UNCERTAIN verdicts with evidence, and the corrected understanding.
2. Detect the original agent's type (e.g., research agent, coding agent) and dispatch a NEW agent of the same type — never the original instance, and never the verifier.
3. Brief it to redo the full investigation from scratch, incorporating the updated information — not to rubber-stamp the earlier result.
4. Collect the new result and confirm it addresses each divergence.
5. Pass the new result to **question-the-result** to begin the next round.
</reinvestigate-with-feedback>

</capabilities>

<rules>
<rule>When an agent or sub-agent returns a result that will be acted upon → apply **question-the-result** before accepting it.</rule>
<rule>When **question-the-result** raises challenges → apply **verify-the-claims** to confirm them independently.</rule>
<rule>When **verify-the-claims** returns verdicts → apply **accept-or-requestion** to compare them with the original result.</rule>
<rule>When **accept-or-requestion** finds a material DISAGREE or UNCERTAIN → apply **reinvestigate-with-feedback** to have a new agent of the same type redo the investigation with the updated info.</rule>
<rule>When **reinvestigate-with-feedback** returns a corrected result → apply **question-the-result** to question it again.</rule>
<rule>When a result passes questioning with no surviving challenges → accept it directly; for high-stakes results, still apply **verify-the-claims**.</rule>
</rules>
