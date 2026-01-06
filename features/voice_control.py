"""
Enhanced SAM AI Assistant - Voice Control Module
"""
import asyncio
import threading
import queue
import speech_recognition as sr
import pyttsx3
import numpy as np
from typing import Optional, Callable, Dict, List
import logging
import time
import re

from core.base_assistant import BaseAssistant
from config.settings import VOICE_CONFIG
from config.settings import AI_CONFIG

class VoiceController:
    """Advanced voice control with multiple features"""
    
    def __init__(self, assistant: BaseAssistant):
        self.assistant = assistant
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = queue.Queue()
        
        # Text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Voice processing
        self.is_listening = False
        self.wake_word_detected = False
        self.voice_commands: Dict[str, Callable] = {}
        self.conversation_mode = False
        # Event loop reference (set when listening starts)
        self.loop = None
        
        # Multi-language support
        self.supported_languages = {
            "en-US": "English (US)",
            "en-GB": "English (UK)",
            "es-ES": "Spanish",
            "fr-FR": "French",
            "de-DE": "German",
            "it-IT": "Italian",
            "pt-BR": "Portuguese",
            "ru-RU": "Russian",
            "ja-JP": "Japanese",
            "ko-KR": "Korean",
            "zh-CN": "Chinese"
        }
        
        self.current_language = VOICE_CONFIG["language"]
        
        # Voice profiles
        self.voice_profiles = {}
        self.current_voice_profile = None
        
        self.setup_voice_recognition()
        self.register_default_commands()
        
    def setup_tts(self):
        """Setup text-to-speech engine with platform-aware voice selection."""
        try:
            voices = self.tts_engine.getProperty('voices')
            if not voices:
                self.logger.warning("No TTS voices available")
                return
            
            # Try to set voice by config index first
            if len(voices) > VOICE_CONFIG["voice_id"]:
                self.tts_engine.setProperty('voice', voices[VOICE_CONFIG["voice_id"]].id)
            
            # Platform-specific voice selection for better quality
            import platform
            if platform.system() == "Darwin":
                # macOS: Prefer Samantha (natural female) or Alex (natural male)
                preferred_voices = ["samantha", "alex", "daniel", "karen"]
            else:
                # Windows: Prefer David or Zira
                preferred_voices = ["david", "zira", "mark"]
            
            # Find and set a preferred voice
            for pref in preferred_voices:
                for voice in voices:
                    if pref in voice.name.lower() or pref in voice.id.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        self.logger.info(f"TTS voice set to: {voice.name}")
                        break
                else:
                    continue
                break
            
            self.tts_engine.setProperty('rate', VOICE_CONFIG["tts_rate"])
            self.tts_engine.setProperty('volume', VOICE_CONFIG["tts_volume"])
            
        except Exception as e:
            self.logger.error(f"Error setting up TTS: {e}")
    
    def setup_voice_recognition(self):
        """Setup speech recognition with calibration"""
        try:
            with self.microphone as source:
                self.logger.info("Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
            self.recognizer.energy_threshold = VOICE_CONFIG["energy_threshold"]
            self.recognizer.dynamic_energy_threshold = VOICE_CONFIG["dynamic_energy_threshold"]
            self.recognizer.pause_threshold = VOICE_CONFIG["phrase_timeout"]
            
            self.logger.info("Voice recognition setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up voice recognition: {e}")
    
    def register_command(self, patterns: List[str], callback: Callable, description: str = ""):
        """Register voice command with multiple patterns"""
        for pattern in patterns:
            self.voice_commands[pattern.lower()] = {
                "callback": callback,
                "description": description,
                "usage_count": 0,
                "last_used": None
            }
    
    def register_default_commands(self):
        """Register default voice commands"""
        self.register_command(
            ["hello sam", "hey sam", "hi sam"],
            self.handle_greeting,
            "Greet the assistant"
        )
        
        self.register_command(
            ["stop listening", "sleep", "quiet"],
            self.stop_listening,
            "Stop voice recognition"
        )
        
        self.register_command(
            ["start listening", "wake up", "listen"],
            self.start_listening,
            "Start voice recognition"
        )
        
        self.register_command(
            ["change language to *", "switch language to *"],
            self.change_language,
            "Change voice recognition language"
        )
        
        self.register_command(
            ["what can you do", "help", "commands"],
            self.list_commands,
            "List available commands"
        )
        
        self.register_command(
            ["conversation mode on", "chat mode"],
            self.enable_conversation_mode,
            "Enable conversation mode"
        )
        
        self.register_command(
            ["conversation mode off", "command mode"],
            self.disable_conversation_mode,
            "Disable conversation mode"
        )

        # Memory-related commands
        self.register_command(
            ["remember that *", "note that *"],
            self.remember_that,
            "Remember a fact about the user"
        )
        self.register_command(
            ["what do you remember about me", "my memories"],
            self.recall_user_memories,
            "Recall user-related memories"
        )
    
    async def start_listening(self):
        """Start continuous voice recognition"""
        if self.is_listening:
            return
            
        self.is_listening = True
        self.assistant.state.is_listening = True
        # Capture the running event loop so we can schedule coroutines from threads
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            # Fallback if called outside an event loop; will be set later when available
            self.loop = None
        
        # Start background listening thread
        self.listen_thread = threading.Thread(target=self._listen_continuously, daemon=True)
        self.listen_thread.start()
        
        self.logger.info("Voice recognition started")
        self.speak("Voice recognition activated")
    
    def stop_listening(self):
        """Stop voice recognition"""
        self.is_listening = False
        self.assistant.state.is_listening = False
        self.conversation_mode = False
        
        self.logger.info("Voice recognition stopped")
        self.speak("Voice recognition deactivated")
    
    def _listen_continuously(self):
        """Continuous listening loop"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(
                        source, 
                        timeout=VOICE_CONFIG["recognition_timeout"],
                        phrase_time_limit=10
                    )
                
                # Process audio in background
                threading.Thread(
                    target=self._process_audio, 
                    args=(audio,), 
                    daemon=True
                ).start()
                
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Error in continuous listening: {e}")
                time.sleep(1)
    
    def _process_audio(self, audio):
        """Process audio input"""
        try:
            # Recognize speech
            text = self.recognizer.recognize_google(
                audio, 
                language=self.current_language
            ).lower()
            
            self.logger.info(f"Recognized: {text}")
            self.assistant.update_activity()
            
            # Check for wake word
            if not self.wake_word_detected and not self.conversation_mode:
                if VOICE_CONFIG["wake_word"] in text:
                    self.wake_word_detected = True
                    self.speak("Yes?")
                    return
                else:
                    return
            
            # Process command
            # Schedule the coroutine on the main event loop from this background thread
            try:
                if self.loop is None:
                    # Attempt to get a running loop again if not set
                    try:
                        self.loop = asyncio.get_running_loop()
                    except RuntimeError:
                        self.loop = None
                if self.loop:
                    asyncio.run_coroutine_threadsafe(self._process_command(text), self.loop)
                else:
                    # As a last resort, run the coroutine in a new event loop (blocking)
                    asyncio.run(self._process_command(text))
            except Exception as e:
                self.logger.error(f"Error scheduling command processing: {e}")
            
            # Reset wake word detection after processing
            if not self.conversation_mode:
                self.wake_word_detected = False
                
        except sr.UnknownValueError:
            if self.wake_word_detected or self.conversation_mode:
                self.speak("I didn't understand that. Could you repeat?")
                self.wake_word_detected = False
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition error: {e}")
            self.speak("Sorry, I'm having trouble with speech recognition.")
    
    async def _process_command(self, text: str):
        """Process recognized command"""
        self.assistant.add_to_conversation("user", text)
        
        # Find matching command
        command_found = False
        
        for pattern, command_info in self.voice_commands.items():
            if self._match_pattern(pattern, text):
                try:
                    # Update usage statistics
                    command_info["usage_count"] += 1
                    command_info["last_used"] = time.time()
                    
                    # Execute command
                    if asyncio.iscoroutinefunction(command_info["callback"]):
                        await command_info["callback"](text)
                    else:
                        command_info["callback"](text)
                    
                    command_found = True
                    break
                    
                except Exception as e:
                    self.logger.error(f"Error executing command '{pattern}': {e}")
                    self.speak("Sorry, I encountered an error processing that command.")
        
        # If no specific command found, use general AI processing
        if not command_found:
            await self._handle_general_query(text)
    
    def _match_pattern(self, pattern: str, text: str) -> bool:
        """Match command pattern with wildcards"""
        if "*" in pattern:
            # Convert pattern to regex
            regex_pattern = pattern.replace("*", ".*")
            return bool(re.match(regex_pattern, text))
        else:
            return pattern in text
    
    async def _handle_general_query(self, text: str):
        """Handle general queries using AI"""
        try:
            # Fall back to echo if LLM not available
            if not getattr(self.assistant, "llm", None):
                response = f"You said: {text}. (LLM is not configured)"
            else:
                context = self.assistant.get_context()
                memories = []
                try:
                    memories = self.assistant.memory.get_relevant_memories(text)
                except Exception:
                    memories = []

                # Run generation in a thread so we don't block the event loop
                response = await asyncio.to_thread(
                    self.assistant.llm.generate_response,
                    user_text=text,
                    context=context,
                    persona=AI_CONFIG.get("personality"),
                    memories=memories,
                    max_tokens=AI_CONFIG.get("max_tokens", 512),
                    temperature=AI_CONFIG.get("temperature", 0.7),
                )

            # Speak and record
            self.speak(response)
            self.assistant.add_to_conversation("assistant", response)
            
        except Exception as e:
            self.logger.error(f"Error handling general query: {e}")
            self.speak("I'm sorry, I couldn't process that request.")

    def remember_that(self, text: str):
        """Store a memory from a voice command like 'remember that ...'"""
        try:
            # Extract the part after 'remember that' or 'note that'
            lowered = text.lower()
            trigger_phrases = ["remember that", "note that"]
            for phrase in trigger_phrases:
                if phrase in lowered:
                    content = text[lowered.find(phrase) + len(phrase):].strip()
                    if content:
                        self.assistant.memory.add_memory(content, tags=["user"])
                        self.speak("Got it. I'll remember that.")
                        return
            self.speak("Please say 'remember that' followed by what you want me to remember.")
        except Exception as e:
            self.logger.error(f"Error storing memory: {e}")
            self.speak("I couldn't store that memory.")

    def recall_user_memories(self, text: str):
        """Recall and speak a summary of user-related memories"""
        try:
            memories = self.assistant.memory.get_memories_by_tag("user")
            if not memories:
                self.speak("I don't have any personal memories yet. You can say 'remember that ...' to teach me.")
                return
            # Summarize last few memories
            last = memories[-5:]
            summary = "; ".join(m["text"] for m in last)
            self.speak(f"Here's what I remember: {summary}")
        except Exception as e:
            self.logger.error(f"Error recalling memories: {e}")
            self.speak("I couldn't recall memories right now.")
    
    def speak(self, text: str, interrupt: bool = False):
        """Text-to-speech with queue management"""
        if interrupt:
            self.tts_engine.stop()
        
        self.assistant.state.is_speaking = True
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
        finally:
            self.assistant.state.is_speaking = False
    
    def change_language(self, text: str):
        """Change voice recognition language"""
        # Extract language from command
        for lang_code, lang_name in self.supported_languages.items():
            if lang_name.lower() in text.lower():
                self.current_language = lang_code
                self.speak(f"Language changed to {lang_name}")
                return
        
        self.speak("Language not supported or not recognized")
    
    def handle_greeting(self, text: str):
        """Handle greeting commands"""
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Greetings! I'm ready to assist you.",
            "Hello! Nice to hear from you again."
        ]
        
        import random
        self.speak(random.choice(greetings))
    
    def list_commands(self, text: str):
        """List available voice commands"""
        commands = []
        for pattern, info in self.voice_commands.items():
            if info["description"]:
                commands.append(f"{pattern}: {info['description']}")
        
        if commands:
            response = "Available commands: " + ", ".join(commands[:5])
            if len(commands) > 5:
                response += f" and {len(commands) - 5} more commands."
        else:
            response = "No commands available."
        
        self.speak(response)
    
    def enable_conversation_mode(self, text: str):
        """Enable conversation mode"""
        self.conversation_mode = True
        self.speak("Conversation mode enabled. I'll listen continuously now.")
    
    def disable_conversation_mode(self, text: str):
        """Disable conversation mode"""
        self.conversation_mode = False
        self.speak("Conversation mode disabled. Use the wake word to activate me.")
    
    def create_voice_profile(self, name: str, voice_sample_duration: int = 10):
        """Create voice profile for speaker recognition"""
        try:
            self.speak(f"Creating voice profile for {name}. Please speak for {voice_sample_duration} seconds.")
            
            # Record voice sample
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=voice_sample_duration + 2)
            
            # Store voice profile (simplified - would use actual voice recognition)
            self.voice_profiles[name] = {
                "created": time.time(),
                "sample": audio,
                "usage_count": 0
            }
            
            self.speak(f"Voice profile for {name} created successfully.")
            
        except Exception as e:
            self.logger.error(f"Error creating voice profile: {e}")
            self.speak("Failed to create voice profile.")
    
    def get_voice_stats(self) -> Dict:
        """Get voice recognition statistics"""
        return {
            "is_listening": self.is_listening,
            "conversation_mode": self.conversation_mode,
            "current_language": self.current_language,
            "wake_word_detected": self.wake_word_detected,
            "total_commands": len(self.voice_commands),
            "voice_profiles": len(self.voice_profiles)
        }