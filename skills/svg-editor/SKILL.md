---
name: svg-editor
description: Create SVG diagrams and illustrations with professional PPT-presentation-quality layout, clear connections, and no overlapping elements. Use when creating flowcharts / process diagrams / architecture diagrams / sequence diagrams / concept diagrams / charts, when fixing overlapping elements and unclear connections in any SVG visual diagram, when editing/modifying an existing SVG file, or when designing presentation-ready diagrams suitable for PPT/Keynote/Google Slides.
---

<when-to-use-this-skill>
- User wants to create a flowchart, process diagram, or workflow diagram as SVG
- User wants to create an architecture diagram, system design diagram, or component diagram as SVG
- User wants to create a sequence diagram or interaction diagram as SVG
- User wants to create a concept diagram, mind map, or visual explanation as SVG
- User wants to create a chart, graph, or data visualization as SVG
- User wants to create any SVG diagram that needs proper layout, visible elements, and clear connections
- User wants to fix overlapping elements, improve connection clarity, or adjust spacing in an existing SVG
- User wants to edit, modify, or update an existing SVG diagram (change colors, text, shapes, fonts, or styling)
- User wants to add, remove, or rearrange elements in an existing SVG diagram
- User wants SVG output that looks polished and professional enough for PowerPoint, Keynote, or Google Slides presentations
- User wants an existing SVG diagram upgraded to PPT-presentation quality (add shadows, gradients, title hierarchy, slide-ready layout)
</when-to-use-this-skill>

<knowledge>

<ppt-design-requirements>
All SVG output must meet professional presentation standards suitable for embedding in PPT/Keynote/Google Slides. These requirements apply to **every** diagram type generated or edited by this skill.

**Slide-ready dimensions**:
- Default aspect ratio: **16:9** (e.g., `viewBox="0 0 960 540"` is the standard PPT slide coordinate space). Use `viewBox="0 0 720 540"` for 4:3 legacy slides only when explicitly requested.
- The diagram should fill 60–85% of the slide area, leaving margins for the PPT title bar and presenter notes.
- Always include a **title area** at the top of the diagram: a bold, centered title text at y=30–40, font-size=20–24px, with optional subtitle at y=55–65, font-size=14–16px, color `#616161`.
- Leave a 30px bottom margin for optional slide footers or source annotations.

**Professional visual effects** (PPT-style polish):
- **Drop shadows**: Apply `<filter id="shadow">` with `feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.15"` to key shapes (title bars, hero containers, callout boxes). This creates the layered depth effect of PPT shapes.
- **Subtle gradients**: Replace flat fills with soft linear gradients for background panels and hero shapes. Use `<linearGradient>` with a 5–10% brightness variation between stops (e.g., `#E3F2FD` → `#BBDEFB`). Do NOT overdo gradients — they should be barely perceptible.
- **Rounded corners**: All rectangles should have `rx="6" ry="6"` or higher (PPT defaults to rounded shapes). Use `rx="4"` for small labels, `rx="8"` for containers.
- **Icons and visual anchors**: Use Unicode symbols, simple SVG paths, or emoji as visual anchors inside shapes when appropriate (e.g., ⚙ for settings, 📊 for data, 🔒 for security). Place icons at 18–24px font-size inside a small circle or to the left of text labels.

**Typography for presentations**:
- **Title**: `font-family="Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif"`, bold, font-size=22px, color=`#1A1A1A`.
- **Section headers**: font-size=16px, bold, color=`#333333`.
- **Body labels**: font-size=14px, regular, color=`#424242`.
- **Small annotations**: font-size=11px, color=`#757575`.
- **Minimum readable font size**: 10px at 960×540 viewBox. Anything smaller is unreadable on a projected slide.
- **Font consistency**: Use exactly one font-family stack across the entire SVG. Do NOT mix serif and sans-serif in the same diagram.

**Color contrast for projection**:
- All text must have a contrast ratio ≥ 4.5:1 against its background (WCAG AA for presentation readability).
- Light fills (`#E3F2FD`, `#E8F5E9`, `#FFF3E0`) with dark text (`#212121`) meet this. Avoid dark fills with dark text, or light fills with light text.
- On dark slide backgrounds, use light fills (`#37474F`, `#455A64`) with white text (`#FFFFFF`).

**Simplicity and scannability**:
- Limit to 5–8 main visual elements per diagram. If the concept requires more, split into multiple diagrams.
- Each shape should contain ≤ 15 words of text. Use keywords, not sentences.
- Group-related elements with subtle background panels (rounded rect with `fill="#F5F5F5"`, no stroke) and a section label.
- Use generous whitespace: minimum 40px between unrelated groups, 20px within groups.
</ppt-design-requirements>

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
Recommended color schemes for different diagram types. Choose the **PPT Professional** palette as the default for all presentation-bound diagrams. Use the Basic palette only when the user explicitly requests flat/minimal styling.

**PPT Professional palette (default for presentations)**:

| Diagram type | Background | Shape fill | Border | Connection | Text |
|---|---|---|---|---|---|
| Flowchart | `#FFFFFF` | Process: `#E8F0FE`→`#D2E3FC` (gradient), Decision: `#FEF7E0`→`#FDE293` (gradient), Start/End: `#E6F4EA`→`#CEEAD6` (gradient) | `#1A73E8` / `#F9AB00` / `#34A853` | `#5F6368` | `#202124` |
| Architecture | `#F8F9FA` | Layer 1: `#E8F0FE`, Layer 2: `#E6F4EA`, Layer 3: `#FEF7E0`, External: `#F3E8FD` | `#3C4043` | `#80868B` | `#202124` |
| Sequence | `#FFFFFF` | Actor box: `#E8F0FE`, Activation bar: `#D2E3FC` | `#1A73E8` | `#5F6368` (solid), `#9AA0A6` (dashed) | `#202124` |
| Concept | `#FFFFFF` | Central: `#E8F0FE`, Branch: `#F3E8FD`, Leaf: `#E6F4EA` | `#1A73E8` | `#80868B` | `#202124` |
| Chart | `#FFFFFF` | Bars: `#1A73E8`, Line: `#EA4335`, Pie: `#1A73E8`/`#EA4335`/`#FBBC04`/`#34A853`/`#8E24AA` | `#DADCE0` | Grid: `#E8EAED` | `#3C4043` |

**Basic palette (flat/minimal, use only when explicitly requested)**:

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
Common SVG elements and attributes used in diagrams. Includes PPT-quality variants with drop shadows and gradients.

```svg
<!-- Drop shadow filter (PPT-style) — define once in <defs> -->
<filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">
  <feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="#000000" flood-opacity="0.12"/>
</filter>

<!-- Gradient definition (PPT-style soft gradient) -->
<linearGradient id="gradBlue" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stop-color="#E8F0FE"/>
  <stop offset="100%" stop-color="#D2E3FC"/>
</linearGradient>

<!-- Rectangle with shadow (PPT-style process step) -->
<rect x="10" y="10" width="140" height="50" rx="8" ry="8" fill="url(#gradBlue)" stroke="#1A73E8" stroke-width="1.5" filter="url(#shadow)"/>

<!-- Rectangle (flat, no shadow — for minimal style) -->
<rect x="10" y="10" width="120" height="40" rx="4" ry="4" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>

<!-- Rounded rectangle (start/end) -->
<rect x="10" y="10" width="120" height="40" rx="20" ry="20" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>

<!-- Diamond (decision) — use polygon -->
<polygon points="60,10 120,60 60,110 0,60" fill="#FFF3E0" stroke="#E65100" stroke-width="2"/>

<!-- Circle / Ellipse (connector, actor) -->
<circle cx="60" cy="60" r="30" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
<ellipse cx="60" cy="60" rx="40" ry="25" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2"/>

<!-- Text with PPT font stack -->
<text x="70" y="35" text-anchor="middle" dominant-baseline="middle" font-family="Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif" font-size="14" fill="#202124">Label</text>

<!-- PPT Title bar -->
<rect x="0" y="0" width="960" height="60" fill="#1A73E8" filter="url(#shadow)"/>
<text x="480" y="36" text-anchor="middle" font-family="Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif" font-size="20" font-weight="bold" fill="#FFFFFF">Diagram Title</text>

<!-- Arrow marker definition -->
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#5F6368"/>
  </marker>
</defs>

<!-- Path with arrow -->
<path d="M 130 30 L 250 30" stroke="#5F6368" stroke-width="2" marker-end="url(#arrow)"/>

<!-- Dashed line -->
<path d="M 130 30 L 250 30" stroke="#9AA0A6" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow)"/>

<!-- Curved connection -->
<path d="M 130 30 C 190 30, 190 60, 250 60" fill="none" stroke="#5F6368" stroke-width="2" marker-end="url(#arrow)"/>

<!-- Label background pill -->
<rect x="180" y="24" width="30" height="16" rx="3" fill="#FFFFFF" stroke="none"/>
<text x="195" y="32" text-anchor="middle" font-size="10" fill="#5F6368">Yes</text>
</svg-element-reference>

<viewbox-strategy>
How to choose and scale the SVG viewBox. For all PPT-bound diagrams, prefer 16:9 aspect ratio.

- **PPT standard (16:9, default)**: `viewBox="0 0 960 540"` — this is the primary viewBox for all presentation diagrams.
- **PPT standard (4:3, legacy)**: `viewBox="0 0 720 540"` — use only when the user explicitly requests 4:3.
- **Simple diagrams** (≤5 nodes): `viewBox="0 0 800 450"` (16:9) or `viewBox="0 0 600 400"` (standalone).
- **Medium diagrams** (5–15 nodes): `viewBox="0 0 960 540"` (16:9) or `viewBox="0 0 800 600"` (standalone).
- **Large diagrams** (15–30 nodes): `viewBox="0 0 1200 675"` (16:9) or `viewBox="0 0 1000 800"` (standalone).
- **Wide diagrams** (many horizontal nodes): `viewBox="0 0 1200 600"`.
- **Tall diagrams** (many vertical nodes): `viewBox="0 0 800 1000"`.
- Rule of thumb: Calculate bounding box of all elements, then add 40px padding on all sides. Round up to nearest 50px.
- For responsive scaling, keep width/height ratio in `viewBox` consistent. Set SVG width to 100% and height to auto in HTML.
- When embedding in PPT, the diagram content area should fit within the middle 80% of the viewBox, leaving top margin for title and bottom margin for footer.
</viewbox-strategy>

<text-sizing>
How to size shapes based on text content. For PPT diagrams, use larger font sizes and generous padding.

- **Single-line text (PPT)**: height = 48px; width = (text length in characters × 10px) + 32px padding; minimum width = 100px.
- **Single-line text (standalone)**: height = 40px; width = (text length in characters × 9px) + 24px padding; minimum width = 80px.
- **Multi-line text**: height = (line count × 24px) + 20px padding; width = (longest line chars × 10px) + 32px padding.
- **PPT title**: font-size 20–24px, bold, color `#1A1A1A`.
- **Section headers**: font-size 16px, bold, color `#333333`.
- **Body labels**: font-size 14px, regular, color `#424242`.
- **Small annotations**: font-size 11px, color `#757575`.
- Use `text-anchor="middle"` and `dominant-baseline="middle"` for centered text.
- For left-aligned text blocks, use `text-anchor="start"` and offset x by +14px from shape left edge.
</text-sizing>

<flowchart-components>
Basic flowchart building blocks, their SVG shapes, valid connection points, and usage rules.

| Component | Shape | SVG Element | Dimensions | Connection points (attach lines here) | Usage |
|---|---|---|---|---|---|
| Start / End (Terminator) | Rounded rectangle | `<rect rx="20" ry="20">` | 120×40px or 140×50px | Center of bottom edge (outgoing), center of top edge (incoming) | One Start per flowchart (no incoming), one or more End nodes (no outgoing) |
| Process (Action Step) | Rectangle | `<rect rx="4" ry="4">` | 140×50px (min width 80px) | Center of top/bottom edges for vertical flow; center of left/right edges for horizontal flow | Standard action step, one incoming and one outgoing line |
| Decision | Diamond | `<polygon>` with 4 points | 80×80px (fit bounding box) | All 4 vertex points: top (incoming), right (Yes/True branch), bottom (incoming or outgoing), left (No/False branch) | Exactly one incoming, two or more outgoing branches; each branch MUST be labeled |
| Subprocess | Rectangle with side bars | `<rect>` + 2 vertical side lines | 140×50px | Same as Process | References another flowchart/subroutine |
| Document | Rectangle with wavy bottom | `<rect>` + `<path>` wave | 140×60px | Center of top edge (incoming), center of bottom edge (outgoing) | Represents a document or report output |
| Data / Database | Cylinder (ellipse + rect + ellipse) | `<ellipse>` + `<rect>` + `<ellipse>` | 100×60px (top ellipse 100×20) | Center of top ellipse (incoming/outgoing) | Data storage, database read/write |
| On-page Connector | Circle | `<circle>` | 30×30px (r=15) | Any edge point (incoming/outgoing) | Jump between non-adjacent flow sections on same page; matching label required |
| Off-page Connector | Pentagon / Home plate | `<polygon>` | 40×40px | Top edge (incoming), bottom edge (outgoing) | Jump to another page; matching label required |
| Parallel / Fork | Horizontal bar | `<rect>` | 160×8px | Center of left edge (incoming), center of right edge (outgoing); top & bottom edges for outgoing parallel branches | Split or join concurrent flows |
| Flow line | Arrow | `<path>` with `marker-end` | stroke-width=2 | Attaches from source connection point to target connection point | Connects two components; use orthogonal routing |

**Connection point rules**:
- **Vertical flow (top-to-bottom, default)**: Connect from bottom-center of source to top-center of target. For decisions, connect from bottom/top vertex to top-center of next shape.
- **Horizontal branches**: Connect from right-center of decision to top-center of branch target. The horizontal segment should extend at least 40px from the decision vertex before turning vertically.
- **Merge points**: When two branches converge to the same target, use a T-junction: the vertical line from above meets the horizontal line from the side at a right angle connection maintained by `<path d="M... L... L...">` without overlap.
- **Minimum edge distance**: Lines must attach to the **exact center** of the designated connection point on the shape edge (±2px tolerance). Off-center connections cause visual misalignment.
- For process/terminator/subprocess shapes, the valid connection points are exactly 4: top-center, bottom-center, left-center, right-center.
- For decision diamonds, the valid connection points are exactly 4: the 4 vertex corners. Never connect to the midpoint of a diamond edge — always use the vertices.
</flowchart-components>

<connection-validation>
Rules for detecting and avoiding connection issues in flowcharts.

<line-intersection-detection>
**Line intersection detection** — checking if two lines cross when they should not.

- **Orthogonal line segments**: A connection path consists of alternating horizontal and vertical segments. For each pair of connections, test every segment of one against every segment of the other.
- **Intersection test (horizontal vs vertical)**: A horizontal segment `(x1,y) → (x2,y)` and a vertical segment `(x,y1) → (x,y2)` intersect if `x` is between `x1` and `x2` AND `y` is between `y1` and `y2`. Ignore intersections at shared endpoints (where two lines meet at the same component is expected).
- **Same-direction segments**: Two horizontal segments on the same y must not overlap in x-range. Two vertical segments on the same x must not overlap in y-range.
- **Resolution when intersection is detected**:
  1. Insert an intermediate waypoint: raise one line to cross above the other at the intersection point, creating a bridge-like detour. Add a vertical offset of at least 10px before and after the crossing.
  2. Re-route one connection around the obstacle using a 3-turn path (Z-shape) instead of a 1-turn path (L-shape).
  3. Increase column spacing between the two branches by 40–60px to eliminate the crossing entirely.
  4. As a last resort, swap the order of branches (left ↔ right) if the semantics allow it.
- **Line-shape intersection**: Treat each shape's bounding box as a rectangle. Test if any line segment passes through a bounding box of a shape that is NOT its source or target. This is a critical error — the line must be re-routed around that shape.
</line-intersection-detection>

<label-position-validation>
**Label position validation** — checking that labels on connection lines are readable and not overlapping.

- **Label placement**: Place labels at the midpoint of the **longest straight segment** of the connection path. For a single-segment connection, this is the standard midpoint between two shapes.
- **Label background**: Always wrap connection labels in a `<rect>` background (white fill, 2–4px padding around text, `rx="3"`) placed directly behind the `<text>` element. This masks any line underneath.
- **Overlap check**: After placing a label, check its bounding box against all other elements (shapes, other labels, connection lines). The label background rect must not overlap any shape or other label. If overlap is detected:
  1. Move the label to the next-longest straight segment of the same connection.
  2. If no segment has sufficient room, shorten the label text or place it offset perpendicularly by +16px from the line (still with background rect).
  3. As last resort, increase spacing between the two shapes to create more room.
- **Label alignment**: Labels on horizontal segments should be centered above the line (offset y -14px). Labels on vertical segments should be centered to the right of the line (offset x +14px). When space is constrained, flip to the opposite side.
- **Label text length**: Ensure the label background rect width = (text chars × 7px) + 12px. If the straight segment is shorter than this width, the label does not fit — apply overflow resolution above.
</label-position-validation>

<connection-endpoint-validation>
**Connection endpoint validation** — checking that lines connect properly to their components.

- **Endpoint-on-edge check**: The line endpoint coordinates must lie exactly on the edge of the target shape's bounding box. For a process rect at `(x, y, w, h)`, the valid endpoint x must equal `x + w/2` (top/bottom edge center) or `x`/`x+w` (left/right edge center with appropriate y).
- **Minimum entry segment**: The straight line segment entering the target shape must be at least **15px long** before the endpoint. This ensures the arrowhead has room to render clearly without clipping into the shape edge.
- **Gap/overlap check**: The endpoint should touch the shape edge exactly. If there's a gap > 2px between endpoint and shape edge, extend the line. If the endpoint is inside the shape (> 2px penetration), retract the line.
- **Arrow alignment**: The arrow marker's orientation must match the direction of the final line segment entering the target. For a downward vertical entry, the arrow must point down. Verify `orient="auto"` is set on the `<marker>`.
- **Orphan connection check**: Every line must have both a valid source component and a valid target component. If a component is removed, all its incident lines must also be removed or re-routed to a new component.
</connection-endpoint-validation>

<arrow-style-guide>
**Arrow style guide** — when to use each arrow type.

| Arrow style | SVG marker | When to use |
|---|---|---|
| Standard solid arrow | `<path d="M 0 0 L 10 5 L 0 10 z" fill="#546E7A">` | Default for all sequential flow connections |
| Dashed line + solid arrow | `stroke-dasharray="6,4"` + standard marker | Async flow, data flow, or alternative path (not the main flow) |
| Open arrow (V-shape) | `<path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="#546E7A" stroke-width="2">` | Data flow in architecture/sequence diagrams; not typical for flowcharts |
| Bidirectional / Double arrow | Two markers (`marker-start` + `marker-end`) | Two-way communication; rare in flowcharts, use for architecture diagrams |
| Dot / Circle terminus | `<circle cx="5" cy="5" r="3" fill="#546E7A">` | Off-page connector references or notes; not for main flow |

- **Marker sizing**: Arrowhead length = stroke-width × 4, arrowhead width = stroke-width × 3. For stroke-width=2: length=8px, width=6px. Use `viewBox="0 0 10 10"` and scale via `markerWidth`/`markerHeight`.
- **Marker color**: Match the line stroke color. When changing line colors, create a new `<marker>` definition per color with matching fill.
- **No-arrow connections**: Merge lines (T-junctions where two lines converge) should not have an arrow on the merging segment — the main line carries the arrow.
</arrow-style-guide>

<turn-routing-guide>
**Turn routing guide** — when and how to bend connection lines.

- **1-turn (L-shaped, single bend)**: Use when source and target are on adjacent axes (e.g., source bottom-center → target left-center). Path: `M sx sy L sx ty L tx ty` — the turn happens at the intersection of the source x and target y (or vice versa).
- **2-turn (Z-shaped, two bends)**: Use when source and target share the same alignment axis but are offset (e.g., both are on the same vertical line but staggered horizontally). Path: `M sx sy L sx midY L tx midY L tx ty` — route away from source to a clear mid-y corridor, travel horizontally, then route to target.
- **3-turn (C-shaped, three bends)**: Use when a direct 1-turn or 2-turn path would intersect another shape or connection. Path: `M sx sy L sx ay L bx ay L bx by L tx by L tx ty` — route away from source, travel to a clear corridor away from obstacles, route around the obstacle, then approach target.
- **When to turn at a right angle**:
  - Turn **immediately** (within 20px of the source shape edge) if the outgoing direction is clear of obstacles.
  - Turn **delayed** (after 40–60px straight travel from source) if there are adjacent branches or parallel lines nearby — the extra straight run creates visual separation.
  - Do NOT turn inside the clearance zone of another shape — maintain ≥25px from any other shape's bounding box at the turn point.
- **Turn direction preference**:
  - In top-to-bottom flowcharts: route right-side turns (decision Yes branch) to the right, left-side turns (No branch) to the left.
  - Route clockwise when possible (turn right, then down, then left) — this is more natural for reader eye-tracking.
  - Avoid routing a line behind (upstream of) its source shape — always route forward in the flow direction.
- **Multi-branch turns**: When one decision node has multiple outgoing branches:
  - The Yes/True branch turns right and flows downward on the right side.
  - The No/False branch turns left and flows downward on the left side.
  - Both branches should maintain ≥40px horizontal distance from the main flow axis.
  - Both branches must converge back to the main flow at a merge point below, using T-junctions.
- **Turn point rounding** (optional): Use `stroke-linejoin="round"` on `<path>` for slightly rounded corners at turn points, making the diagram look polished. Do not add `rx`/`ry` to individual segments — this SVG attribute does not apply to paths.
</turn-routing-guide>

</connection-validation>

<computation-scripts>
All geometric calculations MUST be done by running Python scripts, NOT by AI reasoning or manual coordinate math. The scripts in `scripts/` provide deterministic, tested computations for layout, routing, labeling, and color validation.

**Scripts directory**: `skills/svg-editor/scripts/`

| Script | Purpose | Key functions |
|---|---|---|
| `compute_all.py` | **Main orchestrator** — takes JSON description, outputs JSON with all computed positions/paths/labels | `compute_diagram(desc)` — call from terminal: `python3 scripts/compute_all.py '<json>'` |
| `geometry.py` | Bounding box math, overlap detection, point/segment intersection | `overlap()`, `connection_point()`, `segment_line_intersection()`, `inflate_bbox()`, `union_bbox()` |
| `routing.py` | Orthogonal/bezier connection path computation, endpoint validation, intersection detection | `orthogonal_path()`, `bezier_path()`, `connection_endpoints()`, `detect_intersections()`, `endpoint_valid()` |
| `layout.py` | Grid/radial layout, force-directed overlap resolution, viewBox computation | `flow_layout()`, `decision_branch_positions()`, `force_directed_layout()`, `compute_viewbox()` |
| `labeling.py` | Label placement on connection paths, overlap checking | `label_position()`, `compute_all_labels()`, `label_overlap_check()` |
| `colors.py` | WCAG contrast ratio, PPT palette, gradient/shadow SVG defs | `contrast_ratio()`, `wcag_aa_check()`, `get_gradient_defs()`, `get_shadow_filter()` |

**compute_all.py input format** (JSON):
```json
{
  "diagram_type": "flowchart",
  "title": "Diagram Title",
  "ppt_mode": true,
  "flow_direction": "top-to-bottom",
  "nodes": [
    {"id": "start", "type": "start", "text": "Start", "width": 130, "height": 48, "row": 0, "col": 0},
    {"id": "p1", "type": "process", "text": "Step 1", "width": 150, "height": 54, "row": 1, "col": 0},
    {"id": "d1", "type": "decision", "text": "Ok?", "width": 90, "height": 90, "row": 2, "col": 0},
    {"id": "end", "type": "end", "text": "End", "width": 130, "height": 48, "row": 4, "col": 0}
  ],
  "edges": [
    {"id": "e1", "from": "start", "to": "p1"},
    {"id": "e2", "from": "p1", "to": "d1"},
    {"id": "e3", "from": "d1", "to": "end", "label": "Yes", "branch": "yes", "style": "solid"}
  ]
}
```

**compute_all.py output** includes:
- `nodes[]` — each with computed `x`, `y`, `bbox`
- `edges[]` — each with computed `path_d`, `waypoints[]`, `src_point`, `dst_point`
- `labels[]` — each with `x`, `y`, `bg_rect`, `side` for placement
- `viewbox` — computed `{x, y, width, height}`
- `defs` — SVG `<filter>` and `<linearGradient>` strings (when ppt_mode=true)
- `validation` — `node_overlaps`, `connection_issues`, `color_issues`, `all_clear`

**When to run compute_all.py**:
- Before generating ANY new SVG diagram — always compute layout via the script first
- When the user provides explicit node descriptions and connections — convert to JSON and run
- When modifying layout of an existing diagram — reconstruct JSON from the SVG, modify, re-run
- Do NOT manually calculate x/y coordinates, path d-strings, or label positions — use the script

**When to use individual script functions** (for partial computations):
- Use `geometry.overlap()` to check if two specific shapes overlap
- Use `routing.orthogonal_path()` to re-route a single connection around a new obstacle
- Use `colors.contrast_ratio()` to validate a specific text/background color pair
- Use `labeling.label_position()` to reposition a single label after layout change
</computation-scripts>

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
| Editing or modifying an existing SVG (color/text/element changes, restructuring) | SVG editing example showing style updates, element additions, and restructuring | [examples/modify-existing-svg-example.md](examples/modify-existing-svg-example.md) |
| Executing **modify-existing-svg** (need detailed steps) | SVG editing step-by-step instructions with element identification, modification planning, and structured editing | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Upgrading an existing SVG to PPT-presentation quality (adding shadows, gradients, title bars, slide-ready layout) | PPT upgrade example showing before/after transformation with professional effects | [examples/layout-fix-example.md](examples/layout-fix-example.md) |
| Executing **upgrade-to-ppt-quality** (need detailed steps) | PPT upgrade step-by-step instructions with shadow filters, gradient definitions, typography, and slide layout | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Computing layout, connection paths, or label positions for any diagram type | Python computation scripts for all geometric calculations (overlap, routing, labeling, contrast) | [scripts/compute_all.py](scripts/compute_all.py) |
| Need individual geometry/routing/layout/labeling/color functions for partial computation | Python utility modules for geometric calculations | [scripts/](scripts/) |
</context-loading-guide>

</knowledge>

<capabilities>

<create-flowchart>
**Objective**: Generate a PPT-presentation-quality flowchart, process diagram, or workflow diagram as raw SVG.

**CRITICAL — Computation**: All position, path, and label calculations MUST be done by running `python3 scripts/compute_all.py` with a JSON description of nodes and edges. Never manually calculate coordinates, path d-strings, or label positions. See `<computation-scripts>` for the JSON format and script reference.

Load **reference/create-flowchart.md** for detailed step-by-step instructions.
</create-flowchart>

<create-architecture-diagram>
**Objective**: Generate a PPT-presentation-quality system architecture, component, or deployment diagram as raw SVG.

**CRITICAL — Computation**: All position, path, and label calculations MUST be done by running `python3 scripts/compute_all.py`. Never manually calculate coordinates.

Load **reference/create-architecture-diagram.md** for detailed step-by-step instructions.
</create-architecture-diagram>

<create-sequence-diagram>
**Objective**: Generate a PPT-presentation-quality UML-style sequence diagram showing message passing between actors/components as raw SVG.

**CRITICAL — Computation**: All position, path, and label calculations MUST be done by running `python3 scripts/compute_all.py`. Never manually calculate coordinates.

Load **reference/create-sequence-diagram.md** for detailed step-by-step instructions.
</create-sequence-diagram>

<create-concept-diagram>
**Objective**: Generate a PPT-presentation-quality concept diagram, mind map, or visual explanation as raw SVG.

**CRITICAL — Computation**: All position, path, and label calculations MUST be done by running `python3 scripts/compute_all.py`. Never manually calculate coordinates.

Load **reference/create-concept-diagram.md** for detailed step-by-step instructions.
</create-concept-diagram>

<create-chart>
**Objective**: Generate a PPT-presentation-quality chart, graph, or data visualization as raw SVG.

**CRITICAL — Computation**: All position, path, and label calculations MUST be done by running `python3 scripts/compute_all.py`. Never manually calculate coordinates.

Load **reference/create-chart.md** for detailed step-by-step instructions.
</create-chart>

<analyze-and-fix-layout>
**Objective**: Analyze an existing SVG diagram and fix overlapping elements, unclear connections, or poor spacing. Also apply PPT-quality styling enhancements to the repaired output.

**CRITICAL — Computation**: Overlap detection MUST use `scripts/geometry.py` functions (call via `python3 -c "from scripts.geometry import overlap; ..."`). Connection re-routing MUST use `scripts/routing.py`. Never manually check for overlaps or compute paths.

Load **reference/analyze-and-fix-layout.md** for detailed step-by-step instructions.
</analyze-and-fix-layout>

<modify-existing-svg>
**Objective**: Modify an existing SVG diagram by changing colors, text, fonts, styling, or by adding, removing, or rearranging elements.
Load **reference/modify-existing-svg.md** for detailed step-by-step instructions.
</modify-existing-svg>

<upgrade-to-ppt-quality>
**Objective**: Upgrade an existing SVG diagram to professional PPT-presentation quality by adding drop shadows, soft gradients, a title bar, slide-ready 16:9 dimensions, and PPT-standard typography.

**Steps**:
1. **Analyze current SVG**: Read the existing SVG. Identify whether it already has `<defs>`, `<filter>`, or `<linearGradient>` elements. Note current viewBox dimensions, colors, font families, and whether a title bar exists.
2. **Set PPT viewBox**: If the current viewBox is not 16:9 (960×540), explain to the user that the aspect ratio will change and confirm before proceeding. For 4:3 presentations, use 720×540.
3. **Add PPT defs**: Insert or extend `<defs>` with:
   - Drop shadow filter: `<filter id="shadow">` with `feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.12"`
   - Soft gradients for shape fills (e.g., `#E8F0FE` → `#D2E3FC`) matching the PPT Professional palette
4. **Add title bar**: Insert a full-width title bar `<rect>` at the top of the viewBox (y=0, height=60px) with the diagram's main topic as title text in white, bold, 20–22px font on a `#1A73E8` background with shadow.
5. **Upgrade shape styling**: Apply `filter="url(#shadow)"` to key shapes, replace flat fills with gradient URLs, increase `rx`/`ry` to 6–8px for rounded corners, and update stroke colors to the PPT Professional palette.
6. **Upgrade typography**: Replace font-family with `Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif`. Bump body font-size to 14px minimum. Set text colors to `#202124` (primary), `#424242` (secondary), `#757575` (annotation).
7. **Adjust spacing**: Increase minimum inter-element gap to 40px. Add section background panels (`<rect fill="#F5F5F5" rx="8">`) to group related elements.
8. **Validate**: Check contrast ratios (≥4.5:1 text-to-background), ensure all text ≥10px, verify no elements overflow the viewBox, and confirm the title bar has `filter="url(#shadow)"`.

Load **reference/modify-existing-svg.md** for detailed step-by-step instructions on SVG editing patterns.
</upgrade-to-ppt-quality>

</capabilities>

<rules>
<rule>When generating any new SVG diagram, ALWAYS run `python3 scripts/compute_all.py` first with a JSON description of nodes and edges. Use the script's output (positions, paths, labels, viewbox, defs) to construct the SVG. Never manually calculate x/y coordinates, path d-strings, or label positions.</rule>
<rule>When checking for overlapping elements, ALWAYS use `python3 -c "import sys; sys.path.insert(0, 'scripts'); from geometry import overlap; ..."` — never visually estimate or reason about overlaps.</rule>
<rule>When validating connection endpoints or detecting line intersections, ALWAYS use functions from `scripts/routing.py` — never manually inspect SVG coordinates.</rule>
<rule>When validating color contrast, ALWAYS use `python3 -c "import sys; sys.path.insert(0, 'scripts'); from colors import contrast_ratio; ..."` — never estimate contrast visually.</rule>
<rule>When the user describes a process flow, workflow, or algorithm with branching and decision steps, apply **create-flowchart**. Output will be PPT-presentation-quality by default.</rule>
<rule>When the user describes a system with tiers, layers, components, or services and their relationships, apply **create-architecture-diagram**.</rule>
<rule>When the user describes interactions between actors/components over time with message passing, apply **create-sequence-diagram**.</rule>
<rule>When the user describes a central topic with branching related concepts, a mind map, or an explanatory diagram, apply **create-concept-diagram**.</rule>
<rule>When the user provides data values and wants a visual representation (bar, line, pie, scatter), apply **create-chart**.</rule>
<rule>When the user provides an existing SVG with overlapping elements, unclear lines, or cramped spacing, apply **analyze-and-fix-layout**.</rule>
<rule>When the user provides an existing SVG and wants to change its colors, text, fonts, styling, or add/remove/rearrange elements (without layout overlap issues being the primary concern), apply **modify-existing-svg**.</rule>
<rule>When the user wants to upgrade an existing SVG to PPT-presentation quality — adding professional effects like shadows, gradients, title bars, or slide-ready layout — apply **upgrade-to-ppt-quality**.</rule>
<rule>When the user's request spans multiple diagram types (e.g., a flowchart embedded in an architecture diagram), apply the relevant capabilities sequentially and compose the output as a single SVG.</rule>
</rules>
