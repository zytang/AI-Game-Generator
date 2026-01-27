from backend.prompt_templates import build_game_generation_prompt

prompt = build_game_generation_prompt("Test Game")
with open("debug_prompt_output.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

print("Prompt written to debug_prompt_output.txt")
