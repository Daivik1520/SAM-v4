## Phase 2 — Wake Word, VAD, Offline ASR, Hotword Editor

### Goals
- Reliable wake word (“sam”) + custom hotwords
- End‑of‑speech detection (VAD) with low latency
- Offline ASR fallback for privacy and robustness
- In‑app hotword editor (add/remove, sensitivity)

### Components
- WakeWord: OpenWakeWord (default) + Porcupine (optional)
- VAD: WebRTC VAD (aggressiveness 2) gating STT
- ASR: SpeechRecognition (Google) primary; Vosk offline fallback (auto‑detect)
- UI: Voice state chip, visualizer bar, Hotword editor in Control Panel

### File Changes (scoped to SAM.py)
- Add `VoiceInputManager` with mic lifecycle, buffering, VAD gating
- Add `HotwordEngine` with pluggable detectors; load from `hotwords.json`
- Wire voice button states: Armed → Listening → Transcribing → Error
- Control Panel: Hotword editor (list, thresholds), detector selection

### Dependencies (optional, gated)
- `webrtcvad`, `openwakeword`, `vosk` (extras install; graceful fallback if missing)

### Acceptance Tests
- Wake word triggers within ≤500ms; VAD ends speech reliably
- “Privacy mode” uses offline Vosk only; no network calls
- Editor persists hotwords to `hotwords.json`; takes effect immediately

## Phase 3 — File Open with “Open With”, Full Window Management

### Goals
- “Open file … with <App>” support
- Deterministic window management across displays

### Components
- File Open: Spotlight/resolve → reveal → open (default or specified app)
- Window Manager: AppleScript + pyobjc fallback (position, size, snap, maximize, minimize, focus)
- UI: Window actions panel (Snap Left/Right, Maximize, Move to Display 2)

### File Changes (SAM.py)
- Extend `open_file_human_like(query, kind, open_with)`
- Add `WindowManager` with actions: `focus(app)`, `move(app, x,y)`, `resize(app, w,h)`, `maximize(app)`, `minimize(app)`, `snap(app, side)`
- Add voice intents: “move window left”, “maximize Safari”, “open file report with Preview”

### Acceptance Tests
- “open file logo.png with Preview” opens correctly
- “move window right” and “maximize window” operate on the active app within ≤300ms

## Phase 4 — Orchestrator, Memory, Plugin Registry

### Goals
- Plan/execute multi‑step tasks reliably with checkpoints
- Persist summaries for recall and learning
- Modular tool plugins with enable/disable/versioning

### Components
- Orchestrator: DAG of Steps (tool calls + LLM reasoning), retries/backoff
- Memory: working context per task + JSON summaries in `config/automation/`
- Plugin Registry: `Tool` interface; dynamic discovery and registration

### File Changes (SAM.py)
- Add `TaskOrchestrator`, `Task`, `Step`, `ToolCall`, `Result` data classes
- Add `PluginRegistry` and `Tool` base (system, web, files, window, media)
- Integrate with chat: progress events, result summaries, error recovery

### Acceptance Tests
- “Open YouTube, play song, then open Notes” executes as 3 steps with logs and retries
- Crash/resume restores last checkpoint; memory summaries available for recall

## Rollout Notes
- All code scoped to `SAM.py` + `hotwords.json` as requested
- Optional deps installed only when user opts in; UI indicates missing capabilities
- Logging and metrics added for latency verification and reliability

## Next Action
- Proceed with Phase 2 implementation; then Phase 3; then Phase 4, delivering each with tests and UI hooks