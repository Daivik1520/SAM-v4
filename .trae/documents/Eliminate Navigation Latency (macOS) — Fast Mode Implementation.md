## Problem
- Opening System Settings, apps, and folders still feels slow and sometimes shows “searching…” even for direct actions.

## Goals
- Immediate opens (≤300ms UI response) for settings, apps, and folders.
- No simulated delays; always use the fastest OS-native strategy.
- Clean, professional UX with progress only when truly needed.

## Strategy
- Fast Mode: route navigation through direct OS primitives, avoid Spotlight/heuristics for settings/apps.
- Caching: bundle IDs and deep-link URLs cached in memory for instant reuse.
- Async worker: non-blocking execution but no artificial `after(...)` delays.

## Changes (SAM.py)
1) SystemNavigationService (new in SAM.py)
- `open_settings(section)`: deep link first, AppleScript pane fallback, then app-only fallback.
- `open_app(app_name)`: use `open -b <bundle_id>`; bundle ID cache; fallback to `open -a`.
- `open_folder(path_or_name)`: resolve quickly (Downloads/Documents/Desktop) → `open`/`reveal`; skip Spotlight unless the user asked to “find”.
- `focus(app)`: AppleScript `activate` fast foreground.

2) Deep Links & Pane Map
- Map section → URL: display, sound, wifi/network, bluetooth, battery, keyboard, trackpad, mouse, privacy.
- Handle Ventura+ (`System Settings`) and Monterey− (`System Preferences`) with version checks.

3) Fast Path Routing
- In `intelligent_open_command`, remove simulated search delays and route:
  - `settings for <section>` → `SystemNavigationService.open_settings(section)`
  - `open <app>` → `SystemNavigationService.open_app(app)`
  - `open <folder>` → `SystemNavigationService.open_folder(name)`
- Show immediate status: “Opening …” only; omit “Searching …” for direct actions.

4) Performance & Caching
- Bundle ID cache: pre-index common apps (Safari, Chrome, Terminal, Finder, Notes, Settings) and store misses.
- Pane URL cache: precomputed dict; quick version gate.
- Metrics: log duration per action; warn if >1s to help future tuning.

5) UX Updates
- Remove artificial delays and “Please wait” for direct opens.
- Keep chat feedback succinct: “Opening Settings → Wi‑Fi” or “Opening Safari”.

## Verification
- Commands: “open settings for wifi”, “open settings for bluetooth”, “open settings for sound”, “open safari”, “open downloads”.
- Measure timings in logs; confirm foreground focus.

## Rollout Steps
1) Add SystemNavigationService with fast open methods
2) Replace existing settings/app routing in `intelligent_open_command`
3) Add cache structures and logging
4) Test on macOS; adjust pane map if an OS version differs

## Notes
- All work stays inside `SAM.py` as requested.
- Uses safe system calls: `open`, `osascript`; no Spotlight for direct actions.
- Keeps design modular to swap strategies later (e.g., LaunchServices API via pyobjc if desired).