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
            # upstash-redis might not support desc=True in zrange. Use zrevrange instead.
            results = self.client.zrevrange(key, 0, limit - 1, withscores=True)
            print(f"DEBUG: Leaderboard raw results: {results}") # Log for debugging
            
            # Clean up the parsing logic
            if not results:
                return []

            # Check structure of the first item
            first_item = results[0]
            print(f"DEBUG: First item type: {type(first_item)}, content: {first_item}")

            # Scenario A: List of objects (ScoredMember from upstash-redis)
            # We access .member and .score directly.
            if hasattr(first_item, 'member') and hasattr(first_item, 'score'):
                return [{"name":str(item.member), "score": float(item.score)} for item in results]

            # Scenario B: List of dictionaries (JSON response sometimes)
            if isinstance(first_item, dict):
                 # Try to find common keys
                 name = first_item.get('member') or first_item.get('name') or first_item.get('value')
                 score = first_item.get('score')
                 if name is not None and score is not None:
                     return [{"name": str(item.get('member', item.get('name'))), "score": float(item.get('score', 0))} for item in results]

            # Scenario C: List of tuples/lists [(name, score), ...]
            if isinstance(first_item, (list, tuple)):
                 return [{"name": str(item[0]), "score": float(item[1])} for item in results]

            # Scenario D: Flat list [name, score, name, score]
            # This is the "raw" Redis response for withscores=True
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

    def save_game(self, game_id: str, html_content: str, ttl: int = 86400):
        """Saves generated game HTML to Redis with 24h expiration."""
        if not self.client:
            return False
        key = f"game_html:{game_id}"
        return self.client.set(key, html_content, ex=ttl)

    def get_game(self, game_id: str):
        """Retrieves game HTML from Redis."""
        if not self.client:
            return None
        key = f"game_html:{game_id}"
        return self.client.get(key)

kv_client = KVClient()
