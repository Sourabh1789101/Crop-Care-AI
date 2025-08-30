# Smart Crop Advisory — README

A low-cost, hybrid (edge + lightweight cloud) advisory system for small and marginal farmers. This repo contains:
- **FastAPI backend** with endpoints for crop, fertilizer, disease (stub), weather, and market prices.
- **PWA frontend** (vanilla JS) with offline support and basic voice commands.
- **Telegram bot** (optional) to access the same advisories via chat.

## Quick Start

### 1) Backend
```bash
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
export OPENWEATHER_API_KEY=YOUR_KEY
uvicorn backend.app:app --reload
```

### 2) Frontend
Serve the static files (any server):
```bash
npx serve frontend  # or python -m http.server from inside 'frontend'
```
Open http://localhost:3000 or shown URL.

### 3) Telegram Bot (optional)
```bash
export TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
export API_BASE=http://localhost:8000
python chatbot/telegram_bot.py
```

## Training / Models
- Put trained `crop_model.pkl` and `fertilizer_model.pkl` under `backend/models/`.
- If absent, backend uses heuristics so prototype still runs.

## API
- `POST /recommend_crop` → `{N,P,K,ph,rainfall}`
- `POST /recommend_fertilizer` → `{crop,N,P,K,ph}`
- `POST /detect_disease` → multipart file `file`
- `GET /weather?pincode=XXXXXX`
- `GET /market?crop=wheat`

## Deploy
- **Docker**: `docker build -t sca-backend -f deploy/Dockerfile . && docker run -p 8000:8000 sca-backend`
- **Serverless**: sample `serverless.yml` provided (adjust for your account).

## Notes
- Weather requires `OPENWEATHER_API_KEY`.
- Market prices are mocked; replace with Agmarknet/eNAM official APIs for production.
- Disease detection here is a heuristic placeholder; swap with TFLite/ONNX model on-device to minimize cloud cost.
