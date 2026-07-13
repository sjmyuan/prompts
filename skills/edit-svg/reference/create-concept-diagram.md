# Create Concept Diagram — Detailed Steps

Applies **create-concept-diagram** in the edit-svg skill.

**🔴 Before starting**: Read the zero-tolerance rule in [reference/computation-snippets.md](computation-snippets.md). No manual coordinate math is permitted.

**Steps**:
0. **No manual coordinate math**. Every position, path, and SVG element MUST come from script execution. Never compute positions, bezier control points, or offset values manually.
1. **Identify the central concept and branches**: Determine the core topic (center) and related sub-concepts (≤3 levels).
2. **Build node data**: Define nodes with `id`, `type`, `text`. Mark the central node.
3. **Compute radial positions via script**:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, 'scripts')
   from graph_layout import distribute_along_circle
   from svg_builder import get_shape_dimensions
   center = (480, 270)
   radius = 180
   branch_count = 5
   positions = distribute_along_circle(center, radius, branch_count)
   for i, (px, py) in enumerate(positions):
       dims = get_shape_dimensions(f'Node {i+1}', 'process', ppt_mode=True)
       print(f'x={px - dims[\"width\"]/2:.0f} y={py - dims[\"height\"]/2:.0f} w={dims[\"width\"]:.0f} h={dims[\"height\"]:.0f}')
   "
   ```
   **Do NOT compute radial positions, angles, or offsets manually.**
4. **Route connections via script**: Use `routing.bezier_path()` for curved lines. **Do NOT construct bezier control points or path strings manually.**
5. **Generate SVG elements via script**: Run the **Generate SVG elements** snippet for nodes and edges. **Do NOT write node/edge SVG manually.**
6. **Validate via script**: Run overlap check and viewBox snippets.
7. **Assemble SVG**: Follow the **SVG assembly pattern** in [reference/computation-snippets.md](computation-snippets.md).
8. **Output**: Return raw, valid SVG code.
