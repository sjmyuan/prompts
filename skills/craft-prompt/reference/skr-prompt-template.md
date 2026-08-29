# SKR Prompt Template

The canonical SKR prompt structure to fill when assembling the final prompt.

```
As a [role description], your task is to [task description] by leveraging the following knowledge, skills, and rules.

<knowledge>
[Background information, domain facts, examples, and context the AI needs.]
</knowledge>

<skills>
<skill-name>
[Step-by-step instructions for this skill.]
</skill-name>
</skills>

<rules>
<rule> When [condition], apply **skill-name** to [purpose]. </rule>
</rules>
```

## Fill rules

| Slot | Fill with |
|---|---|
| Role statement | The AI's persona and task |
| `<knowledge>` | Confirmed facts, context, examples, constraints |
| `<skills>` | One block per confirmed skill: name and steps |
| `<rules>` | Confirmed "When [condition], apply **skill-name** to [purpose]." rules |
