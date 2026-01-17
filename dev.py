import uvicorn
import os

if __name__ == "__main__":
    # Binding to 0.0.0.0 allows other devices on your network (like your phone) 
    # to access the server using your computer's local IP address.
    uvicorn.run(
        "backend.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        reload_excludes=["generated_games/*", "debug_output.txt", "*.log"]
    )
