from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os
import uuid

from backend.gemini_client import GeminiClient
from backend.prompt_templates import build_game_generation_prompt
from backend.utils import clean_html_output

# Reload triggered for model version update
app = FastAPI(title="AI Game Generator")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Handle Vercel's read-only file system
if os.environ.get("VERCEL"):
    GENERATED_GAMES_DIR = "/tmp"
else:
    GENERATED_GAMES_DIR = os.path.join(BASE_DIR, "generated_games")

os.makedirs(GENERATED_GAMES_DIR, exist_ok=True)

# Static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
@app.get("/games/{filename}")
def serve_game(filename: str):
    # Extract ID. Filename format: game_{id}.html
    game_id = filename.replace("game_", "").replace(".html", "")
    
    # 1. Try Redis first (Persistent Storage)
    content = kv_client.get_game(game_id)
    if content:
        # Redis might return bytes or string depending on client config, ensure string for HTMLResponse
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        return HTMLResponse(content=content)

    # 2. Fallback to File System (Ephemeral)
    file_path = os.path.join(GENERATED_GAMES_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Game not found or expired. Please generate a new one.")

    return FileResponse(
        file_path,
        media_type="text/html",
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
        }
    )


gemini_client = None

def get_gemini_client():
    global gemini_client
    if gemini_client is None:
        gemini_client = GeminiClient()
    return gemini_client


class GameRequest(BaseModel):
    prompt: str
    difficulty: str = "medium"
    is_timed: bool = True


@app.get("/", response_class=HTMLResponse)
def read_root():
    # In Vercel, the file structure might be flattened or different.
    # We should rely on standard relative paths from the project root.
    index_path = os.path.join(BASE_DIR, "static", "index.html")
    if not os.path.exists(index_path):
        # Fallback for some serverless structures
        index_path = "static/index.html"
    
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>AI Game Generator</h1>
        <p>Frontend file not found. Please ensure static/index.html exists.</p>
        """


from backend.kv_client import kv_client

@app.post("/generate-game")
def generate_game(request: GameRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        # Build strict prompt with options
        prompt_with_options = request.prompt
        prompt_with_options += f"\n\n[OPTIONS]\nDifficulty: {request.difficulty}\nTimed Mode: {'YES' if request.is_timed else 'NO'}"
        
        full_prompt = build_game_generation_prompt(prompt_with_options)

        # Generate HTML from Gemini
        client = get_gemini_client()
        raw_html = client.generate(full_prompt)

        # Clean output defensively
        clean_html = clean_html_output(raw_html)
        
        # Inject Game ID for the shared leaderboard
        game_id = uuid.uuid4().hex
        clean_html = clean_html.replace("[[GAME_ID]]", game_id)

        # Inject Metadata for Import/Edit features
        import json
        from datetime import datetime
        metadata = {
            "prompt": request.prompt,
            "difficulty": request.difficulty,
            "is_timed": request.is_timed,
            "generated_at": datetime.now().isoformat()
        }
        # Securely serialize JSON and inject as a script tag
        metadata_script = f'\n<!-- GENERATED METADATA -->\n<script id="game-metadata" type="application/json">\n{json.dumps(metadata, indent=2)}\n</script>'
        
        if "</body>" in clean_html:
            clean_html = clean_html.replace("</body>", f"{metadata_script}\n</body>")
        else:
            clean_html += metadata_script

        # Save game file
        filename = f"game_{game_id}.html"
        file_path = os.path.join(GENERATED_GAMES_DIR, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(clean_html)

        # Save to Redis (Persistent Storage)
        try:
            kv_client.save_game(game_id, clean_html)
            print(f"Game saved to Redis: {game_id}")
        except Exception as e:
            print(f"Warning: Failed to save to Redis: {e}")

        return JSONResponse({
            "game_url": f"/games/{filename}",
            "game_id": game_id
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PublishRequest(BaseModel):
    html_content: str

@app.post("/publish-game")
def publish_game(request: PublishRequest):
    try:
        html_content = request.html_content
        
        # Basic validation
        if "<!DOCTYPE html>" not in html_content:
             raise HTTPException(status_code=400, detail="Invalid HTML content")

        # Generate new ID for the published version
        game_id = uuid.uuid4().hex
        
        # We might want to inject the NEW game_id into the HTML so the leaderboard works for this new URL?
        # The imported game has the OLD game_id frozen in `const GAME_ID = "..."`.
        # IF we don't update it, it will share the leaderboard with the original game.
        # This is actually DESIRABLE (preserving history).
        # However, if the user "forked" it effectively, maybe they want a new one?
        # User said "publish it", enabling students to play. 
        # If I import Game A (ID: 123), and publish it, it becomes Game B.
        # If Game B keeps ID: 123, it writes to Leaderboard 123. This seems correct for "publishing" the same game.
        # If I want a NEW leaderboard, I should regenerate.
        # But wait, if I technically "publish" it, I am creating a new file `game_{new_id}.html`.
        # If the JS inside says `const GAME_ID = "old_id"`, it will read/write to "old_id".
        # This is fine. The files are just different access points to the same logic/data.
        
        # SAVE FILE
        filename = f"game_{game_id}.html"
        file_path = os.path.join(GENERATED_GAMES_DIR, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # SAVE TO REDIS
        try:
            # 7 Days Retention (604800 seconds) for published games
            kv_client.save_game(game_id, html_content, ttl=604800)
            print(f"Published game saved to Redis: {game_id}")
        except Exception as e:
            print(f"Warning: Failed to save published game to Redis: {e}")

        return JSONResponse({
            "game_url": f"/games/{filename}",
            "game_id": game_id
        })

    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

class ScoreSubmission(BaseModel):
    game_id: str
    player_name: str
    score: float

@app.post("/submit-score")
def submit_score(submission: ScoreSubmission):
    if not kv_client.is_enabled():
        raise HTTPException(status_code=503, detail="Leaderboard service unavailable (Missing Credentials)")

    try:
        kv_client.submit_score(submission.game_id, submission.player_name, submission.score)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Score submission failed: {str(e)}")

@app.get("/leaderboard/{game_id}")
def get_leaderboard(game_id: str):
    try:
        return kv_client.get_leaderboard(game_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Leaderboard retrieval failed: {str(e)}")
