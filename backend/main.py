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

app = FastAPI(title="AI Game Generator")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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


gemini_client = GeminiClient()


class GameRequest(BaseModel):
    prompt: str


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open(os.path.join(BASE_DIR, "static", "index.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.post("/generate-game")
def generate_game(request: GameRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        # Build strict prompt
        full_prompt = build_game_generation_prompt(request.prompt)

        # Generate HTML from Gemini
        raw_html = gemini_client.generate(full_prompt)

        # Clean output defensively
        clean_html = clean_html_output(raw_html)

        # Save game file
        filename = f"game_{uuid.uuid4().hex}.html"
        file_path = os.path.join(GENERATED_GAMES_DIR, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(clean_html)

        return JSONResponse({
            "game_url": f"/games/{filename}"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
