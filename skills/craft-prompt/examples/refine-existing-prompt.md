# Example: Refine an Existing Prompt

**Scenario**: User provides a vague prompt that only states a role and a task. Gap analysis finds missing knowledge, skills, and rules; each gap is filled before reassembly.

**Applies**: **refine-prompt**

## Input / Context

Existing prompt:

```
You are a helpful assistant. Improve my writing.
```

## Gap analysis

| Section | State | What is missing |
|---|---|---|
| Role | Present but vague | No persona, no domain, no quality bar |
| Knowledge | Absent | No facts about content type, audience, or style |
| Skills | Absent | No defined capabilities |
| Rules | Absent | No triggers for when to act |

## Refinement

Applied **collect-prompt-knowledge** — user confirms: content is technical blog posts; audience is developers; goal is clarity and concrete examples.

Applied **identify-prompt-skills** and **define-prompt-rules** — defined skills for accuracy checking and section restructuring, with matching triggers.

## Output — refined prompt

Written per **reference/prompt-writing-style.md** — directive voice, atomic bullets, rule format "When [condition], apply **skill-name** to [purpose].":

```
As a technical editor for developer blogs, your task is to improve draft articles for clarity, accuracy, and structure by leveraging the following knowledge, skills, and rules.

<knowledge>
- Content: technical blog posts
- Audience: developers
- Quality bar: clarity and concrete examples over length
</knowledge>

<skills>
<check-accuracy>
1. Verify technical claims and code examples.
2. Flag unsupported or outdated statements.
3. Suggest concrete examples for abstract points.
</check-accuracy>
<restructure-sections>
1. Split paragraphs over 6 lines.
2. Move off-topic sentences to a better section or delete them.
3. Add a lead sentence per section stating its point.
</restructure-sections>
</skills>

<rules>
<rule> When the user pastes a draft, apply **check-accuracy** first, then **restructure-sections**. </rule>
<rule> When a paragraph is over 6 lines, apply **restructure-sections**. </rule>
</rules>
```

Verification: every gap from the analysis table is filled in the output.
