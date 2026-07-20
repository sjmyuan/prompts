---
name: edit-svg
description: Create SVG diagrams with professional PPT-quality layout, clear connections, and no overlapping elements. Use when creating, editing, modifying, upgrading, or fixing flowcharts, architecture diagrams, comparison diagrams, pyramid diagrams, step-flow diagrams, container diagrams, sequence diagrams, concept diagrams, charts, or donut charts as SVG.
---

<when-to-use-this-skill>
- User wants to create a flowchart, process diagram, or workflow diagram as SVG
- User wants to create an architecture diagram, system design diagram, or component diagram as SVG
- User wants to create a comparison, pyramid, step-flow, container, or donut chart diagram as SVG
- User wants to create a sequence diagram or interaction diagram as SVG
- User wants to create a concept diagram, mind map, or visual explanation as SVG
- User wants to create a bar, line, or pie chart as SVG
- User wants to fix overlapping elements, improve connection clarity, or adjust spacing in an existing SVG
- User wants to edit, modify, or update an existing SVG diagram
- User wants an existing SVG upgraded to PPT-presentation quality
</when-to-use-this-skill>

<knowledge>

**Two SVG authoring approaches**:

| Approach | Used for | Method |
|---|---|---|
| **Script-based** | Flowchart, architecture, sequence, concept, chart | Python scripts compute positions, paths, SVG elements. |
| **Hand-crafted** | Comparison, pyramid, step-flow, container, donut | Write SVG directly following visual patterns. No scripts. |

**Design standards**: 16:9 (960×540) default. Drop shadows, linear gradients, rounded corners (`rx="6"`+). Font stack: `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif` (add `'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei'` for CJK). Title: 16–22px bold, body: 13–15px, annotations: 9–11px. WCAG AA contrast (≥4.5:1). 5–8 main elements per diagram, ≤15 words per shape. See [reference/design-standards.md](reference/design-standards.md).

**SVG assembly pattern**: `<svg viewBox="..." font-family="...">` → `<defs>` (shadow + gradients + arrow markers) → title bar → shapes (backgrounds → panels → connections → node shapes → labels) → `</svg>`.

**Text conventions**: `text-anchor="middle"` + `dominant-baseline="middle"` for single-line centered text. For multi-line CJK in `<tspan>`, use `dy`-based positioning (baseline offset ≈ 0.32×font_size). Color-code semantically: red=problems, green=success, blue=info, orange=warnings.

**Column/Row centering**: Same-column nodes must share the same `center_x = col_left + max_width_in_col / 2`, with each node's `x = center_x - node_width / 2`. Same-row nodes must share the same `center_y`.

**Scripts directory**: `skills/edit-svg/scripts/` — 7 Python modules. Dependencies: `pip install svgwrite networkx matplotlib`. See [reference/computation-snippets.md](reference/computation-snippets.md) for the full API reference.

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Creating any script-based diagram | Script template, calling guide, API signatures | [reference/computation-snippets.md](reference/computation-snippets.md) |
| Creating a flowchart | Node types, dimensions, grid layout, 12-point ports, 16-scenario routing algorithm | [reference/create-flowchart.md](reference/create-flowchart.md) |
| Creating architecture, sequence, concept, or chart diagram | Layout patterns, data structures, dimension guidelines | [reference/scripted-diagram-types.md](reference/scripted-diagram-types.md) |
| Creating a comparison, pyramid, step-flow, container, or donut chart | Visual patterns, dimension tables, SVG element examples | [reference/handcrafted-diagram-types.md](reference/handcrafted-diagram-types.md) |
| Routing scripted connections | Edge routing patterns, validation API, port allocation | [reference/diagram-workflow.md](reference/diagram-workflow.md) |
| Modifying or upgrading an existing SVG | Modification workflow, detection/correction functions, PPT upgrade | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Validating PPT quality | Color semantics, typography, shadow/gradient/marker defs | [reference/design-standards.md](reference/design-standards.md) |
| Viewing visual examples | Output examples per diagram type | [examples/](examples/) |
</context-loading-guide>

</knowledge>

<capabilities>

<create-scripted-diagram>
Generate a PPT-quality diagram for script-based types (flowchart, architecture, sequence, concept, chart) as raw SVG. All positions, paths, and SVG elements MUST be computed via Python scripts.

1. **Identify diagram type and extract content**: Determine type from the user request. Extract nodes, connections, labels, and a title.
2. **Load references**: Load [reference/computation-snippets.md](reference/computation-snippets.md) for the script template, and the type-specific reference from `<context-loading-guide>`.
3. **Create a standalone Python script** (e.g., `generate_diagram.py`) following the template in `computation-snippets.md`: import modules → define data → compute positions → route connections → validate → generate SVG → assemble and save.
4. **Compute positions**: Use `dag_layout()` (pure DAG) or `assign_flow_layout()` (feedback loops marked `_topo_type='feedback'`). For manual layout, set `row`/`col` on nodes and use `flow_layout()` + `center_align_nodes()`. Center all nodes by column (`center_x`) and row (`center_y`).
5. **Route connections**: Use `route_all_edges()` (auto-detects sides, allocates ports). For complex feedback edges, override paths manually via corridor strategy. Validate with `endpoint_valid()` and `detect_intersections()`.
6. **Generate SVG**: Call `generate_node_svg()`, `generate_edge_svg()`, `generate_label_svg()`, `generate_title_bar()`. Assemble via the SVG assembly pattern. For charts, use `chart_builder.render_*_chart()` instead.
7. **Run and validate**: Run `python3 generate_diagram.py`. Open SVG in browser. Check: line-node overlap, parallel line collision, turning point clearance, connection sides, row/column alignment, column gap ≥140px, label overlap, approach segments ≥15px. Fix and re-run until clean.
8. **Compute viewBox**: Use `compute_viewbox()` with `target_aspect=None` for tall diagrams (8+ rows, portrait). Return raw, valid SVG.
</create-scripted-diagram>

<create-handcrafted-diagram>
Generate a PPT-quality diagram for hand-crafted types (comparison, pyramid, step-flow, container, donut) as raw SVG. Write SVG directly — no scripts needed.

1. **Identify diagram type and extract content**: Determine which type. Extract columns, layers, steps, items, segments, and annotations.
2. **Load reference and examples**: Load [reference/handcrafted-diagram-types.md](reference/handcrafted-diagram-types.md) for the visual pattern, dimensions, and SVG elements. Check corresponding example SVGs in `examples/`.
3. **Build the structure**: Create outer containers (panel backgrounds, trapezoids, step boxes, boundary rectangles, or donut rings) per the type's dimension table. Apply gradient fills per the color tables.
4. **Add items and labels**: Place headers, text labels, bullets, and badges. Use `text-anchor="middle"` + `dominant-baseline="middle"`. Align same-row items across columns to identical y-coordinates. For multi-line CJK, use `dy`-based `<tspan>` positioning.
5. **Add connections**: Draw arrows and connecting lines. Distribute connection points evenly along panel edges (left/center/right or top/center/bottom).
6. **Verify**: No overlapping elements, text fits within containers, viewBox adequate. Return raw, valid SVG.
</create-handcrafted-diagram>

<modify-existing-svg>
Modify, fix, or upgrade an existing SVG diagram. All new geometry MUST be computed via a standalone Python script.

1. **Read the SVG and classify change**: Parse the SVG XML. Load [reference/modify-existing-svg.md](reference/modify-existing-svg.md). Classify as: style, content, structural, layout/connection fixes, or PPT upgrade.
2. **Create a standalone fix script**: Create a `.py` file (e.g., `fix_diagram.py`). Import modules from `skills/edit-svg/scripts/`. Load [reference/diagram-workflow.md](reference/diagram-workflow.md) for routing rules.
3. **Apply modifications in the script**:
   - **Layout fixes**: Run `find_overlapping()`, `resolve_overlaps()`, re-route via `route_with_port_allocation()`. Recompute viewBox.
   - **PPT upgrade**: Generate defs (`get_shadow_filter()`, `get_gradient_defs()`), title bar, offset y-coords, switch to 960×540, re-run with `ppt_mode=True`. Use `PPT_PALETTE` consistently.
4. **Write SVG and run**: Save modified SVG. Run `python3 fix_diagram.py`.
5. **Validate**: Open in browser. Check overlaps, connection sides, contrast, viewBox overflow. Fix and re-run. Return complete valid SVG.
</modify-existing-svg>

</capabilities>

<rules>
<rule>When creating script-based types (flowchart, architecture, sequence, concept, chart) → apply **create-scripted-diagram**. Never compute coordinates mentally.</rule>
<rule>When creating hand-crafted types (comparison, pyramid, step-flow, container, donut) → apply **create-handcrafted-diagram**.</rule>
<rule>When fixing, modifying, or upgrading an existing SVG → apply **modify-existing-svg**. All new geometry must use scripts.</rule>
<rule>When the request spans multiple types → apply capabilities sequentially and compose into one SVG.</rule>
<rule>**Turning point clearance**: After routing any edge, verify no turning point (non-endpoint waypoint) shares x with any node's left/right edge or y with any node's top/bottom edge. Use short approach segments (≥15px, validated by `endpoint_valid()`).</rule>
<rule>**Column/row centering**: Always position nodes by `center_x` (per column) and `center_y` (per row), not by top/left edges.</rule>
<rule>**Multi-lane corridors**: Multiple edges traversing the same gap corridor must use distinct x-lanes (≥18px spacing) and staggered horizontal exit y-levels from shared source nodes.</rule>
<rule>**Obstacle-aware edge routing**: Same-column/same-row edges blocked by intermediate nodes → Z-shape (2 turns), NOT L-shape. Diagonal edges → L1→L2→Z escalation.</rule>
<rule>**CJK text in SVG**: For multi-line CJK in `<tspan>`, use `dy`-based positioning with baseline offset ≈ 0.32×font_size. Avoid `dominant-baseline` on `<tspan>`.</rule>
<rule>**Side-entry avoidance**: Avoid entering wide nodes from LEFT/RIGHT (horizontal approach passes through node interior). Route above/below with a ≥15px vertical approach instead.</rule>
<rule>**Column gap enforcement**: After layout, enforce minimum 140–160px inter-column gap for corridor-routed diagrams via `enforce_column_gap()`. Recompute `corridor_x` after shifting.</rule>
<rule>**Manual label placement for complex edges**: For cross-column feedback and backward edges, prefer explicit label position assignment over automatic placement to avoid node overlap.</rule>
<rule>**API return types**: `connection_endpoints()` returns a 4-tuple `(start_pt, end_pt, src_side, dst_side)`, not a dict. `generate_label_svg()` uses `text_color` (not `color`). `generate_edge_svg()` hardcodes `marker-end="url(#arrow)"` — only one marker with `id="arrow"` in `<defs>`.</rule>
</rules>
