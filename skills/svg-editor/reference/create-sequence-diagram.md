# Create Sequence Diagram — Detailed Steps

Applies **create-sequence-diagram** in the svg-editor skill.

**Steps**:
1. **Identify participants and messages**: List all actors/components (participants) and the messages exchanged between them in chronological order. Note synchronous vs. asynchronous messages and return messages.
2. **Plan participant layout**:
   - Place participants horizontally across the top. Equal spacing between participants. Minimum gap = 120px.
   - Participant box: width = text-width + 24px (minimum 100px), height = 40px.
   - Draw a dashed vertical lifeline from the bottom center of each participant box down to the last message's y + 40px.
3. **Plan message positions**:
   - Each message occupies one row. Row height = 30–40px.
   - Total diagram height = (message count × row height) + header (80px) + footer (40px).
   - For each message, determine source participant column and target participant column.
4. **Draw activation bars**:
   - When a participant sends or receives a message, draw a thin solid `<rect>` (width=12px, fill=`#BBDEFB`) on its lifeline spanning the duration of its activity.
5. **Draw messages**:
   - Synchronous call: solid line with filled arrowhead (`marker-end="url(#arrow)"`).
   - Asynchronous call: solid line with open arrowhead.
   - Return message: dashed line with open arrowhead (`stroke-dasharray="6,4"`).
   - Self-message: loop from lifeline back to same lifeline using a small rectangular path.
   - Apply `<connection-routing>` from SKILL.md for proper line placement.
6. **Add message labels**:
   - Place label text above each message line, centered at the midpoint of the line (single segment), offset 8px upward.
7. **Add frames** (optional): Use `<rect rx="4" ry="4" stroke-dasharray="4,4">` for alt/opt/loop frames. Place frame label in top-left corner with a small filled rectangle and white text.
8. **Set viewBox** and output raw SVG.
