# Sequence Diagram Conventions

Use native PlantUML sequence diagram syntax.

## PlantUML Quick Reference

| Pattern | Syntax |
|---|---|
| Participants | `actor "Name"`, `participant "Name"`, `database "Name"` |
| Sync call | `A -> B: N: methodName(params)` (solid arrow) |
| Async/event | `A ->> B: N: eventName(data)` (dashed arrow) |
| Return | `A --> B: N: <return value` (dotted arrow) |
| Activation | `activate A` / `deactivate A` |
| Conditional | `alt / else / end` |
| Loop | `loop N times / end` |
| Parallel | `par / end` |

## Message Numbering

Number messages sequentially for call-stack cross-referencing. Indentation in labels reflects call depth:

```plantuml
A -> B: 1: getUser(id)
B -> C: 2:   findById(id)
C -> D: 3:     SELECT ...
D --> C: 4:     <return
C --> B: 5:   <return
B --> A: 6: <return
```

Return messages get their own numbers. Frame numbers in call stack traces must match these numbers.

## Participant Naming

Use `"repo-name\\nComponentName"` to show both the repo/container and the component on the lifeline.
