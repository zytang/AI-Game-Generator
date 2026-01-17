def build_game_generation_prompt(user_prompt: str) -> str:
    """
    Builds a strict prompt for a shared leaderboard educational game with navigation.
    """

    final_prompt = f"""
You are an expert educational game developer.
Your task is to generate a COMPLETE, VALID, SELF-CONTAINED HTML FILE.

- **SHARED LEADERBOARD**: The game MUST support a global shared leaderboard.
  - When the game finishes, prompt the user for their name if they are in the top scores.
  - Use `fetch('/submit-score', ...)` to send `{{ game_id, player_name, score }}`.
  - Use `fetch('/leaderboard/${{GAME_ID}}')` to retrieve the current top 10 scores.
  - IMPORTANT: Use a placeholder `const GAME_ID = "[[GAME_ID]]";` at the top of your script. This will be replaced by the server.

- **NAVIGATION & PROGRESSION**:
  - After finishing a level, the results screen MUST show clear navigation buttons:
    - "NEXT LEVEL": Only enabled if the player passed the current level and there is a next level.
    - "REPLAY": To try the current level again.
    - "QUIT" or "MAIN MENU": To return to the level selection or start screen.
  - Implement a logical progression where levels are locked until the previous one is cleared (e.g., score > 70%).

- **ARCHITECTURE**: Use a single `gameState` object. Use generic `renderLevel()` and `showScreen()` functions.
- **VISUALS & UI**:
  - **PREMIUM AESTHETICS**: Use modern glassmorphism (backdrop-filter: blur, gradients, rounded corners).
  - **ANIMATIONS**: Use CSS animations for rewards, transitions, and interactions.
  - **LEADERBOARD**: Ensure the global leaderboard table is beautifully styled and prominent.
  - **NAVIGATION**: Navigation buttons (Next/Replay/Quit) must be clear, styled, and always accessible in the results screen.

- **OPTIMIZATION & ARCHITECTURE**:
  - Use a "Question Generator Engine" (functions) instead of hardcoding massive data arrays.
  - Structure the code cleanly with a single `gameState` object.
  - Example: `function generateQuestions(level) {{ ... return questions; }}`

**STRICT FORMATTING**: 
1. Output ONLY raw HTML (no markdown).
2. The JavaScript MUST be the LAST tag in the <body>.
3. The JavaScript MUST contain a single `initGame()` call at the bottom.

USER GAME REQUEST:
{user_prompt}

CRITICAL: Return ONLY complete, valid HTML ending in </html>. No conversational filler.
"""
    return final_prompt.strip()
