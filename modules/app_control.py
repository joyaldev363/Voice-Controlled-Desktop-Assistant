import os
import sys
import subprocess
import time
import psutil
from PIL import ImageGrab
import config

try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    PYCAW_AVAILABLE = True
except Exception:
    PYCAW_AVAILABLE = False


class AppController:
    def __init__(self, logger=None):
        self.log = logger or (lambda msg: None)

    def open_application(self, app_name: str) -> str:
        """Launch an application specified by name."""
        app_name_lower = app_name.lower().strip()
        
        # Check config mapping
        target_app = config.APPLICATIONS.get(app_name_lower, None)
        
        if not target_app:
            # Fuzzy check in config keys
            for key, val in config.APPLICATIONS.items():
                if key in app_name_lower or app_name_lower in key:
                    target_app = val
                    break

        if not target_app:
            # Fallback to direct app name
            target_app = app_name_lower

        try:
            self.log(f"🚀 Launching application: {target_app}")
            if os.name == 'nt':
                subprocess.Popen(target_app, shell=True)
            else:
                subprocess.Popen([target_app])
            return f"Opening {app_name}."
        except Exception as e:
            self.log(f"⚠️ Failed to open {app_name}: {e}")
            return f"Sorry, I couldn't launch {app_name}."

    def close_application(self, app_name: str) -> str:
        """Close processes matching the app name."""
        app_name_lower = app_name.lower().strip()
        closed_count = 0
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pname = proc.info['name'].lower()
                if app_name_lower in pname:
                    proc.kill()
                    closed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        if closed_count > 0:
            return f"Closed {app_name}."
        return f"No running application found matching {app_name}."

    def set_volume(self, level: int) -> str:
        """Set system master volume (0 to 100)."""
        level = max(0, min(100, level))
        if PYCAW_AVAILABLE and os.name == 'nt':
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                # Convert 0-100 scale to scalar (0.0 to 1.0)
                volume.SetMasterVolumeLevelScalar(level / 100.0, None)
                return f"Volume set to {level} percent."
            except Exception as e:
                self.log(f"⚠️ Pycaw error setting volume: {e}")
        
        return f"Unable to adjust volume directly on this system."

    def take_screenshot(self, save_dir: str = None) -> str:
        """Capture screenshot and save to pictures or working folder."""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            
            if not save_dir:
                save_dir = os.path.expanduser("~/Pictures")
                if not os.path.exists(save_dir):
                    save_dir = "."

            filepath = os.path.join(save_dir, filename)
            screenshot = ImageGrab.grab()
            screenshot.save(filepath)
            self.log(f"📸 Screenshot saved to {filepath}")
            return f"Screenshot taken and saved as {filename}."
        except Exception as e:
            self.log(f"⚠️ Screenshot error: {e}")
            return "Failed to take screenshot."

    def get_system_status(self) -> str:
        """Get CPU, RAM usage, and battery statistics."""
        cpu_usage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        ram_usage = memory.percent
        
        status_msg = f"CPU usage is at {cpu_usage} percent, and RAM usage is at {ram_usage} percent."
        
        battery = getattr(psutil, "sensors_battery", lambda: None)()
        if battery:
            percent = round(battery.percent)
            plugged = "plugged in" if battery.power_plugged else "on battery power"
            status_msg += f" Battery is at {percent} percent, {plugged}."
            
        return status_msg

    def lock_workstation(self) -> str:
        """Lock the computer screen."""
        if os.name == 'nt':
            import ctypes
            ctypes.windll.user32.LockWorkStation()
            return "Workstation locked."
        return "Screen lock command is only supported on Windows."
