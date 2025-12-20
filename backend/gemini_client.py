import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 8192,
            }
        )

    def generate(self, prompt: str) -> str:
        """
        Sends prompt to Gemini and returns raw text output.
        """
        response = self.model.generate_content(prompt)

        if not response or not response.text:
            raise RuntimeError("Empty response from Gemini")

        return response.text.strip()
