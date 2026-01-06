import sys
import time
import subprocess
import webbrowser
from typing import Optional

try:
    import pyautogui
except Exception:
    pyautogui = None


class BrowserController:
    """
    A lightweight, modular browser input simulator that uses keyboard/mouse events
    to perform navigation like a human. Designed to be replaceable with other drivers
    (e.g., Playwright, AppleScript, CV-driven clicking) without changing call sites.

    Methods here are intentionally simple to reduce brittleness. They assume the user
    has granted Accessibility permissions on macOS for pyautogui.
    """

    def __init__(self, browser_app: Optional[str] = None):
        self.browser_app = browser_app  # e.g., "Google Chrome" or "Safari"
        self.platform = sys.platform

    def _default_browser_app(self) -> str:
        """Return a sensible default browser app name per platform."""
        if self.platform == "darwin":
            # Prefer Chrome; fall back to Safari when unavailable
            return "Google Chrome"
        if self.platform.startswith("win"):
            # Windows default – not used directly; focus via webbrowser
            return "Chrome"
        # Linux/others
        return "Chrome"

    def _ensure_pyautogui(self):
        if pyautogui is None:
            raise RuntimeError("pyautogui is not available. Please install it and grant Accessibility permissions.")

    def focus_or_launch_browser(self):
        """Bring a browser to the foreground or launch it if needed."""
        app = self.browser_app or self._default_browser_app()
        if self.platform == "darwin":
            # macOS: use 'open -a' to launch and osascript to activate
            try:
                subprocess.run(["open", "-a", app], check=False)
                subprocess.run(["osascript", "-e", f'tell application "{app}" to activate'], check=False)
                time.sleep(0.6)
            except Exception:
                pass
        elif self.platform.startswith("win"):
            # Windows: best-effort, rely on default browser
            webbrowser.open("about:blank")
            time.sleep(0.8)
        else:
            # Linux or other: best-effort
            webbrowser.open("about:blank")
            time.sleep(0.8)

    def new_tab(self):
        self._ensure_pyautogui()
        if self.platform == "darwin":
            pyautogui.hotkey("command", "t")
        else:
            pyautogui.hotkey("ctrl", "t")
        time.sleep(0.4)

    def type_and_submit(self, text: str, interval: float = 0.04):
        self._ensure_pyautogui()
        pyautogui.typewrite(text, interval=interval)
        pyautogui.press("enter")
        time.sleep(1.2)

    def open_url_via_typing(self, url: str):
        """Open a URL by focusing the browser, opening a new tab, typing the URL and submitting."""
        self.focus_or_launch_browser()
        self.new_tab()
        self.type_and_submit(url)

    def _exec_js_chrome(self, js: str) -> bool:
        try:
            subprocess.run(["osascript", "-e", f'tell application "Google Chrome" to tell front window to tell active tab to execute javascript "{js}"'], check=True)
            return True
        except Exception:
            return False

    def _exec_js_safari(self, js: str) -> bool:
        try:
            subprocess.run(["osascript", "-e", f'tell application "Safari" to do JavaScript "{js}" in document 1'], check=True)
            return True
        except Exception:
            return False

    def youtube_click_first_result_js(self):
        """Click the first video on a YouTube results page via JavaScript (Chrome/Safari)."""
        # Wait a bit to allow results to render
        time.sleep(1.2)
        js_candidates = [
            'var l=document.querySelector("a#video-title"); if(l){l.click();}',
            'var l=document.querySelector("ytd-video-renderer a#video-title"); if(l){l.click();}',
            'var a=document.querySelectorAll("a[href*=\\\"watch?v\\\"]"); if(a&&a.length){location.href=a[0].href;}',
        ]
        for js in js_candidates:
            if self._exec_js_chrome(js):
                return True
            if self._exec_js_safari(js):
                return True
        return False

    def youtube_search_via_typing(self, query: str):
        """On YouTube, focus search box with '/' and submit the query."""
        self._ensure_pyautogui()
        # Try to focus the address bar first to ensure we're on YouTube
        if self.platform == "darwin":
            pyautogui.hotkey("command", "l")
        else:
            pyautogui.hotkey("ctrl", "l")
        time.sleep(0.2)
        self.type_and_submit(f"https://www.youtube.com/results?search_query={query}")
        # Attempt to open first result: heuristic Tab navigation
        time.sleep(1.5)
        for _ in range(6):
            pyautogui.press("tab")
            time.sleep(0.08)
        pyautogui.press("enter")
        time.sleep(2.0)


class YouTubeAutomation:
    """
    High-level YouTube task automation with pluggable strategies:
    - direct: use webbrowser.open (fast, reliable, not human-like)
    - simulate: use BrowserController (human-like via keyboard/mouse)

    You can swap this implementation with a Playwright driver or CV driver
    without changing SAM's business logic.
    """

    def __init__(self, strategy: str = "direct", browser_app: Optional[str] = None):
        self.strategy = strategy
        self.bc = BrowserController(browser_app)

    def open_youtube(self):
        if self.strategy == "simulate":
            try:
                self.bc.open_url_via_typing("https://www.youtube.com")
                return "📺 YouTube opened via keyboard typing."
            except Exception as e:
                webbrowser.open("https://www.youtube.com")
                return f"📺 Fallback to direct open due to: {e}"
        else:
            webbrowser.open("https://www.youtube.com")
            return "📺 YouTube opened directly."

    def play_song(self, song: str):
        """Play a song on YouTube like a human would - open, search, and click."""
        import urllib.parse
        url_encoded = urllib.parse.quote(song)
        
        if self.strategy == "simulate":
            try:
                self.bc._ensure_pyautogui()
                
                # Step 1: Open YouTube homepage first
                self.bc.focus_or_launch_browser()
                self.bc.new_tab()
                
                # Type youtube.com and go there
                if self.bc.platform == "darwin":
                    pyautogui.hotkey("command", "l")  # Focus URL bar
                else:
                    pyautogui.hotkey("ctrl", "l")
                time.sleep(0.3)
                
                pyautogui.typewrite("youtube.com", interval=0.05)
                pyautogui.press("enter")
                time.sleep(2.0)  # Wait for YouTube to load
                
                # Step 2: Focus search box and search
                # Press '/' to focus YouTube search (or Tab to search box)
                pyautogui.press("/")
                time.sleep(0.5)
                
                # Use clipboard for unicode text support (Hindi, Telugu, etc.)
                self._type_text_via_clipboard(song)
                time.sleep(0.3)
                
                pyautogui.press("enter")
                time.sleep(2.5)  # Wait for results to load
                
                # Step 3: Click first video result
                # Try JS click first (most reliable)
                if self.bc.youtube_click_first_result_js():
                    return f"🎬 Playing '{song}' on YouTube (human-like)."
                
                # Fallback: Tab to first video and enter
                for _ in range(4):
                    pyautogui.press("tab")
                    time.sleep(0.1)
                pyautogui.press("enter")
                time.sleep(1.5)
                
                return f"🎵 Playing '{song}' on YouTube."
                
            except Exception as e:
                # Fallback to direct URL
                webbrowser.open(f"https://www.youtube.com/results?search_query={url_encoded}")
                return f"🎵 Fallback to direct search: {e}"
        else:
            webbrowser.open(f"https://www.youtube.com/results?search_query={url_encoded}")
            # Try to auto-click first result
            try:
                time.sleep(1.5)
                if self.bc.youtube_click_first_result_js():
                    return f"🎬 Playing '{song}' via JS in browser."
            except Exception:
                pass
            return f"🎵 Searching '{song}' on YouTube."
    
    def _type_text_via_clipboard(self, text: str):
        """Type text using clipboard (supports unicode/non-ASCII)."""
        import subprocess
        platform = self.bc.platform
        if platform == "darwin":
            # macOS: use pbcopy
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            time.sleep(0.1)
            pyautogui.hotkey("command", "v")
        elif platform.startswith("win"):
            # Windows: use pyperclip or direct paste
            try:
                import pyperclip
                pyperclip.copy(text)
                pyautogui.hotkey("ctrl", "v")
            except ImportError:
                # Fallback to typewrite for ASCII
                pyautogui.typewrite(text.replace(" ", " "), interval=0.05)
        else:
            # Linux: use xclip if available
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
                time.sleep(0.1)
                pyautogui.hotkey("ctrl", "v")
            except Exception:
                pyautogui.typewrite(text, interval=0.05)
        time.sleep(0.2)


class WhatsAppAutomation:
    """
    Human-like WhatsApp Desktop App automation for sending messages.
    Uses keyboard/mouse simulation to interact with the WhatsApp desktop application.
    
    Requirements:
    - WhatsApp desktop app must be installed
    - User must be logged into WhatsApp on the desktop app
    - pyautogui must be available with Accessibility permissions (macOS)
    """
    
    def __init__(self):
        self.platform = sys.platform
        # Configurable delays for app responsiveness
        self.app_launch_delay = 2.0   # Wait for WhatsApp app to open/focus
        self.search_delay = 1.0       # Wait for search results
        self.contact_select_delay = 0.8  # Wait after selecting contact
        self.send_delay = 0.3         # Wait after sending
    
    def _ensure_pyautogui(self):
        if pyautogui is None:
            raise RuntimeError("pyautogui is not available. Please install it and grant Accessibility permissions.")
    
    def _open_whatsapp_app(self):
        """Open WhatsApp using Spotlight search like a human would."""
        self._ensure_pyautogui()
        
        if self.platform == "darwin":
            # macOS: Use Spotlight search like a human
            # Step 1: Open Spotlight with Cmd+Space
            pyautogui.hotkey("command", "space")
            time.sleep(0.5)
            
            # Step 2: Type "WhatsApp"
            pyautogui.typewrite("WhatsApp", interval=0.05)
            time.sleep(0.8)
            
            # Step 3: Press Enter to launch
            pyautogui.press("enter")
            
        elif self.platform.startswith("win"):
            # Windows: Use Start menu search like a human
            # Step 1: Open Start menu with Windows key
            pyautogui.press("win")
            time.sleep(0.5)
            
            # Step 2: Type "WhatsApp"
            pyautogui.typewrite("WhatsApp", interval=0.05)
            time.sleep(0.8)
            
            # Step 3: Press Enter to launch
            pyautogui.press("enter")
            
        else:
            # Linux: Try using application launcher
            try:
                pyautogui.hotkey("super")
                time.sleep(0.5)
                pyautogui.typewrite("WhatsApp", interval=0.05)
                time.sleep(0.8)
                pyautogui.press("enter")
            except Exception:
                subprocess.Popen(["whatsapp-desktop"])
        
        time.sleep(self.app_launch_delay)
    
    def _type_text_via_clipboard(self, text: str):
        """Type text using clipboard (supports unicode/non-ASCII characters like Hindi, Telugu, emojis)."""
        if self.platform == "darwin":
            # macOS: use pbcopy
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            time.sleep(0.1)
            pyautogui.hotkey("command", "v")
        elif self.platform.startswith("win"):
            # Windows: use pyperclip or direct paste
            try:
                import pyperclip
                pyperclip.copy(text)
                pyautogui.hotkey("ctrl", "v")
            except ImportError:
                # Fallback to typewrite for ASCII only
                pyautogui.typewrite(text, interval=0.03)
        else:
            # Linux: use xclip if available
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
                time.sleep(0.1)
                pyautogui.hotkey("ctrl", "v")
            except Exception:
                pyautogui.typewrite(text, interval=0.03)
        time.sleep(0.2)
    
    def send_message(self, contact_name: str, message: str) -> str:
        """
        Send a WhatsApp message to a contact using the desktop app.
        
        Args:
            contact_name: Name of the contact to search for
            message: Message text to send
            
        Returns:
            Status message indicating success or failure
        """
        try:
            self._ensure_pyautogui()
            
            # Step 1: Open/Focus WhatsApp desktop app
            self._open_whatsapp_app()
            
            # Step 2: Open new chat / search
            # On macOS WhatsApp: Cmd+N opens new chat search
            # On Windows: Ctrl+N or click on search
            if self.platform == "darwin":
                pyautogui.hotkey("command", "n")
            else:
                pyautogui.hotkey("ctrl", "n")
            time.sleep(0.5)
            
            # Step 3: Type contact name to search
            self._type_text_via_clipboard(contact_name)
            time.sleep(self.search_delay)
            
            # Step 4: Press down arrow to select first result and Enter to open chat
            pyautogui.press("down")
            time.sleep(0.2)
            pyautogui.press("enter")
            time.sleep(self.contact_select_delay)
            
            # Step 5: The chat should now be open with message input focused
            # Type the message
            self._type_text_via_clipboard(message)
            time.sleep(0.2)
            
            # Step 6: Send the message by pressing Enter
            pyautogui.press("enter")
            time.sleep(self.send_delay)
            
            return f"✅ Message sent to {contact_name} on WhatsApp!"
            
        except Exception as e:
            return f"❌ Failed to send WhatsApp message: {str(e)}"
    
    def open_whatsapp(self) -> str:
        """Just open WhatsApp desktop app without sending a message."""
        try:
            self._open_whatsapp_app()
            return "💬 WhatsApp app opened."
        except Exception as e:
            return f"❌ Failed to open WhatsApp: {str(e)}"


class SystemLauncher:
    def __init__(self):
        self.platform = sys.platform

    def _ensure_pyautogui(self):
        if pyautogui is None:
            raise RuntimeError("pyautogui is not available. Please install it and grant Accessibility permissions.")

    def search_and_open(self, app_name: str):
        name = app_name.strip()
        if not name:
            return False
        if self.platform == "darwin":
            try:
                escaped = name.replace('"', '\\"')
                subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke space using {command down}'], check=False)
                time.sleep(0.3)
                subprocess.run(["osascript", "-e", f'tell application "System Events" to keystroke "{escaped}"'], check=False)
                time.sleep(0.4)
                subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke return'], check=False)
                return True
            except Exception:
                # Fallback to pyautogui if AppleScript fails
                try:
                    self._ensure_pyautogui()
                    pyautogui.hotkey("command", "space")
                    time.sleep(0.25)
                    pyautogui.typewrite(name, interval=0.04)
                    time.sleep(0.3)
                    pyautogui.press("enter")
                    return True
                except Exception:
                    return False
        elif self.platform.startswith("win"):
            try:
                pyautogui.hotkey("win")
                time.sleep(0.25)
                pyautogui.typewrite(name, interval=0.04)
                time.sleep(0.3)
                pyautogui.press("enter")
                return True
            except Exception:
                return False
        else:
            try:
                pyautogui.hotkey("ctrl", "alt", "t")
                time.sleep(0.5)
                pyautogui.typewrite(name, interval=0.04)
                pyautogui.press("enter")
                return True
            except Exception:
                return False
