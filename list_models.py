import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API Key not found")
else:
    genai.configure(api_key=api_key)
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(", ".join(models))
    except Exception as e:
        print(f"Error: {e}")
