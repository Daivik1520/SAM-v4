"""
SAM AI - Wake Word Detection Module
Uses Picovoice Porcupine for efficient, low-CPU wake word detection.
"""
import threading
import time
import logging
from typing import Callable, Optional, List
import struct

logger = logging.getLogger(__name__)

# Check for pvporcupine availability
try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False
    logger.warning("pvporcupine not installed. Wake word detection unavailable. Install with: pip install pvporcupine")

# Check for pyaudio availability
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    logger.warning("PyAudio not installed. Install with: pip install pyaudio")


class WakeWordDetector:
    """
    Efficient wake word detection using Picovoice Porcupine.
    
    The free tier supports these built-in keywords:
    - "alexa", "americano", "blueberry", "bumblebee", "computer", "grapefruit",
      "grasshopper", "hey google", "hey siri", "jarvis", "ok google", "picovoice",
      "porcupine", "terminator"
    
    For custom wake words like "hey sam", a Picovoice access key with custom
    keywords is required (paid).
    """
    
    # Free built-in keywords available
    BUILT_IN_KEYWORDS = [
        "alexa", "americano", "blueberry", "bumblebee", "computer", "grapefruit",
        "grasshopper", "hey google", "hey siri", "jarvis", "ok google", "picovoice",
        "porcupine", "terminator"
    ]
    
    def __init__(
        self, 
        access_key: str = "",
        keywords: List[str] = None,
        sensitivities: List[float] = None,
        on_wake_word: Callable[[str], None] = None
    ):
        """
        Initialize wake word detector.
        
        Args:
            access_key: Picovoice access key (get free at https://console.picovoice.ai/)
            keywords: List of wake words to detect (must be built-in or custom paths)
            sensitivities: Detection sensitivity per keyword (0.0-1.0)
            on_wake_word: Callback when wake word detected, receives keyword string
        """
        self.access_key = access_key
        self.keywords = keywords or ["jarvis"]  # Default to 'jarvis'
        self.sensitivities = sensitivities or [0.5] * len(self.keywords)
        self.on_wake_word = on_wake_word
        
        self.porcupine = None
        self.audio_stream = None
        self.pa = None
        self.is_listening = False
        self._listen_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
    def _validate_keywords(self) -> List[str]:
        """Validate and filter keywords to only include available ones."""
        valid_keywords = []
        for kw in self.keywords:
            kw_lower = kw.lower().replace(" ", "_").replace("-", "_")
            # Check if it's a built-in keyword
            if kw_lower in [k.replace(" ", "_") for k in self.BUILT_IN_KEYWORDS]:
                valid_keywords.append(kw_lower)
            else:
                logger.warning(f"Keyword '{kw}' not available in free tier. Skipping.")
        
        if not valid_keywords:
            logger.warning("No valid keywords. Defaulting to 'jarvis'")
            valid_keywords = ["jarvis"]
        
        return valid_keywords
    
    def start(self) -> bool:
        """
        Start wake word detection in background thread.
        Returns True if started successfully.
        """
        if not PORCUPINE_AVAILABLE:
            logger.error("pvporcupine not available. Cannot start wake word detection.")
            return False
        
        if not PYAUDIO_AVAILABLE:
            logger.error("PyAudio not available. Cannot start wake word detection.")
            return False
        
        if self.is_listening:
            logger.warning("Wake word detection already running.")
            return True
        
        if not self.access_key:
            logger.error("Picovoice access key required. Get free key at https://console.picovoice.ai/")
            return False
        
        try:
            # Validate and get keywords
            valid_keywords = self._validate_keywords()
            
            # Initialize Porcupine
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keywords=valid_keywords,
                sensitivities=self.sensitivities[:len(valid_keywords)]
            )
            
            # Initialize PyAudio
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            # Start listening thread
            self._stop_event.clear()
            self.is_listening = True
            self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self._listen_thread.start()
            
            logger.info(f"Wake word detection started. Listening for: {valid_keywords}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start wake word detection: {e}")
            self._cleanup()
            return False
    
    def stop(self):
        """Stop wake word detection."""
        self._stop_event.set()
        self.is_listening = False
        
        if self._listen_thread:
            self._listen_thread.join(timeout=2.0)
            self._listen_thread = None
        
        self._cleanup()
        logger.info("Wake word detection stopped.")
    
    def _cleanup(self):
        """Clean up audio resources."""
        if self.audio_stream:
            try:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            except Exception:
                pass
            self.audio_stream = None
        
        if self.pa:
            try:
                self.pa.terminate()
            except Exception:
                pass
            self.pa = None
        
        if self.porcupine:
            try:
                self.porcupine.delete()
            except Exception:
                pass
            self.porcupine = None
    
    def _listen_loop(self):
        """Main listening loop running in background thread."""
        logger.info("Wake word listening loop started.")
        
        while not self._stop_event.is_set():
            try:
                # Read audio frame
                pcm = self.audio_stream.read(
                    self.porcupine.frame_length,
                    exception_on_overflow=False
                )
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                # Process with Porcupine
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    valid_keywords = self._validate_keywords()
                    detected_keyword = valid_keywords[keyword_index]
                    logger.info(f"Wake word detected: {detected_keyword}")
                    
                    if self.on_wake_word:
                        try:
                            self.on_wake_word(detected_keyword)
                        except Exception as e:
                            logger.error(f"Error in wake word callback: {e}")
                            
            except Exception as e:
                if not self._stop_event.is_set():
                    logger.error(f"Error in wake word detection loop: {e}")
                    time.sleep(0.1)
        
        logger.info("Wake word listening loop ended.")
    
    def is_running(self) -> bool:
        """Check if wake word detection is currently running."""
        return self.is_listening and self._listen_thread is not None and self._listen_thread.is_alive()


# Convenience function for simple usage
def create_wake_word_detector(
    access_key: str,
    keywords: List[str] = None,
    on_detection: Callable[[str], None] = None
) -> Optional[WakeWordDetector]:
    """
    Create and return a wake word detector instance.
    
    Args:
        access_key: Picovoice access key
        keywords: List of wake words (default: ["jarvis"])
        on_detection: Callback when wake word is detected
        
    Returns:
        WakeWordDetector instance or None if dependencies unavailable
    """
    if not PORCUPINE_AVAILABLE or not PYAUDIO_AVAILABLE:
        return None
    
    return WakeWordDetector(
        access_key=access_key,
        keywords=keywords or ["jarvis"],
        on_wake_word=on_detection
    )
