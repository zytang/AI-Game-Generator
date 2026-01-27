# 🎮 AI Educational Game Generator (Enhanced)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)](https://vercel.com/)
[![Gemini](https://img.shields.io/badge/AI-Gemini_2.5_Pro-blue.svg)](https://deepmind.google/technologies/gemini/)

An AI-powered web application that generates fully playable, high-fidelity educational HTML games. Now enhanced with **Shared Global Leaderboards**, **Multi-level Challenges**, and **Performance Tracking**.

The system uses FastAPI (Python) and Google Gemini 2.5 Pro to create self-contained artifacts that run instantly in any browser.

## 🚀 New & Enhanced Features

✅ **Shared Global Leaderboards**: Uses **Vercel KV (Redis)** to sync scores across all players and devices. Scan a QR code and compete in real-time!

✅ **Leveled Challenges & Progression**: Games now feature 3+ difficulty levels with a progression system (levels lock until the previous one is mastered).

✅ **Advanced Game Engine**: Generates more robust, compact code using "Logical Engines" to prevent truncation and ensure complex features fit within token limits.

✅ **Premium UI/UX**: Highly polished glassmorphism aesthetics, smooth CSS animations, and responsive design for mobile play.

✅ **Comprehensive Feedback**: 
- **Star Rewards**: 1-3 star ratings based on percentage score.
- **Review Phase**: Interactive review of missed questions with explanations.
- **Navigation**: Dedicated "Next Level", "Replay", and "Quit" flow.

✅ **Gemini 2.5 Pro Integration**: Optimized for the latest model to provide faster generation and improved logic.

## 🗂️ Updated Project Structure
```bash
ai-game-generator/
│
├── backend/
│   ├── main.py              # FastAPI app with leaderboard endpoints
│   ├── gemini_client.py     # Gemini 2.5 Pro API integration
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
2. **Generate**: The AI designs a multi-level game with premium aesthetics (24-hour draft link).
3. **Draft**: The game is active for 24 hours. Play it, test it, or download it.
4. **Publish**: Click **"☁️ Publish"** to extend the game's life to **7 Days** and create a permanent shareable QR code for students.

## 🛠️ Advanced Features

### 📂 Import & Resume
Don't fear losing your prompt!
1. **Save HTML**: Download your game file.
2. **Import**: Upload it back into the generator.
3. **Restore**: The system automatically extracting your prompt, difficulty, and settings.
4. **Regenerate or Publish**: You can either generate a new version or publish the exact file you imported.

### ☁️ Publishing for Students
To share a game with a class:
1. **Generate** or **Import** a game you like.
2. **Click "Publish"**:
   - Uploads the specific game file to the cloud.
   - **Retention**: 7 Days (vs 24h for drafts).
   - **QR Code**: Updates to a live server link.
3. **Share**: Students scan the QR code to play on mobile. Scores sync to the **Global Leaderboard**.

## 🎓 Instructor's Guide (Classroom Competition)
Use this tool to create engaging "Game of the Day" challenges.

### 1. Create a Game
Enter a prompt: "Create a timed quiz about the French Revolution. Include 3 levels. Timed Mode: YES."

### 2. Verify & Publish
- Test the game yourself.
- If you like it, click **"☁️ Publish"**.
- This gives you a **7-Day Window** for the assignment.

### 3. Run the Competition
- **Share**: Project the QR code.
- **Compete**: Students play on their phones.
- **Rank**: Watch the Global Leaderboard populate in real-time.
- **Save**: Download the HTML file to keep a permanent offline copy for your records.

---
*Enhanced version based on a fork of [YashDewangan/AI-Game-Generator](https://github.com/yashdew3/AI-Game-Generator).*