"""
SAM AI - Cross-Platform Utilities Module
Provides platform-aware audio, brightness, and power management for Windows and macOS.
"""
import platform
import subprocess
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

def get_platform() -> str:
    """Get current platform: 'windows', 'darwin' (macOS), or 'linux'."""
    system = platform.system().lower()
    if system == 'windows':
        return 'windows'
    elif system == 'darwin':
        return 'darwin'
    else:
        return 'linux'

# ============================================================================
# VOLUME CONTROL
# ============================================================================

def get_volume() -> Optional[int]:
    """Get current system volume (0-100). Returns None if unavailable."""
    plat = get_platform()
    
    if plat == 'darwin':
        try:
            result = subprocess.run(
                ['osascript', '-e', 'output volume of (get volume settings)'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return int(result.stdout.strip())
        except Exception as e:
            logger.error(f"Error getting macOS volume: {e}")
        return None
    
    elif plat == 'windows':
        try:
            from comtypes import CLSCTX_ALL
            from ctypes import POINTER, cast
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            return int(volume.GetMasterVolumeLevelScalar() * 100)
        except Exception as e:
            logger.error(f"Error getting Windows volume: {e}")
        return None
    
    return None


def set_volume(percent: int) -> Tuple[bool, str]:
    """Set system volume (0-100). Returns (success, message)."""
    percent = max(0, min(100, percent))
    plat = get_platform()
    
    if plat == 'darwin':
        try:
            subprocess.run(
                ['osascript', '-e', f'set volume output volume {percent}'],
                capture_output=True, check=True
            )
            return True, ""
        except Exception as e:
            return False, f"Failed to set macOS volume: {e}"
    
    elif plat == 'windows':
        try:
            from comtypes import CLSCTX_ALL
            from ctypes import POINTER, cast
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
            return True, ""
        except ImportError:
            return False, "pycaw not installed. Run: pip install pycaw"
        except Exception as e:
            return False, f"Failed to set Windows volume: {e}"
    
    return False, f"Volume control not supported on {plat}"


def adjust_volume(direction: str, amount: int = 10) -> Tuple[bool, str]:
    """Adjust volume up or down by amount. Returns (success, message)."""
    current = get_volume()
    if current is None:
        current = 50  # Assume middle if unknown
    
    if direction.lower() == 'up':
        target = current + amount
    else:
        target = current - amount
    
    return set_volume(target)


def mute_volume(mute: bool = True) -> Tuple[bool, str]:
    """Mute or unmute system volume. Returns (success, message)."""
    plat = get_platform()
    
    if plat == 'darwin':
        try:
            mute_cmd = 'true' if mute else 'false'
            subprocess.run(
                ['osascript', '-e', f'set volume output muted {mute_cmd}'],
                capture_output=True, check=True
            )
            return True, ""
        except Exception as e:
            return False, f"Failed to {'mute' if mute else 'unmute'} macOS: {e}"
    
    elif plat == 'windows':
        try:
            from comtypes import CLSCTX_ALL
            from ctypes import POINTER, cast
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(1 if mute else 0, None)
            return True, ""
        except ImportError:
            # Fallback: use key events
            try:
                import ctypes
                VK_VOLUME_MUTE = 0xAD
                ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
                return True, "(toggle via key event)"
            except Exception as e:
                return False, f"Failed to mute via key events: {e}"
        except Exception as e:
            return False, f"Failed to {'mute' if mute else 'unmute'} Windows: {e}"
    
    return False, f"Mute not supported on {plat}"


# ============================================================================
# BRIGHTNESS CONTROL
# ============================================================================

def _check_brightness_cli() -> bool:
    """Check if brightness CLI is available on macOS."""
    try:
        result = subprocess.run(['which', 'brightness'], capture_output=True)
        return result.returncode == 0
    except Exception:
        return False


def _install_brightness_cli() -> bool:
    """Attempt to install brightness CLI via Homebrew on macOS."""
    try:
        logger.info("Installing brightness CLI via Homebrew...")
        result = subprocess.run(
            ['brew', 'install', 'brightness'],
            capture_output=True, text=True
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to install brightness CLI: {e}")
        return False


def get_brightness() -> Optional[int]:
    """Get current screen brightness (0-100). Returns None if unavailable."""
    plat = get_platform()
    
    if plat == 'darwin':
        # Try brightness CLI first
        if _check_brightness_cli():
            try:
                result = subprocess.run(['brightness', '-l'], capture_output=True, text=True)
                if result.returncode == 0:
                    # Parse output like "display 0: brightness 0.5"
                    for line in result.stdout.split('\n'):
                        if 'brightness' in line:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part == 'brightness' and i + 1 < len(parts):
                                    return int(float(parts[i + 1]) * 100)
            except Exception as e:
                logger.error(f"Error getting macOS brightness: {e}")
        return None
    
    elif plat == 'windows':
        try:
            cmd = "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness | Select-Object -ExpandProperty CurrentBrightness)"
            result = subprocess.run(
                ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', cmd],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                val = result.stdout.strip()
                return int(val) if val.isdigit() else None
        except Exception as e:
            logger.error(f"Error getting Windows brightness: {e}")
        return None
    
    return None


def set_brightness(percent: int) -> Tuple[bool, str]:
    """Set screen brightness (0-100). Returns (success, message)."""
    percent = max(0, min(100, percent))
    plat = get_platform()
    
    if plat == 'darwin':
        # Try brightness CLI
        if not _check_brightness_cli():
            # Attempt auto-install
            if not _install_brightness_cli():
                return False, "Brightness control requires 'brightness' CLI. Install with: brew install brightness"
        
        try:
            brightness_val = percent / 100.0
            subprocess.run(
                ['brightness', str(brightness_val)],
                capture_output=True, check=True
            )
            return True, ""
        except Exception as e:
            return False, f"Failed to set macOS brightness: {e}"
    
    elif plat == 'windows':
        try:
            cmd = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {percent})"
            result = subprocess.run(
                ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', cmd],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return True, ""
            else:
                return False, "Brightness control via WMI not supported on this display."
        except Exception as e:
            return False, f"Failed to set Windows brightness: {e}"
    
    return False, f"Brightness control not supported on {plat}"


def adjust_brightness(direction: str, amount: int = 10) -> Tuple[bool, str]:
    """Adjust brightness up or down. Returns (success, message)."""
    current = get_brightness()
    if current is None:
        current = 50  # Assume middle if unknown
    
    if direction.lower() == 'up':
        target = current + amount
    else:
        target = current - amount
    
    return set_brightness(target)


# ============================================================================
# POWER MANAGEMENT
# ============================================================================

def power_action(action: str) -> Tuple[bool, str]:
    """Execute power action: shutdown, restart, sleep, hibernate, lock. Returns (success, message)."""
    plat = get_platform()
    action = action.lower()
    
    if plat == 'darwin':
        try:
            if action == 'shutdown':
                subprocess.Popen(['osascript', '-e', 'tell app "System Events" to shut down'])
            elif action == 'restart':
                subprocess.Popen(['osascript', '-e', 'tell app "System Events" to restart'])
            elif action == 'sleep':
                subprocess.Popen(['pmset', 'sleepnow'])
            elif action == 'lock':
                subprocess.Popen(['/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession', '-suspend'])
            elif action == 'hibernate':
                # macOS doesn't have true hibernate, use deep sleep
                subprocess.Popen(['pmset', 'sleepnow'])
                return True, "(macOS uses sleep instead of hibernate)"
            else:
                return False, f"Unknown power action: {action}"
            return True, ""
        except Exception as e:
            return False, f"Failed to execute {action} on macOS: {e}"
    
    elif plat == 'windows':
        try:
            if action == 'shutdown':
                subprocess.Popen(['shutdown', '/s', '/t', '0'])
            elif action == 'restart':
                subprocess.Popen(['shutdown', '/r', '/t', '0'])
            elif action == 'sleep':
                subprocess.Popen(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'])
            elif action == 'hibernate':
                subprocess.Popen(['shutdown', '/h'])
            elif action == 'lock':
                subprocess.Popen(['rundll32.exe', 'user32.dll,LockWorkStation'])
            else:
                return False, f"Unknown power action: {action}"
            return True, ""
        except Exception as e:
            return False, f"Failed to execute {action} on Windows: {e}"
    
    return False, f"Power actions not supported on {plat}"


# ============================================================================
# DISPLAY MODE SWITCHING
# ============================================================================

def switch_display_mode(mode: str) -> Tuple[bool, str]:
    """Switch display mode: extend, duplicate/mirror, external, internal. Returns (success, message)."""
    plat = get_platform()
    mode = mode.lower()
    
    if plat == 'darwin':
        # macOS display switching requires System Preferences or displayplacer tool
        try:
            if mode in ['extend', 'extended']:
                # Try using displayplacer if available
                result = subprocess.run(['which', 'displayplacer'], capture_output=True)
                if result.returncode == 0:
                    # Complex: would need to query current displays and set arrangement
                    return False, "Display mode switching on macOS requires manual setup or 'displayplacer' tool"
                return False, "Display mode switching requires 'displayplacer'. Install with: brew install displayplacer"
            elif mode in ['duplicate', 'mirror', 'clone']:
                # Mirror mode via System Preferences automation  
                script = '''
                tell application "System Preferences"
                    activate
                    reveal anchor "displaysDisplayTab" of pane id "com.apple.preference.displays"
                end tell
                '''
                subprocess.run(['osascript', '-e', script])
                return True, "Opened Display Preferences. Please enable mirroring manually."
            else:
                return False, f"Display mode '{mode}' not supported on macOS"
        except Exception as e:
            return False, f"Failed to switch display mode on macOS: {e}"
    
    elif plat == 'windows':
        exe = "DisplaySwitch.exe"
        arg_map = {
            'extend': '/extend',
            'extended': '/extend',
            'duplicate': '/clone',
            'mirror': '/clone',
            'clone': '/clone',
            'external': '/external',
            'second': '/external',
            'internal': '/internal',
            'pc': '/internal'
        }
        arg = arg_map.get(mode)
        if arg is None:
            return False, f"Unknown display mode: {mode}"
        try:
            subprocess.Popen([exe, arg])
            return True, ""
        except Exception as e:
            return False, f"Failed to switch display: {e}"
    
    return False, f"Display switching not supported on {plat}"
