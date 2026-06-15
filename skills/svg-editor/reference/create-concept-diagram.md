# Create Concept Diagram — Detailed Steps

Applies **create-concept-diagram** in the svg-editor skill.

**Steps**:
1. **Identify the central concept and branches**: Determine the core topic (center) and related sub-concepts. Organize into ≤3 hierarchical levels.
2. **Build node data**: Define nodes with `id`, `type`, `text`. Mark the central node. Determine branch nodes.
3. **Compute radial positions**:
   ```bash
   python3 -c "
   import sys; sys.path.insert(0, 'scripts')
   from layout import distribute_along_circle
   from svg_shapes import get_shape_dimensions
   center = (480, 270)
   radius = 180
   branch_count = 5
   positions = distribute_along_circle(center, radius, branch_count)
   for i, (px, py) in enumerate(positions):
       dims = get_shape_dimensions(f'Node {i+1}', 'process', ppt_mode=True)
       print(f'x={px - dims["width"]/2:.0f} y={py - dims["height"]/2:.0f} w={dims["width"]:.0f} h={dims["height"]:.0f}')
   "
   ```
4. **Route connections**: For each edge from central to branch node, run the **Route a connection** snippet with bezier path (use `routing.bezier_path()` instead of `orthogonal_path()` for curved lines).
5. **Generate SVG elements**: Run the **Generate SVG for a shape** snippet for nodes and edges. For concept diagrams, use bezier curves for connections.
6. **Validate and compute viewBox**: Run overlap check and viewBox snippets.
7. **Assemble SVG**: Follow the **SVG assembly pattern** in `<computation-snippets>`.
8. **Output**: Return raw, valid SVG code with no surrounding explanation.
