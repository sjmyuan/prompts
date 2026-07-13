# Flowchart — Visual Pattern & Dimensions

Applies **create-scripted-diagram** in the edit-svg skill.

Load [reference/computation-snippets.md](computation-snippets.md) and [reference/design-standards.md](design-standards.md) for script calls and PPT standards.

## Node Types & Colors

| Type | Shape | Purpose |
|---|---|---|
| `start`/`end` | Rounded rect (`rx=22`) | Entry/exit points |
| `process` | Rect (`rx=6`) | Standard action step |
| `decision` | Diamond (`polygon`) | Yes/no branch |
| `subprocess` | Rect with side lines | Predefined process |
| `data` | Parallelogram | Data input/output |

## Node/Edge Data Structure

- `nodes[]`: each with `id`, `type` (see table above), `text`, `row`, `col`.
- `edges[]`: each with `id`, `from`, `to`, optional `label` and `branch` (`"yes"`/`"no"` for decision branches).

## Flow Direction

Default: top-to-bottom. Use `graph_layout.flow_layout(nodes, 'top-to-bottom')`.
For left-to-right: use `graph_layout.flow_layout(nodes, 'left-to-right')`.

## Dimension Guidelines

| Parameter | Default |
|---|---|
| Node gap (vertical) | 120px |
| Branch gap (horizontal) | 240px (adjust for wide branch nodes) |
| Start offset | (120, 140) |
| Decision node | width = height, computed by `get_shape_dimensions` |
| Minimum node width (short text) | 120px |

## Multi-Column (Branch) Flowcharts

When a flowchart has a main column and a branch/side column, edges between columns require special handling.

### Column Layout
- Normalize node widths within each column so all nodes in the same column share the same width.
- Set `branch_gap` wide enough (≥400px for wide labels) so feedback paths between columns have room for labels.
- Use `start_offset` to leave room for the title bar (y-offset ≥ 140 if title bar is 44px).

### Row Alignment
- All nodes in the same row must share the same y-coordinate for horizontal center alignment.
- After `flow_layout()`, group nodes by row and for each row:
  1. Find the tallest node height in that row.
  2. Vertically center each node: `node['y'] = row_base_y + (max_row_height - node['height']) / 2`
- Example:
  ```python
  rows = {}
  for n in nodes:
      rows.setdefault(n['row'], []).append(n)
  for row_nodes in rows.values():
      max_h = max(n['height'] for n in row_nodes)
      base_y = min(n['y'] for n in row_nodes)
      for n in row_nodes:
          n['y'] = base_y + (max_h - n['height']) / 2
          n['bbox'] = (n['x'], n['y'], n['width'], n['height'])
  ```

### Edge Routing Strategy

| Edge direction | src_side | dst_side | Method | Example |
|---|---|---|---|---|
| Same column, forward (top→bottom) | bottom | top | `connection_endpoints(src, dst, 'top-to-bottom')` | Start → Step1 |
| Same column, forward (left→right) | right | left | `connection_endpoints(src, dst, 'left-to-right')` | Step1 → Step2 |
| Across columns, same row (left→right) | right | left | `orthogonal_path()` with explicit sides | Main → Side |
| Across columns, opposite direction (right→left) | **left** | **right** | `orthogonal_path()` with explicit sides | Side → Main (feedback) |
| Same column, backward (bottom→top) | **top** | **bottom** | `orthogonal_path()` with explicit sides | Bottom → Top |
| Cross-column upward (feedback) | **top-right** | **bottom** | **Corridor strategy** (see below) | Bottom-Right → Top-Left |

> **Critical**: For right→left feedback edges, the source exits from its **left** side and the target enters from its **right** side. This is opposite to what intuition suggests — the left side of the source faces the right side of the target when going backwards across columns. Always verify with `routing.endpoint_valid()` after routing.

### Corridor Strategy for Feedback Edges

For edges that must go from the bottom of a side column back to the top of the main column (or vice versa), a shared **vertical corridor** in the gap between columns produces the cleanest paths.

**Implementation**:
1. Calculate `corridor_x` as the midpoint between the main column's right edge and the branch column's left edge.
2. For each feedback edge, construct a 4-waypoint path manually:
   ```python
   # Exit point on source node
   source_exit = get_corner_or_side_point(src_node, 'top-right')
   
   # Route: source → corridor (horizontal) → target y (vertical) → target
   path = [
       source_exit,
       (corridor_x, source_exit[1]),  # same y to corridor
       (corridor_x, target_entry[1]),  # same x, target y
       target_entry,                   # target bottom-center
   ]
   ```
3. All feedback edges share the same `corridor_x` — this keeps the diagram clean and organized.
4. Place edge labels on the horizontal or vertical corridor segments, using manual offset adjustments (`dx`, `dy`) to avoid overlap with nearby nodes and intersection with other labels.
