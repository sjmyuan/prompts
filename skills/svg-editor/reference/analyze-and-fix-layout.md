# Analyze and Fix Layout — Detailed Steps

Applies **analyze-and-fix-layout** in the svg-editor skill.

**Steps**:
1. **Parse the SVG**: Read the SVG XML and identify all significant elements: `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<path>`, `<text>`, `<line>`. Extract their bounding boxes and connection paths.
2. **Reconstruct node/edge data**: Build node and edge lists from the extracted elements — map SVG shapes to node types, paths to edges.
3. **Detect overlaps via snippet**: Run the **Check shape overlaps** snippet from `<computation-snippets>` with extracted bounding boxes.
4. **Validate connections via snippet**: Run the **Route a connection** snippet with `routing.detect_intersections()` to find line-line and line-shape intersections.
5. **Fix issues**:
   - **Overlaps**: Push elements apart along the axis of overlap. Increase spacing and re-run overlap check.
   - **Line-shape intersections**: Re-route via `routing.orthogonal_path()` with obstacle avoidance.
   - **Endpoint issues**: Use `routing.endpoint_valid()` to check and fix connection endpoints.
   - **ViewBox clipping**: Run the **Compute viewBox** snippet with expanded dimensions.
6. **Regenerate SVG fragments**: Re-run the **Generate SVG for a shape** snippet with corrected positions to regenerate clean SVG elements.
7. **Assemble and output** the corrected SVG following the **SVG assembly pattern** in `<computation-snippets>`.
