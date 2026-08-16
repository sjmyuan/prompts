# Pipeline Integration Design

Used by **create-skill-file** (pipeline step 8) and **validate-created-skill** (rules step 6).

When a skill is part of a multi-skill pipeline (one skill's output is consumed by another), verify these 4 integration points:

1. **Handoff mechanism**: the producing skill includes an export/persist capability that writes output to a file; the consuming skill defines an input schema and supports loading from files. Do not rely on conversation text as the sole transport layer.
2. **Shared schema**: both skills agree on the transferred-data format; the consuming skill defines it and documents it in its knowledge section; the producing skill writes compliant output.
3. **Bidirectional awareness**: each skill references the other by name — the producing skill states what consumes its output; the consuming skill states where its input comes from.
4. **Guard clauses**: the downstream skill's when-to-use includes a constraint preventing premature loading (e.g., "Do NOT load when no plan has been generated yet — let [upstream-skill] handle it first").

Apply when the user describes a workflow involving multiple skills (e.g., "first plan, then execute").
