# Create Architecture Diagram — Detailed Steps

Applies **create-architecture-diagram** in the svg-editor skill.

**🔴 Before starting**: Read the zero-tolerance rule in [reference/computation-snippets.md](computation-snippets.md). No manual coordinate math is permitted.

**Steps**:
0. **No manual coordinate math**. Every position, dimension, path string, and node/edge SVG element MUST come from script execution. Never compute offsets, verify alignment, or construct paths manually.
1. **Identify tiers and components**: Group components into horizontal tiers/layers. Identify communication direction.
2. **Build node/edge data**: Assign `row` for each layer and `col` for components within a layer. Use `type: "process"` for service boxes, `type: "data"` for databases.
3. **Compute positions via script**: Run the **Compute node positions** snippet from [reference/computation-snippets.md](computation-snippets.md). Apply `graph_layout.flow_layout()` with larger `branch_gap` for tier separation. **Do NOT compute any positions manually.**
4. **Route connections via script**: Run the **Route connection** snippet for each edge between tiers. **Do NOT construct path strings manually.**
5. **Generate SVG elements via script**: Run the **Generate SVG elements** snippet for nodes and edges. **Do NOT write node/edge SVG manually.** Additionally:
   - Draw subtle background `<rect>` for each layer band using `PPT_PALETTE["bg_panel"]`.
   - Use `svg_builder.generate_section_panel()` for layer backgrounds.
6. **Validate via script**: Run overlap check and viewBox snippets.
7. **Assemble SVG**: Follow the **SVG assembly pattern** in [reference/computation-snippets.md](computation-snippets.md).
8. **Output**: Return raw, valid SVG code.
