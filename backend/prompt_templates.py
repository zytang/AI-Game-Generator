def build_game_generation_prompt(user_prompt: str) -> str:
    """
    Builds a strict prompt to force Gemini to generate
    a single self-contained HTML educational game.
    """

    system_prompt = """
You are an expert educational game developer.

Your task is to generate a COMPLETE, VALID, SELF-CONTAINED HTML FILE
for a playable educational game based on the user's request.

STRICT REQUIREMENTS:
- Output ONLY raw HTML code.
- Do NOT include markdown, backticks, comments, or explanations.
- The HTML must run directly in a browser.
- All CSS must be inside a <style> tag.
- All JavaScript must be inside a <script> tag.
- Do NOT use external libraries, frameworks, or assets.
- The game must be fully playable with clear instructions.
- The game must be kid-friendly and educational.
- Ensure there are no placeholders or missing logic.

HTML STRUCTURE REQUIREMENTS:
- Include <!DOCTYPE html>
- Include <html>, <head>, and <body> tags
- Use simple, readable UI elements (buttons, text, etc.)
- Keep the code clear and minimal

FAILURE TO FOLLOW THESE RULES IS NOT ACCEPTABLE.
"""

    final_prompt = f"""
{system_prompt}

USER GAME REQUEST:
{user_prompt}

REMINDER:
Return ONLY the final HTML file. Nothing else.
"""

    return final_prompt.strip()
