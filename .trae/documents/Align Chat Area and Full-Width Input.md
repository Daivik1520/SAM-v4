## Goal
- Make the chat area fill the entire center region and the input stretch cleanly across the bottom.
- Fix alignment with a reliable grid layout and consistent paddings.

## Changes
- Center panel grid:
  - In `setup_center_panel`, configure a 3‑row grid: header (row 0, fixed), chat container (row 1, expandable), input container (row 2, fixed).
  - Set `rowconfigure(1, weight=1)` and `columnconfigure(0, weight=1)` so the chat container grows.
- Chat area:
  - In `setup_chat_area`, place `chat_header` at `row=0` and `chat_container` at `row=1` with `sticky="nsew"`.
  - Reduce side padding and ensure the scroll frame fills.
- Input area:
  - In `setup_input_area`, attach the input container to `self.center_panel` instead of `self.main_frame`.
  - Place at `row=2`, `sticky="ew"`, with `text_container.pack(fill="x", expand=True)` and `input_entry.pack(fill="x", expand=True)`.
  - Keep compact right button group; icon widths already reduced.

## File References
- `SAM.py:2060–2106` — `setup_main_content` (no structural change needed other than center/right split kept)
- `SAM.py:2680–2760` — `setup_chat_area` to use grid on `self.center_panel` and `chat_container` sticky expand
- `SAM.py:2766–2950` — `setup_input_area` parent = `self.center_panel`, grid row 2, full‑width stretch

## Result
- Chat area fills the center panel with clean vertical expansion.
- The input spans horizontally and aligns perfectly with the chat content.
- No leftover quick actions or tips cluttering the bottom area.