## Goal
- Make the chat input extend horizontally across the center panel and look clean and aligned.
- Ensure the chat area occupies the entire green‑marked region; remove quick actions (already removed).

## Changes
- Center Panel Width:
  - Confirm `center_panel` fills available width and the chat container uses full width with minimal side padding.
  - Update chat container pack options to `fill="both"`, `expand=True`, tighter `padx`.
- Chat Input Layout:
  - In `setup_input_area`, set `text_container.pack(fill="x", expand=True)` to allow full width.
  - Set `input_entry.pack(side="left", fill="x", expand=True)` so the textbox stretches to the right.
  - Place control buttons (`Voice`, `Send`, `Stop`) in a right‑aligned frame; reduce button widths to avoid crowding.
  - Increase input corner radius and keep height at `48` for comfortable typing.
- Clean Margins:
  - Reduce bottom and side paddings around input container.
  - Remove the tip line and chips (already removed) so the input sits cleanly at the bottom.
- Scrolling:
  - Keep the visible scrollbar and mouse‑wheel behavior for the chat area.

## File References
- `SAM.py:2680–2760` — chat container and scrollable area; update padding and fill.
- `SAM.py:2766–2950` — input area; set `text_container.pack(fill="x", expand=True)` and `input_entry.pack(side="left", fill="x", expand=True)`; right‑align controls.
- `SAM.py:2873–2891`, `2941–2950` — chips and tip removed (already done).

## Result
- The input box spans horizontally across the center region with clean alignment.
- The chat area fills the green‑marked region; no quick actions interfere.
- UI remains responsive on window resize.