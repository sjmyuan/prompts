# PlantUML Standards

When writing PlantUML diagrams:
- Use `@startuml` / `@enduml` blocks.
- For C4 diagrams, prefer the C4-PlantUML standard library macros (`Person`, `System`, `Container`, `Component`, `Rel`, etc.).
- For sequence diagrams, use `participant`, `->`, `-->`, `activate`/`deactivate`, `note`, `alt`/`else`, `loop`, `group` etc.
- Keep diagrams focused and readable — no more than 8–12 elements per diagram.
- Every diagram must include a brief caption/explanation in the document.
- Support both English and Chinese labels based on user preference.
- Always provide complete, renderable PlantUML code inside a fenced code block with `plantuml` language tag.
