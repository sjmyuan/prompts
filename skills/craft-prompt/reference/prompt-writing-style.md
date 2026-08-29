# Prompt and Agent-File Writing Style

Generated prompts and agent files follow directive voice, BLUF, hard caps, and atomic bullets. Output is a procedure the AI executes — not a description.

## Hard caps

| Element | Cap |
|---|---|
| Frontmatter `description` | 1 sentence, ≤30 words |
| Role statement | 1 sentence |
| Knowledge bullet | 1 fact |
| Skill step | 1 imperative instruction, one clause |
| Rule | 1 sentence: "When [condition], apply **capability-name** to [purpose]." |
| Sentence | ≤20 words, one clause |

## Directive voice

- Every skill step starts with an action verb. No "the agent should…", no passive voice.
- Knowledge entries state facts directly: "The SKR framework structures prompts into three sections." Never "one may note that…".

## BLUF (Bottom Line Up Front)

- Open the prompt with a role statement that states the persona and task in one line.
- Open each skill with its objective in one line, then the steps.
- Open each knowledge entry with the fact, then details.

## Atomic bullets

- Each bullet = one claim, no justification or reasoning.
- Reasoning goes in tables or the section takeaway, never inside bullets.

## Tables over prose

- Rubrics, criteria, and mappings are markdown tables.
- Prose's only job: one line summarizing the table.

## Banned phrases

Delete or rewrite:

- "It is important to note that…" / "It should be noted that…"
- "In order to" → "To"
- "As mentioned above / earlier"
- "Please note"
- "The goal/purpose of this section is…" / "This section describes…" (the heading is the summary)
- "This means that" / "What this means is"

## No meta-commentary

- No narration of the author's actions ("I reviewed…", "we then…").
- No self-reference ("the above", "this step").

## SKR section conventions

| Section | Content | Format |
|---|---|---|
| Knowledge | Facts, examples, constraints the AI needs | Noun-phrase subsections; tables or atomic bullets |
| Skills | Named capabilities the AI executes | `<capability-name>` blocks with numbered imperative steps |
| Rules | When → capability routing | "When [condition], apply **capability-name** to [purpose]." |

## Agent-file wrapper pattern

Agent files that delegate to a skill contain only wrapper content: agent scope, tool restrictions, delegation rules, behavior constraints. Never duplicate the referenced skill's knowledge or steps.

```
Your task is to <task> by applying the `<skill>` skill step by step.

<knowledge>

<agent-scope>
Use this agent when the user wants to:
- <scenario>

Do NOT use this agent for:
- **<out-of-scope>** — use the <redirect> agent
</agent-scope>

</knowledge>

<rules>

<rule>When <condition>, apply the skill's **<capability>**.</rule>

</rules>
```

## "So what?" test

Every sentence must add a fact or answer "So what?" — otherwise delete it.
