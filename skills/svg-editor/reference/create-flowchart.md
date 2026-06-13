# Create Flowchart — Detailed Steps

Applies **create-flowchart** in the svg-editor skill.

Before starting, load the following knowledge sections from SKILL.md for reference:
- `<flowchart-components>` — component shapes, dimensions, and connection points
- `<connection-validation>` — line intersection, label position, endpoint, arrow style, and turn routing rules
- `<svg-layout-principles>` — canvas, spacing, alignment, and overlap avoidance
- `<connection-routing>` — orthogonal routing, arrow markers, multi-line separation
- `<color-palettes>` — flowchart color scheme
- `<text-sizing>` — text and shape sizing

**Steps**:

1. **Analyze the process**: Identify start nodes, end nodes, process steps, decision points, and branching paths from the user's description. Determine the flow direction (top-to-bottom or left-to-right — default to top-to-bottom). Consult `<flowchart-components>` for appropriate component types.

2. **Select component types and dimensions**: For each node in the process, choose the matching component from `<flowchart-components>` (Start/End, Process, Decision, Subprocess, Document, Data, Connector, Parallel/Fork). Use the standard dimensions listed there. Adjust width for text content using `<text-sizing>` (width = chars × 9px + 24px padding; minimum 80px).

3. **Plan the layout grid**:
   - Assign each node a row (stage in the process) and column (branch).
   - Use uniform node dimensions from `<flowchart-components>`: Process = 140×50px, Decision = 80×80px, Start/End = 120×40px, etc.
   - Row spacing = 100px (center-to-center vertical gap) for process nodes; 120px for rows containing decision diamonds. This ensures ≥50px edge-to-edge gap for connection lines and arrow clearance.
   - Column spacing = 220px (center-to-center horizontal gap) to allow orthogonal routing room between parallel branches.
   - For parallel/fork bars, allocate 160×8px with 100px vertical spacing from adjacent rows.

4. **Position each node**:
   - Calculate absolute (x, y) from grid position. Center the overall diagram in the viewBox.
   - For decision branches, offset child rows to the left/right of the diamond using `<flowchart-components>` connection point rules (right vertex for Yes branch, left vertex for No branch). Converge back at a merge node below.
   - Apply `<svg-layout-principles>` from SKILL.md for alignment and spacing checks.

5. **Draw connection paths**:
   - Use orthogonal routing (horizontal and vertical segments only) via `<path>` commands.
   - Connect shapes at their **designated connection points** as defined in `<flowchart-components>`:
     - Process/Start/End: top-center (in), bottom-center (out)
     - Decision: bottom vertex (in from above), right vertex (Yes out), left vertex (No out)
     - Parallel bar: left-center (in), right-center (out), top & bottom edges (parallel branches)
   - Apply `<turn-routing-guide>` from `<connection-validation>` for turn decisions:
     - 1-turn (L-shape) for source-to-target on adjacent axes
     - 2-turn (Z-shape) for same-axis offset routing
     - 3-turn (C-shape) for obstacle avoidance
   - Apply `<connection-routing>` from SKILL.md for arrow markers and proper endpoint attachment.
   - After drawing all paths, run `<line-intersection-detection>` to check for unwanted crossings. Fix any detected intersections using the resolution strategies (insert waypoint, re-route, increase spacing, or swap branches).

6. **Add branch labels**:
   - For decision branches, label each branch path with a text label (e.g., "Yes" / "No").
   - Apply `<label-position-validation>` from `<connection-validation>`:
     - Place at midpoint of the **longest straight segment**
     - Wrap in a white `<rect>` background (2–4px padding, `rx="3"`)
     - Check for overlap with other elements; resolve by moving to next-longest segment or offsetting perpendicularly
   - Labels on horizontal segments: centered **above** the line (y offset -14px)
   - Labels on vertical segments: centered **to the right** of the line (x offset +14px)

7. **Render nodes**:
   - Use the SVG elements from `<flowchart-components>`:
     - Process: `<rect rx="4" ry="4">`
     - Start/End: `<rect rx="20" ry="20">`
     - Decision: `<polygon>` diamond with 4 vertices
     - Subprocess: `<rect>` + 2 vertical side bars
     - Document: `<rect>` + wave `<path>`
     - Data/Database: `<ellipse>` + `<rect>` + `<ellipse>`
     - Connector: `<circle>` or pentagon `<polygon>`
     - Parallel/Fork: `<rect>` horizontal bar (160×8px)
   - Apply `<color-palettes>` from SKILL.md for flowchart fills and strokes.
   - Apply `<arrow-style-guide>` from `<connection-validation>` for arrow marker definitions: use standard solid arrow for main flow, dashed for alternative/async paths.

8. **Validate connections**: After rendering all nodes and connections, run these validation checks from `<connection-validation>`:
   - `<connection-endpoint-validation>`: Verify every line endpoint lies exactly on the target shape edge (±2px), the entry segment is ≥15px, no gap/overlap at endpoints, and no orphaned connections.
   - `<line-intersection-detection>`: Confirm no unwanted line-line or line-shape intersections remain.
   - `<label-position-validation>`: Confirm all labels have background rects and do not overlap any elements.

9. **Set viewBox**: Compute the bounding box of all elements, add 40px padding, and set the `viewBox` attribute. Use `<viewbox-strategy>` from SKILL.md for guidance.

10. **Final output**: Return raw, valid SVG code with no surrounding explanation. Verify the SVG is well-formed XML with all `<defs>`, `<marker>`, and element definitions properly closed.

```svg
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#546E7A"/>
    </marker>
  </defs>
  <!-- Nodes and connections rendered here -->
</svg>
```
