import sys
import threading
import queue
import time
import pythoncom

# Compatibility patch for PyAudio / PyAudioWPatch on Windows
try:
    import pyaudio
except ImportError:
    try:
        import pyaudiowpatch as pyaudio
        sys.modules['pyaudio'] = pyaudio
    except ImportError:
        pass

import speech_recognition as sr
import pyttsx3
import config

class SpeechEngine:
    def __init__(self, on_status_change=None, on_log=None):
        self.on_status_change = on_status_change or (lambda status: None)
        self.on_log = on_log or (lambda msg: None)
        
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = config.AUDIO_ENERGY_THRESHOLD
        self.recognizer.pause_threshold = config.AUDIO_PAUSE_THRESHOLD
        self.recognizer.dynamic_energy_threshold = True

        self.tts_queue = queue.Queue()
        self.is_speaking = False
        self._stop_tts_thread = False
        
        # Start background TTS worker thread for thread safety
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()

    def _tts_worker(self):
        """Dedicated background thread for pyttsx3 to prevent thread blocking/crashes."""
        try:
            pythoncom.CoInitialize()
        except Exception:
            pass

        try:
            while not self._stop_tts_thread:
                try:
                    text = self.tts_queue.get(timeout=0.5)
                    if text:
                        self.is_speaking = True
                        self.on_status_change("speaking")
                        self.on_log(f"🤖 {config.ASSISTANT_NAME}: {text}")
                        
                        try:
                            engine = pyttsx3.init()
                            engine.setProperty('rate', config.SPEECH_RATE)
                            engine.setProperty('volume', config.SPEECH_VOLUME)
                            
                            voices = engine.getProperty('voices')
                            if voices and len(voices) > config.PREFERRED_VOICE_INDEX:
                                engine.setProperty('voice', voices[config.PREFERRED_VOICE_INDEX].id)
                            
                            engine.say(text)
                            engine.runAndWait()
                            engine.stop()
                        except Exception as e:
                            print(f"TTS Error: {e}")
                        finally:
                            self.is_speaking = False
                            self.on_status_change("idle")
                            self.tts_queue.task_done()
                except queue.Empty:
                    continue
        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass

    def speak(self, text: str, wait: bool = False):
        """Queue text for speech output."""
        if not text:
            return
        self.tts_queue.put(text)
        if wait:
            self.tts_queue.join()

    def listen(self) -> str:
        """Capture audio from microphone and perform Speech-To-Text."""
        self.on_status_change("listening")
        self.on_log("🎤 Listening for voice command...")

        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=config.AUDIO_TIMEOUT,
                    phrase_time_limit=config.AUDIO_PHRASE_LIMIT
                )

            self.on_status_change("processing")
            self.on_log("⚡ Processing speech...")

            query = self.recognizer.recognize_google(audio, language="en-US")
            self.on_log(f"👤 User: {query}")
            self.on_status_change("idle")
            return query.strip()

        except AttributeError as e:
            if "pyaudio" in str(e).lower() or "microphone" in str(e).lower():
                self.on_log("⚠️ PyAudio is missing. Install with 'pip install pyaudio' to enable mic input. You can type commands below!")
                self.speak("PyAudio is not installed for microphone input. You can type commands in the text box.")
            else:
                self.on_log(f"⚠️ Speech Error: {e}")
            self.on_status_change("idle")
            return ""
        except sr.WaitTimeoutError:
            self.on_log("⚠️ Listening timed out. No speech detected.")
            self.on_status_change("idle")
            return ""
        except sr.UnknownValueError:
            self.on_log("⚠️ Speech was recognized, but could not understand the audio.")
            self.speak("Sorry, I could not understand that. Could you please repeat?")
            self.on_status_change("idle")
            return ""
        except sr.RequestError as e:
            self.on_log(f"⚠️ Speech Recognition Service Error: {e}")
            self.speak("Speech recognition service is currently unavailable.")
            self.on_status_change("idle")
            return ""
        except Exception as e:
            err_msg = str(e)
            if "pyaudio" in err_msg.lower() or "could not find pyaudio" in err_msg.lower():
                self.on_log("⚠️ PyAudio missing. Run 'pip install pyaudio' in terminal. Typing commands works!")
                self.speak("PyAudio is missing. Please install PyAudio or type commands in the text box.")
            else:
                self.on_log(f"⚠️ Microphone or Speech Error: {e}")
            self.on_status_change("idle")
            return ""

    def stop(self):
        self._stop_tts_thread = True
