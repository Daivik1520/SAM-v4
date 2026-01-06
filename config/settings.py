"""
Enhanced SAM AI Assistant - Configuration Settings
"""
import os
from pathlib import Path

# Base Configuration
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
MODELS_DIR = BASE_DIR / "models"
CACHE_DIR = BASE_DIR / "cache"

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, MODELS_DIR, CACHE_DIR]:
    directory.mkdir(exist_ok=True)

# UI Configuration
UI_CONFIG = {
    "theme": "dark",
    "appearance_mode": "dark",
    "color_theme": "blue",
    "window_size": (1200, 800),
    "min_window_size": (800, 600),
    "transparency": 0.95,
    "animation_speed": 0.3,
    "font_family": "Segoe UI",
    "font_size": 12
}

# Voice Configuration
VOICE_CONFIG = {
    "recognition_timeout": 5,
    "phrase_timeout": 1,
    "energy_threshold": 4000,
    "dynamic_energy_threshold": True,
    "tts_rate": 200,
    "tts_volume": 0.8,
    "wake_word": "sam",
    "language": "en-US",
    "voice_id": 0
}

# Wake Word Detection Configuration (Picovoice Porcupine)
# Get free access key at: https://console.picovoice.ai/
WAKE_WORD_CONFIG = {
    "enabled": True,
    # Built-in keywords (free): alexa, americano, blueberry, bumblebee, computer,
    # grapefruit, grasshopper, hey google, hey siri, jarvis, ok google, picovoice,
    # porcupine, terminator
    "keywords": ["jarvis"],  # Using 'jarvis' - sounds like an AI assistant
    "sensitivity": 0.5,  # 0.0-1.0, higher = more sensitive but more false positives
    "access_key": "",  # Your Picovoice access key (get free at https://console.picovoice.ai/)
}

# System Tray Configuration
TRAY_CONFIG = {
    "enabled": True,  # Enable system tray icon
    "minimize_to_tray": True,  # Minimize to tray instead of taskbar
    "start_minimized": False,  # Start app minimized to tray
    "hotkey": "ctrl+shift+s",  # Global hotkey to show/hide SAM (Cmd+Shift+S on macOS)
    "show_notifications": True,  # Show notifications from tray
    "mini_mode_width": 400,  # Width of mini floating window
    "mini_mode_height": 80,  # Height of mini floating window
}


# AI Configuration
AI_CONFIG = {
    # Provider can be: "gemini" (Google), "openai", etc.
    "provider": "gemini",
    "model_name": "gemini-1.5-flash",
    "max_tokens": 2000,
    "temperature": 0.8,  # Slightly higher for more personality
    "context_window": 10,
    "enable_rag": True,
    "enable_memory": True,
    # JARVIS-inspired personality - witty, intelligent, efficient
    "personality": """You are SAM, an AI assistant inspired by JARVIS from Iron Man. Your characteristics:
- Speak with subtle wit and dry humor, but never be sarcastic to the point of rudeness
- Be concise and efficient - give direct answers, don't ramble
- Show intelligence and competence in every response
- Address the user respectfully, occasionally with light formality ("Sir", "Indeed", "Right away")
- Be proactive - anticipate needs and offer relevant suggestions
- Keep responses SHORT and punchy like a real assistant would speak
- Use occasional British-isms but stay natural
- Never break character or mention being an AI unless asked directly
- Sound confident and capable, like you've done this a thousand times"""
}

# Computer Vision Configuration
CV_CONFIG = {
    "camera_index": 0,
    "face_detection_model": "haarcascade_frontalface_default.xml",
    "object_detection_confidence": 0.5,
    "gesture_recognition": True,
    "emotion_detection": True,
    "ocr_language": "eng"
}

# System Configuration
SYSTEM_CONFIG = {
    "monitoring_interval": 1,
    "max_cpu_usage": 80,
    "max_memory_usage": 80,
    "auto_cleanup": True,
    "backup_interval": 24,  # hours
    "log_level": "INFO"
}

# Security Configuration
SECURITY_CONFIG = {
    "encryption_key": None,  # Will be generated
    "biometric_auth": False,
    "privacy_mode": False,
    "secure_storage": True,
    "session_timeout": 30  # minutes
}

# API Keys (to be set via environment variables)
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "google_search": os.getenv("GOOGLE_SEARCH_API_KEY"),
    "weather": os.getenv("WEATHER_API_KEY"),
    "news": os.getenv("NEWS_API_KEY"),
    "spotify": os.getenv("SPOTIFY_API_KEY"),
    "calendar": os.getenv("CALENDAR_API_KEY"),
    # Gemini (Google): set GEMINI_API_KEY in your environment
    "gemini": os.getenv("GEMINI_API_KEY"),
}

# Optional: load local overrides without committing secrets
try:
    from config.local_settings import OVERRIDES as LOCAL_OVERRIDES  # type: ignore
    # Allow overriding API keys and AI config locally
    if isinstance(LOCAL_OVERRIDES, dict):
        if "API_KEYS" in LOCAL_OVERRIDES and isinstance(LOCAL_OVERRIDES["API_KEYS"], dict):
            API_KEYS.update(LOCAL_OVERRIDES["API_KEYS"])
        if "AI_CONFIG" in LOCAL_OVERRIDES and isinstance(LOCAL_OVERRIDES["AI_CONFIG"], dict):
            AI_CONFIG.update(LOCAL_OVERRIDES["AI_CONFIG"])
except Exception:
    # No local overrides present; safe to ignore
    pass

# Feature Flags
FEATURES = {
    "voice_control": True,
    "computer_vision": True,
    "smart_home": True,
    "productivity": True,
    "entertainment": True,
    "health_wellness": True,
    "security": True,
    "learning": True,
    "gaming": True,
    "web_integration": True
}