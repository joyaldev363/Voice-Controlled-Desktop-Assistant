import re
import config
from modules.app_control import AppController
from modules.web_services import WebServices
from modules.ai_assistant import AIAssistant

class CommandHandler:
    def __init__(self, speech_engine, logger=None):
        self.speech_engine = speech_engine
        self.log = logger or (lambda msg: None)
        
        self.app_control = AppController(logger=self.log)
        self.web_services = WebServices(logger=self.log)
        self.ai_assistant = AIAssistant(logger=self.log)

    def process_command(self, query: str) -> str:
        """Parse text query and execute corresponding system/web/AI command."""
        if not query:
            return ""

        raw_query = query
        q = query.lower().strip()

        # Remove assistant wake word if present at start
        wake_words = [config.ASSISTANT_NAME.lower(), "hey assistant", "assistant", "jarvis", "computer"]
        for wake in wake_words:
            if q.startswith(wake):
                q = q[len(wake):].strip()
                break

        if not q:
            response = f"Yes, {config.USER_NAME}? I am listening."
            self.speech_engine.speak(response)
            return response

        # 1. Exit / Goodbye commands
        if any(cmd in q for cmd in ["exit", "shutdown assistant", "bye", "goodbye", "stop listening"]):
            response = f"Goodbye {config.USER_NAME}! Have a great day."
            self.speech_engine.speak(response, wait=True)
            return "EXIT"

        # 2. Time & Date
        if any(phrase in q for phrase in ["time", "date", "what time", "today's date"]):
            response = self.web_services.get_time_and_date()
            self.speech_engine.speak(response)
            return response

        # 3. System Status (CPU, RAM, Battery)
        if any(phrase in q for phrase in ["system status", "cpu", "ram", "battery", "performance"]):
            response = self.app_control.get_system_status()
            self.speech_engine.speak(response)
            return response

        # 4. Screenshot
        if "screenshot" in q or "capture screen" in q:
            response = self.app_control.take_screenshot()
            self.speech_engine.speak(response)
            return response

        # 5. Lock Workstation
        if "lock" in q and ("pc" in q or "computer" in q or "screen" in q or "workstation" in q):
            response = self.app_control.lock_workstation()
            self.speech_engine.speak(response)
            return response

        # 6. Volume Control
        if "volume" in q:
            vol_match = re.search(r'\b(\d+)\b', q)
            if vol_match:
                level = int(vol_match.group(1))
                response = self.app_control.set_volume(level)
            else:
                response = "Please specify a volume percentage level between 0 and 100."
            self.speech_engine.speak(response)
            return response

        # 7. Open Application
        if q.startswith("open app") or q.startswith("open application") or q.startswith("launch"):
            app_name = re.sub(r'^(open app|open application|launch)\s+', '', q)
            response = self.app_control.open_application(app_name)
            self.speech_engine.speak(response)
            return response

        # Check direct website or application match
        for site_key in config.WEBSITES.keys():
            if q == f"open {site_key}" or q == f"launch {site_key}":
                response = self.web_services.open_website(site_key)
                self.speech_engine.speak(response)
                return response

        for app_key in config.APPLICATIONS.keys():
            if q == f"open {app_key}" or q == f"launch {app_key}":
                response = self.app_control.open_application(app_key)
                self.speech_engine.speak(response)
                return response

        if q.startswith("open "):
            target = q[5:].strip()
            # If target looks like a website domain or URL
            if "." in target or target in config.WEBSITES:
                response = self.web_services.open_website(target)
            else:
                response = self.app_control.open_application(target)
            self.speech_engine.speak(response)
            return response

        # 8. Close Application
        if q.startswith("close "):
            app_name = q[6:].strip()
            response = self.app_control.close_application(app_name)
            self.speech_engine.speak(response)
            return response

        # 9. Search YouTube / Play Music
        if q.startswith("play ") or "search youtube for" in q or "youtube " in q:
            search_query = re.sub(r'^(play|search youtube for|youtube)\s+', '', q)
            response = self.web_services.search_youtube(search_query)
            self.speech_engine.speak(response)
            return response

        # 10. Wikipedia Lookup
        if q.startswith("who is ") or q.startswith("what is ") or q.startswith("wikipedia "):
            topic = re.sub(r'^(who is|what is|wikipedia)\s+', '', q)
            # Check if it's asking for current time/date or system status before wiki
            if not any(k in topic for k in ["time", "date", "cpu", "ram"]):
                response = self.web_services.get_wikipedia_summary(topic)
                self.speech_engine.speak(response)
                return response

        # 11. Google Search
        if q.startswith("search google for ") or q.startswith("google ") or q.startswith("search for "):
            search_term = re.sub(r'^(search google for|google|search for)\s+', '', q)
            response = self.web_services.search_google(search_term)
            self.speech_engine.speak(response)
            return response

        # 12. General AI Conversational Query (Fallback)
        response = self.ai_assistant.ask(raw_query)
        self.speech_engine.speak(response)
        return response
