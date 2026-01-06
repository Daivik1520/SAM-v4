## Goal
- Remove the prefilled placeholder text in the chat input so it starts empty and stays clean.

## Changes
- In `setup_input_area`:
  - Delete the line that inserts placeholder text into `self.input_entry`.
  - Remove focus-in/out bindings and the immediate call to `show_placeholder()`.
  - Keep the Enter key binding.
  - Set `self.placeholder_text = ""` to disable placeholder logic.
- No other UI elements affected.

## File References
- `SAM.py:2981–2988` — remove insertion and bindings; set placeholder text empty.
- Methods `show_placeholder`/`hide_placeholder` remain but won’t be used.

## Result
- Input field renders empty by default, without any placeholder text or automatic reinsert on focus events.