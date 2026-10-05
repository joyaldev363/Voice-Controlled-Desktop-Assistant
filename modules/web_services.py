import webbrowser
import urllib.parse
import datetime
import requests
import config

class WebServices:
    def __init__(self, logger=None):
        self.log = logger or (lambda msg: None)

    def open_website(self, name: str) -> str:
        """Open a website by name or URL."""
        name_clean = name.lower().strip()
        url = config.WEBSITES.get(name_clean, None)

        if not url:
            if not name_clean.startswith("http://") and not name_clean.startswith("https://"):
                url = f"https://www.{name_clean}.com"
            else:
                url = name_clean

        try:
            self.log(f"🌐 Opening website: {url}")
            webbrowser.open(url)
            return f"Opening {name}."
        except Exception as e:
            self.log(f"⚠️ Web browser error: {e}")
            return f"Could not open {name}."

    def search_google(self, query: str) -> str:
        """Perform Google Search in web browser."""
        if not query:
            return "What would you like me to search for on Google?"
        
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        
        try:
            self.log(f"🔍 Searching Google for: '{query}'")
            webbrowser.open(url)
            return f"Searching Google for {query}."
        except Exception as e:
            self.log(f"⚠️ Search error: {e}")
            return "Failed to perform search."

    def search_youtube(self, query: str) -> str:
        """Search or play video on YouTube."""
        if not query:
            url = "https://www.youtube.com"
            webbrowser.open(url)
            return "Opening YouTube."
            
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        try:
            self.log(f"▶️ Searching YouTube for: '{query}'")
            webbrowser.open(url)
            return f"Playing {query} on YouTube."
        except Exception as e:
            self.log(f"⚠️ YouTube search error: {e}")
            return "Failed to open YouTube."

    def get_wikipedia_summary(self, topic: str) -> str:
        """Fetch a summary from Wikipedia REST API."""
        if not topic:
            return "What topic would you like to search on Wikipedia?"

        try:
            encoded_topic = urllib.parse.quote(topic)
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_topic}"
            headers = {"User-Agent": "VoiceAssistant/1.0"}
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                extract = data.get("extract", "")
                if extract:
                    # Truncate to first 2 sentences for brevity
                    sentences = extract.split(". ")
                    summary = ". ".join(sentences[:2])
                    if not summary.endswith("."):
                        summary += "."
                    return f"According to Wikipedia: {summary}"
            
            return f"I couldn't find a Wikipedia page for {topic}."
        except Exception as e:
            self.log(f"⚠️ Wikipedia API error: {e}")
            return f"Sorry, I had trouble searching Wikipedia for {topic}."

    def get_time_and_date(self) -> str:
        """Get current formatted time and date."""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")
        return f"The current time is {time_str} on {date_str}."
