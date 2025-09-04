import os
import io
import pickle
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image
import numpy as np

from utils.soil_helper import fertilizer_plan
from utils.market_api import get_prices
from whatsapp_webhook import router as whatsapp_router

# Optional: weather (requires env var OPENWEATHER_API_KEY)
WEATHER_ENABLED = True
try:
    from utils.weather_api import WeatherClient
    weather_client = WeatherClient()
except Exception:
    WEATHER_ENABLED = False
    weather_client = None

app = FastAPI(title="Smart Crop Advisory API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include WhatsApp webhook router
app.include_router(whatsapp_router, prefix="/api")

# -------------------- Models -------------------- #
CROP_MODEL = None
FERT_MODEL = None

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
try:
    with open(os.path.join(MODELS_DIR, "crop_model.pkl"), "rb") as f:
        CROP_MODEL = pickle.load(f)
except Exception:
    CROP_MODEL = None

try:
    with open(os.path.join(MODELS_DIR, "fertilizer_model.pkl"), "rb") as f:
        FERT_MODEL = pickle.load(f)
except Exception:
    FERT_MODEL = None

# -------------------- Schemas -------------------- #
class SoilInput(BaseModel):
    N: float
    P: float
    K: float
    ph: float
    rainfall: Optional[float] = 100
    soil_type: Optional[str] = "loam"
    location: Optional[str] = None  # pincode or lat,long

class CropRecoRequest(SoilInput):
    pass

class FertRequest(SoilInput):
    crop: str

# -------------------- Routes -------------------- #
@app.get("/")
async def root():
    return {
        "message": "Smart Crop Advisory API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "crop_recommendation": "/recommend_crop",
            "fertilizer_recommendation": "/recommend_fertilizer", 
            "disease_detection": "/detect_disease",
            "weather": "/weather",
            "market_prices": "/market",
            "documentation": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok", "weather": WEATHER_ENABLED}

@app.post("/recommend_crop")
async def recommend_crop(payload: CropRecoRequest):
    features = np.array([[payload.N, payload.P, payload.K, payload.ph, payload.rainfall]])
    if CROP_MODEL is not None:
        pred = CROP_MODEL.predict(features)[0]
        proba = getattr(CROP_MODEL, "predict_proba", None)
        conf = float(max(proba(features)[0])) if proba else 0.75
        return {"crop": str(pred), "confidence": round(conf, 3)}
    
    # Fallback heuristic
    ph = payload.ph
    if 6.0 <= ph <= 7.5:
        guess = "wheat"
    elif ph < 6.0:
        guess = "rice"
    else:
        guess = "maize"
    return {"crop": guess, "confidence": 0.6, "note": "heuristic fallback (train and drop crop_model.pkl to enable ML)"}

@app.post("/recommend_fertilizer")
async def recommend_fertilizer(payload: FertRequest):
    soil = payload.model_dump()
    soil.pop("crop", None)
    plan = fertilizer_plan(payload.crop, soil)
    return {"crop": payload.crop, **plan}

@app.post("/detect_disease")
async def detect_disease(file: UploadFile = File(...)):
    try:
        img_bytes = await file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((64, 64))
        arr = np.array(img).astype(np.float32) / 255.0
        mean_green = float(arr[:, :, 1].mean())
        # Very naive heuristic: greener → "healthy" else "leaf_blight"
        if mean_green > 0.35:
            label = "healthy"
            conf = 0.7
        else:
            label = "leaf_blight_suspected"
            conf = 0.65
        remedy = "Use copper-based fungicide; remove affected leaves; avoid overhead irrigation."
        if label == "healthy":
            remedy = "No action needed; maintain regular scouting."
        return {"label": label, "confidence": round(conf, 3), "remedy": remedy}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

@app.get("/weather")
async def weather(pincode: str):
    if not WEATHER_ENABLED or weather_client is None:
        return {"error": "Weather disabled. Set OPENWEATHER_API_KEY env var."}
    try:
        summary = weather_client.get_agricultural_summary(pincode)
        return summary
    except Exception as e:
        return {"error": f"Weather data unavailable: {str(e)}"}

@app.get("/weather/simple")
async def weather_simple(pincode: str):
    """Simple weather endpoint (backward compatibility)"""
    if not WEATHER_ENABLED or weather_client is None:
        return {"error": "Weather disabled. Set OPENWEATHER_API_KEY env var."}
    try:
        current = weather_client.current_by_pincode(pincode)
        alerts = weather_client.simple_alerts(current)
        return {"current": current, "alerts": alerts}
    except Exception as e:
        return {"error": f"Weather data unavailable: {str(e)}"}

@app.get("/market")
async def market(crop: Optional[str] = None, state: Optional[str] = None):
    return get_prices(crop=crop, state=state)

@app.get("/languages")
async def languages():
    return {"supported": ["en", "hi", "gu", "mr", "bn", "ta", "te", "kn", "pa"]}
