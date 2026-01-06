## Goals
- SAM remembers the user (name, preferences, favorites) and uses them to personalize responses and behavior.
- Memory persists locally (profile JSON) and is easy to view/edit.
- Modular design so we can extend memory types later (facts, routines, recent items).

## Memory Design
- Storage: add a `memory` section inside the existing profile JSON (e.g., `profile_Developer.json`).
- Schema (initial):
  - `identity`: `{ name, timezone, locale }`
  - `preferences`: `{ theme, language, voice, fast_mode, wakeword }`
  - `favorites`: `{ apps: [], folders: [], websites: [] }`
  - `recents`: `{ commands: [{text, ts}], files: [{path, ts}], apps: [{name, ts}] }`
  - `facts`: array of `{ key, value, tags }` for custom info (e.g., birthday, city)
- API: `MemoryManager` with `load()`, `save()`, `remember(key, value)`, `recall(key)`, `remember_fact(text)`, `get_pref(name)`, `set_pref(name, value)`.

## Implementation (SAM.py)
- Add `MemoryManager` class (in SAM.py) to wrap reading/writing the profile’s `memory` section.
- Instantiate in `EnhancedJarvisGUI.__init__` after profile load.
- Personalization hooks:
  - Startup greeting uses `identity.name`: in `show_main_ui()` personalize message
  - Commands use preferences: language/voice/theme
  - “Open …” commands record to `recents`
  - Voice: use `preferences.voice` if set
- Natural-language “remember”:
  - Parse inputs like “my name is X”, “remember that my favorite browser is Chrome” → write to memory
  - Basic regex extraction first; optional LLM extraction later

## UI
- Control Panel → Memory card:
  - Show identity and preferences; allow edit/save
  - List favorites and recent items (top 5)
  - Buttons: Add favorite app/folder/website, Clear memory, Export

## Integration Points
- Profile load/save: extend existing `load_or_prompt_profile` and `save_profile` flows to include `memory`
- Greeting message: `SAM.py:1645–1649`
- Command processing: `process_command` and `intelligent_open_command` update `recents`
- Voice/TTS: use preference voice/language when present

## Privacy & Security
- Local-only storage; do not send memory to network services unless explicitly allowed
- “Privacy Mode”: disable external ASR and avoid logging sensitive facts
- Clear-all and selective delete options

## Acceptance Tests
- Set name once → SAM greets by name on next run
- Change theme/voice in Memory card → UI/TTS reflect immediately
- “remember that my favorite browser is Chrome” → opening web defaults to Chrome if installed
- Recents update when opening apps/files and appear in Memory card

## Delivery Steps
1) Implement `MemoryManager` and integrate with profile load/save
2) Hook greeting, preferences, and recents
3) Add simple “remember” intent parsing in `process_command`
4) Add Memory card UI to Control Panel (view/edit/export/clear)
5) Verify persistence across sessions and personalization in responses

## Notes
- All code changes stay in `SAM.py` and reuse the existing profile JSON.
- The design is modular so we can add long‑term semantic memory and retrieval later.