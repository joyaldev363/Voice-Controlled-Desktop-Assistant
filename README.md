# Voice-Controlled Desktop Assistant (Astra)

A Python-based Voice-Controlled Desktop Assistant that enables hands-free computer control using speech recognition, text-to-speech feedback, system automation, web integration, and AI-driven conversational capabilities.

---

## Features

- **Voice & Text Input**: Control your desktop via microphone voice commands or type commands directly in the GUI/CLI.
- **Text-to-Speech (TTS)**: Offline, low-latency audio feedback using `pyttsx3`.
- **Desktop System Automation**:
  - Open/close desktop applications (Notepad, Calculator, VS Code, Browser, Command Prompt, File Explorer, etc.).
  - Volume control (set volume percentage).
  - Take screen screenshots saved directly to your Pictures folder.
  - Check real-time CPU, RAM, and Battery usage.
  - Lock workstation screen.
- **Web Services & Media Integration**:
  - Open popular websites (Google, YouTube, GitHub, Wikipedia, Reddit, Gmail).
  - Perform instant Google searches.
  - Search and play music/videos on YouTube.
  - Fetch instant Wikipedia summaries.
  - Query current local time and date.
- **AI Conversational Intelligence**: Integrated fallback with Google Gemini API (`gemini-2.5-flash`) for smart conversational answers.
- **Modern Dark Desktop GUI**: Powered by `CustomTkinter` with live status indicators (`LISTENING`, `PROCESSING`, `SPEAKING`, `IDLE`), transcript logs, and quick action buttons.

---

## Project Structure

```
Voice-Controlled Desktop Assistant/
├── config.py               # Global settings (voice speed, default apps, hotkeys, API keys)
├── main.py                 # Application entry point (GUI / CLI launcher)
├── requirements.txt        # Python package dependencies
├── README.md               # Documentation and setup guide
├── modules/
│   ├── __init__.py
│   ├── speech_engine.py    # Speech Recognition & Text-to-Speech handling
│   ├── command_handler.py  # Intent parser and command router
│   ├── app_control.py      # System apps, volume, screenshots, & resource metrics
│   ├── web_services.py     # Web search, YouTube, Wikipedia, & date/time
│   └── ai_assistant.py     # Google Gemini AI fallback integration
└── ui/
    ├── __init__.py
    └── gui.py              # CustomTkinter Graphical User Interface
```

---

## Getting Started

### 1. Environment Setup
Open your terminal inside the project directory and create a virtual environment:

```bash
# Navigate to project directory
cd "e:\Python\Voice-Controlled Desktop Assistant"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows Command Prompt:
# .\venv\Scripts\activate.bat
```

### 2. Install Dependencies
Install all required libraries using `pip`:

```bash
pip install -r requirements.txt
```

> **Note for PyAudio on Windows**: If `pip install -r requirements.txt` reports an error building `pyaudio`, install `pyaudiowpatch`:
> ```bash
> pip install pyaudiowpatch
> ```

---

## Running the Assistant

### Launch GUI Mode (Default)
```bash
python main.py
```

### Launch CLI Mode (Command Line)
```bash
python main.py --cli
```

---

## Voice Command Reference

| Category | Example Voice Commands | Action |
| :--- | :--- | :--- |
| **System Info** | *"What time is it?"*, *"What is today's date?"* | Speaks time and date |
| **System Status** | *"Check system status"*, *"CPU usage"*, *"Battery level"* | Reports CPU, RAM %, and battery |
| **Applications** | *"Open Notepad"*, *"Launch Calculator"*, *"Close Notepad"* | Opens or closes application |
| **Web Browsing** | *"Open Google"*, *"Open YouTube"*, *"Open GitHub"* | Opens site in web browser |
| **Web Search** | *"Search Google for Python tutorials"*, *"Google machine learning"* | Opens Google search results |
| **Media / Music** | *"Play Lofi Beats on YouTube"*, *"YouTube classical music"* | Opens YouTube search results |
| **Wikipedia** | *"Who is Albert Einstein?"*, *"What is Quantum Computing?"* | Reads a 2-sentence Wikipedia summary |
| **Utilities** | *"Take a screenshot"*, *"Capture screen"* | Saves screenshot in Pictures folder |
| **Volume Control** | *"Set volume to 50"*, *"Set volume to 80"* | Adjusts system master volume level |
| **Workstation** | *"Lock computer"*, *"Lock screen"* | Locks Windows workstation |
| **AI Q&A** | *"Why is the sky blue?"*, *"Tell me a fun fact"* | Answers using Gemini AI or fallback |
| **Exit** | *"Goodbye"*, *"Exit"*, *"Stop listening"* | Closes the assistant application |

---

## Optional Google Gemini AI Configuration

To enable smart conversational AI answers:
1. Obtain an API Key from [Google AI Studio](https://aistudio.google.com/).
2. Set the environment variable in your terminal:
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your_api_key_here"
   ```
   Or paste your key into `config.py`:
   ```python
   GEMINI_API_KEY = "your_api_key_here"
   ```
