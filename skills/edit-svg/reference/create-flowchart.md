# Flowchart — Visual Pattern, Dimensions & Routing Algorithm

Applies **create-scripted-diagram** in the edit-svg skill.

Load [reference/computation-snippets.md](reference/computation-snippets.md) and [reference/design-standards.md](design-standards.md) for script calls and PPT standards.

Also load [reference/diagram-workflow.md](reference/diagram-workflow.md) for routing rules, multi-port allocation, and side-entry avoidance.

The full algorithm code is in [scripts/routing.py](scripts/routing.py) (scenario classification, path selection, obstacle detection, overlap tracking) and [scripts/graph_layout.py](scripts/graph_layout.py) (topological sort, grid layout, column gap). Import functions from these into your standalone scripts.

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

## Phase 4: 16-Scenario Edge Routing (8 Base + 8 Obstacle Variants)

Classify each edge into one of 8 spatial scenarios using `classify_edge(src_node, dst_node)` from `scripts/routing.py`. The obstacle-aware path selection in `generate_candidates()` then detects intermediate nodes and upgrades the path if needed — producing 8 additional obstacle variants automatically.

### Base Scenario Routing Table (No Obstacles)

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

### Obstacle Variant Routing (Intermediate Nodes Detected)

When intermediate nodes (elements strictly between src and dst in the grid) block the base path, the path is upgraded automatically by `generate_candidates()`:

| Base # | Original Path | Obstacle Behavior | Upgraded To | Turns |
|--------|-------------|-------------------|-------------|-------|
| 1, 2 | Straight (0 turns) | Intermediate node blocks direct vertical line | Z-shape via RIGHT or LEFT bypass | 2 |
| 3, 4 | Straight (0 turns) | Intermediate node blocks direct horizontal line | Z-shape via BOTTOM or TOP bypass | 2 |
| 5–8 | L1/L2 (1 turn) | L1 blocked by node at (src.row, dst.col) or (dst.row, src.col) | Try L2; if both blocked → Z-shape | 1→2 |
| 5–8 | Both L1+L2 blocked | Obstacles in both intermediate grid cells | Z-shape extending past obstacles | 2 |

**Key principle for straight-line scenarios**: When a same-column/same-row edge is blocked by an intermediate node, the path **skips L-shape** and goes directly to Z-shape (2 turns). A 1-turn L-shape cannot resolve collinear blocking because both the exit and entry sides are on the same axis — there is no orthogonal axis to route through in a single turn without passing through the blocker.

**Key principle for diagonal scenarios**: Follow L1→L2→Z→perimeter escalation. `generate_candidates()` automatically includes all options; `select_best_path()` disqualifies blocked ones.

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

### Obstacle Detection (Pixel-Based)

`_detect_intermediate_nodes()` now uses **pixel bounding-box overlap** (not grid row/col) to find nodes between src and dst. This aligns with `segment_intersects_element()` and eliminates grid/pixel inconsistency. A 2px `MARGIN` prevents edge-contact false positives.

`segment_intersects_element()` uses a 1px `_SEG_EPSILON` tolerance on element boundaries, so connection points on element edges are not falsely flagged as intersecting adjacent elements.

### Candidate Priority

Use `generate_candidates(scenario, src, dst, all_nodes)` to produce paths in this priority order:

1. **Straight** (0 turns) — only for same-row/same-col scenarios; detected as blocked → skip to Z-shape
2. **L1 primary** (1 turn) — primary L-shape for diagonals
3. **L2 alternate** (1 turn) — secondary L-shape for diagonals
4. **Z-shape** (2 turns) — generates BOTH Z1+Z2 bypasses, filters by element obstacle, selects shortest valid path
5. **Perimeter** (fallback) — routes around all nodes

### Z-Path Self-Validation

`build_Z_path()` and `build_Z_path_for_straight()` now:
1. Generate all candidate Z-paths (Z1 + Z2)
2. Filter each through `_filter_valid_candidates()` against ALL elements (not just original obstacles)
3. Return the shortest valid path via `_select_shortest_path()`

### Scoring

Use `select_best_path(candidates, all_nodes, src, dst, placed_edges)`:
- **Element obstacle** → DISQUALIFIED (path passes through any node)
- **Turn count** → `×100` weight (primary sorting axis)
- **Parallel overlaps** → added to score (secondary axis)
- **Sub-point switching** → if best path has overlaps, `_try_switch_sub_points()` tries different sub-points on the same sides to avoid overlaps without adding turns

### Key Functions

| Function | Purpose |
|---|---|
| `segment_intersects_element(seg_start, seg_end, bbox)` | Check if a path segment crosses any node interior (with EPSILON tolerance) |
| `_detect_intermediate_nodes(src_node, dst_node, all_nodes)` | Pixel-based detection of nodes between src and dst |
| `select_best_path(candidates, all_nodes, src, dst, placed_edges)` | Score, pick best path, attempt sub-point switching |
| `generate_candidates(scenario, src, dst, all_nodes)` | Generate paths in priority order (obstacle-aware) |
| `build_Z_path(src, dst, scenario, all_nodes)` | Z-shaped 2-turn path around diagonal obstacles (self-validating) |
| `build_Z_path_for_straight(src, dst, scenario, all_nodes)` | Z-shaped 2-turn path for straight-line obstacles (self-validating) |
| `build_perimeter_path(src, dst, all_nodes)` | Fallback routing around all nodes |
| `_filter_valid_candidates(candidates, all_nodes, src, dst)` | Filter Z-paths that pass through any element |
| `_select_shortest_path(candidates)` | Select the candidate with shortest total path length |
| `_try_switch_sub_points(path, placed_edges, src, dst, src_side, dst_side, scenario)` | Try different sub-points to avoid overlap without adding turns |

---

## Phase 6: Line Overlap Detection & Resolution

### OccupiedLanes

Track placed edge segments to detect parallel overlaps. Create an `OccupiedLanes` instance, call `.register(edge)` after each edge is placed. Before selecting a path, call `_count_parallel_overlaps(path, placed_edges)`.

Overlap types: **parallel** (same y/x with overlapping range → resolve with sub-point switch or micro-offset), **vertical cross** (allowed), **tight parallel** (avoid or merge).

**Tolerance**: Uses 5px `_LANE_TOLERANCE` for near-miss lane detection — segments within 5px of an existing lane are counted as overlaps, encouraging clearly separated lanes.

### Overlap Resolution Priority

1. **Sub-point switching** (`_try_switch_sub_points`) — tries different sub-points on the same exit/entry sides (e.g., R-C→R-T). Keeps path shape unchanged (0 extra turns). This is the preferred approach from flowchart.md §5.7.4.

2. **Accept as-is** — if no sub-point combination avoids overlap, the best path is used directly. Micro-offset (adding turns) is reserved as a last resort.

### Global Refinement (Phase 7)

After all edges are routed, call `global_refine_pass(placed_edges, all_nodes, node_map)` to iteratively re-route edges. Each edge is temporarily removed and re-routed with updated lane occupancy. If the new route has fewer turns (or same turns but fewer overlaps), it replaces the old route. Runs up to 3 iterations or until convergence.

```python
from routing import OccupiedLanes, compute_segments, global_refine_pass

lanes = OccupiedLanes()
for edge in routed_edges:
    edge['_segments'] = compute_segments(edge['waypoints'])
    lanes.register(edge)

# After all edges are placed, run global optimization
routed_edges = global_refine_pass(routed_edges, nodes, node_map)
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

