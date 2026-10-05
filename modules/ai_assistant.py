import os
import config

class AIAssistant:
    def __init__(self, logger=None):
        self.log = logger or (lambda msg: None)
        self.client = None
        self._init_client()

    def _init_client(self):
        api_key = config.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=api_key)
                self.log("✨ Google Gemini AI Engine Initialized Successfully.")
            except Exception as e:
                self.log(f"⚠️ Could not initialize Gemini API: {e}")
                self.client = None

    def ask(self, query: str) -> str:
        """Send prompt to Gemini AI or provide intelligent fallback response."""
        if not query:
            return "How can I help you?"

        if self.client:
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Respond in 1-2 concise, conversational sentences suitable for speech output: {query}"
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                self.log(f"⚠️ Gemini API query error: {e}")

        # Intelligent Fallback matching
        q = query.lower()
        if "who are you" in q or "your name" in q:
            return f"I am {config.ASSISTANT_NAME}, your voice-controlled desktop assistant."
        elif "how are you" in q:
            return "I am functioning at peak efficiency! How can I assist you today?"
        elif "what can you do" in q or "help" in q:
            return ("I can open applications, search Google and YouTube, read Wikipedia summaries, "
                    "check system status, take screenshots, adjust volume, tell the time, and answer your questions.")
        
        return f"I heard '{query}'. For complex questions, you can configure a Gemini API key in config.py."
