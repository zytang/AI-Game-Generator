
import requests
import json
import os

BASE_URL = "http://localhost:8000"

def test_generation_and_metadata():
    print("Testing Generation API with Metadata...")
    
    payload = {
        "prompt": "Test Game for Metadata",
        "difficulty": "hard",
        "is_timed": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate-game", json=payload)
        response.raise_for_status()
        
        data = response.json()
        print(f"Success! Game URL: {data['game_url']}")
        
        # Download the game
        game_id = data["game_id"]
        game_url = f"{BASE_URL}{data['game_url']}"
        
        game_response = requests.get(game_url)
        content = game_response.text
        
        # Verify Metadata
        if 'id="game-metadata"' in content:
            print("✅ Metadata Script Tag Found")
        else:
            print("❌ Metadata Script Tag MISSING")
            
        if '"difficulty": "hard"' in content:
             print("✅ Metadata Content Verified (Difficulty: Hard)")
        else:
             print("❌ Metadata Content Incorrect")

    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(e.response.text)

if __name__ == "__main__":
    test_generation_and_metadata()
