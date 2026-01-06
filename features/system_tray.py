"""
SAM AI Assistant - System Tray Module
Provides system tray integration, global hotkeys, and mini floating mode.
Cross-platform support for Windows and macOS.
"""

import threading
import platform
import logging
from typing import Optional, Callable, Dict
from PIL import Image, ImageDraw

# Try importing pystray for system tray support
try:
    import pystray
    from pystray import MenuItem as item
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False
    print("[INFO] pystray not available. Install with: pip install pystray")

# Try importing pynput for global hotkeys
try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("[INFO] pynput not available. Install with: pip install pynput")

# Import customtkinter for mini window
try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

logger = logging.getLogger(__name__)


def create_tray_icon_image(size: int = 64, color: str = "#7C3AED") -> Image.Image:
    """Create a simple SAM icon for the system tray."""
    # Create a circular icon with 'S' for SAM
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw filled circle
    padding = 4
    draw.ellipse(
        [padding, padding, size - padding, size - padding],
        fill=color,
        outline=None
    )
    
    # Draw 'S' in the center
    try:
        from PIL import ImageFont
        # Try to use a system font
        font_size = size // 2
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            except:
                font = ImageFont.load_default()
        
        text = "S"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 2
        draw.text((x, y), text, fill="white", font=font)
    except Exception as e:
        logger.warning(f"Could not draw text on tray icon: {e}")
    
    return image


class TrayManager:
    """Manages the system tray icon and context menu."""
    
    def __init__(self, app, callbacks: Dict[str, Callable] = None):
        """
        Initialize the tray manager.
        
        Args:
            app: Reference to the main application (EnhancedJarvisGUI)
            callbacks: Dictionary of callback functions for menu actions
        """
        self.app = app
        self.callbacks = callbacks or {}
        self.icon = None
        self.running = False
        self._thread = None
        
        if not PYSTRAY_AVAILABLE:
            logger.warning("System tray not available - pystray not installed")
            return
    
    def start(self):
        """Start the system tray icon."""
        if not PYSTRAY_AVAILABLE:
            return False
        
        if self.running:
            return True
        
        try:
            # Create the icon image
            icon_image = create_tray_icon_image()
            
            # Create the menu
            menu = self._create_menu()
            
            # Create the icon
            self.icon = pystray.Icon(
                name="SAM",
                icon=icon_image,
                title="SAM AI Assistant",
                menu=menu
            )
            
            # Run in a separate thread
            self._thread = threading.Thread(target=self._run_icon, daemon=True)
            self._thread.start()
            self.running = True
            
            logger.info("System tray icon started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start system tray: {e}")
            return False
    
    def _run_icon(self):
        """Run the tray icon (blocking call)."""
        try:
            # On macOS, pystray may have permission issues
            if platform.system() == "Darwin":
                import signal
                # Set up signal handler for trace trap
                def handle_sigtrap(signum, frame):
                    logger.error("Received SIGTRAP - likely accessibility permission issue")
                    self.running = False
                    return
                signal.signal(signal.SIGTRAP, handle_sigtrap)
            
            self.icon.run()
        except Exception as e:
            logger.error(f"Tray icon error: {e}")
            self.running = False
    
    def _create_menu(self) -> pystray.Menu:
        """Create the context menu for the tray icon."""
        return pystray.Menu(
            item("🤖 SAM AI Assistant", None, enabled=False),
            pystray.Menu.SEPARATOR,
            item("👁️ Show/Hide SAM", self._on_show_hide),
            item("📌 Always on Top", self._on_toggle_always_on_top, checked=lambda _: self._is_always_on_top()),
            item("💬 Mini Mode", self._on_mini_mode),
            pystray.Menu.SEPARATOR,
            item("🎤 Start Listening", self._on_toggle_listening),
            item("🔇 Mute", self._on_mute),
            pystray.Menu.SEPARATOR,
            item("⚙️ Settings", self._on_settings),
            item("❌ Exit", self._on_exit)
        )
    
    def _is_always_on_top(self) -> bool:
        """Check if always-on-top is enabled."""
        try:
            return getattr(self.app, 'always_on_top', False)
        except:
            return False
    
    def _on_show_hide(self, icon, item):
        """Toggle main window visibility."""
        if 'toggle_visibility' in self.callbacks:
            self.app.root.after(0, self.callbacks['toggle_visibility'])
    
    def _on_toggle_always_on_top(self, icon, item):
        """Toggle always-on-top mode."""
        if 'toggle_always_on_top' in self.callbacks:
            self.app.root.after(0, self.callbacks['toggle_always_on_top'])
    
    def _on_mini_mode(self, icon, item):
        """Open mini floating mode."""
        if 'show_mini_mode' in self.callbacks:
            self.app.root.after(0, self.callbacks['show_mini_mode'])
    
    def _on_toggle_listening(self, icon, item):
        """Toggle voice listening."""
        if 'toggle_listening' in self.callbacks:
            self.app.root.after(0, self.callbacks['toggle_listening'])
    
    def _on_mute(self, icon, item):
        """Mute SAM."""
        if 'mute' in self.callbacks:
            self.app.root.after(0, self.callbacks['mute'])
    
    def _on_settings(self, icon, item):
        """Open settings."""
        if 'show_settings' in self.callbacks:
            self.app.root.after(0, self.callbacks['show_settings'])
    
    def _on_exit(self, icon, item):
        """Exit the application."""
        self.stop()
        if 'exit' in self.callbacks:
            self.app.root.after(0, self.callbacks['exit'])
    
    def stop(self):
        """Stop the system tray icon."""
        if self.icon and self.running:
            try:
                self.icon.stop()
                self.running = False
                logger.info("System tray icon stopped")
            except Exception as e:
                logger.error(f"Error stopping tray icon: {e}")
    
    def notify(self, title: str, message: str):
        """Show a notification from the tray icon."""
        if self.icon and self.running:
            try:
                self.icon.notify(message, title)
            except Exception as e:
                logger.warning(f"Could not show notification: {e}")


class HotkeyManager:
    """Manages global hotkeys for SAM."""
    
    def __init__(self, app, hotkey: str = "ctrl+shift+s"):
        """
        Initialize the hotkey manager.
        
        Args:
            app: Reference to the main application
            hotkey: Hotkey combination string (e.g., "ctrl+shift+s")
        """
        self.app = app
        self.hotkey_str = hotkey
        self.listener = None
        self.running = False
        self.callbacks: Dict[str, Callable] = {}
        
        # Parse the hotkey
        self._current_keys = set()
        self._target_keys = self._parse_hotkey(hotkey)
        
        if not PYNPUT_AVAILABLE:
            logger.warning("Global hotkeys not available - pynput not installed")
    
    def _parse_hotkey(self, hotkey: str) -> set:
        """Parse a hotkey string into a set of key objects."""
        keys = set()
        parts = hotkey.lower().split('+')
        
        for part in parts:
            part = part.strip()
            if part in ('ctrl', 'control'):
                keys.add(keyboard.Key.ctrl)
            elif part in ('cmd', 'command'):
                keys.add(keyboard.Key.cmd)
            elif part == 'shift':
                keys.add(keyboard.Key.shift)
            elif part == 'alt':
                keys.add(keyboard.Key.alt)
            elif len(part) == 1:
                keys.add(keyboard.KeyCode.from_char(part))
        
        return keys
    
    def register(self, action: str, callback: Callable):
        """Register a callback for a hotkey action."""
        self.callbacks[action] = callback
    
    def start(self):
        """Start listening for hotkeys."""
        if not PYNPUT_AVAILABLE:
            return False
        
        if self.running:
            return True
        
        # On macOS, pynput keyboard listener requires accessibility permissions
        # which can cause trace trap errors if not granted. Skip for now.
        if platform.system() == "Darwin":
            logger.warning("Global hotkeys disabled on macOS (requires accessibility permissions)")
            logger.info("Use tray menu to access mini mode instead")
            return False
        
        try:
            self.listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )
            self.listener.start()
            self.running = True
            
            # Determine display hotkey based on platform
            if platform.system() == "Darwin":
                display_hotkey = "Cmd+Shift+S"
            else:
                display_hotkey = "Ctrl+Shift+S"
            
            logger.info(f"Hotkey listener started ({display_hotkey})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start hotkey listener: {e}")
            return False
    
    def _on_press(self, key):
        """Handle key press events."""
        try:
            # Normalize the key
            if hasattr(key, 'char') and key.char:
                self._current_keys.add(keyboard.KeyCode.from_char(key.char.lower()))
            else:
                # Handle modifier keys
                if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
                    self._current_keys.add(keyboard.Key.ctrl)
                elif key in (keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
                    self._current_keys.add(keyboard.Key.cmd)
                elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
                    self._current_keys.add(keyboard.Key.shift)
                elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
                    self._current_keys.add(keyboard.Key.alt)
                else:
                    self._current_keys.add(key)
            
            # Check if target hotkey is pressed
            if self._check_hotkey():
                self._trigger_hotkey()
                
        except Exception as e:
            logger.debug(f"Key press error: {e}")
    
    def _on_release(self, key):
        """Handle key release events."""
        try:
            # Remove the key from current keys
            if hasattr(key, 'char') and key.char:
                self._current_keys.discard(keyboard.KeyCode.from_char(key.char.lower()))
            else:
                if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
                    self._current_keys.discard(keyboard.Key.ctrl)
                elif key in (keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
                    self._current_keys.discard(keyboard.Key.cmd)
                elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
                    self._current_keys.discard(keyboard.Key.shift)
                elif key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
                    self._current_keys.discard(keyboard.Key.alt)
                else:
                    self._current_keys.discard(key)
        except Exception as e:
            logger.debug(f"Key release error: {e}")
    
    def _check_hotkey(self) -> bool:
        """Check if the target hotkey combination is pressed."""
        # On macOS, also check for cmd when ctrl is in target
        if platform.system() == "Darwin":
            # Allow either Ctrl or Cmd on macOS
            target_copy = self._target_keys.copy()
            if keyboard.Key.ctrl in target_copy:
                target_copy.discard(keyboard.Key.ctrl)
                target_copy.add(keyboard.Key.cmd)
                if target_copy.issubset(self._current_keys):
                    return True
        
        return self._target_keys.issubset(self._current_keys)
    
    def _trigger_hotkey(self):
        """Trigger the hotkey callback."""
        if 'toggle_visibility' in self.callbacks:
            # Use after() to run on the main thread
            try:
                self.app.root.after(0, self.callbacks['toggle_visibility'])
            except Exception as e:
                logger.error(f"Error triggering hotkey callback: {e}")
    
    def stop(self):
        """Stop listening for hotkeys."""
        if self.listener and self.running:
            try:
                self.listener.stop()
                self.running = False
                logger.info("Hotkey listener stopped")
            except Exception as e:
                logger.error(f"Error stopping hotkey listener: {e}")


class MiniFloatingWindow:
    """A compact floating window for quick SAM interactions."""
    
    def __init__(self, app, theme_colors: dict = None):
        """
        Initialize the mini floating window.
        
        Args:
            app: Reference to the main application
            theme_colors: Color scheme dictionary
        """
        self.app = app
        self.colors = theme_colors or {
            "bg": "#1a1a2e",
            "fg": "#ffffff",
            "accent": "#7C3AED",
            "input_bg": "#2d2d44",
            "input_border": "#3d3d5c"
        }
        self.window = None
        self.is_visible = False
        self._drag_data = {"x": 0, "y": 0}
        
        if not CTK_AVAILABLE:
            logger.warning("Mini floating window not available - customtkinter not installed")
    
    def show(self):
        """Show the mini floating window."""
        if not CTK_AVAILABLE:
            return
        
        if self.window and self.is_visible:
            self.window.focus_force()
            return
        
        try:
            self._create_window()
            self.is_visible = True
            logger.info("Mini floating window shown")
        except Exception as e:
            logger.error(f"Failed to create mini window: {e}")
    
    def _create_window(self):
        """Create the mini floating window."""
        # Create toplevel window
        self.window = ctk.CTkToplevel(self.app.root)
        self.window.title("SAM Mini")
        self.window.geometry("400x80")
        self.window.resizable(False, False)
        
        # Make it always on top
        self.window.attributes("-topmost", True)
        
        # On macOS, keep the window decorated to ensure proper visibility and input
        # On other platforms, use overrideredirect for frameless look
        if platform.system() != "Darwin":
            self.window.overrideredirect(True)
        
        # Configure appearance
        self.window.configure(fg_color=self.colors["bg"])
        
        # Position at top-center of screen
        self.window.update_idletasks()  # Ensure geometry is calculated
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - 400) // 2
        y = 50
        self.window.geometry(f"400x80+{x}+{y}")
        
        # Ensure the window is visible
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
        
        # Make window draggable
        self.window.bind("<Button-1>", self._start_drag)
        self.window.bind("<B1-Motion>", self._on_drag)
        
        # Create main container with rounded corners
        main_frame = ctk.CTkFrame(
            self.window,
            fg_color=self.colors["bg"],
            corner_radius=20,
            border_width=2,
            border_color=self.colors["input_border"]
        )
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Inner container
        inner_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # SAM label
        sam_label = ctk.CTkLabel(
            inner_frame,
            text="🤖",
            font=("Segoe UI", 24),
            text_color=self.colors["accent"]
        )
        sam_label.pack(side="left", padx=(0, 10))
        
        # Input field
        self.input_field = ctk.CTkEntry(
            inner_frame,
            placeholder_text="Ask SAM anything...",
            font=("Segoe UI", 14),
            fg_color=self.colors["input_bg"],
            text_color=self.colors["fg"],
            border_color=self.colors["input_border"],
            corner_radius=20,
            height=40
        )
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self._on_send)
        
        # Mic button
        self.mic_button = ctk.CTkButton(
            inner_frame,
            text="🎤",
            font=("Segoe UI", 16),
            width=40,
            height=40,
            corner_radius=20,
            fg_color=self.colors["accent"],
            hover_color="#9333EA",
            command=self._on_mic
        )
        self.mic_button.pack(side="left", padx=(0, 5))
        
        # Expand button
        expand_button = ctk.CTkButton(
            inner_frame,
            text="⬆️",
            font=("Segoe UI", 14),
            width=40,
            height=40,
            corner_radius=20,
            fg_color=self.colors["input_bg"],
            hover_color=self.colors["input_border"],
            command=self._on_expand
        )
        expand_button.pack(side="left", padx=(0, 5))
        
        # Close button
        close_button = ctk.CTkButton(
            inner_frame,
            text="✕",
            font=("Segoe UI", 14),
            width=40,
            height=40,
            corner_radius=20,
            fg_color=self.colors["input_bg"],
            hover_color="#ef4444",
            command=self.hide
        )
        close_button.pack(side="left")
        
        # Ensure input field gets focus and can be clicked
        self.window.update_idletasks()  # Process all pending events
        self.input_field.focus_force()
        
        # Prevent drag binding from interfering with input field clicks
        self.input_field.bind("<Button-1>", lambda e: self.input_field.focus_set())
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.hide)
    
    def _start_drag(self, event):
        """Start dragging the window."""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
    
    def _on_drag(self, event):
        """Handle window dragging."""
        if self.window:
            x = self.window.winfo_x() + event.x - self._drag_data["x"]
            y = self.window.winfo_y() + event.y - self._drag_data["y"]
            self.window.geometry(f"+{x}+{y}")
    
    def _on_send(self, event=None):
        """Handle sending a command."""
        text = self.input_field.get().strip()
        if text:
            self.input_field.delete(0, "end")
            # Process command through main app
            try:
                self.app.root.after(0, lambda: self.app.process_command(text))
            except Exception as e:
                logger.error(f"Error processing mini window command: {e}")
    
    def _on_mic(self):
        """Handle microphone button click."""
        try:
            if hasattr(self.app, 'toggle_listening'):
                self.app.toggle_listening()
            elif hasattr(self.app, 'start_listening'):
                self.app.start_listening()
        except Exception as e:
            logger.error(f"Error toggling mic from mini window: {e}")
    
    def _on_expand(self):
        """Expand to show the main window."""
        try:
            self.hide()
            if hasattr(self.app, 'restore_from_tray'):
                self.app.restore_from_tray()
            else:
                self.app.root.deiconify()
                self.app.root.focus_force()
        except Exception as e:
            logger.error(f"Error expanding from mini window: {e}")
    
    def hide(self):
        """Hide the mini floating window."""
        if self.window:
            try:
                self.window.destroy()
                self.window = None
                self.is_visible = False
                logger.info("Mini floating window hidden")
            except Exception as e:
                logger.error(f"Error hiding mini window: {e}")
    
    def toggle(self):
        """Toggle the mini window visibility."""
        if self.is_visible:
            self.hide()
        else:
            self.show()
