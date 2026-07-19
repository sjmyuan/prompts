# Flowchart — Visual Pattern, Dimensions & Routing Algorithm

Applies **create-scripted-diagram** in the edit-svg skill.

Load [reference/computation-snippets.md](reference/computation-snippets.md) and [reference/design-standards.md](design-standards.md) for script calls and PPT standards.

Also load [reference/diagram-workflow.md](reference/diagram-workflow.md) for routing rules, multi-port allocation, and side-entry avoidance.

The full algorithm code is in [scripts/flowchart_routing.py](scripts/flowchart_routing.py) (path selection, obstacle detection, overlap tracking) and [scripts/graph_layout.py](scripts/graph_layout.py) (topological sort, grid layout, column gap). Import functions from these into your standalone scripts.

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

---

## Phase 1: Topological Sort (Auto Row/Col Assignment)

When `row`/`col` values are not provided, use **Kahn's algorithm** to auto-assign rows from the edge dependency graph.

Import and call: `topological_sort(nodes, edges)` from `scripts/graph_layout.py`.

**Returns** nodes with `row` and `col` assigned. Handles cycles, branches, and disconnected subgraphs automatically.

---

## Phase 2: Grid Layout & Centering

Size grid cells by the largest element in each row/column, then center elements within cells.

```python
from graph_layout import compute_grid_cells, position_elements, align_rows

cell_w, cell_h = compute_grid_cells(nodes, padding_x=40, padding_y=60)
nodes = position_elements(nodes, cell_w, cell_h, start_offset=(120, 140))
nodes = align_rows(nodes)  # Same-row nodes share the same y-coordinate
```

---

## Phase 3: 12-Point Connection System

Each element has **12 fixed connection points** — 3 per side:

```
      T-L      T-C      T-R
       ┌─────────────────┐
  L-T  │                 │  R-T
  L-C  │    Element      │  R-C
  L-B  │    Center       │  R-B
       └─────────────────┘
      B-L      B-C      B-R
```

**Geometry**: `stepX = w / 4`, `stepY = h / 4`. Named as `<Side>-<SubPos>` (T/B/L/R + L/C/R/T/C/B).

**Allocation priority**: 1 edge → center; 2 edges → center + left/top; 3 edges → all three. Handled automatically by `allocate_ports_for_edges()` in `geometry.py`.

---

## Phase 4: 8-Scenario Edge Routing

Classify each edge into one of 8 spatial scenarios using `classify_edge(src_node, dst_node)` from `scripts/flowchart_routing.py`.

### Scenario Routing Table

| # | Scenario | Primary src→dst | Turns | Secondary src→dst | Turns |
|---|---|---|---|---|---|
| 1 | SAME_COL_DOWN | B-C → T-C | 0 | — | — |
| 2 | SAME_COL_UP | T-C → B-C | 0 | — | — |
| 3 | SAME_ROW_RIGHT | R-C → L-C | 0 | — | — |
| 4 | SAME_ROW_LEFT | L-C → R-C | 0 | — | — |
| 5 | DIAG_DOWN_RIGHT | R-C → T-C | 1 | B-C → L-C | 1 |
| 6 | DIAG_DOWN_LEFT | L-C → T-C | 1 | B-C → R-C | 1 |
| 7 | DIAG_UP_RIGHT | R-C → B-C | 1 | T-C → L-C | 1 |
| 8 | DIAG_UP_LEFT | L-C → B-C | 1 | T-C → R-C | 1 |

**Sub-point hint**: For diagonals, prefer the sub-point closest to target (e.g., R-B+T-R for DIAG_DOWN_RIGHT).

### Path Pattern Diagrams

```
SAME_COL_DOWN    SAME_ROW_RIGHT    DIAG_DOWN_RIGHT    DIAG_DOWN_LEFT
  ┌───┐           ┌───┐   ┌───┐    ┌───┐              ┌───┐
  │ A │           │ A │──→│ B │    │ A │───┐      ┌───│ A │
  └─┬─┘           └───┘   └───┘    └───┘   │      │   └───┘
    │                                         │      │
  ┌─┴─┐                                     ┌─┴───┐  │  ┌───┐
  │ B │                                     │  B  │  └──│ B │
  └───┘                                     └─────┘     └───┘
```

---

## Phase 5: Obstacle Detection & Path Selection

### Candidate Priority
Use `generate_candidates(scenario, src, dst, all_nodes)` to produce paths in this priority order:

1. **Straight** (0 turns) — only for same-row/same-col scenarios
2. **L1 primary** (1 turn) — primary L-shape for diagonals
3. **L2 alternate** (1 turn) — secondary L-shape for diagonals
4. **Z-shape** (2 turns) — navigates around obstacles via extension
5. **Perimeter** (fallback) — routes around all nodes

### Scoring
Use `select_best_path(candidates, all_nodes, src, dst, placed_edges)`:
- **Element obstacle** → DISQUALIFIED (path passes through any node)
- **Turn count** → `×100` weight (primary sorting axis)
- **Parallel overlaps** → added to score (secondary axis)

### Key Functions

| Function | Purpose |
|---|---|
| `segment_intersects_element(seg_start, seg_end, bbox)` | Check if a path segment crosses any node interior |
| `select_best_path(candidates, all_nodes, src, dst, placed_edges)` | Score and pick the best path |
| `generate_candidates(scenario, src, dst, all_nodes)` | Generate paths in priority order |
| `build_Z_path(src, dst, scenario, all_nodes)` | Z-shaped 2-turn path around obstacles |
| `build_perimeter_path(src, dst, all_nodes)` | Fallback routing around all nodes |

---

## Phase 6: Line Overlap Detection & Resolution

### OccupiedLanes

Track placed edge segments to detect parallel overlaps. Create an `OccupiedLanes` instance, call `.register(edge)` after each edge is placed. Before selecting a path, call `count_parallel_overlaps(path, placed_edges)`.

Overlap types: **parallel** (same y/x with overlapping range → resolve with micro-offset), **vertical cross** (allowed), **tight parallel** (avoid or merge).

```python
from flowchart_routing import OccupiedLanes, compute_segments

lanes = OccupiedLanes()
for edge in routed_edges:
    edge['_segments'] = compute_segments(edge['waypoints'])
    lanes.register(edge)
```

---

## Decision Branch Handling

- **"Yes"** branches → green arrow (`#16A34A`), continues main flow downward/rightward
- **"No"** branches → red arrow (`#DC2626`), routes to side column

Render branch labels as small `rect+text` overlays positioned on the first horizontal segment after the decision diamond, offset above the segment:

```python
# Custom branch label pattern (not in library — implement in your script)
svg_fragments.append(
    f'<g class="branch-label">'
    f'<rect x="{x - lw/2}" y="{y - lh/2}" width="{lw}" height="{lh}" '
    f'rx="3" fill="#FFFFFF" stroke="{color}" stroke-width="1"/>'
    f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" '
    f'font-size="11" fill="{color}" font-family="...">{label}</text>'
    f'</g>'
)

