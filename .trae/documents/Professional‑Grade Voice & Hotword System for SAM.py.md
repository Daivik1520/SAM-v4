## Goals
- Reliable, low‑latency voice input with professional UX
- Robust hotword detection (“SAM”) with user‑configurable custom wake words
- Graceful fallbacks when the mic/PortAudio/PyAudio are missing
- Modular design so you can swap detectors/ASR engines later

## Architecture
- VoiceInputManager (new, in SAM.py): microphone lifecycle, VAD, buffering, state
- HotwordEngine (new): pluggable detectors (OpenWakeWord default, Porcupine optional)
- ASR Pipeline: SpeechRecognition (Google) by default, optional offline Vosk
- Orchestrator: Wake → Listen → Transcribe → Route command → Resume wake

## Implementation Outline
1) Microphone & Dependencies
- Detect PyAudio/PortAudio availability at app start; show actionable UI toast if missing
- Lazily initialize mic to avoid startup crashes; retry on failure with backoff
- Sample rate 16kHz, 16‑bit mono; normalize chunk sizes for consistent detection latency

2) Voice Activity Detection (VAD)
- Integrate WebRTC VAD (webrtcvad) for end‑of‑speech; parameters: aggressiveness 2
- Gate STT only when VAD detects speech; auto‑stop after silence (e.g., 800ms)

3) Hotword Detection
- Use OpenWakeWord (lightweight, pip) as default detector; load models for “sam”
- Support custom hotwords from `hotwords.json` (already in repo): confidence thresholds, enable/disable per entry
- Provide an on‑device fallback energy‑based wake (if OWW not available)
- Debounce: ignore duplicate triggers within 1s; add small “Yes?” audio cue

4) STT (ASR)
- Default: SpeechRecognition with Google recognizer, `language` from settings
- Fallback: optional Vosk (offline) if installed; detect automatically
- Timeouts: max phrase 8–10s, network timeout 5s; show status clearly in UI

5) TTS & Barge‑In
- Pause TTS when wake word detected (“barge‑in”) and resume after STT completes
- Optional confirmation prompt (“Did you mean…?”) for low confidence transcriptions

6) UI/UX Enhancements (SAM.py)
- Voice button reflects states: Idle, Wake listening, Command listening, Error
- Visualizer bars tied to VAD; red when muted/error, green when active
- Status chip near input: “Listening…”, “Transcribing…”, “Wake word armed”
- Control Panel entries:
  - Settings → Voice: toggle wake word, detector (OpenWakeWord/Porcupine/Energy), sensitivity, language, auto‑resume
  - Custom Hotword: add/remove words, set threshold; saves to `hotwords.json`

7) Error Handling & Logging
- Structured logs for microphone errors, detector init, STT failures
- UI toasts for: mic missing, permission denied, network error; non‑blocking

8) Performance & Reliability
- Pre‑warm detector models on app start (async) to reduce first‑use latency
- Keep short audio ring buffer for VAD; reclaim memory after processing
- Thread‑safe queues; ensure clean stop on app exit

9) Security & Privacy
- Respect privacy mode: disable streaming STT, use offline only; never store raw audio
- Clearly indicate when mic is active; easy one‑click mute

## File Changes (Modular)
- SAM.py: add VoiceInputManager, HotwordEngine classes; wire to existing voice button and status
- hotwords.json: use as source of custom wake words (format: [{"word":"sam","threshold":0.5}, …])
- Optional: requirements extras for `webrtcvad`, `openwakeword`, `vosk` (gated; not required to run)

## Validation
- Unit tests for detector triggers & VAD gates
- Manual flows:
  - Wake → “open settings for wifi” → executes fast path
  - No mic: shows toast, does not crash
  - Privacy mode: blocks network STT and shows reason

## Rollout Steps
1) Implement core classes & wire to UI
2) Add OpenWakeWord default; fallback energy detector
3) Integrate VAD; tune thresholds
4) Add settings UI and hotword editor
5) Optional offline ASR (Vosk) integration
6) Test on macOS with and without PyAudio/PortAudio

## Notes
- All changes are scoped to SAM.py and use existing UI components
- Detectors/ASR are pluggable so you can replace them later without touching orchestration