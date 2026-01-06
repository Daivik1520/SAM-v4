## Goals
- Enable the assistant to open any file like a human: search, locate visually, click, and launch.
- Keep it modular: strategies (Spotlight, Finder UI, CV) are pluggable and replaceable.
- Integrate with voice/UI, use event bus for progress, and preserve security controls.

## User Experience
- Voice: “Open file report.pdf” → assistant searches, reveals, and opens the best match; asks if multiple.
- UI: “Find & Open” input with filters (type, folder, recency), progress, and selectable matches.
- Feedback: step-by-step status (searching → revealing → opening), with error recovery.

## Capabilities
- Search strategies: Spotlight index (`mdfind`), Finder UI search, recent files heuristics.
- Disambiguation: top N results returned; user picks by voice or UI.
- Open behavior: reveal in Finder, select, and open (default or specified app).
- Fallbacks: CV-assisted click when AppleScript selection/open fails.

## Strategies & Flow
1) Spotlight (preferred):
   - `mdfind` fuzzy search by name/content; optional filters (`kMDItemContentType`, folders).
   - If single good match → reveal and open; else present choices.
2) Finder UI search (human-like):
   - Activate Finder → `Cmd+F` → type query → navigate results → double-click.
3) CV assist:
   - Detect file row/icon; click coordinates; confirm opening.

## Architecture
- Tool abstraction: `SystemNavigationTool` with subtools `spotlight`, `finder_actions`, `ui_search`, `cv_click`.
- Event-driven: emit progress via `core/base_assistant.py:174-181`; logging via `core/base_assistant.py:153-167`.
- Configurable: feature flags and strategy order in `config/settings.py:112-124`.

## APIs
- `open_file(request)` → `Result`:
  - `request.query` (string), `open_with` (optional app), `strategy_order` (list), `scope` (folders), `filters` (type, ext, recency), `max_results`.
- `search_files(query, scope, filters, strategy)` → `[Match]` with `path`, `score`, `source`.
- `reveal_in_finder(path)` → `bool`.
- `open_path(path, app=None)` → `bool`.
- `ui_find_and_open(query)` → `bool`.
- `cv_click(target_hint)` → `bool`.

## Files to Add/Edit (minimal, modular)
- Add `core/navigation/spotlight_search.py`: wrapper around `mdfind` producing ranked matches.
- Add `core/navigation/finder_actions.py`: AppleScript helpers to reveal/activate/open selection.
- Add `core/navigation/ui_search.py`: Finder UI search (Cmd+F + typed query + navigate + open) using `pyautogui`.
- Add `core/navigation/system_navigation.py`: orchestrates strategies; exposes `open_file`.
- Edit `SAM_Enhanced.py`:
  - Initialize navigation tool in feature startup (`SAM_Enhanced.py:123-151`).
  - Wire LLM intents (optional) via provider (`SAM_Enhanced.py:84-96`).
- Edit `features/voice_control.py`:
  - Register intents: “open file …”, “find … and open” (`features/voice_control.py:96-140`).
- Edit `ui/main_window.py`:
  - Add “Find & Open” panel/button and results list (`ui/main_window.py:27-35`).
- Edit `config/settings.py`:
  - Feature flags: `SYSTEM_NAVIGATION` (enable/disable strategies), allowlists.

## Integration Points (existing code)
- Event bus registration/emission: `core/base_assistant.py:168-181`.
- Logging setup: `core/base_assistant.py:153-167`.
- Feature startup orchestration: `SAM_Enhanced.py:123-151`.
- LLM provider wiring: `SAM_Enhanced.py:84-96`, `core/llm/gemini_provider.py:46-55`.
- Voice command registration: `features/voice_control.py:96-140`.
- CV detection callbacks: `features/computer_vision.py:477-482`.

## Safety & Permissions
- Accessibility check for UI scripting and `pyautogui`.
- Path allowlist (e.g., `~/Documents`, `~/Downloads`), configurable in `SYSTEM_CONFIG`.
- Command whitelist for AppleScript; prevent shell injection; audit all tool calls.

## Validation Plan
- Scenarios:
  - Open “report” (multiple matches → choose → open).
  - Open latest “invoice.pdf” in Downloads.
  - Open “logo.png” with Preview.
- Verify: events emitted, logs written, voice/UI flows work; CV fallback clicks when AppleScript fails.

## Phased Execution
- Phase 1: Implement Spotlight search + Finder reveal/open, voice/UI hooks, logging, flags.
- Phase 2: Implement Finder UI search (Cmd+F typing), robust result navigation; open-with.
- Phase 3: CV templates/coordinates, multi-monitor handling; refine disambiguation UX.

## Next Step
- On approval, implement Phase 1 with new navigation modules and integrate with voice/UI while keeping everything feature-gated and replaceable.