import sys
import argparse
import config
from modules.speech_engine import SpeechEngine
from modules.command_handler import CommandHandler
from ui.gui import AssistantGUI

def run_cli():
    print(f"==================================================")
    print(f" 🎙️ {config.ASSISTANT_NAME} - Voice Controlled Desktop Assistant (CLI)")
    print(f"==================================================")
    
    def log(msg):
        print(msg)

    speech_engine = SpeechEngine(on_log=log)
    handler = CommandHandler(speech_engine=speech_engine, logger=log)

    print(f"Say 'exit' or press Ctrl+C to quit.\n")
    speech_engine.speak(f"Hello {config.USER_NAME}, I am {config.ASSISTANT_NAME}. How can I help you today?")

    try:
        while True:
            mode = input("\nPress [Enter] to speak, type a command, or type 'exit': ").strip()
            if mode.lower() in ["exit", "quit"]:
                break
                
            if mode:
                # User typed a text command
                result = handler.process_command(mode)
            else:
                # User pressed enter -> trigger microphone speech listening
                query = speech_engine.listen()
                if query:
                    result = handler.process_command(query)
                else:
                    result = None
                    
            if result == "EXIT":
                break
    except KeyboardInterrupt:
        print("\nExiting Assistant...")
    finally:
        speech_engine.stop()

def run_gui():
    app = AssistantGUI()
    app.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voice-Controlled Desktop Assistant")
    parser.add_argument("--cli", action="store_true", help="Run in Command Line Interface (CLI) mode instead of GUI")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        run_gui()
