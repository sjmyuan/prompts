# Create Concept Diagram — Detailed Steps

Applies **create-concept-diagram** in the svg-editor skill.

**Steps**:
1. **Identify the central concept and branches**: Determine the core topic (center) and related sub-concepts. Organize sub-concepts into hierarchical levels (depth ≤ 3 levels for clarity).
2. **Plan the radial layout**:
   - Place the central concept at the diagram center.
   - Level-1 nodes radiate outward from center, equally distributed in angle (360° / count). Radius from center = 120–150px.
   - Level-2 nodes radiate from their parent Level-1 node. Radius from parent = 100–120px. Distribute in a ±30° arc from the parent's direction.
   - Node size: central = 80×80px (or circle r=40), Level-1 = 120×50px, Level-2 = 100×40px.
   - Overlap check: after placing all nodes, verify no bounding boxes overlap. If overlap detected, increase radius or adjust angles by ±10°.
3. **Draw curved connections**:
   - Use cubic bezier curves (`C` command) from parent edge to child edge.
   - Central → Level-1: direct bezier with control points at mid-distance.
   - Level-1 → Level-2: bezier starting from the parent's outward-facing edge.
   - Attach arrowheads where direction matters.
   - Apply `<connection-routing>` from SKILL.md for natural-looking curves.
4. **Add labels**:
   - Central concept: larger font (18px, bold). Level-1: 14px, bold. Level-2: 12px, regular.
   - For connection labels (relationships), place at the parametric midpoint of the curve (the longest and only segment) with a white background rect.
5. **Apply color coding**: Use `<color-palettes>` from SKILL.md for concept diagrams. Color intensity can decrease radially (central: most saturated, outer: lighter).
6. **Set viewBox** and output raw SVG.
