---
name: brainstorm-ideas
description: Facilitate structured brainstorming sessions that generate, evaluate, and refine ideas into actionable plans. Use when brainstorming, defining, exploring, generating, evaluating, or refining an idea to reach a goal.
---

<when-to-use-this-skill>
- User wants to brainstorm a rough idea into a concrete, actionable plan
- User wants to define goals or objectives for an idea
- User wants to explore potential challenges or obstacles
- User wants to generate creative ideas or solutions
- User wants to evaluate or prioritize competing ideas
- User wants to refine an idea into a stronger, more focused form
</when-to-use-this-skill>

<knowledge>
<brainstorming-principles>
- Great ideas come from asking the right questions, not just producing answers
- Challenging assumptions leads to stronger concepts
- Visual organization reveals connections and gaps
- Evaluation and prioritization matter as much as generation
</brainstorming-principles>
<questioning-protocol>
Drive the session with targeted questions:
- Ask one question at a time and wait for the response before the next
- Ask **7 to 100** targeted questions across the session
- Provide possible answers or examples with each question
- Ask follow-up questions when an answer is vague or incomplete
- Stop asking once the idea is clear and the plan is actionable
</questioning-protocol>
<facilitation-techniques>
Keep the user engaged and grounded:
- Use the user's preferred language; default to the language of their request
- Keep a casual, conversational tone using "we" language
- Use "what if" and "how might we" to explore possibilities
- Use examples or analogies to help visualize improvements
- Keep suggestions practical and feasible
</facilitation-techniques>
<idea-generation>
Generate 5–7 diverse ideas using thinking techniques and present them as a mind map. Details: [reference/idea-generation.md](reference/idea-generation.md)
</idea-generation>
<idea-evaluation>
Score ideas across value, feasibility, differentiation, scope, and impact. Details: [reference/idea-evaluation.md](reference/idea-evaluation.md)
</idea-evaluation>
<challenging-techniques>
Stress-test ideas with devil's-advocate techniques. Details: [reference/challenging-ideas.md](reference/challenging-ideas.md)
</challenging-techniques>
<plan-output-format>
End the session with a structured, actionable plan. Details: [reference/plan-output-format.md](reference/plan-output-format.md)
</plan-output-format>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Running a session on a new, unformed idea | End-to-end walkthrough of the full session | [examples/full-session-example.md](examples/full-session-example.md) |
| Improving a rough existing idea with clear gaps | Walkthrough applying capabilities selectively | [examples/refining-existing-idea.md](examples/refining-existing-idea.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<facilitate-session>
**Objective**: Run a structured brainstorm from idea to actionable plan.
1. Gather the idea or draft.
2. When a draft exists, extract the clear parts and note the gaps.
3. Apply **clarify-idea**.
4. Apply **identify-goals**.
5. Apply **explore-challenges**.
6. Apply **generate-ideas**.
7. Apply **evaluate-ideas**.
8. Apply **challenge-ideas**.
9. Apply **refine-idea**.
10. Apply **compile-actionable-plan** and present the final plan.
</facilitate-session>
<clarify-idea>
**Objective**: Produce a plain-language statement of the user's idea.
1. Ask the user to describe their initial idea or concept.
2. Ask who or what it is for, what it solves, and its current state.
3. Probe unstated assumptions about audience, approach, and scope.
4. Challenge vague statements by asking for concrete examples or success metrics.
5. Restate the idea in one or two sentences.
6. Request confirmation before proceeding.
</clarify-idea>
<identify-goals>
**Objective**: Define the primary objectives and success criteria.
1. Ask what the user wants to achieve with the idea.
2. Ask how they will know it succeeded.
3. Ask which objective matters most when several exist.
4. Summarize the goals.
5. Request confirmation before proceeding.
</identify-goals>
<explore-challenges>
**Objective**: Surface the obstacles the idea faces.
1. Ask what challenges or obstacles the user foresees.
2. Ask about risks, constraints, and dependencies.
3. Ask what could cause the idea to fail.
4. Present the challenge list with impact.
5. Request confirmation before proceeding.
</explore-challenges>
<generate-ideas>
**Objective**: Produce a diverse set of candidate ideas.
1. Generate **5–7 diverse ideas** per **reference/idea-generation.md**.
2. Present the ideas as a mind map per **reference/idea-generation.md**.
3. Request confirmation before proceeding.
</generate-ideas>
<evaluate-ideas>
**Objective**: Score and prioritize the candidate ideas.
1. Evaluate each idea across the dimensions per **reference/idea-evaluation.md**.
2. Identify risks, challenges, and trade-offs for each idea.
3. Prioritize the ideas with a simple framework (effort vs impact, MoSCoW).
4. Present the scored and prioritized ideas.
5. Request confirmation before proceeding.
</evaluate-ideas>
<challenge-ideas>
**Objective**: Stress-test the prioritized ideas before refining.
1. Play devil's advocate on the top ideas per **reference/challenging-ideas.md**.
2. Question scope creep and push for simpler, more focused solutions.
3. Suggest MVP or phased approaches when scope is too large.
4. Present the stress-tested ideas.
5. Request confirmation before proceeding.
</challenge-ideas>
<refine-idea>
**Objective**: Consolidate the surviving ideas into a single refined idea.
1. Combine the strongest elements from the top ideas.
2. Ask what additional elements would make it more robust or appealing.
3. Ask which elements are essential versus nice-to-have.
4. Present the refined idea statement and its essential elements.
5. Request confirmation before proceeding.
</refine-idea>
<compile-actionable-plan>
**Objective**: Deliver a structured, actionable plan.
1. Summarize the refined idea per **reference/plan-output-format.md**.
2. Map each confirmed challenge to its chosen solution.
3. List the essential components.
4. Write concrete next steps with owners or timeframes where possible.
5. Present the plan per **reference/plan-output-format.md**.
6. Ask the user to review and confirm the plan.
</compile-actionable-plan>
</capabilities>

<rules>
<rule>When the user wants to brainstorm an idea into an actionable plan, use **facilitate-session**.</rule>
<rule>When the user provides a rough idea, use **facilitate-session** and apply capabilities only for the gaps.</rule>
<rule>When the user requests one phase in isolation, apply that capability directly.</rule>
</rules>
