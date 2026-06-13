# Create Flowchart — Detailed Steps

Applies **create-flowchart** in the svg-editor skill.

**Steps**:
1. **Analyze the process**: Identify start nodes, end nodes, process steps, decision points, and branching paths from the user's description. Determine the flow direction (top-to-bottom or left-to-right — default to top-to-bottom).
2. **Plan the layout grid**:
   - Assign each node a row (stage in the process) and column (branch).
   - Use uniform node dimensions: processes = 140×50px, decisions = 80×80px (diamond), start/end = 120×40px (rounded).
   - Row spacing = 100px (center-to-center vertical gap) for process nodes; 120px for rows containing decision diamonds. This ensures ≥50px edge-to-edge gap for connection lines and arrow clearance.
   - Column spacing = 220px (center-to-center horizontal gap) to allow orthogonal routing room between parallel branches.
3. **Position each node**:
   - Calculate absolute (x, y) from grid position. Center the overall diagram in the viewBox.
   - For decision branches, offset child rows to the left/right of the diamond, then converge back at a merge node.
   - Apply `<svg-layout-principles>` from SKILL.md for alignment and spacing checks.
4. **Draw connection paths**:
   - Use orthogonal routing (horizontal and vertical segments only) via `<path>` commands.
   - Attach arrows to the end of each path using `marker-end="url(#arrow)"`.
   - For decision branches, label each branch path with a text label (e.g., "Yes" / "No") placed at the midpoint of the longest straight segment (typically the only segment), on a small white rectangular background.
   - Apply `<connection-routing>` from SKILL.md for proper endpoint attachment.
5. **Render nodes**:
   - Process steps: `<rect rx="6" ry="6">`
   - Start/End: `<rect rx="20" ry="20">`
   - Decisions: `<polygon>` diamond
   - Subprocess/Document: `<rect>` with a folded-corner effect using a small `<path>` overlay
   - Apply `<color-palettes>` from SKILL.md for flowchart fills and strokes.
6. **Add labels**:
   - Center text within each shape using `text-anchor="middle"` and `dominant-baseline="middle"`.
   - Apply `<text-sizing>` from SKILL.md for proper font sizes.
7. **Set viewBox**: Compute the bounding box of all elements, add 40px padding, and set the `viewBox` attribute. Use `<viewbox-strategy>` from SKILL.md for guidance.
8. **Output only SVG**: Return raw, valid SVG code with no surrounding explanation.

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
