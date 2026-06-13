---
name: svg-editor
description: Create SVG diagrams and illustrations with professional layout, clear connections, and no overlapping elements. Use when creating flowcharts / process diagrams / architecture diagrams / sequence diagrams / concept diagrams / charts, or when fixing overlapping elements and unclear connections in any SVG visual diagram.
---

<when-to-use-this-skill>
- User wants to create a flowchart, process diagram, or workflow diagram as SVG
- User wants to create an architecture diagram, system design diagram, or component diagram as SVG
- User wants to create a sequence diagram or interaction diagram as SVG
- User wants to create a concept diagram, mind map, or visual explanation as SVG
- User wants to create a chart, graph, or data visualization as SVG
- User wants to create any SVG diagram that needs proper layout, visible elements, and clear connections
- User wants to fix overlapping elements, improve connection clarity, or adjust spacing in an existing SVG
</when-to-use-this-skill>

<knowledge>

<svg-layout-principles>
Core rules for arranging elements in any diagram type.

- **Canvas**: Use `viewBox="0 0 800 600"` as default. Scale proportionally for larger diagrams. Always leave 20–40px padding on all edges.
- **Spacing**: Minimum 20px gap between adjacent shapes. Group-related elements with 10–15px internal spacing and 30–40px external spacing from unrelated groups.
- **Connection corridor spacing**: Between two adjacent shapes that need connection lines, leave **minimum 40px gap** (20px per side for line routing). For shapes with multiple outgoing/incoming connections, increase gap to 60px minimum. Never place elements so close that connection lines have no room to pass between them.
- **Line clearance at turns**: Any point where a line bends (L-junction) must be at least **25px away** from the nearest edge of any other element. This prevents the corner of a line from appearing to collide with or clip into adjacent shapes.
- **Alignment**: Align elements of the same level (e.g., all siblings in a flowchart) to the same horizontal or vertical baseline. Center-align text within shapes.
- **Sizing**: Keep shapes of the same semantic type uniform in size. For text-based shapes, compute width from text length (approximately 8–10px per character + 20px padding).
- **Z-order**: Render connections (lines/arrows) **before** the shapes they connect so lines appear underneath shapes. Render text labels last (on top).
- **Overlap avoidance**: Before placing any new element, check bounding-box overlap with all placed elements. If overlap is detected, shift the new element (or redistribute surrounding elements) using a force-directed approach — increase spacing along the axis of overlap.
</svg-layout-principles>

<color-palettes>
Recommended color schemes for different diagram types.

| Diagram type | Background | Shape fill | Border | Connection | Text |
|---|---|---|---|---|---|
| Flowchart | `#FFFFFF` | Process: `#E3F2FD` (blue), Decision: `#FFF3E0` (orange), Start/End: `#E8F5E9` (green) | `#1565C0` / `#E65100` / `#2E7D32` | `#546E7A` | `#212121` |
| Architecture | `#FAFAFA` | Layer 1: `#E3F2FD`, Layer 2: `#E8F5E9`, Layer 3: `#FFF3E0`, External: `#F3E5F5` | `#37474F` | `#78909C` | `#212121` |
| Sequence | `#FFFFFF` | Actor box: `#E3F2FD`, Activation bar: `#BBDEFB` | `#1565C0` | `#546E7A` (solid), `#90A4AE` (dashed) | `#212121` |
| Concept | `#FFFFFF` | Central: `#E3F2FD`, Branch: `#F3E5F5`, Leaf: `#E8F5E9` | `#1565C0` | `#78909C` | `#212121` |
| Chart | `#FFFFFF` | Bars: `#42A5F5`, Line: `#EF5350`, Pie slices: `#42A5F5`/`#EF5350`/`#FFA726`/`#66BB6A`/`#AB47BC` | `#37474F` | Grid: `#E0E0E0` | `#424242` |

When displaying on dark backgrounds, invert: use light fills (`#37474F`), lighter borders (`#90A4AE`), and white text.
</color-palettes>

<connection-routing>
Guidelines for drawing lines and arrows between elements.

- **Orthogonal routing (default for flowcharts/architecture)**: Use horizontal and vertical line segments only (no diagonals). Build with `<path d="M x1 y1 L x2 y1 L x2 y2">` or `M x1 y1 L x1 y2 L x2 y2` depending on axis direction.
- **Curved routing (default for concept/sequence)**: Use cubic bezier curves for natural-looking connections. `<path d="M x1 y1 C cx1 cy1, cx2 cy2, x2 y2">` where control points create a smooth S-curve.
- **Arrow markers**: Define `<marker id="arrow" ...>` in `<defs>` and reference with `marker-end="url(#arrow)"`. Arrowhead size should be proportional to stroke width: arrowhead length = stroke-width × 4, arrowhead width = stroke-width × 3. The marker `refX` must be set so the arrow tip aligns exactly with the line endpoint (typically `refX="9"` for a 10×10 viewBox marker with a 2px stroke).
- **Arrow-line coordination**: The arrow marker's orientation must follow the line's tangent direction. Use `orient="auto"` on the `<marker>` so the arrowhead rotates to match the final line segment. The arrow shaft width should visually match the line stroke-width. After drawing, visually verify: the arrow tip should touch the target shape edge cleanly, the arrow body should align perfectly with the line, and there should be no gap or overlap between the line end and the arrow base.
- **Avoiding line-element overlap**: Connection endpoints should attach to the nearest edge of the target shape (not center-to-center). Calculate intersection of the line with the shape's bounding box and place the endpoint on the edge. The straight segment entering the target shape must be at least **15px long** (before the endpoint) so the arrowhead has room to render clearly.
- **Turn clearance at junctions**: For any L-shaped or Z-shaped line bend, the bend point (corner) must be **≥25px away** from the nearest edge of any shape, label, or other line junction. If a line must turn near a shape, route it in two segments: first move away from the shape to a clear turning zone, then turn and proceed to the destination.
- **Multi-line separation**: When multiple parallel lines run between the same two shapes (or through the same corridor), space them **≥8px apart** (center-to-center). Use different stroke colors or dash patterns to distinguish them. Never let two lines share the exact same path segment.
- **Label placement**: Place connection labels at the midpoint of the **longest straight segment** of the connection line, offset 8–12px perpendicular to the line direction. For single-segment lines this is the standard midpoint; for multi-segment (orthogonal) lines this avoids bends and corners. The label must not overlap any line segment — if the longest segment is too short to fit the label, move it to the next-longest straight segment with sufficient room. Use a white `<rect>` behind the label text to mask the line underneath.
- **Dashed lines**: Use `stroke-dasharray="6,4"` for asynchronous or data-flow connections, solid lines for synchronous/direct connections. For dashed lines, the arrow marker must also use a dashed-compatible fill (solid fill for the arrowhead is fine even on a dashed line).
</connection-routing>

<svg-element-reference>
Common SVG elements and attributes used in diagrams.

```svg
<!-- Rectangle (process step, node, component) -->
<rect x="10" y="10" width="120" height="40" rx="4" ry="4" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>

<!-- Rounded rectangle (start/end, database) -->
<rect x="10" y="10" width="120" height="40" rx="20" ry="20" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>

<!-- Diamond (decision) — use polygon -->
<polygon points="60,10 120,60 60,110 0,60" fill="#FFF3E0" stroke="#E65100" stroke-width="2"/>

<!-- Circle / Ellipse (connector, actor) -->
<circle cx="60" cy="60" r="30" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
<ellipse cx="60" cy="60" rx="40" ry="25" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2"/>

<!-- Text -->
<text x="70" y="35" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Label</text>

<!-- Arrow marker definition -->
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#546E7A"/>
  </marker>
</defs>

<!-- Path with arrow -->
<path d="M 130 30 L 250 30" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

<!-- Dashed line -->
<path d="M 130 30 L 250 30" stroke="#90A4AE" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow)"/>

<!-- Curved connection -->
<path d="M 130 30 C 190 30, 190 60, 250 60" fill="none" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

<!-- Label background pill -->
<rect x="180" y="24" width="30" height="16" rx="3" fill="#FFFFFF" stroke="none"/>
<text x="195" y="32" text-anchor="middle" font-size="10" fill="#546E7A">Yes</text>
</svg-element-reference>

<viewbox-strategy>
How to choose and scale the SVG viewBox.

- **Simple diagrams** (≤5 nodes): `viewBox="0 0 600 400"`
- **Medium diagrams** (5–15 nodes): `viewBox="0 0 800 600"`
- **Large diagrams** (15–30 nodes): `viewBox="0 0 1000 800"`
- **Wide diagrams** (many horizontal nodes): `viewBox="0 0 1200 600"`
- **Tall diagrams** (many vertical nodes): `viewBox="0 0 800 1000"`
- Rule of thumb: Calculate bounding box of all elements, then add 40px padding on all sides. Round up to nearest 50px.
- For responsive scaling, keep width/height ratio in `viewBox` consistent. Set SVG width to 100% and height to auto in HTML.
</viewbox-strategy>

<text-sizing>
How to size shapes based on text content.

- **Single-line text**: height = 40px; width = (text length in characters × 9px) + 24px padding; minimum width = 80px.
- **Multi-line text**: height = (line count × 22px) + 16px padding; width = (longest line chars × 9px) + 24px padding.
- **Headers/titles**: font-size 18px, bold.
- **Body labels**: font-size 14px, regular.
- **Small annotations**: font-size 11px, color `#757575`.
- Use `text-anchor="middle"` and `dominant-baseline="middle"` for centered text.
- For left-aligned text blocks, use `text-anchor="start"` and offset x by +12px from shape left edge.
</text-sizing>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Creating a flowchart with decision diamonds, branching paths, and process steps | Complete flowchart example with orthogonal routing and decision nodes | [examples/flowchart-example.md](examples/flowchart-example.md) |
| Executing **create-flowchart** (need detailed steps) | Flowchart step-by-step instructions with grid planning, orthogonal routing, and node rendering | [reference/create-flowchart.md](reference/create-flowchart.md) |
| Creating an architecture or system-design diagram with tiers and layers | Architecture diagram example with layered layout and curved connections | [examples/architecture-example.md](examples/architecture-example.md) |
| Executing **create-architecture-diagram** (need detailed steps) | Architecture diagram step-by-step instructions with layer layout and connection routing | [reference/create-architecture-diagram.md](reference/create-architecture-diagram.md) |
| Creating a UML-style sequence diagram with lifelines and activation bars | Sequence diagram example with proper lifeline and activation rendering | [examples/sequence-example.md](examples/sequence-example.md) |
| Executing **create-sequence-diagram** (need detailed steps) | Sequence diagram step-by-step instructions with lifeline, activation bar, and message rendering | [reference/create-sequence-diagram.md](reference/create-sequence-diagram.md) |
| Creating a concept map, mind map, or explanatory diagram | Concept diagram example with radial layout and bezier connections | [examples/concept-example.md](examples/concept-example.md) |
| Executing **create-concept-diagram** (need detailed steps) | Concept diagram step-by-step instructions with radial layout and bezier curve routing | [reference/create-concept-diagram.md](reference/create-concept-diagram.md) |
| Creating a bar chart, pie chart, line chart, or data visualization | Chart/graph example with axes, gridlines, and data series | [examples/chart-example.md](examples/chart-example.md) |
| Executing **create-chart** (need detailed steps) | Chart step-by-step instructions with axis planning, data rendering, and legend placement | [reference/create-chart.md](reference/create-chart.md) |
| Fixing overlapping elements, unclear connections, or spacing issues in an existing SVG | Layout analysis and fix example showing before/after transformation | [examples/layout-fix-example.md](examples/layout-fix-example.md) |
| Executing **analyze-and-fix-layout** (need detailed steps) | Layout analysis step-by-step instructions with overlap detection and connection re-routing | [reference/analyze-and-fix-layout.md](reference/analyze-and-fix-layout.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<create-flowchart>
**Objective**: Generate a flowchart, process diagram, or workflow diagram as raw SVG.
Load **reference/create-flowchart.md** for detailed step-by-step instructions.
</create-flowchart>

<create-architecture-diagram>
**Objective**: Generate a system architecture, component, or deployment diagram as raw SVG.
Load **reference/create-architecture-diagram.md** for detailed step-by-step instructions.
</create-architecture-diagram>

<create-sequence-diagram>
**Objective**: Generate a UML-style sequence diagram showing message passing between actors/components as raw SVG.
Load **reference/create-sequence-diagram.md** for detailed step-by-step instructions.
</create-sequence-diagram>

<create-concept-diagram>
**Objective**: Generate a concept diagram, mind map, or visual explanation as raw SVG.
Load **reference/create-concept-diagram.md** for detailed step-by-step instructions.
</create-concept-diagram>

<create-chart>
**Objective**: Generate a chart, graph, or data visualization as raw SVG.
Load **reference/create-chart.md** for detailed step-by-step instructions.
</create-chart>

<analyze-and-fix-layout>
**Objective**: Analyze an existing SVG diagram and fix overlapping elements, unclear connections, or poor spacing.
Load **reference/analyze-and-fix-layout.md** for detailed step-by-step instructions.
</analyze-and-fix-layout>

</capabilities>

<rules>
<rule>When the user describes a process flow, workflow, or algorithm with branching and decision steps, apply **create-flowchart**.</rule>
<rule>When the user describes a system with tiers, layers, components, or services and their relationships, apply **create-architecture-diagram**.</rule>
<rule>When the user describes interactions between actors/components over time with message passing, apply **create-sequence-diagram**.</rule>
<rule>When the user describes a central topic with branching related concepts, a mind map, or an explanatory diagram, apply **create-concept-diagram**.</rule>
<rule>When the user provides data values and wants a visual representation (bar, line, pie, scatter), apply **create-chart**.</rule>
<rule>When the user provides an existing SVG with overlapping elements, unclear lines, or cramped spacing, apply **analyze-and-fix-layout**.</rule>
<rule>When the user's request spans multiple diagram types (e.g., a flowchart embedded in an architecture diagram), apply the relevant capabilities sequentially and compose the output as a single SVG.</rule>
</rules>
