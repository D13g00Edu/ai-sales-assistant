import google.generativeai as genai
from app.core.config import get_settings
from app.core.exceptions import SecurityError

class GeminiClient:
    def __init__(self):
        self.s = get_settings()
        if self.s.GEMINI_API_KEY: genai.configure(api_key=self.s.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.s.GEMINI_MODEL)

    def prompt(self, txt: str) -> str:
        if not self.s.GEMINI_API_KEY: raise SecurityError('GEMINI API Key is missing')
        return self.model.generate_content(txt).text.strip()
