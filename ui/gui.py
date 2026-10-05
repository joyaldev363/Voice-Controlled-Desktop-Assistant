import sys
import threading
import tkinter as tk
import customtkinter as ctk
import config
from modules.speech_engine import SpeechEngine
from modules.command_handler import CommandHandler

# Set CTk appearance and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{config.ASSISTANT_NAME} - Desktop Voice Assistant")
        self.geometry("850x650")
        self.minsize(700, 500)

        # Initialize speech engine & command dispatcher
        self.speech_engine = SpeechEngine(
            on_status_change=self.update_status,
            on_log=self.log_message
        )
        self.command_handler = CommandHandler(
            speech_engine=self.speech_engine,
            logger=self.log_message
        )

        self.is_listening_loop = False

        # Build User Interface Elements
        self._build_ui()

        # Initial Welcome Message
        self.after(500, self._initial_greeting)

    def _build_ui(self):
        # Configure layout grid (3 rows: Header, Center Log, Control Panel)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- ROW 0: HEADER BAR ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E2E")
        self.header_frame.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=f"✨ {config.ASSISTANT_NAME.upper()} ASSISTANT",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#89B4FA"
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=12, sticky="w")

        # Status Badge Pill
        self.status_pill = ctk.CTkLabel(
            self.header_frame,
            text="IDLE",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#313244",
            text_color="#A6ADC8",
            corner_radius=12,
            padx=12,
            pady=4
        )
        self.status_pill.grid(row=0, column=1, padx=20, pady=12, sticky="e")

        # --- ROW 1: TRANSCRIPT & LOG AREA ---
        self.log_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#181825")
        self.log_frame.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
        self.log_frame.grid_rowconfigure(0, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)

        self.log_box = ctk.CTkTextbox(
            self.log_frame,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="transparent",
            text_color="#CDD6F4",
            wrap="word"
        )
        self.log_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.log_box.configure(state="disabled")

        # --- ROW 2: CONTROLS & INPUT BAR ---
        self.control_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E2E")
        self.control_frame.grid(row=2, column=0, padx=15, pady=(10, 15), sticky="ew")
        self.control_frame.grid_columnconfigure(0, weight=1)

        # Quick Action Pill Buttons
        self.quick_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.quick_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")

        quick_cmds = [
            ("🕒 Time", "what time is it"),
            ("📸 Screenshot", "take screenshot"),
            ("💻 System", "system status"),
            ("🌐 Google", "open google"),
            ("▶️ YouTube", "open youtube")
        ]

        for text, cmd in quick_cmds:
            btn = ctk.CTkButton(
                self.quick_frame,
                text=text,
                width=100,
                height=26,
                font=ctk.CTkFont(size=11),
                fg_color="#313244",
                hover_color="#45475A",
                command=lambda c=cmd: self.send_text_command(c)
            )
            btn.pack(side="left", padx=5)

        # Command Entry & Action Buttons
        self.entry = ctk.CTkEntry(
            self.control_frame,
            placeholder_text="Type a voice command or click the mic button...",
            font=ctk.CTkFont(size=13),
            fg_color="#313244",
            text_color="#CDD6F4",
            height=40
        )
        self.entry.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="ew")
        self.entry.bind("<Return>", lambda event: self.send_text_command(self.entry.get()))

        self.mic_btn = ctk.CTkButton(
            self.control_frame,
            text="🎤 Speak",
            width=110,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#89B4FA",
            hover_color="#B4BEFE",
            text_color="#11111B",
            command=self.toggle_voice_input
        )
        self.mic_btn.grid(row=1, column=1, padx=(5, 10), pady=(5, 10))

    def _initial_greeting(self):
        greeting = f"Hello {config.USER_NAME}! I am {config.ASSISTANT_NAME}. Click 'Speak' or type a command to get started."
        self.speech_engine.speak(greeting)

    def log_message(self, message: str):
        """Append log messages safely to the text UI."""
        def _append():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", message + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        
        self.after(0, _append)

    def update_status(self, status: str):
        """Update status pill color and text dynamically."""
        status_map = {
            "idle": ("IDLE", "#313244", "#A6ADC8"),
            "listening": ("🎤 LISTENING...", "#A6E3A1", "#11111B"),
            "processing": ("⚡ PROCESSING...", "#FAB387", "#11111B"),
            "speaking": ("🔊 SPEAKING...", "#89B4FA", "#11111B")
        }
        
        text, bg_color, text_color = status_map.get(status.lower(), ("IDLE", "#313244", "#A6ADC8"))
        
        def _update():
            self.status_pill.configure(text=text, fg_color=bg_color, text_color=text_color)
            if status.lower() == "listening":
                self.mic_btn.configure(text="🛑 Listening", fg_color="#F38BA8")
            elif status.lower() == "idle":
                self.mic_btn.configure(text="🎤 Speak", fg_color="#89B4FA")

        self.after(0, _update)

    def toggle_voice_input(self):
        """Trigger single voice command listening in a background thread."""
        threading.Thread(target=self._voice_listen_worker, daemon=True).start()

    def _voice_listen_worker(self):
        query = self.speech_engine.listen()
        if query:
            res = self.command_handler.process_command(query)
            if res == "EXIT":
                self.after(1000, self.destroy)

    def send_text_command(self, text: str):
        """Execute text command typed in input entry or triggered by quick button."""
        query = text.strip()
        if not query:
            return
            
        self.entry.delete(0, "end")
        self.log_message(f"👤 User (Text): {query}")

        def _worker():
            res = self.command_handler.process_command(query)
            if res == "EXIT":
                self.after(1000, self.destroy)

        threading.Thread(target=_worker, daemon=True).start()

    def destroy(self):
        """Clean up threads upon application exit."""
        self.speech_engine.stop()
        super().destroy()
