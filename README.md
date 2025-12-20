# 🎮 AI Educational Game Generator

[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered web application that generates fully playable, self-contained HTML educational games based on user prompts.
The system uses FastAPI (Python) for the backend and Google Gemini (free tier) for game generation.

The generated games run directly in the browser with no external libraries, no setup, and no dependencies.

## 🚀Project Overview
**Check it Out:** [AI Game Generator🔗](https://ai-game-generator-yiw2.onrender.com)
### Objective

- User provides a short educational game idea (e.g., math game for kids)
- Backend uses Gemini AI to generate a complete HTML game
- The generated game includes:
    - `HTML`
    - `CSS`
    - `JavaScript` (all in a single file)
- User can immediately play the game in a new browser tab

### This project focuses on:

- Clean system design
- Prompt engineering
- Safe LLM integration
- End-to-end functionality rather than UI polish.

## 🧠Key Features

✅ AI-generated fully playable HTML games

✅ No external libraries or frameworks in generated games

✅ Works entirely on Gemini free tier

✅ Simple and clear frontend

✅ FastAPI backend with clean separation of concerns

✅ Safe handling of LLM output (validation + caching control)

✅ GitHub-ready project structure

## 🗂️ Folder Structure
```bash
ai-game-generator/
│
├── backend/
│   ├── main.py              # FastAPI app & API routes
│   ├── gemini_client.py     # Gemini API integration
│   ├── prompt_templates.py  # System + user prompt builder
│   └── utils.py             # Output cleaning & validation
│
├── static/
│   ├── index.html           # Frontend UI
│   └── style.css            # Minimal styling
│
├── generated_games/         # AI-generated HTML games
│
├── requirements.txt
├── LICENSE
├── .gitignore
└── README.md
```

### 🔧 Prerequisites

- Python 3.9+
- Google Gemini API key (free tier)
- Internet connection (for Gemini API)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yashdew3/AI-Game-Generator.git
cd AI-Game-Generator
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## ▶️ Running the Project Locally
From the project root:
```bash
uvicorn backend.main:app --reload
```
The application will be available at:
```cpp
http://127.0.0.1:8000
```

## 🕹️ How to Generate and Play a Game

1. Open the app in your browser:
http://127.0.0.1:8000

2. Enter an educational game prompt, for example:
```css
Create a kid-friendly math addition game for ages 6–8 with five questions and a score counter.
```
3. Click Generate Game
4. Once generation is complete, click ▶ Play Game
5. The game opens in a new browser tab and is immediately playable

## 🤖 AI & Prompting Details
- Model used: Gemini 2.5 Flash
- Free-tier compatible
- Strict system prompt enforces:
    - Single valid HTML file
    - Inline CSS & JavaScript
    - No external assets or libraries

The backend validates the AI output to ensure:
- Complete HTML document
- No truncated or broken files
- Safe serving without caching issues

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yashdew3/AI-Game-Generator/issues) (if you have one) or open a new issue to discuss changes. Pull requests are also appreciated.

## 📝 License

This project is licensed under the MIT License © Yash Dewangan

## Let's Connect
Feel free to connect or suggest improvements!
- Built by **Yash Dewangan**
- 🐙Github: [YashDewangan](https://github.com/yashdew3)
- 📧Email: [yashdew06@gmail.com](mailto:yashdew06@gmail.com)
- 🔗Linkedin: [YashDewangan](https://www.linkedin.com/in/yash-dewangan/)

---