import os
from upstash_redis import Redis
from dotenv import load_dotenv
from pathlib import Path

# Load env from parent dir if needed
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

class KVClient:
    def __init__(self):
        # Try Vercel KV vars first, then generic Upstash vars
        url = os.getenv("KV_REST_API_URL") or os.getenv("UPSTASH_REDIS_REST_URL")
        token = os.getenv("KV_REST_API_TOKEN") or os.getenv("UPSTASH_REDIS_REST_TOKEN")
        
        if not url or not token:
            self.client = None
            print("WARNING: Vercel KV credentials missing. Global leaderboard will be disabled.")
        else:
            self.client = Redis(url=url, token=token)

    def submit_score(self, game_id: str, name: str, score: float):
        if not self.client:
            return None
        
        # Use a sorted set for leaderboard
        key = f"leaderboard:{game_id}"
        return self.client.zadd(key, {name: score})

    def get_leaderboard(self, game_id: str, limit: int = 10):
        if not self.client:
            return []
        
        key = f"leaderboard:{game_id}"
        # Get top scores (descending)
        results = self.client.zrange(key, 0, limit - 1, desc=True, withscores=True)
        
        # Format for frontend: [{"name": "...", "score": ...}, ...]
        return [{"name": r[0], "score": float(r[1])} for r in results]

kv_client = KVClient()
