from backend.utils import clean_html_output
import os

game_path = r"c:\Users\ztang\.gemini\AI-Game-Generator\generated_games\game_3f971e2cda0d4b358376fff1f0580d12.html"

with open(game_path, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Original length: {len(content)}")
fixed_content = clean_html_output(content)
print(f"Fixed length: {len(fixed_content)}")

fixed_path = game_path.replace(".html", "_fixed.html")
with open(fixed_path, "w", encoding="utf-8") as f:
    f.write(fixed_content)

print(f"Saved to {fixed_path}")
