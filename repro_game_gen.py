
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.gemini_client import GeminiClient
from backend.prompt_templates import build_game_generation_prompt
from backend.utils import clean_html_output

def generate_repro_game():
    # Load env
    env_path = Path("backend/.env")
    load_dotenv(dotenv_path=env_path)

    prompt = "Create a quiz about Solar System. 3 levels. Timed Mode: YES."
    
    print("Building prompt...")
    full_prompt = build_game_generation_prompt(prompt)
    
    print("Generating game with Gemini...")
    client = GeminiClient()
    raw_html = client.generate(full_prompt)
    
    clean_html = clean_html_output(raw_html)
    
    # Inject dummy GAME_ID
    clean_html = clean_html.replace("[[GAME_ID]]", "debug_repro_id")
    
    output_path = "repro_game_debug.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(clean_html)
    
    print(f"✅ Game generated at: {output_path}")

if __name__ == "__main__":
    generate_repro_game()
