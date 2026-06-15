# Create Flowchart — Detailed Steps

Applies **create-flowchart** in the svg-editor skill.

Before starting, load the following from SKILL.md:
- `<computation-scripts>` — **MANDATORY**: script usage and JSON format
- `<ppt-design-requirements>` — PPT-quality standards

**Steps**:

1. **Analyze the process**: Identify start/end nodes, process steps, decisions, and branching paths from the user's description. Determine flow direction (default: top-to-bottom). Extract a diagram title.

2. **Build the JSON description**: Construct JSON matching the `<computation-scripts>` input format:
   - `diagram_type`: `"flowchart"`
   - `title`: extracted title
   - `ppt_mode`: `true` (default)
   - `flow_direction`: `"top-to-bottom"` or `"left-to-right"`
   - `nodes[]`: each with `id`, `type` (`start`/`end`/`process`/`decision`/`subprocess`/`document`/`data`/`connector`/`fork`), `text`, `row`, `col`. Omit `width`/`height` — scripts auto-compute.
   - `edges[]`: each with `id`, `from`, `to`, optional `label` and `branch` (`"yes"`/`"no"` for decision branches)

3. **Run compute_all.py**: Execute `python3 scripts/compute_all.py '<json>'`. The script outputs SVG fragments (see `<computation-scripts>` output fields).

4. **Review validation**: Check `validation.all_clear`. If `false`:
   - `node_overlaps`: adjust row/col spacing and re-run
   - `connection_issues`: adjust node positions and re-run
   - `color_issues`: the script flags contrast problems — fix colors and re-run

5. **Assemble SVG output**: The script's output includes ready-to-use SVG fragments:
   - `svg_title_bar` — full title bar SVG
   - `svg_markers` — arrow marker definitions
   - `edges[].svg_line` — complete `<path>` elements with markers and styling
   - `nodes[].svg_shape` — complete shape elements (rects, polygons, text) with computed colors, gradients, shadows
   - `labels[].svg_label` — label background rects and text
   - Wrap everything in `<svg viewBox="..."><defs>...</defs>...</svg>` using `output.viewbox` and `output.defs`.

6. **Final output**: Return raw, valid SVG code with no surrounding explanation.
