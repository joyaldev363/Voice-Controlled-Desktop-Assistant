import os

# Assistant Configuration
ASSISTANT_NAME = "Astra"
USER_NAME = "Boss"

# Text-To-Speech (TTS) Settings
SPEECH_RATE = 175        # Words per minute (default ~200)
SPEECH_VOLUME = 1.0      # 0.0 to 1.0
PREFERRED_VOICE_INDEX = 1 # 0: Male, 1: Female (varies by OS installed voices)

# Speech-To-Text (STT) Settings
AUDIO_ENERGY_THRESHOLD = 400
AUDIO_PAUSE_THRESHOLD = 0.8
AUDIO_TIMEOUT = 5
AUDIO_PHRASE_LIMIT = 8

# AI API Key (Optional for smart conversational responses)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Quick Application Shortcuts (Windows / Cross-platform)
APPLICATIONS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "terminal": "wt.exe",
    "powershell": "powershell.exe",
    "vs code": "code",
    "code": "code",
    "paint": "mspaint.exe",
    "task manager": "taskmgr.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
}

# Web Shortcuts
WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "wikipedia": "https://www.wikipedia.org",
    "reddit": "https://www.reddit.com",
    "gmail": "https://mail.google.com",
    "stack overflow": "https://stackoverflow.com",
    "chatgpt": "https://chat.openai.com",
}
