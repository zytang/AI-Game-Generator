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
    file_path = os.path.join(GENERATED_GAMES_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Game not found")

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
        # Build strict prompt
        full_prompt = build_game_generation_prompt(request.prompt)

        # Generate HTML from Gemini
        client = get_gemini_client()
        raw_html = client.generate(full_prompt)

        # Clean output defensively
        clean_html = clean_html_output(raw_html)
        
        # Inject Game ID for the shared leaderboard
        game_id = uuid.uuid4().hex
        clean_html = clean_html.replace("[[GAME_ID]]", game_id)

        # Save game file
        filename = f"game_{game_id}.html"
        file_path = os.path.join(GENERATED_GAMES_DIR, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(clean_html)

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
