# Analyze and Fix Layout — Detailed Steps

Applies **analyze-and-fix-layout** in the svg-editor skill.

**Steps**:
1. **Parse the SVG**: Read the SVG XML and identify all significant elements: `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<path>`, `<text>`, `<line>`.
2. **Compute bounding boxes**: For each shape element, compute its bounding box (x, y, width, height). For `<text>` elements, estimate width ≈ characters × 9px, height ≈ 20px.
3. **Detect overlaps**:
   - Compare every pair of bounding boxes. If two boxes intersect with overlap area > 10% of either box's area, flag as overlap.
   - Check for text that extends beyond its parent shape's bounds.
   - Check for connection lines that pass through shapes (line-bounding-box intersection).
4. **For each overlap, apply a fix strategy**:
   - **Increase spacing**: Push overlapping elements apart along the axis of overlap by the overlap distance + 10px buffer.
   - **Reposition connection endpoints**: Move arrow endpoints to the nearest edge of the target shape, not center-to-center.
   - **Rebalance layout**: If multiple elements are clustered, redistribute them evenly in available space.
   - **Adjust viewBox**: If elements are clipped or too cramped, expand the viewBox.
5. **Re-route connections**:
   - For any connection path crossing through a non-target shape, insert intermediate waypoints to route around the obstacle.
   - Use orthogonal detours for orthogonal paths: insert an offset segment (L) in the axis perpendicular to the original direction.
   - For curved paths, adjust control points to steer the curve away from obstacles.
   - Apply `<connection-routing>` from SKILL.md for turn clearance and multi-line separation rules.
6. **Output the fixed SVG**: Produce the complete corrected SVG with all fixes applied. Ensure all `<defs>`, `<marker>`, and filter definitions are preserved.
