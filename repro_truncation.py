from backend.gemini_client import GeminiClient
from backend.prompt_templates import build_game_generation_prompt
import sys

def test_generation():
    prompt = "Create a game for active learning for students in the Introduction to Information Systems class at the college level."
    client = GeminiClient()
    full_prompt = build_game_generation_prompt(prompt)
    print(f"Sending prompt of length {len(full_prompt)}")
    try:
        raw_html = client.generate(full_prompt)
        print(f"Received output of length {len(raw_html)}")
        
        with open("generation_debug.log", "w", encoding="utf-8") as log:
            log.write(f"Output length: {len(raw_html)}\n")
            log.write(f"End of output: {raw_html[-200:]}\n")
        
        with open("repro_output.html", "w", encoding="utf-8") as f:
            f.write(raw_html)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_generation()
