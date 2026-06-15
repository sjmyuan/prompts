# Create Architecture Diagram — Detailed Steps

Applies **create-architecture-diagram** in the svg-editor skill.

**Steps**:
1. **Identify tiers and components**: Group components into horizontal tiers/layers (e.g., Client → API → Service → Database → External). Identify communication direction.
2. **Build node/edge data**: Assign `row` for each layer (0=top, 1, 2...) and `col` for components within a layer. Use `type: "process"` for standard service boxes, `type: "data"` for databases. Define edges for communication paths.
3. **Compute positions**: Run the **Compute node positions** snippet (adjust `start_offset` and gaps for wide tiers). Apply `layout.flow_layout()` with larger `branch_gap` for tier separation.
4. **Route connections**: Run the **Route a connection** snippet for each edge between tiers.
5. **Generate SVG elements**: Run the **Generate SVG for a shape** snippet for nodes and edges. Additionally:
   - Draw subtle background `<rect>` for each layer band using `PPT_PALETTE["bg_panel"]`. Add layer header labels.
   - Use `svg_shapes.generate_section_panel()` for layer backgrounds.
   - Optionally add cloud shapes, database cylinders, or container bounding boxes as decorative elements.
6. **Validate and compute viewBox**: Run overlap check and viewBox snippets.
7. **Assemble SVG**: Follow the **SVG assembly pattern** in `<computation-snippets>`.
8. **Output**: Return raw, valid SVG code.
