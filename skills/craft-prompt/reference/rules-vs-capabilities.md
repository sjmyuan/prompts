# Rules vs Capabilities in Agent Files

Rules and capabilities serve distinct roles. Rules define **when** to act; capabilities define **how** to act.

| Element | Answers | Format |
|---|---|---|
| Rule | When to act | "When [condition], apply **capability-name** to [purpose]." |
| Capability | How to act | Numbered step-by-step procedure |

## Violation example

Procedural steps leaked into a rule:

```
<rule> **Plan phase**: Apply the plan-development-task skill to classify the change,
clarify requirements, generate a TDD plan, and present it for confirmation. </rule>
```

This rule embeds a 4-step procedure — it should be a capability, with the rule reduced to: "When the user submits a code change request, apply **plan-change**."

## Correct pattern

```
<capabilities>
<plan-change>
1. Apply the plan-development-task skill to classify the change type.
2. Clarify the scope with the user as needed.
3. Generate a TDD-based step-by-step plan and present for confirmation.
</plan-change>
</capabilities>

<rules>
<rule> When the user submits a code change request, apply **plan-change**. </rule>
</rules>
```

## Check

If removing a rule would lose procedural knowledge, that knowledge belongs in a capability, not the rule.
