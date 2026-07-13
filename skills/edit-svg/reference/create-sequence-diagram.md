# Create Sequence Diagram — Detailed Steps

Applies **create-sequence-diagram** in the edit-svg skill.

**🔴 Before starting**: Read the zero-tolerance rule in [reference/computation-snippets.md](computation-snippets.md). No manual coordinate math is permitted.

**Steps**:
0. **No manual coordinate math**. Every participant position, message path, and SVG element MUST come from script execution. Never compute positions, path strings, or alignment offsets manually.
1. **Identify participants and messages**: List all actors/components and the messages exchanged chronologically.
2. **Build node/edge data**: Define participants as `nodes[]` with `type: "process"` and `row: 0`. Define messages as `edges[]` with optional `style: "dashed"` for return messages.
3. **Compute participant positions via script**: Run the **Compute node positions** snippet from [reference/computation-snippets.md](computation-snippets.md). Adjust `branch_gap` (recommend: 180–220). **Do NOT compute positions manually.**
4. **Compute message paths via script**: For each edge, run the **Route connection** snippet. **Do NOT construct path strings manually.**
5. **Generate SVG elements via script**: Run the **Generate SVG elements** snippet for participants and edges. **Do NOT write participant/edge SVG manually.** Additionally:
   - Draw dashed vertical lifelines using participant center-x from script output.
   - Draw activation bars: thin `<rect>` on lifelines using `PPT_PALETTE["blue_fill_end"]`.
   - For self-messages, construct a loop path manually.
   - Use `svg_builder.generate_section_panel()` for alt/opt/loop frames.
6. **Validate via script**: Run overlap check and viewBox snippets.
7. **Assemble SVG**: Follow the **SVG assembly pattern** in [reference/computation-snippets.md](computation-snippets.md).
8. **Output**: Return raw, valid SVG code.
