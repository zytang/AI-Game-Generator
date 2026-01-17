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
        # Get top scores (descending)
        try:
            results = self.client.zrange(key, 0, limit - 1, desc=True, withscores=True)
            print(f"DEBUG: Leaderboard raw results: {results}") # Log for debugging
            
            # Handle different return formats
            formatted = []
            if not results:
                return []
                
            # Case 1: List of tuples/lists/objects (standard)
            # Check if first item is iterable and not a string
            first = results[0]
            if isinstance(first, (list, tuple)):
                formatted = [{"name": str(r[0]), "score": float(r[1])} for r in results]
            elif hasattr(first, 'member') and hasattr(first, 'score'):
                 # Object style (ScoredMember)
                 formatted = [{"name": r.member, "score": float(r.score)} for r in results]
            else:
                # Case 2: Flat list [member, score, member, score] (some clients)
                # Iterate in chunks of 2
                for i in range(0, len(results), 2):
                    if i + 1 < len(results):
                        formatted.append({"name": str(results[i]), "score": float(results[i+1])})
            
            return formatted

        except Exception as e:
            print(f"ERROR Parsing Leaderboard: {e}")
            return []

kv_client = KVClient()
