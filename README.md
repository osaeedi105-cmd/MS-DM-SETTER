# DM Setter Mock Bot

## Deploy in 5 minutes on Railway (free)

### Step 1 — Get your Anthropic API key
1. Go to console.anthropic.com
2. Click API Keys → Create Key
3. Copy the key

### Step 2 — Deploy to Railway
1. Go to railway.app and sign up (free)
2. Click "New Project" → "Deploy from GitHub repo"
3. Upload this folder as a GitHub repo (or use Railway's CLI)
4. In Railway, go to Variables → Add:
   - Key: `ANTHROPIC_API_KEY`
   - Value: your API key from Step 1
5. Railway auto-deploys — you'll get a live URL like `https://your-app.up.railway.app`

### Step 3 — Use it
Open your Railway URL in any browser. Share it with your setters.

### Alternative: Run locally
```bash
export ANTHROPIC_API_KEY=your_key_here
python server.py
```
Then open http://localhost:8080 in your browser.

## What's included
- `server.py` — Python backend (no external dependencies)
- `static/index.html` — Full DM mock UI
- `Procfile` — Railway deployment config

## Features
- 7 randomised lead personas (qualified, yellow flag, red flag)
- Lead always opens with "Ready" keyword
- Reactive lead — opens up with good relatability, goes cold with robotic replies
- Yellow/red flag financial qualifying system
- Natural objection handling
- Auto scorecard out of 100 after every session
- Scores: Relatability, Listening & context, Framework, Qualifying
- Identifies single biggest weakness with targeted feedback
