# Call Stack Trace Conventions

## Format

```
[N] MethodSignature(params)
  File: project-relative/path/File.java:Line
  Parameters: name1=value1, name2=value2
  Returns: ReturnValue (Type)
  Code:
  │  Line: relevant code
  ╰─→ [N+1] NextMethod(params)
```

Each frame includes: method signature, file path + line number, parameter values (omit large payloads), return value, 2-5 lines of relevant code, and side effects (DB writes, event publishing, external API calls).

## Hierarchy Notation

- `├─→` for first branch, `╰─→` for last branch
- `[async]` prefix for asynchronous calls
- `[condition]` for conditional branches
- `[repeated N×]` for loops
- `[repo: repo-name]` for cross-repo calls

## Correlation with Sequence Diagrams

Frame `[N]` must match message number `N` in the corresponding sequence diagram:

```
Sequence:  A -> B: 3: findById(id)
Call Stack: [3] B.findById(id: String)
```
