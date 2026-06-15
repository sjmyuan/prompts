# Create Flowchart — Detailed Steps

Applies **create-flowchart** in the svg-editor skill.

Before starting, load the following from SKILL.md:
- `<computation-snippets>` — **MANDATORY**: snippet patterns and SVG assembly
- `<ppt-design-requirements>` — PPT-quality standards

**Steps**:

1. **Analyze the process**: Identify start/end nodes, process steps, decisions, and branching paths from the user's description. Determine flow direction (default: top-to-bottom). Extract a diagram title.

2. **Build node/edge data**: Construct lists of nodes and edges:
   - `nodes[]`: each with `id`, `type` (`start`/`end`/`process`/`decision`/`subprocess`/`document`/`data`/`connector`/`fork`), `text`, `row`, `col`.
   - `edges[]`: each with `id`, `from`, `to`, optional `label` and `branch` (`"yes"`/`"no"` for decision branches)

3. **Compute node positions**: Run the **Compute node positions (flowchart grid)** snippet from `<computation-snippets>` with your node list to get `x`, `y`, `width`, `height`, `bbox` for each node.

4. **Route connections**: For each edge, run the **Route a connection** snippet using source/destination node bounding boxes. Capture the SVG path string.

5. **Generate SVG elements**: Run the **Generate SVG for a shape** snippet for each node and edge to get their SVG element strings.

6. **Generate defs and decorations**: Call `colors.get_shadow_filter()` + `colors.get_gradient_defs()` + `svg_shapes.generate_arrow_marker()` for `<defs>`. Call `svg_shapes.generate_title_bar(title, width)` for the title bar.

7. **Validate**: Run the **Check shape overlaps** and **Validate color contrast** snippets. Fix any issues by adjusting row/col and re-running.

8. **Compute viewBox**: Run the **Compute viewBox for SVG** snippet with all element bounding boxes.

9. **Assemble SVG**: Follow the **SVG assembly pattern** in `<computation-snippets>`.

10. **Final output**: Return raw, valid SVG code with no surrounding explanation.
