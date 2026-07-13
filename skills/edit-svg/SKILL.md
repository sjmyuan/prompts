---
name: edit-svg
description: Create SVG diagrams with professional PPT-quality layout, clear connections, and no overlapping elements. Use when creating, editing, modifying, upgrading, or fixing flowcharts, architecture diagrams, comparison diagrams, pyramid diagrams, step-flow diagrams, container diagrams, sequence diagrams, concept diagrams, charts, or donut charts as SVG.
---

<when-to-use-this-skill>
- User wants to create a flowchart, process diagram, or workflow diagram as SVG
- User wants to create an architecture diagram, system design diagram, or component diagram as SVG
- User wants to create a comparison diagram, side-by-side layout, or panel comparison as SVG
- User wants to create a pyramid diagram, layered structure, or hierarchical stack as SVG
- User wants to create a step-flow diagram, numbered step sequence, or horizontal process flow as SVG
- User wants to create a container diagram, boundary diagram, or zone-based layout as SVG
- User wants to create a sequence diagram or interaction diagram as SVG
- User wants to create a concept diagram, mind map, or visual explanation as SVG
- User wants to create a chart, graph, data visualization, or donut chart as SVG
- User wants to fix overlapping elements, improve connection clarity, or adjust spacing in an existing SVG
- User wants to edit, modify, or update an existing SVG diagram
- User wants an existing SVG upgraded to PPT-presentation quality

<knowledge>

**Two SVG authoring approaches**:

| Approach | Used for | Method |
|---|---|---|
| **Script-based** | Flowcharts, architecture, sequence, concept, bar/line/pie charts | Python scripts compute positions, paths, SVG elements. Load [reference/computation-snippets.md](reference/computation-snippets.md). |
| **Hand-crafted** | Comparison, pyramid, step-flow, container, donut charts | Write SVG directly following visual patterns in `examples/`. No scripts. |

**Design standards**: 16:9 (960×540) default. Drop shadows, linear gradients, rounded corners (`rx="6"`+). Font stack: `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif` (add `'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei'` for Chinese). Title: 16–22px bold, body: 13–15px, annotations: 9–11px. WCAG AA contrast (≥4.5:1). 5–8 main elements per diagram, ≤15 words per shape. See [reference/design-standards.md](reference/design-standards.md).

**SVG assembly pattern**: `<svg viewBox="..." font-family="...">` → `<defs>` (shadow + gradients + arrow markers) → background → title → layers → connections → shapes → labels → `</svg>`.

**Key conventions**: `text-anchor="middle"` + `alignment-baseline="middle"` for centered text in single-line nodes. For multi-line CJK text with `<tspan>`, use `dy`-based positioning instead of `dominant-baseline` (which has inconsistent browser support on `<tspan>`). Baseline offset ≈ 0.32×font_size for visual centering. Panel headers: full-width `<rect>` with same `rx` at panel top. Color-code semantically (red=problems, green=success, blue=info, orange=warnings).

**Column/Row centering**: All nodes in the same column must share the same `center_x` (not just the same left edge). Compute `col_center_x = col_left + max_width_in_col / 2`, then set each node's `x = col_center_x - node_width / 2`. All nodes in the same row must share the same `center_y`. Compute `center_y = start_y + row * node_gap`, then set `y = center_y - height / 2`. This gives both perfect horizontal and vertical alignment.

**Edge routing by skip detection**: When routing same-column forward edges, detect whether intermediate nodes exist between source and destination:
  - **No intermediate** + same center_x → straight line (0 turns)
  - **No intermediate** + different center_x → L-shape (1 turn, horizontal-first)
  - **Has intermediate** → Z-shape (2+ turns) with clearance from intermediate nodes
  Compute `skip_count = number of nodes in same column with row between src and dst`.

**Multi-lane corridor strategy**: When multiple feedback edges share the same gap corridor between columns, assign each edge its own x-lane in the corridor (e.g., `lane_c`, `lane_r`, `lane_l`, `lane_rr` with 18px spacing). Also stagger the y-levels of horizontal segments exiting from shared source nodes (e.g., use `0.5×height` and `0.85×height` for different edges from the same node side).

**Turning point clearance**: Turning points (waypoints that are not connection endpoints) must NOT share x with any node's left/right edge nor y with any node's top/bottom edge. Otherwise the line visually overlaps the element border. After routing use _short approach segments_ (6-10px) to enter/exit node edges: route the final horizontal segment at `edge_y - 8`, then drop vertically into the edge. Validate with:
  ```
  for each turning point (tx, ty), for each node (nx, ny, nw, nh):
    assert not (abs(tx-(nx))<2 or abs(tx-(nx+nw))<2 or abs(ty-ny)<2 or abs(ty-(ny+nh))<2)
  ```

**Label placement**: For complex diagrams with long CJK labels, prefer explicit position assignment after analyzing the diagram layout. Place labels on horizontal segments when possible (natural left-to-right reading). On vertical segments, offset right. Ensure minimum 8px clearance from all node edges. When automated placement is needed, try all segments and pick the one where push-down displacement is smallest.

**ViewBox**: For tall diagrams (portrait orientation with 8+ rows), do NOT enforce 16:9 aspect ratio. Pass `target_aspect=None` to `compute_viewbox()` so the viewBox matches content proportions.

**Diagram workflow reference**: See [reference/diagram-workflow.md](reference/diagram-workflow.md) for edge routing patterns, corridor strategy, standalone script file approach, iterative validation loop, row alignment rules, and connection side specification rules.

**Multi-port connection system**: Each edge of a node has multiple fixed connection ports (default 3 per side: left, center, right for top/bottom; top, center, bottom for left/right). When allocating edges to ports, each port can be used by at most one line per node per side. Lines pick the closest unused port to minimize turning points. See [reference/diagram-workflow.md](reference/diagram-workflow.md) for detailed port allocation rules and API reference.

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Creating a script-based diagram | Script calling guide, assembly pattern, arrow geometry | [reference/computation-snippets.md](reference/computation-snippets.md) |
| Creating a flowchart | Visual pattern, dimensions, colors, SVG elements | [reference/create-flowchart.md](reference/create-flowchart.md) |
| Creating an architecture diagram | Tier layout, layer bands, SVG elements | [reference/create-architecture-diagram.md](reference/create-architecture-diagram.md) |
| Creating a sequence diagram | Participant layout, lifelines, activation bars, SVG elements | [reference/create-sequence-diagram.md](reference/create-sequence-diagram.md) |
| Creating a concept diagram | Radial layout, branch routing, SVG elements | [reference/create-concept-diagram.md](reference/create-concept-diagram.md) |
| Creating a bar/line/pie chart | Chart builder API calls | [reference/create-chart.md](reference/create-chart.md) |
| Creating a comparison diagram | Panel layout, dimension table, SVG elements | [reference/create-comparison-diagram.md](reference/create-comparison-diagram.md) |
| Creating a pyramid diagram | Trapezoid geometry, layer table, SVG elements | [reference/create-pyramid-diagram.md](reference/create-pyramid-diagram.md) |
| Creating a step-flow diagram | Step box layout, color progression, SVG elements | [reference/create-step-flow-diagram.md](reference/create-step-flow-diagram.md) |
| Creating a container diagram | Boundary layout, badge style, SVG elements | [reference/create-container-diagram.md](reference/create-container-diagram.md) |
| Creating a donut chart | Arc geometry, annotation layout, SVG elements | [reference/create-donut-chart.md](reference/create-donut-chart.md) |
| Creating or modifying a scripted diagram | Edge routing, corridor strategy, standalone scripts, validation, row alignment, side specs | [reference/diagram-workflow.md](reference/diagram-workflow.md) |
| Modifying or upgrading an existing SVG | Modification workflow, PPT upgrade steps | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Need design standards or example output | PPT design rules and diagram examples | [reference/design-standards.md](reference/design-standards.md) and [examples/](examples/) |
</context-loading-guide>

</knowledge>

<capabilities>

<create-scripted-diagram>
Generate a PPT-quality diagram for script-based types (flowchart, architecture, sequence, concept, chart) as raw SVG. All positions, paths, and SVG elements MUST be computed via Python scripts — never manually.

1. **Identify diagram type and extract content**: Determine type and extract nodes, connections, etc. Determine a diagram title.
2. **Load the type-specific reference**: Load the corresponding file from `<context-loading-guide>`.
3. **Create standalone script file**: Generate a `.py` file (e.g., `generate_diagram.py`). Read [reference/computation-snippets.md](reference/computation-snippets.md) for script patterns. See [reference/diagram-workflow.md](reference/diagram-workflow.md) for the standalone script approach.
4. **Build node/edge data**: Construct `nodes[]` and `edges[]` in the script.
5. **Compute positions**: Compute node dimensions first (handle multi-line text by measuring the longest line). Position all nodes by **center_x per column** and **center_y per row**:
   - For each column, find `max_width`. Compute `col_center_x = col_left + max_width / 2`. Set each node's `x = col_center_x - node_width / 2`.
   - For each row, compute `center_y = start_y + row * node_gap`. Set each node's `y = center_y - node_height / 2`.
   - This ensures both horizontal (within column) and vertical (within row) center alignment.
6. **Route connections**: Classify each edge by spatial relationship.
   - **Same column, forward**: Detect intermediate nodes with `skip_count`. Use straight line (no intermediates, same center_x), L-shape (1 turn, no intermediates, different center_x), or Z-shape (2+ turns, has intermediates).
   - **Cross-column feedback**: Use **multi-lane corridor strategy** — assign each edge its own x-lane in the gap corridor (18px spacing between lanes) and stagger y-levels when multiple edges exit from the same node side.
   - After routing, verify **turning point clearance**: no turning point should share x with any node's left/right edge nor y with any node's top/bottom edge. Add short approach segments (6-10px) to disconnect horizontal segments from element edges.
   - Verify with `endpoint_valid()` on every edge. Run `detect_intersections()`. See [reference/diagram-workflow.md](reference/diagram-workflow.md) for side specification rules.
7. **Generate SVG elements**: Call `generate_node_svg()` for each node (or custom multi-line node SVG with `dy`-based `<tspan>` positioning). Call `generate_edge_svg()` for each edge. For charts, use `chart_builder.render_*_chart()`.
8. **Generate defs and decorations**: Call `get_shadow_filter()`, `get_gradient_defs()`, `generate_arrow_marker()`, `generate_title_bar()`.
9. **Write SVG and run**: Assemble fragments following the **SVG assembly pattern**. Save to `.svg` file. Run `python3 generate_diagram.py`.
10. **Visually validate and iterate**: Open in browser. Check:
    - **Line overlap**: No two lines share the same corridor x-position. Parallel edges must be staggered.
    - **Turning point clearance**: No turning point aligns with any node's edge.
    - **Connection sides**: Edges enter/exit from correct sides of nodes.
    - **Row alignment**: All same-row nodes have identical center_y; all same-column nodes have identical center_x.
    - **Label overlap**: Labels do not overlap with nodes or each other.
    - **Port allocation**: No two lines converge at the same spot on a node edge; parallel edges spread apart.
    Fix issues in script and re-run until all criteria are met.
11. **Compute viewBox**: Call `compute_viewbox()` with all bounding boxes. For tall diagrams (8+ rows, portrait orientation), pass `target_aspect=None` to let the viewBox match content proportions rather than enforcing 16:9.
12. **Assemble and output**: Follow the **SVG assembly pattern**. Return raw, valid SVG code.
</create-scripted-diagram>

<create-handcrafted-diagram>
Generate a PPT-quality diagram for hand-crafted types (comparison, pyramid, step-flow, container, donut) as raw SVG. Write SVG directly — no scripts needed.

1. **Identify diagram type and extract content**: Determine which type (comparison, pyramid, step-flow, container, or donut). Extract columns, layers, steps, items, segments, and annotations from the user request.
2. **Load the type-specific reference and example**: Load the corresponding reference file and examine the matching example SVG in `examples/` for visual patterns.
3. **Determine viewBox and layout dimensions**: Use the dimension guidelines from the reference file. Follow the visual pattern (panel layout, trapezoid geometry, step spacing, boundary zones, or donut center).
4. **Build panel/layer/step structure**: Create the outer container(s) — panel backgrounds, pyramid trapezoids, step boxes, boundary rectangles, or donut ring. Apply gradient fills per the reference color table.
5. **Add items, labels, and annotations**: Place headers, text labels, bullets, badges, and annotation boxes. Use `text-anchor="middle"` + `dominant-baseline="middle"`. Align same-row items across columns to identical y-coordinates.
6. **Add connections and markers**: Draw arrows, lifelines, dashed boundaries, or connecting lines between elements. Use correct `refX`/`refY` for arrow markers (tip-reference: `refX=arrow_width, refY=half_h`). When multiple lines connect to the same edge of a panel or container, distribute the connection points evenly along that edge (left/center/right or top/center/bottom) to avoid overlap.
7. **Verify and output**: Check that no elements overlap, text fits within containers, and the viewBox is adequate. Return raw, valid SVG code.
</create-handcrafted-diagram>

<modify-existing-svg>
Modify, fix, or upgrade an existing SVG diagram. All new geometry MUST be computed via a standalone Python script.

1. **Parse the existing SVG**: Read the SVG XML. Load [reference/modify-existing-svg.md](reference/modify-existing-svg.md).
2. **Classify the change type**: Style, content, structural, layout/connection fixes, or PPT upgrade.
3. **Create standalone script**: Create a `.py` file (e.g., `fix_diagram.py`). Plan modifications. Load [reference/diagram-workflow.md](reference/diagram-workflow.md) for routing rules.
4. **Apply modifications via the script**:
   - For layout fixes: Run `find_overlapping()`, `resolve_overlaps()`, `route_with_port_allocation()`, `compute_viewbox()`. Use strict side specification rules from [reference/diagram-workflow.md](reference/diagram-workflow.md). When fixing connection overlap, re-allocate ports via `allocate_ports_for_edges()`.
   - For PPT upgrade: Generate defs, title bar, offset y-coords, switch to 960×540, re-run with `ppt_mode=True`.
   - Preserve existing `<defs>` and `<g>` groupings. Use `PPT_PALETTE` consistently. Remove orphaned connections.
5. **Write SVG and run**: Save modified SVG to file. Run `python3 fix_diagram.py`.
6. **Visually validate and iterate**: Open in browser. Check overlaps, connection sides, contrast, viewBox overflow. Fix and re-run until quality is met. Return complete, valid SVG.
</modify-existing-svg>

</capabilities>

<rules>
<rule>When creating script-based types (flowchart, architecture, sequence, concept, chart) → apply **create-scripted-diagram**. Never compute coordinates mentally.</rule>
<rule>When creating hand-crafted types (comparison, pyramid, step-flow, container, donut) → apply **create-handcrafted-diagram**.</rule>
<rule>When fixing, modifying, or upgrading an existing SVG → apply **modify-existing-svg**. All new geometry must use scripts.</rule>
<rule>When the request spans multiple types → apply capabilities sequentially and compose into one SVG.</rule>
<rule>**Turning point clearance**: After routing any edge, verify that no turning point (non-endpoint waypoint) shares an x-coordinate with any node's left/right edge or a y-coordinate with any node's top/bottom edge. Use short approach segments (6-10px) if needed.</rule>
<rule>**Column/row centering**: Always position nodes by center_x (within column) and center_y (within row), not by top/left edges. Same-column nodes must share center_x; same-row nodes must share center_y.</rule>
<rule>**Multi-lane corridors**: When multiple edges traverse a gap corridor between columns, assign each edge a distinct x-lane (≥18px spacing) and stagger horizontal exit y-levels from shared source nodes.</rule>
<rule>**Skip-based edge routing**: For same-column forward edges, detect intermediate nodes. No intermediate + same center_x → straight line. No intermediate + different center_x → L-shape (1 turn). Has intermediate → Z-shape (2+ turns).</rule>
<rule>**CJK text in SVG**: For multi-line CJK text in `<tspan>` elements, use `dy`-based positioning with baseline offset ≈ 0.32×font_size. Avoid `dominant-baseline` on `<tspan>` due to inconsistent browser support.</rule>
</rules>
