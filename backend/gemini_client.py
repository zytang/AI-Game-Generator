import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash", 
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 16384,
            }
        )

    def generate(self, prompt: str) -> str:
        """
        Sends prompt to Gemini and returns raw text output.
        """
        try:
            response = self.model.generate_content(prompt)
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed using {self.model.model_name}: {str(e)}")

        if not response:
            raise RuntimeError("Empty response object from Gemini")

        # Check for safety blocks or other finish reasons
        if response.candidates:
            finish_reason = response.candidates[0].finish_reason
            if finish_reason != 1:  # 1 is STOP (Natural stop)
                print(f"WARNING: Game generation stopped prematurely. Reason: {finish_reason}")
            
            # Log token usage if available
            try:
                print(f"Tokens generated: {response.usage_metadata.candidates_token_count}")
            except:
                pass

        try:
            text = response.text
            if not text:
                raise RuntimeError("Response text is empty")
            return text.strip()
        except ValueError:
            # This often happens when the model blocks the output due to safety
            reason = "Unknown"
            if response.prompt_feedback:
                reason = str(response.prompt_feedback)
            raise RuntimeError(f"Gemini blocked the response. Feedback: {reason}")
        except Exception as e:
            raise RuntimeError(f"Error accessing Gemini response text: {str(e)}")
