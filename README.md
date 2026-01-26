# 🎮 AI Educational Game Generator (Enhanced)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)](https://vercel.com/)
[![Gemini](https://img.shields.io/badge/AI-Gemini_2.5_Flash-blue.svg)](https://deepmind.google/technologies/gemini/)

An AI-powered web application that generates fully playable, high-fidelity educational HTML games. Now enhanced with **Shared Global Leaderboards**, **Multi-level Challenges**, and **Performance Tracking**.

The system uses FastAPI (Python) and Google Gemini 2.5 Flash to create self-contained artifacts that run instantly in any browser.

## 🚀 New & Enhanced Features

✅ **Shared Global Leaderboards**: Uses **Vercel KV (Redis)** to sync scores across all players and devices. Scan a QR code and compete in real-time!

✅ **Leveled Challenges & Progression**: Games now feature 3+ difficulty levels with a progression system (levels lock until the previous one is mastered).

✅ **Advanced Game Engine**: Generates more robust, compact code using "Logical Engines" to prevent truncation and ensure complex features fit within token limits.

✅ **Premium UI/UX**: Highly polished glassmorphism aesthetics, smooth CSS animations, and responsive design for mobile play.

✅ **Comprehensive Feedback**: 
- **Star Rewards**: 1-3 star ratings based on percentage score.
- **Review Phase**: Interactive review of missed questions with explanations.
- **Navigation**: Dedicated "Next Level", "Replay", and "Quit" flow.

✅ **Gemini 2.5 Flash Integration**: Optimized for the latest model to provide faster generation and improved logic.

## 🗂️ Updated Project Structure
```bash
ai-game-generator/
│
├── backend/
│   ├── main.py              # FastAPI app with leaderboard endpoints
│   ├── gemini_client.py     # Gemini 2.5 API integration
│   ├── kv_client.py         # Vercel KV / Redis score persistence
│   ├── prompt_templates.py  # Advanced multi-level + navigation prompts
│   └── utils.py             # Output cleaning & placeholder injection
│
├── static/
│   ├── index.html           # Modernized Frontend UI
│   └── style.css            # Premium Glassmorphism styling
│
├── generated_games/         # Local dev game storage
├── requirements.txt         # Added upstash-redis for KV support
└── README.md
```

## ️⚙️ Prerequisites

- Python 3.9+
- Google Gemini API key (Paid tier recommended for high throughput)
- **Vercel KV** (for shared leaderboards)

## 🚀 Deployment (Vercel)

This project is optimized for Vercel deployment. To enable the shared leaderboard, you must configure the following environment variables:

1. **Push to GitHub**: Initialize a repo and push your code.
2. **Connect to Vercel**: Import the repository.
3. **Configure KV**: Add a **Vercel KV** storage instance to your project.
4. **Environment Variables**:
   - `GEMINI_API_KEY`: Your Google AI Studio key.
   - `KV_REST_API_URL`: Automatically added by Vercel KV.
   - `KV_REST_API_TOKEN`: Automatically added by Vercel KV.

## ▶️ Running Locally

1. Create a `.env` in `backend/`:
   ```env
   GEMINI_API_KEY=your_key
   KV_REST_API_URL=your_upstash_url
   KV_REST_API_TOKEN=your_upstash_token
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   uvicorn backend.main:app --reload
   ```

## 🕹️ How to Play

1. **Describe**: Enter a prompt (e.g., "Space-themed multiplication for 5th graders").
2. **Generate**: The AI designs a multi-level game with premium aesthetics.
3. **Compete**: Scan the QR code to play on mobile. Submit your score to the **Global Leaderboard** and see how you rank against other students!

## 🛠️ Modifying Generated Games

The game artifacts are single-file HTML applications. To edit content (e.g., fix a typo or change a question):

1. **Download**: Click the "Save HTML" button after generation.
2. **Open**: Open the `.html` file in any text editor (Notepad, VS Code, etc.).
3. **Edit**: Search for the text you want to change or modify the JavaScript `questions` array.
4. **Save**: Save the file and open it in your browser to play the updated version.

## 🎓 Instructor's Guide (Classroom Competition)
Use this tool to create engaging "Game of the Day" challenges for your students.

### 1. Create a Game
Enter a prompt that specifies the topic, difficulty, and format.
> **Example Prompt**: "Create a timed quiz about the French Revolution for college students. Include 3 levels of difficulty. Timed Mode: YES."

### 2. Run the Competition (24-Hour Window)
Once generated, the game link stays active for **24 hours**.
- **Share**: Project the QR code or share the URL with your class.
- **Compete**: Students play on their phones/laptops and submit scores.
- **Rank**: Watch the Global Leaderboard populate in real-time to see who masters the material!
- **Note**: After 24 hours, the link expires to keep the system clean.

### 3. Keep the Game Forever
To use the same game for future classes:
- Click **"Download HTML"** immediately after generation.
- Host this HTML file on your own LMS (Canvas, Blackboard), Google Drive, or personal website.
- **Note**: The shared leaderboard requires the game to be hosted on the original server URL. Downloaded games work perfectly but will not sync to the global leaderboard.

---
*Enhanced version based on a fork of [YashDewangan/AI-Game-Generator](https://github.com/yashdew3/AI-Game-Generator).*