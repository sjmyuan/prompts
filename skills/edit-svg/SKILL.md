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

**Key conventions**: `text-anchor="middle"` + `dominant-baseline="middle"` for centered text. Panel headers: full-width `<rect>` with same `rx` at panel top. Color-code semantically (red=problems, green=success, blue=info, orange=warnings).

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
| Modifying or upgrading an existing SVG | Modification workflow, PPT upgrade steps | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Need design standards or example output | PPT design rules and diagram examples | [reference/design-standards.md](reference/design-standards.md) and [examples/](examples/) |
</context-loading-guide>

</knowledge>

<capabilities>

<create-scripted-diagram>
Generate a PPT-quality diagram for script-based types (flowchart, architecture, sequence, concept, chart) as raw SVG. All positions, paths, and SVG elements MUST be computed via Python scripts — never manually.

1. **Identify diagram type and extract content**: Determine which type (flowchart, architecture, sequence, concept, or chart). Extract nodes, connections, tiers, participants, messages, or data series from the user request. Determine a diagram title.
2. **Load the type-specific reference**: Load the corresponding reference file from `<context-loading-guide>` for the identified type.
3. **Load computation-snippets.md**: Read [reference/computation-snippets.md](reference/computation-snippets.md) for the zero-tolerance rule, calling convention, and snippet patterns.
4. **Build node/edge data**: Construct `nodes[]` (with `id`, `type`, `text`, `row`, `col` for grid types) and `edges[]` (with `from`, `to`, optional `label` and `branch`) as appropriate for the diagram type.
5. **Compute positions via script**: Run the **Compute node positions** snippet from `computation-snippets.md` with your node data. For concept diagrams, use `distribute_along_circle()`. For charts, skip to step 8.
6. **Route connections via script**: For each edge, run the **Route connection** snippet using source/target bounding boxes. For concept diagrams, use `routing.bezier_path()`. Do NOT construct path `d` strings manually.
7. **Generate SVG elements via script**: Run the **Generate SVG elements** snippet for each node and edge. For charts, call `chart_builder.render_bar_chart()`, `render_line_chart()`, or `render_pie_chart()` — these return complete SVG.
8. **Generate defs and decorations via script**: Call `colors.get_shadow_filter()` + `colors.get_gradient_defs()` + `svg_builder.generate_arrow_marker()` for `<defs>`. Call `svg_builder.generate_title_bar()` for the title bar.
9. **Validate via script**: Run overlap detection (`geometry.find_overlapping()`) and contrast checks (`colors.wcag_aa_check()`). Fix issues by adjusting row/col and re-running scripts.
10. **Compute viewBox via script**: Run `graph_layout.compute_viewbox()` with all element bounding boxes.
11. **Assemble and output**: Follow the **SVG assembly pattern**. Return raw, valid SVG code with no surrounding explanation. All SVG fragments must be pre-generated by scripts.
</create-scripted-diagram>

<create-handcrafted-diagram>
Generate a PPT-quality diagram for hand-crafted types (comparison, pyramid, step-flow, container, donut) as raw SVG. Write SVG directly — no scripts needed.

1. **Identify diagram type and extract content**: Determine which type (comparison, pyramid, step-flow, container, or donut). Extract columns, layers, steps, items, segments, and annotations from the user request.
2. **Load the type-specific reference and example**: Load the corresponding reference file and examine the matching example SVG in `examples/` for visual patterns.
3. **Determine viewBox and layout dimensions**: Use the dimension guidelines from the reference file. Follow the visual pattern (panel layout, trapezoid geometry, step spacing, boundary zones, or donut center).
4. **Build panel/layer/step structure**: Create the outer container(s) — panel backgrounds, pyramid trapezoids, step boxes, boundary rectangles, or donut ring. Apply gradient fills per the reference color table.
5. **Add items, labels, and annotations**: Place headers, text labels, bullets, badges, and annotation boxes. Use `text-anchor="middle"` + `dominant-baseline="middle"`. Align same-row items across columns to identical y-coordinates.
6. **Add connections and markers**: Draw arrows, lifelines, dashed boundaries, or connecting lines between elements. Use correct `refX`/`refY` for arrow markers (tip-reference: `refX=arrow_width, refY=half_h`).
7. **Verify and output**: Check that no elements overlap, text fits within containers, and the viewBox is adequate. Return raw, valid SVG code.
</create-handcrafted-diagram>

<modify-existing-svg>
Modify, fix, or upgrade an existing SVG diagram. All new geometry (positions, paths, dimensions) MUST be computed via scripts.

1. **Parse the existing SVG**: Read the SVG XML. Identify `viewBox`, `<defs>`, colors, fonts, element positions, and connection paths. Load [reference/modify-existing-svg.md](reference/modify-existing-svg.md).
2. **Classify the change type**: Determine if the request is one of:
   - **Style changes**: Colors, borders, fonts, gradients
   - **Content changes**: Text labels, titles, annotations
   - **Structural changes**: Add/remove/reorder elements
   - **Layout/connection fixes**: Overlap resolution, path re-routing, viewBox expansion
   - **PPT upgrade**: Shadows, gradients, title bar, 16:9 aspect ratio, PPT typography
3. **Plan modifications** — list each target element with its change. For additions, compute positions via scripts (load `computation-snippets.md` for snippet patterns). For text changes, call `svg_builder.get_shape_dimensions()`.
4. **Apply modifications via scripts**:
   - For layout fixes: Run `geometry.find_overlapping()` to detect overlaps, `graph_layout.resolve_overlaps()` to fix, `routing.orthogonal_path()` to re-route connections, `graph_layout.compute_viewbox()` to expand viewBox.
   - For PPT upgrade: Generate defs via `colors.get_shadow_filter()` + `colors.get_gradient_defs()`, title bar via `svg_builder.generate_title_bar()`, offset y-coordinates, switch to 960×540 viewBox, re-run **Generate SVG elements** with `ppt_mode=True`.
   - For modifications: Preserve existing `<defs>` and `<g>` groupings. Use `colors.PPT_PALETTE` consistently. Remove orphaned connections when deleting elements.
5. **Verify via scripts**: Run `geometry.overlap()` to check for new overlaps, `routing.endpoint_valid()` for connections, `colors.wcag_aa_check()` for contrast, `graph_layout.compute_viewbox()` for overflow. Return the complete, valid SVG.
</modify-existing-svg>

</capabilities>

<rules>
<rule>When creating script-based types (flowchart, architecture, sequence, concept, chart) → apply **create-scripted-diagram**. Never compute coordinates mentally.</rule>
<rule>When creating hand-crafted types (comparison, pyramid, step-flow, container, donut) → apply **create-handcrafted-diagram**.</rule>
<rule>When fixing, modifying, or upgrading an existing SVG → apply **modify-existing-svg**. All new geometry must use scripts.</rule>
<rule>When the request spans multiple types → apply capabilities sequentially and compose into one SVG.</rule>
</rules>
