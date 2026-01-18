
import os
import sys
import uuid
import time
from dotenv import load_dotenv
from pathlib import Path
from upstash_redis import Redis

def test_leaderboard_logic():
    # 1. Load Environment Variables
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)

    url = os.getenv("KV_REST_API_URL")
    token = os.getenv("KV_REST_API_TOKEN")

    if not url or not token:
        print("❌ FAILURE: Missing Connection Credentials.")
        return

    # 2. Initialize Client
    try:
        redis = Redis(url=url, token=token)
        print("✅ Redis Client Initialized.")
    except Exception as e:
        print(f"❌ FAILURE: Client Init Failed: {e}")
        return

    # 3. Setup Test Data
    test_game_id = f"debug_game_{uuid.uuid4().hex[:8]}"
    key = f"leaderboard:{test_game_id}"
    player_name = "DebugPlayer"
    score = 1500.0

    print(f"Testing with Key: {key}")

    # 4. Test ZADD (Submit Score)
    try:
        print(f"Attempting to ZADD {player_name}: {score}...")
        # Note: upstash-redis syntax usually supports dictionary for multiple
        result = redis.zadd(key, {player_name: score})
        print(f"✅ ZADD Result: {result}") 
    except Exception as e:
        print(f"❌ FAILURE: ZADD Failed: {e}")
        return

    # 5. Test ZRANGE (Get Leaderboard)
    try:
        print("Attempting to ZRANGE...")
        # Get raw results first
        raw_results = redis.zrange(key, 0, -1, desc=True, withscores=True)
        print(f"✅ Raw ZRANGE Result: {raw_results}")
        print(f"   Type: {type(raw_results)}")
        if raw_results:
             print(f"   First Item Type: {type(raw_results[0])}")
             print(f"   First Item Content: {raw_results[0]}")
    except Exception as e:
        print(f"❌ FAILURE: ZRANGE Failed: {e}")

if __name__ == "__main__":
    test_leaderboard_logic()
