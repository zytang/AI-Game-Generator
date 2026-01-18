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

    def is_enabled(self):
        return self.client is not None

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
        # Get top scores (descending)
        try:
            results = self.client.zrange(key, 0, limit - 1, desc=True, withscores=True)
            print(f"DEBUG: Leaderboard raw results: {results}") # Log for debugging
            
            # Clean up the parsing logic
            if not results:
                return []

            # Check structure of the first item
            first_item = results[0]

            # Scenario A: List of ScoredMember objects (typical for upstash-redis python client)
            if hasattr(first_item, 'member') and hasattr(first_item, 'score'):
                return [{"name": str(item.member), "score": float(item.score)} for item in results]

            # Scenario B: List of tuples/lists [(name, score), ...]
            if isinstance(first_item, (list, tuple)):
                 return [{"name": str(item[0]), "score": float(item[1])} for item in results]

            # Scenario C: Flat list [name, score, name, score]
            # This happens if withscores=True returns a flat list (older redis-py behavior or raw)
            # We assume it's flat if the first item is a string/bytes and the second is a number (or string number)
            formatted = []
            for i in range(0, len(results), 2):
                if i + 1 < len(results):
                    name = str(results[i])
                    score = float(results[i+1])
                    formatted.append({"name": name, "score": score})
            return formatted

        except Exception as e:
            print(f"ERROR Parsing Leaderboard: {e}")
            return []

kv_client = KVClient()
