
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from upstash_redis import Redis

def test_kv_connection():
    # 1. Load Environment Variables
    env_path = Path(__file__).parent / ".env"
    print(f"Loading environment from: {env_path}")
    load_dotenv(dotenv_path=env_path)

    url = os.getenv("KV_REST_API_URL")
    token = os.getenv("KV_REST_API_TOKEN")

    print(f"URL: {url}")
    print(f"Token: {'*' * 5}{token[-5:] if token else 'None'}")

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

    # 3. Test Write
    try:
        print("Attempting to write test key...")
        redis.set("debug_test_key", "success_value")
        print("✅ Write Successful.")
    except Exception as e:
        print(f"❌ FAILURE: Write Failed: {e}")
        return

    # 4. Test Read
    try:
        print("Attempting to read test key...")
        val = redis.get("debug_test_key")
        print(f"Read Value: {val}")
        if val == "success_value":
            print("✅ Read Successful. (Value matches)")
        else:
            print(f"❌ FAILURE: Read Value Mismatch. Got: {val}")
    except Exception as e:
        print(f"❌ FAILURE: Read Failed: {e}")

if __name__ == "__main__":
    test_kv_connection()
