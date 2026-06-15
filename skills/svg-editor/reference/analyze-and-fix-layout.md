# Analyze and Fix Layout — Detailed Steps

Applies **analyze-and-fix-layout** in the svg-editor skill.

**Steps**:
1. **Parse the SVG**: Read the SVG XML and identify all significant elements: `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<path>`, `<text>`, `<line>`.
2. **Reconstruct node/edge data**: Build a JSON description that matches `compute_all.py` input format — extract node types, text, positions, and connection paths from the SVG.
3. **Detect overlaps via script**: Run:
   ```bash
   python3 -c "
   from scripts.geometry import overlap, find_overlapping
   bboxes = [(x, y, w, h), ...]  # extracted from SVG
   issues = find_overlapping(bboxes, margin=10)
   print(issues)
   "
   ```
4. **Run compute_all.py** with reconstructed JSON: This validates connections (intersections, endpoint validity) alongside overlap detection.
5. **Fix issues**:
   - **Overlaps**: Push elements apart along the axis of overlap. Increase spacing and re-run the script.
   - **Line-shape intersections**: Re-route via `routing.orthogonal_path()` with obstacle avoidance.
   - **Endpoint issues**: The script's `endpoint_valid()` function flags these — adjust positions.
   - **ViewBox clipping**: Expand viewBox via `layout.compute_viewbox()`.
6. **Re-run compute_all.py** with corrected positions to regenerate clean SVG fragments (`svg_shape`, `svg_line`, etc.).
7. **Assemble and output** the corrected SVG using the script's SVG fragments.
