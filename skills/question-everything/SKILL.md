---
name: question-everything
description: Question agent-reported information like a skeptic across six questioning dimensions, raising challenges for others to verify. Use when questioning, challenging, or validating information returned by an agent or sub-agent.
---

<when-to-use-this-skill>
- User asks to question or challenge a result returned by an agent or sub-agent
- User asks the agent to act as a skeptic toward a result or claim
- A result will be consumed downstream (decision, commit, merge, release) and being wrong is costly
- Two agents or sub-agents return conflicting results and a resolution is needed
- User asks to validate the correctness, completeness, or clarity of a returned result
- User asks to raise questions about sub-agent results inside a spike pipeline — investigation findings or ADR decisions (via `conduct-spike`)
- Do NOT load to verify or accept a result yourself — this skill only raises challenges; verification belongs to the owning pipeline (e.g., `conduct-spike`)
</when-to-use-this-skill>

<knowledge>

<skeptic-mindset>
Treat every returned result as an unverified claim. The default stance is suspicion, not trust — trust is earned through questioning and independent verification. Never accept a result merely because it is confident, detailed, or produced by a capable-looking agent.
</skeptic-mindset>

<questioning-dimensions>
Question results across six dimensions: **Completeness** (missing paths/cases), **Correctness** (accuracy vs. primary sources), **Ambiguity** (vague wording), **Consistency** (self-contradiction), **Evidence** (claims backed by sources), **Assumptions** (silent premises). Load [reference/questioning-dimensions.md](reference/questioning-dimensions.md) for the full rubric with concrete questions per dimension.
</questioning-dimensions>

<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| About to generate challenges on a returned result | Six-dimension rubric, prioritization rules, and challenge output format | [reference/questioning-dimensions.md](reference/questioning-dimensions.md) |
| Seeing a worked questioning pass on a returned result | End-to-end example of raising prioritized challenges only | [examples/raising-challenges.md](examples/raising-challenges.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<question-the-result>
**Objective**: Apply a skeptic's lens to a returned result and produce concrete, prioritized challenges.

1. Load [reference/questioning-dimensions.md](reference/questioning-dimensions.md) via the **context-loading-guide**.
2. Restate the result's key claims so each challenge targets one specific claim, never the result as a whole.
3. Probe each claim against the six dimensions using the rubric's questions.
4. Formulate each challenge using the rubric's output format — the claim questioned, the dimension, why it is suspect, and a satisfactory answer.
5. Prioritize by impact — what breaks if the claim is wrong, and how plausible the error is.
6. Output the ordered challenge list; if no challenge survives, state that the result passes initial questioning.
7. Validate the output: each challenge names exactly one claim, states its dimension, explains why it is suspect, and defines a satisfactory answer; challenges are ordered by impact. Fix any failure before presenting.
</question-the-result>

</capabilities>

<rules>
<rule>When the user asks to question, challenge, or act as a skeptic toward an agent- or sub-agent-returned result, apply **question-the-result**.</rule>
<rule>When the user asks to validate the correctness, completeness, or clarity of a returned result, apply **question-the-result**.</rule>
<rule>When a result will be consumed downstream and being wrong is costly, apply **question-the-result** before the result is accepted.</rule>
<rule>When two agents or sub-agents return conflicting results, apply **question-the-result** to each result to surface the conflict.</rule>
<rule>When raising questions on sub-agent results inside a spike pipeline (investigation findings or ADR decisions via `conduct-spike`), apply **question-the-result** before verification.</rule>
<rule>Do NOT apply **question-the-result** to verify or accept a result — verification belongs to the owning pipeline (e.g., `conduct-spike`).</rule>
</rules>
