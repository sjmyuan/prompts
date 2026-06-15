# Create Flowchart — Detailed Steps

Applies **create-flowchart** in the svg-editor skill.

Before starting, load the following knowledge sections from SKILL.md for reference:
- `<computation-scripts>` — **MANDATORY**: all geometric calculations via `python3 scripts/compute_all.py`
- `<ppt-design-requirements>` — PPT-quality standards: slide dimensions, visual effects, typography, contrast, and simplicity rules
- `<flowchart-components>` — component shapes, dimensions, and connection points
- `<color-palettes>` — PPT Professional palette (default) and Basic palette (minimal)
- `<text-sizing>` — text and shape sizing with PPT typography defaults
- `<svg-element-reference>` — PPT-quality SVG patterns with drop shadows and gradients

**Steps**:

1. **Analyze the process**: Identify start nodes, end nodes, process steps, decision points, and branching paths from the user's description. Determine the flow direction (top-to-bottom or left-to-right — default to top-to-bottom). Extract a title for the diagram. Consult `<flowchart-components>` for appropriate component types.

2. **Build the JSON description**: Construct a JSON object matching the `<computation-scripts>` input format:
   - `diagram_type`: `"flowchart"`
   - `title`: extracted title string
   - `ppt_mode`: `true` (default) or `false` if user wants minimal style
   - `nodes[]`: each with `id`, `type` (start/end/process/decision/subprocess/document/data/connector/fork), `text`, `width`, `height`, `row`, `col`
   - `edges[]`: each with `id`, `from`, `to`, optional `label` and `branch` (`"yes"`/`"no"` for decision branches)

3. **Run compute_all.py**: Execute `python3 scripts/compute_all.py '<json>'` (use `<computation-scripts>` for exact JSON format). The script outputs a JSON result with:
   - `nodes[]` — each with computed `x`, `y`, `bbox`
   - `edges[]` — each with computed `path_d`, `waypoints[]`
   - `labels[]` — each with `x`, `y`, `bg_rect`, `side`
   - `viewbox` — computed `{x, y, width, height}`
   - `defs` — SVG `<filter>` and `<linearGradient>` strings
   - `validation` — `node_overlaps`, `connection_issues`, `color_issues`, `all_clear`

4. **Review validation results**: Check `validation.all_clear`. If `false`, review the issues:
   - `node_overlaps`: nodes are too close — adjust row/col or increase `node_gap`/`branch_gap` and re-run
   - `connection_issues`: lines intersect or endpoints are invalid — script already used orthogonal routing with obstacle avoidance; if issues persist, adjust node positions and re-run
   - `color_issues`: text/background contrast below 4.5:1 — adjust colors and re-run

5. **Assemble SVG output**: Using the computed JSON:
   - Set `<svg viewBox="...">` from `output.viewbox`
   - Insert `<defs>` from `output.defs.shadow_filter` and `output.defs.gradients`
   - Add `<marker id="arrow">` definition for connection arrows (see `<svg-element-reference>`)
   - Add PPT title bar at top of viewBox (60px height, `#1A73E8`, shadow, white bold title text)
   - For each node in `output.nodes`, render the shape using the `<flowchart-components>` SVG element and the `<svg-element-reference>` PPT-quality patterns (gradient fill, shadow, rounded corners). Use computed `x`, `y`, `width`, `height`.
   - For each edge in `output.edges`, render `<path d="...">` using computed `path_d`. Apply `marker-end="url(#arrow)"`. Use `stroke-dasharray="6,4"` for dashed style.
   - For each label in `output.labels`, render a white `<rect>` background at `bg_rect` and `<text>` at `x`, `y`.

6. **Final output**: Return raw, valid SVG code with no surrounding explanation.
