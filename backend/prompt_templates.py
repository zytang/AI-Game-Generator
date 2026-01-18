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

- **GAME STATE MANAGEMENT**:
  - Track `currentLevel` (1-based) and `totalLevels` (e.g., 3).
  - **INTERMEDIATE LEVEL (currentLevel < totalLevels)**: Show "Level Complete", Score, and "Next Level" button.
  - **FINAL LEVEL (currentLevel === totalLevels)**: Show "Victory", Final Score, and the **MANDATORY SUBMISSION UI**.
  - **GAME OVER (Lost)**: Show "Game Over", Final Score, and the **MANDATORY SUBMISSION UI**.

- **DIFFICULTY CONFIGURATION**:
  - **DIFFICULTY CONFIGURATION**:
  - **Analyze the [OPTIONS] block in the prompt**:
    - If `Timed Mode: YES`:
      - Implement a **VISUAL TIMER BAR** (CSS progress bar) that shrinks from 100% to 0% width over the duration.
      - Do NOT show a countdown number (e.g. "15"). Use the bar for visual impact.
      - Set time limit (e.g., 15s/30s/60s) based on difficulty.
    - If `Timed Mode: NO`: Do NOT implement a timer. Remove "Time" from UI.
  - **INSTRUCTIONS TEXT**: In the "How to Play" section, **HARDCODE** the numbers.
    - Write: "You have 15 seconds..." NOT "You have {{time}} seconds...".
    - Write: "Score 70% to pass..." NOT "Score {{pct}}% to pass...".
    - Ensure these numbers match your Javascript logic.

- **NAVIGATION & PROGRESSION**:
  - After finishing a level, the results screen MUST show clear navigation buttons:
    - "NEXT LEVEL": Only enabled if the player passed the current level and there is a next level.
    - "REPLAY": To try the current level again.
    - "QUIT" or "MAIN MENU": To return to the level selection or start screen.
  - Implement a logical progression where levels are locked until the previous one is cleared (e.g., score > 70%).

- **ARCHITECTURE**: Use a single `gameState` object. Use generic `renderLevel()` and `showScreen()` functions.
- **VISUALS & UI**:
  - **PREMIUM AESTHETICS**: Use modern glassmorphism (backdrop-filter: blur, gradients, rounded corners).
  - **ACCESSIBILITY (CRITICAL)**: Ensure HIGH CONTRAST. Do NOT use white text on light backgrounds. Use dark text (#1a1a2e) on light cards, or white text on very dark backgrounds.
  - **TYPOGRAPHY**: Center titles, but ALWAYS left-align (`text-align: left`) lists, instructions, and body text for readability.
  - **ANIMATIONS**: Use CSS animations for rewards, transitions, and interactions.
  - **LEADERBOARD**: Ensure the global leaderboard table is beautifully styled and prominent.
  - **NAVIGATION**: Navigation buttons (Next/Replay/Quit) must be clear, styled, and always accessible in the results screen.

- **MOBILE RESPONSIVENESS (CRITICAL)**:
  - **VIEWPORT**: Must include `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
  - **TOUCH TARGETS**: Buttons must be at least 44px height/width for touch.
  - **LAYOUT**: Use CSS Grid/Flexbox to ensure content stacks vertically on small screens. Text must be readable without zooming.

- **SHARED LEADERBOARD & SUBMISSION (MANDATORY)**:
  - **SUBMISSION UI**: MUST appear on "Victory" and "Game Over" screens.
    - Input: `<input id="playerName" type="text" placeholder="Enter Name">`
    - Button: `<button onclick="submitScore()">Submit Score</button>`
  - **Behave**:
    - On click -> `fetch('/submit-score', ...)`
    - On success -> Disable button, show "Submitted!", then `fetch('/leaderboard/...')` to update table.
    - On error -> Show simple "Connection error" text.

- **NAVIGATION**:
  - **FINAL SCREENS ONLY**: The "EXIT" or "MAIN MENU" button (linking to `/`) must ONLY appear on the "Victory" or "Game Over" screens.
  - **NO CLUTTER**: Do NOT show this button during active gameplay (questions/levels).

- **SCORING SYSTEM (CRITICAL)**:
  - **STANDARD POINTS**: EXACTLY 100 points per correct answer. NO TIME BONUSES.
  - **TOTAL SCORE**: Max score = (Total Questions) * 100.
  - **NO INFLATION**: random scores like 730 are strictly forbidden.

- **LOGIC & DATA INTEGRITY**:
  - **NO DUPLICATES**: Explicitly ensure all 4 answer options for a question are UNIQUE. No repeated questions.
  - **API CONTRACT**: `/leaderboard/${{GAME_ID}}` returns a JSON ARRAY: `[{{ name: "Player", score: 100 }}, ...]`.
  - Handle empty leaderboard arrays gracefully (show "No scores yet").
  - **ERROR HANDLING**: Log fetch errors to console. If leaderboard fails, show specific error message.

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
